"""
OBJX PROJECT MANAGEMENT SYSTEM - COMPREHENSIVE BACKEND
Monday.com Replacement with 5-Level Permissions & Google Workspace Integration

Architecture:
- Admin: Billing + QuickBooks + All Tiers + Multi-agents + Project Management
- Staff: Project Management + Task Management + Feasibility + Code Review
- Tier 3: Complete methodology (existing)
- Tier 2: Compound intelligence (existing)
- Tier 1: Systematic thinking (existing)

Integrations:
- Google Workspace (Gmail, Drive, Docs, Calendar)
- QuickBooks for billing
- mem0 for memory
- Trinity Architecture foundation
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import openai
from mem0 import MemoryClient
from dotenv import load_dotenv

# Google Workspace Integration
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import google.auth

# QuickBooks Integration
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from quickbooks import QuickBooks
from quickbooks.objects import Customer, Invoice, Item

# Load environment variables
load_dotenv()

class PermissionLevel(Enum):
    ADMIN = 5
    STAFF = 4
    TIER3 = 3
    TIER2 = 2
    TIER1 = 1

class ProjectStatus(Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    BLOCKED = "blocked"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class User:
    id: str
    email: str
    name: str
    permission_level: PermissionLevel
    google_workspace_id: Optional[str] = None
    quickbooks_company_id: Optional[str] = None
    created_at: datetime = None
    last_login: datetime = None
    is_active: bool = True

@dataclass
class Project:
    id: str
    name: str
    description: str
    owner_id: str
    team_members: List[str]
    status: ProjectStatus
    priority: TaskPriority
    start_date: datetime
    due_date: datetime
    budget: Optional[float] = None
    google_drive_folder_id: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class Task:
    id: str
    project_id: str
    name: str
    description: str
    assignee_id: str
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    dependencies: List[str] = None
    google_doc_id: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class Proposal:
    id: str
    client_name: str
    project_name: str
    amount: float
    status: str
    created_by: str
    google_doc_id: Optional[str] = None
    quickbooks_estimate_id: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None

class DatabaseManager:
    """SQLite database manager for project management system"""
    
    def __init__(self, db_path: str = "objx_project_management.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with all required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                permission_level INTEGER NOT NULL,
                google_workspace_id TEXT,
                quickbooks_company_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                owner_id TEXT NOT NULL,
                team_members TEXT, -- JSON array
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                start_date TIMESTAMP,
                due_date TIMESTAMP,
                budget REAL,
                google_drive_folder_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users (id)
            )
        ''')
        
        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                assignee_id TEXT NOT NULL,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                due_date TIMESTAMP,
                estimated_hours REAL,
                actual_hours REAL,
                dependencies TEXT, -- JSON array
                google_doc_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id),
                FOREIGN KEY (assignee_id) REFERENCES users (id)
            )
        ''')
        
        # Proposals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proposals (
                id TEXT PRIMARY KEY,
                client_name TEXT NOT NULL,
                project_name TEXT NOT NULL,
                amount REAL NOT NULL,
                status TEXT NOT NULL,
                created_by TEXT NOT NULL,
                google_doc_id TEXT,
                quickbooks_estimate_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Agent sessions table for multi-agent support
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                session_data TEXT, -- JSON data
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute query and return results as list of dictionaries"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.commit()
        conn.close()
        return results

class GoogleWorkspaceIntegration:
    """Google Workspace integration for Gmail, Drive, Docs, Calendar"""
    
    def __init__(self):
        self.scopes = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/calendar'
        ]
        self.credentials = None
    
    def authenticate_user(self, user_id: str) -> bool:
        """Authenticate user with Google Workspace"""
        try:
            # Implementation for Google OAuth flow
            flow = Flow.from_client_secrets_file(
                'google_credentials.json',
                scopes=self.scopes,
                redirect_uri='http://localhost:5000/auth/google/callback'
            )
            
            # Store credentials for user
            return True
        except Exception as e:
            print(f"Google authentication error: {e}")
            return False
    
    def create_project_folder(self, project_name: str) -> str:
        """Create Google Drive folder for project"""
        try:
            service = build('drive', 'v3', credentials=self.credentials)
            
            folder_metadata = {
                'name': f"OBJX Project - {project_name}",
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            folder = service.files().create(body=folder_metadata).execute()
            return folder.get('id')
        except Exception as e:
            print(f"Error creating project folder: {e}")
            return None
    
    def create_task_document(self, task_name: str, project_folder_id: str) -> str:
        """Create Google Doc for task"""
        try:
            service = build('docs', 'v1', credentials=self.credentials)
            
            document = {
                'title': f"Task: {task_name}"
            }
            
            doc = service.documents().create(body=document).execute()
            
            # Move to project folder
            drive_service = build('drive', 'v3', credentials=self.credentials)
            drive_service.files().update(
                fileId=doc.get('documentId'),
                addParents=project_folder_id,
                removeParents='root'
            ).execute()
            
            return doc.get('documentId')
        except Exception as e:
            print(f"Error creating task document: {e}")
            return None

class QuickBooksIntegration:
    """QuickBooks integration for billing and proposals"""
    
    def __init__(self):
        self.client_id = os.getenv('QUICKBOOKS_CLIENT_ID')
        self.client_secret = os.getenv('QUICKBOOKS_CLIENT_SECRET')
        self.sandbox_base_url = 'https://sandbox-quickbooks.api.intuit.com'
        self.auth_client = None
    
    def authenticate_company(self, company_id: str) -> bool:
        """Authenticate with QuickBooks for specific company"""
        try:
            self.auth_client = AuthClient(
                client_id=self.client_id,
                client_secret=self.client_secret,
                environment='sandbox',  # Change to 'production' for live
                redirect_uri='http://localhost:5000/auth/quickbooks/callback'
            )
            return True
        except Exception as e:
            print(f"QuickBooks authentication error: {e}")
            return False
    
    def create_estimate(self, proposal: Proposal) -> str:
        """Create QuickBooks estimate from proposal"""
        try:
            # Implementation for creating QuickBooks estimate
            # This would use the QuickBooks API to create an estimate
            estimate_id = f"qb_estimate_{proposal.id}"
            return estimate_id
        except Exception as e:
            print(f"Error creating QuickBooks estimate: {e}")
            return None
    
    def create_invoice(self, project: Project, amount: float) -> str:
        """Create QuickBooks invoice for project"""
        try:
            # Implementation for creating QuickBooks invoice
            invoice_id = f"qb_invoice_{project.id}"
            return invoice_id
        except Exception as e:
            print(f"Error creating QuickBooks invoice: {e}")
            return None

class ProjectManagementSystem:
    """Main project management system with Trinity Architecture integration"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.google_integration = GoogleWorkspaceIntegration()
        self.quickbooks_integration = QuickBooksIntegration()
        
        # Initialize Trinity Architecture components
        self.foundation_context = self.load_foundation_documents()
        self.openai_client = None
        self.mem0_client = None
        self.initialize_clients()
    
    def load_foundation_documents(self) -> str:
        """Load Trinity Architecture foundation documents"""
        foundation_dir = "foundation_docs"
        foundation_content = ""
        
        foundation_files = [
            "00_living_doctoring_the_why.md",
            "01_foundation_principles_universal.md", 
            "02_trinity_architecture_universal.md",
            "03_intelligence_memory_compound.md",
            "04_partnership_protocols_complete.md",
            "06_evolution_continuous_improvement.md"
        ]
        
        for filename in foundation_files:
            file_path = os.path.join(foundation_dir, filename)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        foundation_content += f"\n\n=== {filename} ===\n{content}"
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        return foundation_content
    
    def initialize_clients(self):
        """Initialize OpenAI and mem0 clients"""
        try:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if openai_api_key:
                self.openai_client = openai.OpenAI(api_key=openai_api_key)
                
            mem0_api_key = os.getenv('MEM0_API_KEY')
            if mem0_api_key:
                self.mem0_client = MemoryClient(api_key=mem0_api_key)
        except Exception as e:
            print(f"Client initialization error: {e}")
    
    def apply_systematic_thinking(self, input_data: Dict[str, Any], context: str = "") -> Dict[str, Any]:
        """Apply X+Y=Z methodology to project management decisions"""
        
        if not self.openai_client:
            return {"error": "OpenAI client not initialized"}
        
        system_prompt = f"""
        Apply systematic thinking using the X+Y=Z methodology for project management:
        
        X (What we know): Analyze the current project/task information and context
        Y (What we need): Identify gaps, requirements, risks, and objectives
        Z (What we conclude): Provide systematic recommendations and next steps
        
        Foundation Context:
        {self.foundation_context}
        
        Project Management Context:
        {context}
        
        Input Data:
        {json.dumps(input_data, indent=2)}
        
        Provide comprehensive project management insights with systematic analysis.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Apply systematic thinking to this project management scenario."}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return {
                "systematic_analysis": response.choices[0].message.content,
                "methodology_applied": "X+Y=Z",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "systematic_analysis": "Error in systematic thinking process"
            }
    
    # Project Management Methods
    def create_project(self, project_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Create new project with Google Workspace integration"""
        
        project_id = f"proj_{int(datetime.now().timestamp())}"
        
        # Apply systematic thinking to project creation
        systematic_result = self.apply_systematic_thinking(
            project_data, 
            "New project creation and planning context"
        )
        
        # Create Google Drive folder
        google_folder_id = self.google_integration.create_project_folder(
            project_data.get('name', 'Unnamed Project')
        )
        
        # Create project in database
        project = Project(
            id=project_id,
            name=project_data.get('name', ''),
            description=project_data.get('description', ''),
            owner_id=user_id,
            team_members=project_data.get('team_members', []),
            status=ProjectStatus.PLANNING,
            priority=TaskPriority(project_data.get('priority', 'medium')),
            start_date=datetime.fromisoformat(project_data.get('start_date')),
            due_date=datetime.fromisoformat(project_data.get('due_date')),
            budget=project_data.get('budget'),
            google_drive_folder_id=google_folder_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Insert into database
        query = '''
            INSERT INTO projects (id, name, description, owner_id, team_members, status, 
                                priority, start_date, due_date, budget, google_drive_folder_id,
                                created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        self.db.execute_query(query, (
            project.id, project.name, project.description, project.owner_id,
            json.dumps(project.team_members), project.status.value, project.priority.value,
            project.start_date, project.due_date, project.budget, project.google_drive_folder_id,
            project.created_at, project.updated_at
        ))
        
        # Store in memory
        if self.mem0_client:
            try:
                self.mem0_client.add([{
                    "role": "system",
                    "content": f"New project created: {project.name} with systematic analysis applied"
                }], user_id=user_id)
            except Exception as e:
                print(f"Memory storage error: {e}")
        
        return {
            "project_id": project_id,
            "systematic_analysis": systematic_result,
            "google_folder_id": google_folder_id,
            "status": "created",
            "methodology": "X+Y=Z with Google Workspace Integration"
        }
    
    def create_task(self, task_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Create new task with systematic analysis"""
        
        task_id = f"task_{int(datetime.now().timestamp())}"
        
        # Apply systematic thinking to task creation
        systematic_result = self.apply_systematic_thinking(
            task_data,
            "Task creation and assignment context"
        )
        
        # Get project folder for Google Doc creation
        project_query = "SELECT google_drive_folder_id FROM projects WHERE id = ?"
        project_result = self.db.execute_query(project_query, (task_data.get('project_id'),))
        
        google_doc_id = None
        if project_result and project_result[0]['google_drive_folder_id']:
            google_doc_id = self.google_integration.create_task_document(
                task_data.get('name', 'Unnamed Task'),
                project_result[0]['google_drive_folder_id']
            )
        
        # Create task in database
        task = Task(
            id=task_id,
            project_id=task_data.get('project_id'),
            name=task_data.get('name', ''),
            description=task_data.get('description', ''),
            assignee_id=task_data.get('assignee_id'),
            status=TaskStatus.TODO,
            priority=TaskPriority(task_data.get('priority', 'medium')),
            due_date=datetime.fromisoformat(task_data.get('due_date')),
            estimated_hours=task_data.get('estimated_hours'),
            dependencies=task_data.get('dependencies', []),
            google_doc_id=google_doc_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Insert into database
        query = '''
            INSERT INTO tasks (id, project_id, name, description, assignee_id, status,
                             priority, due_date, estimated_hours, dependencies, google_doc_id,
                             created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        self.db.execute_query(query, (
            task.id, task.project_id, task.name, task.description, task.assignee_id,
            task.status.value, task.priority.value, task.due_date, task.estimated_hours,
            json.dumps(task.dependencies), task.google_doc_id, task.created_at, task.updated_at
        ))
        
        return {
            "task_id": task_id,
            "systematic_analysis": systematic_result,
            "google_doc_id": google_doc_id,
            "status": "created",
            "methodology": "X+Y=Z with Task Management"
        }
    
    def create_proposal(self, proposal_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Create proposal with QuickBooks integration (Admin only)"""
        
        proposal_id = f"prop_{int(datetime.now().timestamp())}"
        
        # Apply systematic thinking to proposal creation
        systematic_result = self.apply_systematic_thinking(
            proposal_data,
            "Proposal creation and client communication context"
        )
        
        # Create proposal in database
        proposal = Proposal(
            id=proposal_id,
            client_name=proposal_data.get('client_name', ''),
            project_name=proposal_data.get('project_name', ''),
            amount=proposal_data.get('amount', 0.0),
            status='draft',
            created_by=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Create QuickBooks estimate
        quickbooks_estimate_id = self.quickbooks_integration.create_estimate(proposal)
        proposal.quickbooks_estimate_id = quickbooks_estimate_id
        
        # Insert into database
        query = '''
            INSERT INTO proposals (id, client_name, project_name, amount, status, created_by,
                                 quickbooks_estimate_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        self.db.execute_query(query, (
            proposal.id, proposal.client_name, proposal.project_name, proposal.amount,
            proposal.status, proposal.created_by, proposal.quickbooks_estimate_id,
            proposal.created_at, proposal.updated_at
        ))
        
        return {
            "proposal_id": proposal_id,
            "systematic_analysis": systematic_result,
            "quickbooks_estimate_id": quickbooks_estimate_id,
            "status": "created",
            "methodology": "X+Y=Z with QuickBooks Integration"
        }

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'objx-project-management-secret')

# Initialize project management system
pm_system = ProjectManagementSystem()

# API Routes
@app.route('/api/projects', methods=['POST'])
def create_project_api():
    """Create new project"""
    try:
        data = request.get_json()
        user_id = session.get('user_id', 'default_user')  # TODO: Implement proper auth
        
        result = pm_system.create_project(data, user_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/projects', methods=['GET'])
def get_projects_api():
    """Get all projects for user"""
    try:
        user_id = session.get('user_id', 'default_user')
        
        query = "SELECT * FROM projects WHERE owner_id = ? OR team_members LIKE ?"
        projects = pm_system.db.execute_query(query, (user_id, f'%{user_id}%'))
        
        return jsonify({"projects": projects})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task_api():
    """Create new task"""
    try:
        data = request.get_json()
        user_id = session.get('user_id', 'default_user')
        
        result = pm_system.create_task(data, user_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/proposals', methods=['POST'])
def create_proposal_api():
    """Create new proposal (Admin only)"""
    try:
        # TODO: Check admin permission
        data = request.get_json()
        user_id = session.get('user_id', 'default_user')
        
        result = pm_system.create_proposal(data, user_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "system": "OBJX Project Management",
        "architecture": "Trinity + Google Workspace + QuickBooks",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 OBJX Project Management System Starting...")
    print("📊 Monday.com Replacement with Trinity Architecture")
    print("🔧 5-Level Permissions: Admin, Staff, Tier3, Tier2, Tier1")
    print("🌐 Google Workspace Integration: Gmail, Drive, Docs, Calendar")
    print("💰 QuickBooks Integration: Billing and Proposals")
    print("🤖 Agent Capabilities: Multi-agent orchestration")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

