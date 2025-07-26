"""
Unified Integration Manager for OBJX Intelligence Platform
Centralized authentication and connection management for all external services
Aligned with Trinity Foundation methodology: clarify • compound • create
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import hashlib
import base64
from urllib.parse import urlencode
import secrets

class UnifiedIntegrationManager:
    """
    Manages all external service integrations through the OBJX platform
    Provides centralized authentication, connection management, and data synchronization
    """
    
    def __init__(self):
        self.supported_integrations = {
            'google_workspace': {
                'name': 'Google Workspace',
                'services': ['gmail', 'drive', 'calendar', 'docs', 'sheets', 'contacts'],
                'auth_type': 'oauth2',
                'scopes': [
                    'https://www.googleapis.com/auth/gmail.readonly',
                    'https://www.googleapis.com/auth/drive.readonly',
                    'https://www.googleapis.com/auth/calendar.readonly',
                    'https://www.googleapis.com/auth/documents.readonly',
                    'https://www.googleapis.com/auth/spreadsheets.readonly',
                    'https://www.googleapis.com/auth/contacts.readonly'
                ],
                'trinity_alignment': {
                    'clarify': 'Email and document analysis for project requirements',
                    'compound': 'Cross-platform data intelligence and pattern recognition',
                    'create': 'Automated document generation and collaboration',
                    'complete': 'Task management and delivery coordination'
                }
            },
            'quickbooks': {
                'name': 'QuickBooks Online',
                'services': ['accounting', 'invoicing', 'expenses', 'reports'],
                'auth_type': 'oauth2',
                'scopes': ['com.intuit.quickbooks.accounting'],
                'trinity_alignment': {
                    'clarify': 'Financial requirements and budget analysis',
                    'compound': 'Financial intelligence and cost optimization',
                    'create': 'Automated invoicing and expense categorization',
                    'complete': 'Payment tracking and financial reporting'
                }
            },
            'stripe': {
                'name': 'Stripe Payments',
                'services': ['payments', 'subscriptions', 'invoicing', 'analytics'],
                'auth_type': 'api_key',
                'scopes': ['read_write'],
                'trinity_alignment': {
                    'clarify': 'Payment requirements and subscription analysis',
                    'compound': 'Revenue intelligence and customer insights',
                    'create': 'Automated payment processing and subscription management',
                    'complete': 'Payment completion and revenue tracking'
                }
            },
            'microsoft_365': {
                'name': 'Microsoft 365',
                'services': ['outlook', 'onedrive', 'teams', 'sharepoint'],
                'auth_type': 'oauth2',
                'scopes': [
                    'https://graph.microsoft.com/mail.read',
                    'https://graph.microsoft.com/files.read',
                    'https://graph.microsoft.com/calendars.read'
                ],
                'trinity_alignment': {
                    'clarify': 'Email and document analysis for project clarity',
                    'compound': 'Cross-platform intelligence and collaboration',
                    'create': 'Document creation and team coordination',
                    'complete': 'Task completion and delivery management'
                }
            },
            'slack': {
                'name': 'Slack',
                'services': ['messaging', 'channels', 'files', 'notifications'],
                'auth_type': 'oauth2',
                'scopes': ['channels:read', 'chat:write', 'files:read', 'users:read'],
                'trinity_alignment': {
                    'clarify': 'Team communication analysis and requirement gathering',
                    'compound': 'Communication intelligence and pattern recognition',
                    'create': 'Automated notifications and team coordination',
                    'complete': 'Delivery notifications and completion tracking'
                }
            },
            'zapier': {
                'name': 'Zapier',
                'services': ['automation', 'workflows', 'triggers', 'actions'],
                'auth_type': 'api_key',
                'scopes': ['read_write'],
                'trinity_alignment': {
                    'clarify': 'Workflow analysis and automation opportunities',
                    'compound': 'Cross-platform automation intelligence',
                    'create': 'Automated workflow creation and optimization',
                    'complete': 'Execution automation and completion tracking'
                }
            }
        }
        
        self.connection_states = {}  # Store active connections
        self.oauth_states = {}       # Store OAuth state tokens
        
    def initiate_integration_connection(self, user_id: str, integration_type: str, 
                                      connection_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Initiate connection to an external service through OBJX platform
        """
        try:
            if integration_type not in self.supported_integrations:
                return {
                    'success': False,
                    'error': f"Integration type '{integration_type}' not supported"
                }
            
            integration_info = self.supported_integrations[integration_type]
            
            # Generate unique connection session
            connection_id = f"conn_{uuid.uuid4().hex[:12]}"
            state_token = secrets.token_urlsafe(32)
            
            # Store connection state
            self.connection_states[connection_id] = {
                'user_id': user_id,
                'integration_type': integration_type,
                'state_token': state_token,
                'initiated_at': datetime.now().isoformat(),
                'status': 'initiated',
                'config': connection_config or {}
            }
            
            # Generate authentication URL based on integration type
            if integration_info['auth_type'] == 'oauth2':
                auth_url = self._generate_oauth2_url(
                    integration_type, connection_id, state_token, integration_info
                )
                
                return {
                    'success': True,
                    'connection_id': connection_id,
                    'auth_url': auth_url,
                    'auth_type': 'oauth2',
                    'integration_info': {
                        'name': integration_info['name'],
                        'services': integration_info['services'],
                        'trinity_alignment': integration_info['trinity_alignment']
                    },
                    'instructions': f"Click the authentication URL to connect your {integration_info['name']} account"
                }
            
            elif integration_info['auth_type'] == 'api_key':
                return {
                    'success': True,
                    'connection_id': connection_id,
                    'auth_type': 'api_key',
                    'integration_info': {
                        'name': integration_info['name'],
                        'services': integration_info['services'],
                        'trinity_alignment': integration_info['trinity_alignment']
                    },
                    'instructions': f"Please provide your {integration_info['name']} API key to complete the connection"
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to initiate integration connection: {str(e)}"
            }

# Initialize the unified integration manager
integration_manager = UnifiedIntegrationManager()

