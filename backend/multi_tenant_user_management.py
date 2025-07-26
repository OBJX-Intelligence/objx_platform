"""
OBJX Intelligence Platform - Multi-Tenant User Management System
White-label ready architecture with tenant isolation and configurable branding
"""

import os
import sqlite3
import hashlib
import secrets
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class UserRole(Enum):
    ADMIN = "admin"
    STAFF = "staff"
    TIER_1 = "tier_1"
    TIER_2 = "tier_2"
    TIER_3 = "tier_3"

class UserStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"

@dataclass
class Organization:
    id: str
    name: str
    domain: str
    branding: Dict
    settings: Dict
    created_at: datetime
    status: str

@dataclass
class User:
    id: str
    organization_id: str
    email: str
    name: str
    role: UserRole
    status: UserStatus
    google_oauth_connected: bool
    invitation_token: Optional[str]
    created_at: datetime
    last_login: Optional[datetime]
    settings: Dict

class MultiTenantUserManager:
    """
    Multi-tenant user management system with white-label capabilities
    
    Features:
    - Complete tenant isolation
    - Configurable branding per organization
    - Role-based access control
    - Email invitation system
    - Google OAuth integration ready
    - White-label deployment ready
    """
    
    def __init__(self, db_path: str = "objx_platform.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize multi-tenant database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Organizations table (white-label tenants)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS organizations (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                domain TEXT UNIQUE NOT NULL,
                branding TEXT NOT NULL,  -- JSON: logo, colors, theme
                settings TEXT NOT NULL,  -- JSON: features, limits, config
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Users table with tenant isolation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                organization_id TEXT NOT NULL,
                email TEXT NOT NULL,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                password_hash TEXT,
                google_oauth_connected BOOLEAN DEFAULT FALSE,
                google_oauth_data TEXT,  -- JSON: tokens, profile
                invitation_token TEXT,
                invitation_expires TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                settings TEXT DEFAULT '{}',
                FOREIGN KEY (organization_id) REFERENCES organizations (id),
                UNIQUE(organization_id, email)
            )
        ''')
        
        # User sessions for multi-tenant auth
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                organization_id TEXT NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (organization_id) REFERENCES organizations (id)
            )
        ''')
        
        # Organization invitations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invitations (
                id TEXT PRIMARY KEY,
                organization_id TEXT NOT NULL,
                email TEXT NOT NULL,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                invited_by TEXT NOT NULL,
                invitation_token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                accepted_at TIMESTAMP,
                FOREIGN KEY (organization_id) REFERENCES organizations (id),
                FOREIGN KEY (invited_by) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_organization(self, name: str, domain: str, admin_email: str, admin_name: str, 
                          branding: Dict = None, settings: Dict = None) -> str:
        """Create a new organization (white-label tenant)"""
        org_id = f"org_{secrets.token_urlsafe(16)}"
        
        default_branding = {
            "logo_url": "/static/logos/objx-logo.png",
            "primary_color": "#8B5CF6",
            "secondary_color": "#7C3AED",
            "background_gradient": "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
            "company_name": name,
            "theme": "dark"
        }
        
        default_settings = {
            "max_users": 100,
            "features": {
                "memory_management": True,
                "project_management": True,
                "google_integration": True,
                "custom_branding": True
            },
            "email_domain": domain,
            "timezone": "UTC"
        }
        
        branding = branding or default_branding
        settings = settings or default_settings
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Create organization
            cursor.execute('''
                INSERT INTO organizations (id, name, domain, branding, settings)
                VALUES (?, ?, ?, ?, ?)
            ''', (org_id, name, domain, json.dumps(branding), json.dumps(settings)))
            
            # Create admin user
            admin_id = f"user_{secrets.token_urlsafe(16)}"
            cursor.execute('''
                INSERT INTO users (id, organization_id, email, name, role, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, org_id, admin_email, admin_name, UserRole.ADMIN.value, UserStatus.ACTIVE.value))
            
            conn.commit()
            return org_id
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise ValueError(f"Organization creation failed: {e}")
        finally:
            conn.close()
    
    def invite_user(self, organization_id: str, email: str, name: str, role: UserRole, 
                   invited_by_user_id: str) -> str:
        """Send user invitation with tenant isolation"""
        invitation_token = secrets.token_urlsafe(32)
        invitation_id = f"inv_{secrets.token_urlsafe(16)}"
        expires_at = datetime.now() + timedelta(days=7)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if user already exists in this organization
            cursor.execute('''
                SELECT id FROM users WHERE organization_id = ? AND email = ?
            ''', (organization_id, email))
            
            if cursor.fetchone():
                raise ValueError("User already exists in this organization")
            
            # Create invitation
            cursor.execute('''
                INSERT INTO invitations (id, organization_id, email, name, role, invited_by, 
                                       invitation_token, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (invitation_id, organization_id, email, name, role.value, 
                  invited_by_user_id, invitation_token, expires_at))
            
            conn.commit()
            
            # Send invitation email
            self._send_invitation_email(organization_id, email, name, role, invitation_token)
            
            return invitation_token
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def accept_invitation(self, invitation_token: str, password: str = None) -> Dict:
        """Accept user invitation and create account"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get invitation details
            cursor.execute('''
                SELECT i.*, o.name as org_name, o.domain, o.branding
                FROM invitations i
                JOIN organizations o ON i.organization_id = o.id
                WHERE i.invitation_token = ? AND i.status = 'pending' AND i.expires_at > ?
            ''', (invitation_token, datetime.now()))
            
            invitation = cursor.fetchone()
            if not invitation:
                raise ValueError("Invalid or expired invitation")
            
            # Create user account
            user_id = f"user_{secrets.token_urlsafe(16)}"
            password_hash = hashlib.sha256(password.encode()).hexdigest() if password else None
            
            cursor.execute('''
                INSERT INTO users (id, organization_id, email, name, role, status, password_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, invitation[1], invitation[2], invitation[3], invitation[4], 
                  UserStatus.ACTIVE.value, password_hash))
            
            # Mark invitation as accepted
            cursor.execute('''
                UPDATE invitations SET status = 'accepted', accepted_at = ?
                WHERE invitation_token = ?
            ''', (datetime.now(), invitation_token))
            
            conn.commit()
            
            return {
                "user_id": user_id,
                "organization_id": invitation[1],
                "email": invitation[2],
                "name": invitation[3],
                "role": invitation[4],
                "organization": {
                    "name": invitation[7],
                    "domain": invitation[8],
                    "branding": json.loads(invitation[9])
                }
            }
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_organization_users(self, organization_id: str) -> List[Dict]:
        """Get all users for a specific organization"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, name, role, status, google_oauth_connected, 
                   created_at, last_login, settings
            FROM users 
            WHERE organization_id = ?
            ORDER BY created_at DESC
        ''', (organization_id,))
        
        users = []
        for row in cursor.fetchall():
            users.append({
                "id": row[0],
                "email": row[1],
                "name": row[2],
                "role": row[3],
                "status": row[4],
                "google_oauth_connected": bool(row[5]),
                "created_at": row[6],
                "last_login": row[7],
                "settings": json.loads(row[8] or '{}')
            })
        
        conn.close()
        return users
    
    def get_organization_branding(self, organization_id: str) -> Dict:
        """Get organization branding for white-label customization"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT branding FROM organizations WHERE id = ?
        ''', (organization_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return json.loads(result[0])
        return {}
    
    def update_organization_branding(self, organization_id: str, branding: Dict) -> bool:
        """Update organization branding for white-label customization"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE organizations SET branding = ? WHERE id = ?
            ''', (json.dumps(branding), organization_id))
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def _send_invitation_email(self, organization_id: str, email: str, name: str, 
                             role: UserRole, invitation_token: str):
        """Send invitation email with organization branding"""
        # Get organization details for branded email
        branding = self.get_organization_branding(organization_id)
        company_name = branding.get('company_name', 'OBJX Intelligence')
        
        # Email configuration (would be configurable per organization)
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_user = os.getenv('SMTP_USER')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not smtp_user or not smtp_password:
            print(f"Email not configured. Invitation token for {email}: {invitation_token}")
            return
        
        # Create invitation URL
        base_url = os.getenv('BASE_URL', 'http://localhost:5000')
        invitation_url = f"{base_url}/accept-invitation?token={invitation_token}"
        
        # Create email content
        subject = f"Invitation to join {company_name} Intelligence Platform"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 40px;">
            <div style="max-width: 600px; margin: 0 auto; background: rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 40px;">
                <h1 style="color: {branding.get('primary_color', '#8B5CF6')}; text-align: center;">
                    Welcome to {company_name}
                </h1>
                <p>Hello {name},</p>
                <p>You've been invited to join {company_name} Intelligence Platform as a <strong>{role.value.replace('_', ' ').title()}</strong> user.</p>
                <p>Click the button below to accept your invitation and set up your account:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{invitation_url}" 
                       style="background: linear-gradient(135deg, {branding.get('primary_color', '#8B5CF6')} 0%, {branding.get('secondary_color', '#7C3AED')} 100%); 
                              color: white; padding: 15px 30px; text-decoration: none; border-radius: 10px; 
                              font-weight: bold; display: inline-block;">
                        Accept Invitation
                    </a>
                </div>
                <p><small>This invitation expires in 7 days. If you didn't expect this invitation, you can safely ignore this email.</small></p>
            </div>
        </body>
        </html>
        """
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = smtp_user
            msg['To'] = email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
                
            print(f"Invitation email sent to {email}")
            
        except Exception as e:
            print(f"Failed to send email to {email}: {e}")
            print(f"Invitation URL: {invitation_url}")

# Global instance
user_manager = MultiTenantUserManager()

