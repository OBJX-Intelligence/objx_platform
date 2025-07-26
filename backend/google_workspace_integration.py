"""
OBJX Intelligence Platform - Google Workspace Integration
Multi-account management for Admin level with full Google Workspace suite
"""

import os
import json
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from flask import Flask, request, jsonify, session, redirect, url_for
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Google Workspace Services
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/admin.directory.user.readonly',
    'https://www.googleapis.com/auth/admin.directory.group.readonly'
]

@dataclass
class GoogleAccount:
    email: str
    name: str
    credentials: Credentials
    account_type: str  # 'business', 'personal'
    is_primary: bool
    created_at: datetime
    last_used: datetime

class GoogleWorkspaceManager:
    """
    Multi-account Google Workspace integration for OBJX Platform
    Supports Admin multi-account and Staff single-account access
    """
    
    def __init__(self):
        self.credentials_file = 'google_credentials.json'
        self.token_dir = 'google_tokens'
        self.accounts: Dict[str, GoogleAccount] = {}
        self.current_account = None
        
        # Ensure token directory exists
        os.makedirs(self.token_dir, exist_ok=True)
        
        # Load existing accounts
        self.load_accounts()
    
    def get_oauth_flow(self, redirect_uri: str) -> Flow:
        """Create OAuth flow for Google authentication"""
        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        return flow
    
    def get_auth_url(self, redirect_uri: str, account_type: str = 'business') -> str:
        """Get Google OAuth authorization URL"""
        flow = self.get_oauth_flow(redirect_uri)
        
        # Add account type to state
        flow.state = json.dumps({
            'account_type': account_type,
            'timestamp': datetime.now().isoformat()
        })
        
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'  # Force consent to get refresh token
        )
        
        return auth_url
    
    def handle_oauth_callback(self, code: str, state: str, redirect_uri: str) -> GoogleAccount:
        """Handle OAuth callback and store credentials"""
        flow = self.get_oauth_flow(redirect_uri)
        flow.fetch_token(code=code)
        
        credentials = flow.credentials
        
        # Parse state
        state_data = json.loads(state) if state else {'account_type': 'business'}
        account_type = state_data.get('account_type', 'business')
        
        # Get user info
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()
        
        email = user_info.get('email')
        name = user_info.get('name', email)
        
        # Create account object
        account = GoogleAccount(
            email=email,
            name=name,
            credentials=credentials,
            account_type=account_type,
            is_primary=len(self.accounts) == 0,  # First account is primary
            created_at=datetime.now(),
            last_used=datetime.now()
        )
        
        # Store account
        self.accounts[email] = account
        self.save_account(account)
        
        # Set as current if first account
        if not self.current_account:
            self.current_account = email
        
        return account
    
    def save_account(self, account: GoogleAccount):
        """Save account credentials to disk"""
        token_file = os.path.join(self.token_dir, f"{account.email.replace('@', '_at_')}.pickle")
        
        account_data = {
            'email': account.email,
            'name': account.name,
            'account_type': account.account_type,
            'is_primary': account.is_primary,
            'created_at': account.created_at.isoformat(),
            'last_used': account.last_used.isoformat(),
            'credentials': account.credentials
        }
        
        with open(token_file, 'wb') as token:
            pickle.dump(account_data, token)
    
    def load_accounts(self):
        """Load all saved accounts from disk"""
        if not os.path.exists(self.token_dir):
            return
        
        for filename in os.listdir(self.token_dir):
            if filename.endswith('.pickle'):
                token_file = os.path.join(self.token_dir, filename)
                try:
                    with open(token_file, 'rb') as token:
                        account_data = pickle.load(token)
                    
                    # Refresh credentials if needed
                    credentials = account_data['credentials']
                    if credentials.expired and credentials.refresh_token:
                        credentials.refresh(Request())
                    
                    account = GoogleAccount(
                        email=account_data['email'],
                        name=account_data['name'],
                        credentials=credentials,
                        account_type=account_data['account_type'],
                        is_primary=account_data['is_primary'],
                        created_at=datetime.fromisoformat(account_data['created_at']),
                        last_used=datetime.fromisoformat(account_data['last_used'])
                    )
                    
                    self.accounts[account.email] = account
                    
                    # Set primary as current
                    if account.is_primary:
                        self.current_account = account.email
                        
                except Exception as e:
                    print(f"Error loading account {filename}: {e}")
    
    def switch_account(self, email: str) -> bool:
        """Switch to a different Google account"""
        if email in self.accounts:
            self.current_account = email
            self.accounts[email].last_used = datetime.now()
            self.save_account(self.accounts[email])
            return True
        return False
    
    def get_current_account(self) -> Optional[GoogleAccount]:
        """Get currently active account"""
        if self.current_account and self.current_account in self.accounts:
            return self.accounts[self.current_account]
        return None
    
    def get_service(self, service_name: str, version: str = 'v1') -> Any:
        """Get Google API service for current account"""
        account = self.get_current_account()
        if not account:
            raise Exception("No active Google account")
        
        return build(service_name, version, credentials=account.credentials)
    
    def get_gmail_messages(self, query: str = '', max_results: int = 10) -> List[Dict]:
        """Get Gmail messages for current account"""
        try:
            service = self.get_service('gmail', 'v1')
            
            # Get message list
            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            # Get message details
            detailed_messages = []
            for message in messages:
                msg = service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='metadata'
                ).execute()
                
                # Extract headers
                headers = {h['name']: h['value'] for h in msg['payload'].get('headers', [])}
                
                detailed_messages.append({
                    'id': message['id'],
                    'subject': headers.get('Subject', 'No Subject'),
                    'from': headers.get('From', 'Unknown'),
                    'date': headers.get('Date', ''),
                    'snippet': msg.get('snippet', '')
                })
            
            return detailed_messages
            
        except HttpError as error:
            print(f'Gmail API error: {error}')
            return []
    
    def get_drive_files(self, folder_id: str = None, max_results: int = 10) -> List[Dict]:
        """Get Google Drive files for current account"""
        try:
            service = self.get_service('drive', 'v3')
            
            query = f"parents in '{folder_id}'" if folder_id else ""
            
            results = service.files().list(
                q=query,
                pageSize=max_results,
                fields="files(id, name, mimeType, modifiedTime, size)"
            ).execute()
            
            return results.get('files', [])
            
        except HttpError as error:
            print(f'Drive API error: {error}')
            return []
    
    def get_calendar_events(self, calendar_id: str = 'primary', max_results: int = 10) -> List[Dict]:
        """Get Google Calendar events for current account"""
        try:
            service = self.get_service('calendar', 'v3')
            
            # Get events for next 30 days
            now = datetime.utcnow().isoformat() + 'Z'
            end_time = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=now,
                timeMax=end_time,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                formatted_events.append({
                    'id': event['id'],
                    'summary': event.get('summary', 'No Title'),
                    'start': start,
                    'description': event.get('description', ''),
                    'location': event.get('location', '')
                })
            
            return formatted_events
            
        except HttpError as error:
            print(f'Calendar API error: {error}')
            return []
    
    def create_drive_folder(self, name: str, parent_id: str = None) -> str:
        """Create a new Google Drive folder"""
        try:
            service = self.get_service('drive', 'v3')
            
            folder_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                folder_metadata['parents'] = [parent_id]
            
            folder = service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            
            return folder.get('id')
            
        except HttpError as error:
            print(f'Drive folder creation error: {error}')
            return None
    
    def send_email(self, to: str, subject: str, body: str, html_body: str = None) -> bool:
        """Send email via Gmail API"""
        try:
            service = self.get_service('gmail', 'v1')
            
            message = self._create_message(to, subject, body, html_body)
            
            service.users().messages().send(
                userId='me',
                body=message
            ).execute()
            
            return True
            
        except HttpError as error:
            print(f'Gmail send error: {error}')
            return False
    
    def _create_message(self, to: str, subject: str, body: str, html_body: str = None) -> Dict:
        """Create email message for Gmail API"""
        import base64
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        if html_body:
            message = MIMEMultipart('alternative')
            message.attach(MIMEText(body, 'plain'))
            message.attach(MIMEText(html_body, 'html'))
        else:
            message = MIMEText(body)
        
        message['to'] = to
        message['subject'] = subject
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw_message}
    
    def get_account_summary(self) -> Dict:
        """Get summary of all connected accounts"""
        summary = {
            'total_accounts': len(self.accounts),
            'current_account': self.current_account,
            'accounts': []
        }
        
        for email, account in self.accounts.items():
            summary['accounts'].append({
                'email': account.email,
                'name': account.name,
                'account_type': account.account_type,
                'is_primary': account.is_primary,
                'is_current': email == self.current_account,
                'last_used': account.last_used.isoformat()
            })
        
        return summary

# Global instance
google_workspace = GoogleWorkspaceManager()

