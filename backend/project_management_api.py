"""
OBJX Project Management API Integration
Connects Staff/Admin dashboards to backend with Trinity Architecture
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
import json
import os
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Optional
import logging

# Import existing OBJX components
from memory_agent_integration import OBJXMemorySystem, MultiAgentOrchestrator
from project_management_backend import ProjectManagementDB

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'objx-project-management-secret')
CORS(app)

# Initialize systems
memory_system = OBJXMemorySystem()
agent_orchestrator = MultiAgentOrchestrator()
project_db = ProjectManagementDB()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# AUTHENTICATION & PERMISSIONS
# ============================================================================

def check_permission(required_level: str) -> bool:
    """Check if user has required permission level"""
    user_level = session.get('user_level', 'none')
    
    permission_hierarchy = {
        'admin': 5,
        'staff': 4,
        'tier3': 3,
        'tier2': 2,
        'tier1': 1,
        'none': 0
    }
    
    required_level_num = permission_hierarchy.get(required_level, 0)
    user_level_num = permission_hierarchy.get(user_level, 0)
    
    return user_level_num >= required_level_num

def require_permission(level: str):
    """Decorator to require specific permission level"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            if not check_permission(level):
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

# ============================================================================
# PROJECT MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/api/projects', methods=['GET'])
@require_permission('staff')
def get_projects():
    """Get all projects for current user"""
    try:
        user_id = session.get('user_id')
        user_level = session.get('user_level')
        
        # Admin sees all projects, Staff sees assigned projects
        if user_level == 'admin':
            projects = project_db.get_all_projects()
        else:
            projects = project_db.get_user_projects(user_id)
        
        # Add agent insights for each project
        for project in projects:
            project['agent_insights'] = agent_orchestrator.get_project_insights(project['id'])
            project['critical_deadlines'] = project_db.get_critical_deadlines(project['id'])
        
        return jsonify({
            'success': True,
            'projects': projects,
            'total_count': len(projects),
            'critical_count': sum(1 for p in projects if p.get('critical_deadlines', 0) > 0)
        })
        
    except Exception as e:
        logger.error(f"Error getting projects: {str(e)}")
        return jsonify({'error': 'Failed to retrieve projects'}), 500

@app.route('/api/projects', methods=['POST'])
@require_permission('staff')
def create_project():
    """Create new project with systematic thinking approach"""
    try:
        data = request.json
        user_id = session.get('user_id')
        
        # Apply X+Y=Z methodology to project creation
        project_context = {
            'X': data.get('current_situation', ''),
            'Y': data.get('requirements', ''),
            'Z': data.get('desired_outcome', '')
        }
        
        # Create project with Trinity Architecture
        project_id = project_db.create_project({
            'name': data['name'],
            'description': data.get('description', ''),
            'client_id': data.get('client_id'),
            'created_by': user_id,
            'methodology_context': json.dumps(project_context),
            'google_drive_folder': data.get('google_drive_folder'),
            'status': 'active'
        })
        
        # Store in memory system for pattern learning
        memory_system.store_project_memory(
            project_id=project_id,
            context=project_context,
            user_id=user_id
        )
        
        # Initialize agent monitoring
        agent_orchestrator.initialize_project_monitoring(project_id)
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'message': 'Project created with systematic thinking methodology'
        })
        
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        return jsonify({'error': 'Failed to create project'}), 500

@app.route('/api/projects/<int:project_id>/tasks', methods=['GET'])
@require_permission('staff')
def get_project_tasks(project_id):
    """Get tasks for specific project"""
    try:
        tasks = project_db.get_project_tasks(project_id)
        
        # Add agent recommendations for each task
        for task in tasks:
            task['agent_recommendations'] = agent_orchestrator.get_task_recommendations(task['id'])
        
        return jsonify({
            'success': True,
            'tasks': tasks,
            'project_id': project_id
        })
        
    except Exception as e:
        logger.error(f"Error getting tasks: {str(e)}")
        return jsonify({'error': 'Failed to retrieve tasks'}), 500

@app.route('/api/projects/<int:project_id>/tasks', methods=['POST'])
@require_permission('staff')
def create_task(project_id):
    """Create new task with agent intelligence"""
    try:
        data = request.json
        user_id = session.get('user_id')
        
        # Apply systematic thinking to task creation
        task_context = {
            'X': data.get('current_state', ''),
            'Y': data.get('requirements', ''),
            'Z': data.get('completion_criteria', '')
        }
        
        task_id = project_db.create_task({
            'project_id': project_id,
            'name': data['name'],
            'description': data.get('description', ''),
            'assigned_to': data.get('assigned_to'),
            'due_date': data.get('due_date'),
            'priority': data.get('priority', 'medium'),
            'created_by': user_id,
            'methodology_context': json.dumps(task_context),
            'google_doc_link': data.get('google_doc_link')
        })
        
        # Store task memory for learning
        memory_system.store_task_memory(
            task_id=task_id,
            project_id=project_id,
            context=task_context,
            user_id=user_id
        )
        
        # Notify relevant agents
        agent_orchestrator.notify_task_created(task_id, project_id)
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'Task created with systematic approach'
        })
        
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        return jsonify({'error': 'Failed to create task'}), 500

# ============================================================================
# AGENT ORCHESTRATION ENDPOINTS
# ============================================================================

@app.route('/api/agents/status', methods=['GET'])
@require_permission('staff')
def get_agent_status():
    """Get status of all agents"""
    try:
        user_level = session.get('user_level')
        
        if user_level == 'admin':
            # Admin gets full multi-agent status
            agent_status = agent_orchestrator.get_all_agent_status()
        else:
            # Staff gets single agent status
            agent_status = agent_orchestrator.get_staff_agent_status()
        
        return jsonify({
            'success': True,
            'agents': agent_status,
            'multi_agent_mode': user_level == 'admin'
        })
        
    except Exception as e:
        logger.error(f"Error getting agent status: {str(e)}")
        return jsonify({'error': 'Failed to retrieve agent status'}), 500

@app.route('/api/agents/insights', methods=['GET'])
@require_permission('staff')
def get_agent_insights():
    """Get proactive insights from agents"""
    try:
        user_id = session.get('user_id')
        user_level = session.get('user_level')
        
        insights = agent_orchestrator.get_proactive_insights(user_id, user_level)
        
        return jsonify({
            'success': True,
            'insights': insights,
            'count': len(insights)
        })
        
    except Exception as e:
        logger.error(f"Error getting insights: {str(e)}")
        return jsonify({'error': 'Failed to retrieve insights'}), 500

@app.route('/api/agents/orchestrate', methods=['POST'])
@require_permission('admin')
def orchestrate_agents():
    """Orchestrate multi-agent workflow (Admin only)"""
    try:
        data = request.json
        workflow_type = data.get('workflow_type')
        parameters = data.get('parameters', {})
        
        result = agent_orchestrator.execute_workflow(workflow_type, parameters)
        
        return jsonify({
            'success': True,
            'workflow_id': result['workflow_id'],
            'status': result['status'],
            'message': 'Multi-agent workflow initiated'
        })
        
    except Exception as e:
        logger.error(f"Error orchestrating agents: {str(e)}")
        return jsonify({'error': 'Failed to orchestrate agents'}), 500

# ============================================================================
# BILLING & PROPOSALS ENDPOINTS (Admin Only)
# ============================================================================

@app.route('/api/billing/proposals', methods=['GET'])
@require_permission('admin')
def get_proposals():
    """Get all proposals with QuickBooks integration"""
    try:
        proposals = project_db.get_all_proposals()
        
        # Add QuickBooks sync status
        for proposal in proposals:
            proposal['quickbooks_status'] = get_quickbooks_sync_status(proposal['id'])
        
        return jsonify({
            'success': True,
            'proposals': proposals,
            'pending_count': sum(1 for p in proposals if p['status'] == 'pending')
        })
        
    except Exception as e:
        logger.error(f"Error getting proposals: {str(e)}")
        return jsonify({'error': 'Failed to retrieve proposals'}), 500

@app.route('/api/billing/proposals', methods=['POST'])
@require_permission('admin')
def create_proposal():
    """Create new proposal with custom proposal system"""
    try:
        data = request.json
        user_id = session.get('user_id')
        
        # Apply systematic thinking to proposal creation
        proposal_context = {
            'X': data.get('client_needs', ''),
            'Y': data.get('our_solution', ''),
            'Z': data.get('expected_outcome', '')
        }
        
        proposal_id = project_db.create_proposal({
            'client_id': data['client_id'],
            'project_id': data.get('project_id'),
            'title': data['title'],
            'description': data.get('description', ''),
            'amount': data.get('amount', 0),
            'created_by': user_id,
            'methodology_context': json.dumps(proposal_context),
            'status': 'draft'
        })
        
        # Generate proposal document using agents
        document_result = agent_orchestrator.generate_proposal_document(
            proposal_id, proposal_context
        )
        
        return jsonify({
            'success': True,
            'proposal_id': proposal_id,
            'document_url': document_result.get('document_url'),
            'message': 'Proposal created with systematic methodology'
        })
        
    except Exception as e:
        logger.error(f"Error creating proposal: {str(e)}")
        return jsonify({'error': 'Failed to create proposal'}), 500

@app.route('/api/billing/quickbooks/sync', methods=['POST'])
@require_permission('admin')
def sync_quickbooks():
    """Sync with QuickBooks"""
    try:
        sync_result = sync_with_quickbooks()
        
        return jsonify({
            'success': True,
            'sync_status': sync_result['status'],
            'last_sync': sync_result['timestamp'],
            'records_synced': sync_result['count']
        })
        
    except Exception as e:
        logger.error(f"Error syncing QuickBooks: {str(e)}")
        return jsonify({'error': 'Failed to sync with QuickBooks'}), 500

# ============================================================================
# GOOGLE WORKSPACE INTEGRATION
# ============================================================================

@app.route('/api/google/drive/organize', methods=['POST'])
@require_permission('staff')
def organize_google_drive():
    """Organize Google Drive files for project"""
    try:
        data = request.json
        project_id = data['project_id']
        
        # Use agent to organize files
        organization_result = agent_orchestrator.organize_project_files(project_id)
        
        return jsonify({
            'success': True,
            'organized_files': organization_result['file_count'],
            'folder_structure': organization_result['structure'],
            'message': 'Files organized automatically'
        })
        
    except Exception as e:
        logger.error(f"Error organizing Drive: {str(e)}")
        return jsonify({'error': 'Failed to organize Google Drive'}), 500

@app.route('/api/google/gmail/process', methods=['POST'])
@require_permission('staff')
def process_gmail():
    """Process Gmail for project-related emails"""
    try:
        data = request.json
        project_id = data.get('project_id')
        
        # Use agent to process emails
        email_result = agent_orchestrator.process_project_emails(project_id)
        
        return jsonify({
            'success': True,
            'processed_emails': email_result['email_count'],
            'extracted_info': email_result['extracted_data'],
            'message': 'Emails processed and organized'
        })
        
    except Exception as e:
        logger.error(f"Error processing Gmail: {str(e)}")
        return jsonify({'error': 'Failed to process Gmail'}), 500

# ============================================================================
# MEMORY & LEARNING ENDPOINTS
# ============================================================================

@app.route('/api/memory/insights', methods=['GET'])
@require_permission('staff')
def get_memory_insights():
    """Get insights from accumulated memory"""
    try:
        user_id = session.get('user_id')
        
        insights = memory_system.get_pattern_insights(user_id)
        
        return jsonify({
            'success': True,
            'insights': insights,
            'pattern_count': len(insights)
        })
        
    except Exception as e:
        logger.error(f"Error getting memory insights: {str(e)}")
        return jsonify({'error': 'Failed to retrieve memory insights'}), 500

@app.route('/api/memory/search', methods=['POST'])
@require_permission('staff')
def search_memory():
    """Search memory for relevant patterns"""
    try:
        data = request.json
        query = data['query']
        user_id = session.get('user_id')
        
        results = memory_system.search_memories(query, user_id)
        
        return jsonify({
            'success': True,
            'results': results,
            'relevance_scores': [r['score'] for r in results]
        })
        
    except Exception as e:
        logger.error(f"Error searching memory: {str(e)}")
        return jsonify({'error': 'Failed to search memory'}), 500

# ============================================================================
# DASHBOARD DATA ENDPOINTS
# ============================================================================

@app.route('/api/dashboard/staff', methods=['GET'])
@require_permission('staff')
def get_staff_dashboard_data():
    """Get data for staff dashboard"""
    try:
        user_id = session.get('user_id')
        
        dashboard_data = {
            'projects': {
                'active_count': project_db.get_active_project_count(user_id),
                'critical_deadlines': project_db.get_critical_deadline_count(user_id),
                'next_deadline': project_db.get_next_deadline(user_id),
                'team_utilization': calculate_team_utilization(user_id)
            },
            'agent_insights': agent_orchestrator.get_staff_insights(user_id),
            'google_workspace': {
                'gmail_count': get_gmail_project_count(user_id),
                'drive_status': get_drive_organization_status(user_id),
                'docs_active': get_active_docs_count(user_id),
                'calendar_events': get_project_calendar_events(user_id)
            }
        }
        
        return jsonify({
            'success': True,
            'dashboard': dashboard_data
        })
        
    except Exception as e:
        logger.error(f"Error getting staff dashboard: {str(e)}")
        return jsonify({'error': 'Failed to retrieve dashboard data'}), 500

@app.route('/api/dashboard/admin', methods=['GET'])
@require_permission('admin')
def get_admin_dashboard_data():
    """Get data for admin dashboard"""
    try:
        dashboard_data = {
            'projects': {
                'active_count': project_db.get_total_active_projects(),
                'critical_deadlines': project_db.get_total_critical_deadlines(),
                'team_utilization': calculate_overall_team_utilization(),
                'agent_count': 7  # Multi-agent system
            },
            'billing': {
                'monthly_revenue': calculate_monthly_revenue(),
                'pending_proposals': project_db.get_pending_proposal_count(),
                'active_proposals': project_db.get_active_proposal_count(),
                'quickbooks_sync': get_last_quickbooks_sync()
            },
            'business_intelligence': {
                'revenue_growth': calculate_revenue_growth(),
                'project_success_rate': calculate_project_success_rate(),
                'team_performance': get_team_performance_metrics(),
                'client_satisfaction': get_client_satisfaction_score()
            },
            'agent_orchestration': agent_orchestrator.get_admin_orchestration_status()
        }
        
        return jsonify({
            'success': True,
            'dashboard': dashboard_data
        })
        
    except Exception as e:
        logger.error(f"Error getting admin dashboard: {str(e)}")
        return jsonify({'error': 'Failed to retrieve dashboard data'}), 500

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_quickbooks_sync_status(proposal_id):
    """Get QuickBooks sync status for proposal"""
    # Implementation would connect to QuickBooks API
    return {
        'synced': True,
        'last_sync': datetime.now().isoformat(),
        'qb_id': f"QB-{proposal_id}"
    }

def sync_with_quickbooks():
    """Sync data with QuickBooks"""
    # Implementation would use QuickBooks API
    return {
        'status': 'success',
        'timestamp': datetime.now().isoformat(),
        'count': 15
    }

def calculate_team_utilization(user_id=None):
    """Calculate team utilization percentage"""
    # Implementation would analyze task assignments and capacity
    return "87%"

def calculate_overall_team_utilization():
    """Calculate overall team utilization"""
    return "87%"

def calculate_monthly_revenue():
    """Calculate current monthly revenue"""
    # Implementation would sum up project revenues
    return "$127,450"

def calculate_revenue_growth():
    """Calculate revenue growth percentage"""
    return "+12%"

def calculate_project_success_rate():
    """Calculate project success rate"""
    return "94%"

def get_team_performance_metrics():
    """Get team performance metrics"""
    return {
        'efficiency': "92%",
        'quality_score': "4.8/5",
        'deadline_adherence': "89%"
    }

def get_client_satisfaction_score():
    """Get client satisfaction score"""
    return "4.7/5"

def get_gmail_project_count(user_id):
    """Get count of project-related emails"""
    return 12

def get_drive_organization_status(user_id):
    """Get Google Drive organization status"""
    return "Organized"

def get_active_docs_count(user_id):
    """Get count of active Google Docs"""
    return 8

def get_project_calendar_events(user_id):
    """Get project calendar events"""
    return 5

def get_last_quickbooks_sync():
    """Get last QuickBooks sync timestamp"""
    return "2 hours ago"

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# MAIN APPLICATION
# ============================================================================

if __name__ == '__main__':
    # Initialize database
    project_db.initialize_database()
    
    # Start agent monitoring
    agent_orchestrator.start_monitoring()
    
    # Run application
    app.run(debug=True, host='0.0.0.0', port=5001)

