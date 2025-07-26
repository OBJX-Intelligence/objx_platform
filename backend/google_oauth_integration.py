"""
Google OAuth Integration System
Multi-account executive access for OBJX Intelligence Platform
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, request, redirect, session, jsonify, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import secrets
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleOAuthManager:
    """Manages Google OAuth integration for OBJX Intelligence Platform"""
    
    def __init__(self, client_secrets_file=None):
        self.client_secrets_file = client_secrets_file or 'google_client_secrets.json'
        self.scopes = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile'
        ]
        self.redirect_uri = 'http://localhost:5001/oauth/callback'
        self.init_database()
    
    def init_database(self):
        """Initialize OAuth database tables"""
        conn = sqlite3.connect('objx_platform.db')
        cursor = conn.cursor()
        
        # Google OAuth accounts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS google_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                account_email TEXT NOT NULL,
                account_name TEXT,
                access_token TEXT NOT NULL,
                refresh_token TEXT,
                token_expiry DATETIME,
                scopes TEXT,
                account_type TEXT DEFAULT 'workspace',
                is_primary BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, account_email)
            )
        ''')
        
        # OAuth state tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS oauth_states (
                state TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                account_type TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("OAuth database tables initialized")
    
    def create_client_secrets_template(self):
        """Create template for Google OAuth client secrets"""
        template = {
            "web": {
                "client_id": "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com",
                "project_id": "your-project-id",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "YOUR_GOOGLE_CLIENT_SECRET",
                "redirect_uris": ["http://localhost:5001/oauth/callback"]
            }
        }
        
        with open('google_client_secrets_template.json', 'w') as f:
            json.dump(template, f, indent=2)
        
        logger.info("Google OAuth client secrets template created")
        return template
    
    def initiate_oauth_flow(self, user_id, account_type='workspace'):
        """Initiate Google OAuth flow for user"""
        try:
            # Create OAuth flow
            flow = Flow.from_client_secrets_file(
                self.client_secrets_file,
                scopes=self.scopes
            )
            flow.redirect_uri = self.redirect_uri
            
            # Generate secure state parameter
            state = secrets.token_urlsafe(32)
            
            # Store state in database
            conn = sqlite3.connect('objx_platform.db')
            cursor = conn.cursor()
            
            expires_at = datetime.now() + timedelta(minutes=10)
            cursor.execute('''
                INSERT INTO oauth_states (state, user_id, account_type, expires_at)
                VALUES (?, ?, ?, ?)
            ''', (state, user_id, account_type, expires_at))
            
            conn.commit()
            conn.close()
            
            # Get authorization URL
            authorization_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                state=state,
                prompt='consent'  # Force consent to get refresh token
            )
            
            logger.info(f"OAuth flow initiated for user {user_id}")
            return {
                'success': True,
                'authorization_url': authorization_url,
                'state': state
            }
            
        except Exception as e:
            logger.error(f"Error initiating OAuth flow: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def handle_oauth_callback(self, code, state):
        """Handle OAuth callback and store credentials"""
        try:
            # Verify state parameter
            conn = sqlite3.connect('objx_platform.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, account_type FROM oauth_states 
                WHERE state = ? AND expires_at > ?
            ''', (state, datetime.now()))
            
            result = cursor.fetchone()
            if not result:
                return {'success': False, 'error': 'Invalid or expired state parameter'}
            
            user_id, account_type = result
            
            # Exchange code for credentials
            flow = Flow.from_client_secrets_file(
                self.client_secrets_file,
                scopes=self.scopes,
                state=state
            )
            flow.redirect_uri = self.redirect_uri
            
            flow.fetch_token(code=code)
            credentials = flow.credentials
            
            # Get user info from Google
            user_service = build('oauth2', 'v2', credentials=credentials)
            user_info = user_service.userinfo().get().execute()
            
            account_email = user_info.get('email')
            account_name = user_info.get('name')
            
            # Store credentials in database
            cursor.execute('''
                INSERT OR REPLACE INTO google_accounts 
                (user_id, account_email, account_name, access_token, refresh_token, 
                 token_expiry, scopes, account_type, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                account_email,
                account_name,
                credentials.token,
                credentials.refresh_token,
                credentials.expiry,
                json.dumps(self.scopes),
                account_type,
                datetime.now()
            ))
            
            # Clean up state
            cursor.execute('DELETE FROM oauth_states WHERE state = ?', (state,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"OAuth credentials stored for user {user_id}, account {account_email}")
            return {
                'success': True,
                'account_email': account_email,
                'account_name': account_name,
                'account_type': account_type
            }
            
        except Exception as e:
            logger.error(f"Error handling OAuth callback: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user_accounts(self, user_id):
        """Get all Google accounts for a user"""
        conn = sqlite3.connect('objx_platform.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT account_email, account_name, account_type, is_primary, created_at
            FROM google_accounts 
            WHERE user_id = ?
            ORDER BY is_primary DESC, created_at ASC
        ''', (user_id,))
        
        accounts = []
        for row in cursor.fetchall():
            accounts.append({
                'email': row[0],
                'name': row[1],
                'type': row[2],
                'is_primary': bool(row[3]),
                'connected_at': row[4]
            })
        
        conn.close()
        return accounts
    
    def get_credentials_for_account(self, user_id, account_email):
        """Get and refresh credentials for specific account"""
        conn = sqlite3.connect('objx_platform.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT access_token, refresh_token, token_expiry, scopes
            FROM google_accounts 
            WHERE user_id = ? AND account_email = ?
        ''', (user_id, account_email))
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            return None
        
        access_token, refresh_token, token_expiry, scopes = result
        
        # Create credentials object
        credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=self.get_client_id(),
            client_secret=self.get_client_secret(),
            scopes=json.loads(scopes) if scopes else self.scopes
        )
        
        if token_expiry:
            credentials.expiry = datetime.fromisoformat(token_expiry.replace('Z', '+00:00'))
        
        # Refresh if needed
        if credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
                
                # Update database with new token
                cursor.execute('''
                    UPDATE google_accounts 
                    SET access_token = ?, token_expiry = ?, updated_at = ?
                    WHERE user_id = ? AND account_email = ?
                ''', (
                    credentials.token,
                    credentials.expiry,
                    datetime.now(),
                    user_id,
                    account_email
                ))
                conn.commit()
                
                logger.info(f"Refreshed credentials for {account_email}")
                
            except Exception as e:
                logger.error(f"Error refreshing credentials: {str(e)}")
                conn.close()
                return None
        
        conn.close()
        return credentials
    
    def get_client_id(self):
        """Get Google OAuth client ID"""
        try:
            with open(self.client_secrets_file, 'r') as f:
                secrets = json.load(f)
                return secrets['web']['client_id']
        except:
            return None
    
    def get_client_secret(self):
        """Get Google OAuth client secret"""
        try:
            with open(self.client_secrets_file, 'r') as f:
                secrets = json.load(f)
                return secrets['web']['client_secret']
        except:
            return None
    
    def disconnect_account(self, user_id, account_email):
        """Disconnect a Google account"""
        conn = sqlite3.connect('objx_platform.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM google_accounts 
            WHERE user_id = ? AND account_email = ?
        ''', (user_id, account_email))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Disconnected Google account {account_email} for user {user_id}")
        return True

# Google API Service Builder
class GoogleServiceBuilder:
    """Build Google API services with proper credentials"""
    
    def __init__(self, oauth_manager):
        self.oauth_manager = oauth_manager
    
    def build_service(self, service_name, version, user_id, account_email=None):
        """Build Google API service for user"""
        # Get credentials
        if account_email:
            credentials = self.oauth_manager.get_credentials_for_account(user_id, account_email)
        else:
            # Use primary account
            accounts = self.oauth_manager.get_user_accounts(user_id)
            if not accounts:
                return None
            primary_account = next((acc for acc in accounts if acc['is_primary']), accounts[0])
            credentials = self.oauth_manager.get_credentials_for_account(user_id, primary_account['email'])
        
        if not credentials:
            return None
        
        try:
            return build(service_name, version, credentials=credentials)
        except Exception as e:
            logger.error(f"Error building {service_name} service: {str(e)}")
            return None

# Initialize OAuth manager
oauth_manager = GoogleOAuthManager()
service_builder = GoogleServiceBuilder(oauth_manager)

# Create client secrets template if needed
if not os.path.exists('google_client_secrets.json'):
    oauth_manager.create_client_secrets_template()
    logger.info("Created Google OAuth client secrets template - please configure with your credentials")

