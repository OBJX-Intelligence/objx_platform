"""
OBJX Intelligence Platform - Integrated Flask Application
Complete backend integration with chat, memory, and notification systems
"""

import os
import json
import asyncio
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string, send_from_directory, redirect, session
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our backend systems
from universal_chat_system import universal_chat, UserTier
from memory_command_center import memory_center, MemoryType, MemoryPriority
from notification_system import notification_system, NotificationType, NotificationPriority, UserRole
from role_based_memory_manager import role_based_memory, UserTier as MemoryUserTier, MemoryScope, MemoryType as RoleMemoryType
from multi_tenant_user_management import user_manager, UserRole as UserManagementRole
from google_oauth_integration import oauth_manager, service_builder
from payment_integration import get_payment_integration
from agent_management_system import get_agent_management
from project_intelligence_system import get_project_intelligence

app = Flask(__name__)
CORS(app)

# Configure Flask
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'objx-intelligence-platform-secret')

# User session simulation (in production, this would use proper authentication)
user_sessions = {
    'demo_user_tier1': {'tier': UserTier.TIER_1, 'role': UserRole.CLIENT},
    'demo_user_tier2': {'tier': UserTier.TIER_2, 'role': UserRole.CLIENT},
    'demo_user_tier3': {'tier': UserTier.TIER_3, 'role': UserRole.CLIENT},
    'demo_staff': {'tier': UserTier.STAFF, 'role': UserRole.STAFF},
    'demo_admin': {'tier': UserTier.ADMIN, 'role': UserRole.ADMIN}
}

@app.route('/')
def index():
    """Serve the main landing page"""
    try:
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'index.html')
        with open(frontend_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Landing page not found", 404

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    try:
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', filename)
        with open(frontend_path, 'r') as f:
            content = f.read()
        
        # Determine content type
        if filename.endswith('.html'):
            return content, 200, {'Content-Type': 'text/html'}
        elif filename.endswith('.css'):
            return content, 200, {'Content-Type': 'text/css'}
        elif filename.endswith('.js'):
            return content, 200, {'Content-Type': 'application/javascript'}
        elif filename.endswith('.svg'):
            return content, 200, {'Content-Type': 'image/svg+xml'}
        else:
            return content
    except FileNotFoundError:
        return f"File {filename} not found", 404

@app.route('/api/chat', methods=['POST'])
async def chat_endpoint():
    """Handle chat messages with tier-based permissions"""
    try:
        data = request.get_json()
        
        # Extract request data
        message = data.get('message', '')
        user_id = data.get('user_id', 'demo_user_tier3')  # Default for testing
        agent_type = data.get('agent_type', 'systematic_thinking')
        conversation_history = data.get('conversation_history', [])
        
        # Get user session
        user_session = user_sessions.get(user_id, {
            'tier': UserTier.TIER_1, 
            'role': UserRole.CLIENT
        })
        
        user_tier = user_session['tier']
        
        # Validate message
        if not message.strip():
            return jsonify({
                'error': 'Message cannot be empty',
                'response': 'Please provide a message to continue our conversation.'
            }), 400
        
        # Process message through universal chat system
        context = {
            'conversation_history': conversation_history,
            'agent_type': agent_type
        }
        
        response_data = await universal_chat.process_chat_message(
            user_id=user_id,
            user_tier=user_tier,
            message=message,
            context=context
        )
        
        # Create notification for new chat interaction (for admin/staff)
        if user_tier in [UserTier.ADMIN, UserTier.STAFF]:
            notification_system.create_notification(
                title="Chat Interaction",
                message=f"New chat message processed for {user_tier.value}",
                notification_type=NotificationType.SYSTEM_EVENT,
                priority=NotificationPriority.LOW,
                user_id=user_id,
                user_role=user_session['role']
            )
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'response': 'I apologize, but I\'m experiencing technical difficulties. Please try again.'
        }), 500

@app.route('/api/memory/search', methods=['POST'])
def memory_search():
    """Search memories with tier-based filtering"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        user_id = data.get('user_id', 'demo_user_tier3')
        
        # Get user session
        user_session = user_sessions.get(user_id, {
            'tier': UserTier.TIER_1, 
            'role': UserRole.CLIENT
        })
        
        # Only allow memory search for Tier 2+
        if user_session['tier'] == UserTier.TIER_1:
            return jsonify({
                'error': 'Memory access not available for Tier 1',
                'memories': []
            }), 403
        
        # Search memories
        memories = memory_center.search_memories(
            query=query,
            user_id=user_id if user_session['tier'] in [UserTier.TIER_2, UserTier.TIER_3] else None
        )
        
        # Format response
        memory_list = []
        for memory in memories[:10]:  # Limit to 10 results
            memory_list.append({
                'id': memory.id,
                'content': memory.content[:200] + '...' if len(memory.content) > 200 else memory.content,
                'created_at': memory.created_at.isoformat(),
                'memory_type': memory.memory_type.value,
                'priority': memory.priority.value,
                'relevance_score': getattr(memory, 'relevance_score', 0.0)
            })
        
        return jsonify({
            'memories': memory_list,
            'total': len(memory_list)
        })
        
    except Exception as e:
        print(f"Memory search error: {e}")
        return jsonify({
            'error': 'Memory search failed',
            'memories': []
        }), 500

@app.route('/api/memory/create', methods=['POST'])
def memory_create():
    """Create new memory with tier-based permissions"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        user_id = data.get('user_id', 'demo_user_tier3')
        memory_type = data.get('memory_type', 'client')
        priority = data.get('priority', 'medium')
        tags = data.get('tags', [])
        
        # Get user session
        user_session = user_sessions.get(user_id, {
            'tier': UserTier.TIER_1, 
            'role': UserRole.CLIENT
        })
        
        # Only allow memory creation for Tier 2+
        if user_session['tier'] == UserTier.TIER_1:
            return jsonify({
                'error': 'Memory creation not available for Tier 1'
            }), 403
        
        # Create memory
        memory_id = memory_center.create_memory(
            content=content,
            user_id=user_id,
            memory_type=MemoryType(memory_type),
            priority=MemoryPriority(priority),
            client_id=user_id if user_session['tier'] in [UserTier.TIER_2, UserTier.TIER_3] else None,
            tags=tags
        )
        
        return jsonify({
            'memory_id': memory_id,
            'status': 'created'
        })
        
    except Exception as e:
        print(f"Memory creation error: {e}")
        return jsonify({
            'error': 'Memory creation failed'
        }), 500

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    """Get notifications for user"""
    try:
        user_id = request.args.get('user_id', 'demo_user_tier3')
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        limit = int(request.args.get('limit', 20))
        
        notifications = notification_system.get_user_notifications(
            user_id=user_id,
            unread_only=unread_only,
            limit=limit
        )
        
        return jsonify({
            'notifications': notifications,
            'total': len(notifications)
        })
        
    except Exception as e:
        print(f"Get notifications error: {e}")
        return jsonify({
            'error': 'Failed to retrieve notifications',
            'notifications': []
        }), 500

@app.route('/api/notifications/<notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    """Mark notification as read"""
    try:
        user_id = request.json.get('user_id', 'demo_user_tier3')
        
        success = notification_system.mark_notification_read(
            notification_id=notification_id,
            user_id=user_id
        )
        
        return jsonify({
            'success': success
        })
        
    except Exception as e:
        print(f"Mark notification read error: {e}")
        return jsonify({
            'error': 'Failed to mark notification as read',
            'success': False
        }), 500

@app.route('/api/user/tier', methods=['GET'])
def get_user_tier():
    """Get user tier information"""
    try:
        user_id = request.args.get('user_id', 'demo_user_tier3')
        
        user_session = user_sessions.get(user_id, {
            'tier': UserTier.TIER_1, 
            'role': UserRole.CLIENT
        })
        
        # Get available agents for this tier
        available_agents = universal_chat.get_available_agents(user_session['tier'])
        
        # Get permissions
        permissions = universal_chat._get_tier_permissions(user_session['tier'])
        
        return jsonify({
            'user_id': user_id,
            'tier': user_session['tier'].value,
            'role': user_session['role'].value,
            'available_agents': available_agents,
            'permissions': permissions
        })
        
    except Exception as e:
        print(f"Get user tier error: {e}")
        return jsonify({
            'error': 'Failed to retrieve user information'
        }), 500

@app.route('/api/memory/stats', methods=['GET'])
def memory_stats():
    """Get memory statistics for admin users"""
    try:
        user_id = request.args.get('user_id', 'demo_admin')
        
        user_session = user_sessions.get(user_id, {
            'tier': UserTier.TIER_1, 
            'role': UserRole.CLIENT
        })
        
        # Only allow for admin users
        if user_session['tier'] != UserTier.ADMIN:
            return jsonify({
                'error': 'Admin access required'
            }), 403
        
        stats = memory_center.get_memory_statistics()
        
        return jsonify(stats)
        
    except Exception as e:
        print(f"Memory stats error: {e}")
        return jsonify({
            'error': 'Failed to retrieve memory statistics'
        }), 500

# ============================================================================
# USER MANAGEMENT API ENDPOINTS
# ============================================================================

@app.route('/api/users/invite', methods=['POST'])
def invite_user():
    """Send user invitation for staff or admin"""
    try:
        data = request.get_json()
        
        # Extract request data
        email = data.get('email', '').strip()
        name = data.get('name', '').strip()
        role = data.get('role', '').lower()
        invited_by_user_id = data.get('invited_by', 'demo_admin')
        
        # Validate input
        if not email or not name or not role:
            return jsonify({
                'error': 'Email, name, and role are required'
            }), 400
        
        # Validate role
        if role not in ['admin', 'staff']:
            return jsonify({
                'error': 'Role must be either "admin" or "staff"'
            }), 400
        
        # Check if inviting user has permission (admin only for now)
        user_session = user_sessions.get(invited_by_user_id, {})
        if user_session.get('tier') != UserTier.ADMIN:
            return jsonify({
                'error': 'Admin access required to invite users'
            }), 403
        
        # For now, use a default organization (your business)
        # In future white-label, this would be dynamic
        organization_id = "objx_main_org"
        
        # Ensure organization exists (create if first time)
        try:
            user_manager.create_organization(
                name="OBJX Intelligence",
                domain="objx.design",
                admin_email="admin@objx.design",
                admin_name="OBJX Admin"
            )
        except ValueError:
            # Organization already exists, continue
            pass
        
        # Convert role to UserManagementRole
        user_role = UserManagementRole.ADMIN if role == 'admin' else UserManagementRole.STAFF
        
        # Send invitation
        invitation_token = user_manager.invite_user(
            organization_id=organization_id,
            email=email,
            name=name,
            role=user_role,
            invited_by_user_id=invited_by_user_id
        )
        
        return jsonify({
            'success': True,
            'message': f'Invitation sent to {email}',
            'invitation_token': invitation_token,
            'role': role
        })
        
    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400
    except Exception as e:
        print(f"User invitation error: {e}")
        return jsonify({
            'error': 'Failed to send invitation'
        }), 500

@app.route('/api/users/list', methods=['GET'])
def list_users():
    """Get list of users for admin dashboard"""
    try:
        user_id = request.args.get('user_id', 'demo_admin')
        
        # Check admin permission
        user_session = user_sessions.get(user_id, {})
        if user_session.get('tier') != UserTier.ADMIN:
            return jsonify({
                'error': 'Admin access required'
            }), 403
        
        # Get users for main organization
        organization_id = "objx_main_org"
        users = user_manager.get_organization_users(organization_id)
        
        return jsonify({
            'users': users,
            'total': len(users)
        })
        
    except Exception as e:
        print(f"List users error: {e}")
        return jsonify({
            'error': 'Failed to retrieve users',
            'users': []
        }), 500

@app.route('/api/users/current', methods=['GET'])
def get_current_user():
    """Get current user information"""
    try:
        user_id = request.args.get('user_id', 'demo_admin')
        
        # For demo, return mock current user data
        # In production, this would get real user data from database
        user_session = user_sessions.get(user_id, {})
        
        return jsonify({
            'id': user_id,
            'name': 'OBJX Admin',
            'email': 'admin@objx.design',
            'role': 'admin',
            'tier': user_session.get('tier', UserTier.ADMIN).value,
            'google_connected': True,  # Mock for now
            'organization': {
                'name': 'OBJX Intelligence',
                'domain': 'objx.design'
            }
        })
        
    except Exception as e:
        print(f"Get current user error: {e}")
        return jsonify({
            'error': 'Failed to retrieve user information'
        }), 500

@app.route('/accept-invitation')
def accept_invitation_page():
    """Serve invitation acceptance page"""
    try:
        token = request.args.get('token')
        if not token:
            return "Invalid invitation link", 400
        
        # Create a simple invitation acceptance page
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Accept Invitation - OBJX Intelligence</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    color: white;
                    padding: 40px;
                    margin: 0;
                }}
                .container {{
                    max-width: 500px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 20px;
                    padding: 40px;
                    text-align: center;
                }}
                .btn {{
                    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
                    color: white;
                    padding: 15px 30px;
                    border: none;
                    border-radius: 10px;
                    font-weight: bold;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to OBJX Intelligence</h1>
                <p>You've been invited to join our platform!</p>
                <p>Click below to accept your invitation and set up your account:</p>
                <a href="/dashboard_admin.html" class="btn">Accept & Continue</a>
                <p><small>Invitation token: {token}</small></p>
            </div>
        </body>
        </html>
        """
        return html_content
        
    except Exception as e:
        print(f"Accept invitation page error: {e}")
        return "Error loading invitation page", 500

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify API is working"""
    return jsonify({
        'status': 'success',
        'message': 'OBJX Intelligence Platform API is running',
        'timestamp': datetime.now().isoformat(),
        'systems': {
            'chat': 'operational',
            'memory': 'operational',
            'notifications': 'operational',
            'user_management': 'operational',
            'google_oauth': 'operational'
        }
    })

# ============================================================================
# GOOGLE OAUTH ENDPOINTS
# ============================================================================

@app.route('/api/oauth/initiate', methods=['POST'])
def oauth_initiate():
    """Initiate Google OAuth flow for user"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'demo_admin')
        account_type = data.get('account_type', 'workspace')
        
        # Initiate OAuth flow
        result = oauth_manager.initiate_oauth_flow(user_id, account_type)
        
        if result['success']:
            return jsonify({
                'success': True,
                'authorization_url': result['authorization_url'],
                'message': 'OAuth flow initiated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        print(f"OAuth initiation error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to initiate OAuth flow'
        }), 500

@app.route('/oauth/callback')
def oauth_callback():
    """Handle Google OAuth callback"""
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if error:
            return redirect('/dashboard_admin.html?oauth_error=' + error)
        
        if not code or not state:
            return redirect('/dashboard_admin.html?oauth_error=missing_parameters')
        
        # Handle OAuth callback
        result = oauth_manager.handle_oauth_callback(code, state)
        
        if result['success']:
            return redirect(f'/dashboard_admin.html?oauth_success=true&account={result["account_email"]}')
        else:
            return redirect('/dashboard_admin.html?oauth_error=' + result['error'])
            
    except Exception as e:
        print(f"OAuth callback error: {e}")
        return redirect('/dashboard_admin.html?oauth_error=callback_failed')

@app.route('/api/oauth/accounts/<user_id>')
def oauth_get_accounts(user_id):
    """Get all Google accounts for user"""
    try:
        accounts = oauth_manager.get_user_accounts(user_id)
        return jsonify({
            'success': True,
            'accounts': accounts
        })
        
    except Exception as e:
        print(f"Get accounts error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve accounts'
        }), 500

@app.route('/api/oauth/disconnect', methods=['POST'])
def oauth_disconnect():
    """Disconnect Google account"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        account_email = data.get('account_email')
        
        if not user_id or not account_email:
            return jsonify({
                'success': False,
                'error': 'Missing user_id or account_email'
            }), 400
        
        oauth_manager.disconnect_account(user_id, account_email)
        
        return jsonify({
            'success': True,
            'message': 'Account disconnected successfully'
        })
        
    except Exception as e:
        print(f"Disconnect account error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to disconnect account'
        }), 500

@app.route('/api/oauth/test/<user_id>')
def oauth_test_connection(user_id):
    """Test Google API connection for user"""
    try:
        accounts = oauth_manager.get_user_accounts(user_id)
        
        if not accounts:
            return jsonify({
                'success': False,
                'error': 'No Google accounts connected'
            })
        
        # Test with primary account
        primary_account = next((acc for acc in accounts if acc['is_primary']), accounts[0])
        
        # Build Gmail service to test connection
        gmail_service = service_builder.build_service('gmail', 'v1', user_id, primary_account['email'])
        
        if gmail_service:
            # Test API call
            profile = gmail_service.users().getProfile(userId='me').execute()
            
            return jsonify({
                'success': True,
                'account': primary_account['email'],
                'gmail_address': profile.get('emailAddress'),
                'total_messages': profile.get('messagesTotal', 0),
                'total_threads': profile.get('threadsTotal', 0)
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to build Gmail service'
            })
            
    except Exception as e:
        print(f"OAuth test error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# MEMORY COMMAND CENTER ENDPOINTS
# ============================================================================

@app.route('/api/memory/analytics')
def memory_analytics():
    """Get memory analytics and statistics with role-based permissions"""
    try:
        # Get user info (in production, this would come from session/auth)
        user_id = "demo_admin"
        user_tier = MemoryUserTier.ADMIN  # This would be determined from user session
        
        # Get analytics based on user permissions
        analytics = role_based_memory.get_memory_analytics(user_id, user_tier)
        return jsonify(analytics)
        
    except PermissionError as e:
        return jsonify({
            'error': 'Permission denied',
            'message': str(e)
        }), 403
    except Exception as e:
        print(f"Memory analytics error: {e}")
        return jsonify({
            'total_memories': 0,
            'client_memories': 0,
            'project_memories': 0,
            'health_score': 'N/A'
        })

@app.route('/api/memory/recent')
def memory_recent():
    """Get recent memories"""
    try:
        memories = memory_center.get_all_memories()
        # Sort by created_at and take last 10
        recent_memories = sorted(memories, key=lambda x: x.created_at, reverse=True)[:10]
        
        return jsonify({
            'memories': [
                {
                    'id': mem.id,
                    'content': mem.content,
                    'type': mem.memory_type.value,
                    'priority': mem.priority.value,
                    'created_at': mem.created_at.isoformat(),
                    'relevance_score': mem.relevance_score
                }
                for mem in recent_memories
            ]
        })
    except Exception as e:
        print(f"Recent memories error: {e}")
        return jsonify({'memories': []})

@app.route('/api/memory/search', methods=['POST'])
def memory_command_search():
    """Search memories by query with role-based permissions"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'memories': []})
        
        # Get user info (in production, this would come from session/auth)
        user_id = "demo_admin"
        user_tier = MemoryUserTier.ADMIN  # This would be determined from user session
        
        # Search memories with role-based filtering
        memories = role_based_memory.search_memories(
            user_id=user_id,
            user_tier=user_tier,
            query=query,
            scope=MemoryScope.PERSONAL  # Could be dynamic based on request
        )
        
        return jsonify({'memories': memories})
        
    except PermissionError as e:
        return jsonify({
            'error': 'Permission denied',
            'message': str(e)
        }), 403
    except Exception as e:
        print(f"Memory search error: {e}")
        return jsonify({'memories': []})

@app.route('/api/memory/create', methods=['POST'])
def memory_command_create():
    """Create a new memory with role-based permissions"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        memory_type = data.get('type', 'factual')
        priority = data.get('priority', 'medium')
        
        if not content:
            return jsonify({
                'success': False,
                'error': 'Content is required'
            }), 400
        
        # Get user info (in production, this would come from session/auth)
        user_id = "demo_admin"
        user_tier = MemoryUserTier.ADMIN  # This would be determined from user session
        
        # Map frontend types to role-based memory types
        type_mapping = {
            'client': RoleMemoryType.FACTUAL,
            'project': RoleMemoryType.FACTUAL,
            'system': RoleMemoryType.SEMANTIC,
            'pattern': RoleMemoryType.SEMANTIC,
            'insight': RoleMemoryType.EPISODIC,
            'factual': RoleMemoryType.FACTUAL
        }
        
        role_memory_type = type_mapping.get(memory_type, RoleMemoryType.FACTUAL)
        
        # Create memory with role-based permissions
        memory_id = role_based_memory.create_memory(
            user_id=user_id,
            user_tier=user_tier,
            content=content,
            memory_type=role_memory_type,
            scope=MemoryScope.PERSONAL,
            metadata={
                'priority': priority,
                'original_type': memory_type
            }
        )
        
        if memory_id:
            return jsonify({
                'success': True,
                'memory_id': memory_id
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create memory'
            }), 500
            
    except PermissionError as e:
        return jsonify({
            'success': False,
            'error': f'Permission denied: {str(e)}'
        }), 403
    except Exception as e:
        print(f"Memory creation error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to create memory'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested API endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    print("🚀 Starting OBJX Intelligence Platform...")
    print("✅ Universal Chat System loaded")
    print("✅ Memory Command Center loaded")
    print("✅ Notification System loaded")
    print("🌐 Server starting on http://localhost:5000")
    
    # Create some demo notifications for testing
    try:
        notification_system.create_notification(
            title="Welcome to OBJX Intelligence",
            message="Your platform is ready for systematic thinking and compound intelligence.",
            notification_type=NotificationType.SYSTEM_EVENT,
            priority=NotificationPriority.MEDIUM,
            user_id='demo_user_tier3',
            user_role=UserRole.CLIENT
        )
        
        notification_system.create_notification(
            title="Memory System Active",
            message="Your personal memory system is learning and ready to compound your intelligence.",
            notification_type=NotificationType.MEMORY_ALERT,
            priority=NotificationPriority.LOW,
            user_id='demo_user_tier3',
            user_role=UserRole.CLIENT
        )
        
        print("✅ Demo notifications created")
    except Exception as e:
        print(f"⚠️ Demo notification creation failed: {e}")

# Import real project data integration
from real_project_data_integration import get_project_intelligence

# Real Project Management API Endpoints
@app.route('/api/projects/overview')
def get_projects_overview():
    """Get project portfolio overview with real data"""
    try:
        from real_project_data_integration import get_project_intelligence
        
        user_tier = request.args.get('tier', 'admin')
        project_system = get_project_intelligence()
        overview = project_system.get_portfolio_overview(user_tier)
        
        return jsonify({
            "success": True,
            "data": overview
        })
    except Exception as e:
        print(f"Error in projects overview: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/projects/<project_id>')
def get_project_detail(project_id):
    """Get detailed project information"""
    try:
        from real_project_data_integration import get_project_intelligence
        
        user_tier = request.args.get('tier', 'admin')
        project_system = get_project_intelligence()
        project_detail = project_system.get_project_detail(project_id, user_tier)
        
        if not project_detail:
            return jsonify({
                "success": False,
                "error": "Project not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": project_detail
        })
    except Exception as e:
        print(f"Error in project detail: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/projects/<project_id>/gantt')
def get_project_gantt(project_id):
    """Get Gantt chart data for project"""
    try:
        from real_project_data_integration import get_project_intelligence
        
        user_tier = request.args.get('tier', 'admin')
        project_system = get_project_intelligence()
        project_detail = project_system.get_project_detail(project_id, user_tier)
        
        if not project_detail:
            return jsonify({
                "success": False,
                "error": "Project not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": project_detail.get("gantt_chart", {})
        })
    except Exception as e:
        print(f"Error in project Gantt: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/projects/<project_id>/schedule')
def get_project_schedule(project_id):
    """Get smart schedule for project"""
    try:
        from real_project_data_integration import get_project_intelligence
        
        user_tier = request.args.get('tier', 'admin')
        project_system = get_project_intelligence()
        project_detail = project_system.get_project_detail(project_id, user_tier)
        
        if not project_detail:
            return jsonify({
                "success": False,
                "error": "Project not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": project_detail.get("smart_schedule", {})
        })
    except Exception as e:
        print(f"Error in project schedule: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/projects/<project_id>/gantt', methods=['GET'])
def get_project_gantt_chart(project_id):
    """Get Gantt chart data for specific project"""
    try:
        project_system = get_project_intelligence()
        project_data = project_system.get_project_detail(project_id)
        
        if not project_data:
            return jsonify({
                "success": False,
                "error": "Project not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": project_data["gantt_chart"],
            "message": "Gantt chart data retrieved successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve Gantt chart data"
        }), 500

@app.route('/api/projects/<project_id>/schedule', methods=['GET'])
def get_smart_schedule(project_id):
    """Get AI-optimized smart schedule for project"""
    try:
        project_system = get_project_intelligence()
        project_data = project_system.get_project_detail(project_id)
        
        if not project_data:
            return jsonify({
                "success": False,
                "error": "Project not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": project_data["smart_schedule"],
            "message": "Smart schedule retrieved successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve smart schedule"
        }), 500

@app.route('/api/projects/<project_id>/agents', methods=['GET'])
def get_project_agent_recommendations(project_id):
    """Get AI agent recommendations for specific project"""
    try:
        project_system = get_project_intelligence()
        project_data = project_system.get_project_detail(project_id)
        
        if not project_data:
            return jsonify({
                "success": False,
                "error": "Project not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": project_data["agent_recommendations"],
            "message": "Agent recommendations retrieved successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve agent recommendations"
        }), 500

# Dynamic Project Fields API Endpoints
@app.route('/api/projects/<project_id>/fields', methods=['POST'])
def create_dynamic_field(project_id):
    """Create a new dynamic field for a project"""
    try:
        from backend.dynamic_project_fields import dynamic_field_manager
        
        field_data = request.json
        agent_context = field_data.get('agent_context', {})
        
        result = dynamic_field_manager.create_dynamic_field(project_id, field_data, agent_context)
        
        if result['success']:
            return jsonify({
                'success': True,
                'field': result['field'],
                'organization_suggestions': result['organization_suggestions'],
                'integration_opportunities': result['integration_opportunities']
            })
        else:
            return jsonify({'success': False, 'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<project_id>/fields/organize', methods=['POST'])
def organize_project_fields(project_id):
    """Organize all project fields using Trinity Foundation methodology"""
    try:
        from backend.dynamic_project_fields import dynamic_field_manager
        
        fields_data = request.json.get('fields', [])
        
        result = dynamic_field_manager.organize_project_fields(project_id, fields_data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'organized_fields': result['organized_fields'],
                'insights': result['insights'],
                'recommendations': result['recommendations']
            })
        else:
            return jsonify({'success': False, 'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Email Integration API Endpoints
@app.route('/api/projects/<project_id>/email/analyze', methods=['POST'])
def analyze_email_for_project(project_id):
    """Analyze email content for project-relevant information"""
    try:
        from backend.email_drive_integration import email_drive_manager
        
        email_data = request.json
        
        result = email_drive_manager.analyze_email_for_project_data(email_data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'project_relevance': result['data']['project_relevance'],
                'extracted_fields': result['data']['extracted_fields'],
                'suggested_connections': result['data']['suggested_connections'],
                'automation_opportunities': result['data']['automation_opportunities'],
                'email_metadata': result['email_metadata']
            })
        else:
            return jsonify({'success': False, 'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Google Drive Integration API Endpoints
@app.route('/api/projects/<project_id>/drive/analyze', methods=['POST'])
def analyze_drive_file_for_project(project_id):
    """Analyze Google Drive file for project-relevant information"""
    try:
        from backend.email_drive_integration import email_drive_manager
        
        file_data = request.json
        
        result = email_drive_manager.analyze_drive_file_for_project_data(file_data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'project_relevance': result['data']['project_relevance'],
                'file_category': result['data']['file_category'],
                'extracted_fields': result['data']['extracted_fields'],
                'automation_opportunities': result['data']['automation_opportunities'],
                'file_metadata': result['file_metadata']
            })
        else:
            return jsonify({'success': False, 'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# QuickBooks Integration API Endpoints
@app.route('/api/projects/<project_id>/expenses/analyze', methods=['POST'])
def analyze_project_expenses(project_id):
    """Analyze project expenses for QuickBooks integration"""
    try:
        from backend.quickbooks_billing_integration import quickbooks_manager
        
        data = request.json
        project_data = data.get('project', {})
        expense_data = data.get('expenses', [])
        
        result = quickbooks_manager.analyze_project_expenses(project_data, expense_data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'analysis': result['analysis']
            })
        else:
            return jsonify({'success': False, 'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<project_id>/invoice/generate', methods=['POST'])
def generate_project_invoice(project_id):
    """Generate invoice for project services"""
    try:
        from backend.quickbooks_billing_integration import quickbooks_manager
        
        data = request.json
        project_data = data.get('project', {})
        billing_data = data.get('billing', {})
        
        result = quickbooks_manager.generate_project_invoice(project_data, billing_data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'invoice': result['invoice'],
                'qb_sync_instructions': result['qb_sync_instructions']
            })
        else:
            return jsonify({'success': False, 'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Agent-Driven Field Creation API
@app.route('/api/chat/create-field', methods=['POST'])
def agent_create_field():
    """Allow agents to create fields through chat interface"""
    try:
        from backend.dynamic_project_fields import dynamic_field_manager
        
        data = request.json
        project_id = data.get('project_id')
        field_data = data.get('field_data')
        agent_context = data.get('agent_context', {
            'agent_name': 'chat_agent',
            'agent_type': 'universal_chat',
            'conversation_context': data.get('conversation_context', '')
        })
        
        result = dynamic_field_manager.create_dynamic_field(project_id, field_data, agent_context)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f"Created field '{field_data.get('name')}' and organized it under {result['field']['trinity_category']} category",
                'field': result['field'],
                'organization_suggestions': result['organization_suggestions'],
                'integration_opportunities': result['integration_opportunities']
            })
        else:
            return jsonify({'success': False, 'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Integration Status and Health API
@app.route('/api/integrations/status', methods=['GET'])
def get_integration_status():
    """Get status of all integrations"""
    try:
        integration_status = {
            'gmail': {
                'connected': True,  # This would check actual Gmail API connection
                'last_sync': '2025-01-26T10:30:00Z',
                'emails_processed': 45,
                'status': 'active'
            },
            'google_drive': {
                'connected': True,  # This would check actual Drive API connection
                'last_sync': '2025-01-26T10:25:00Z',
                'files_processed': 23,
                'status': 'active'
            },
            'quickbooks': {
                'connected': True,  # This would check actual QB API connection
                'last_sync': '2025-01-26T09:45:00Z',
                'transactions_synced': 12,
                'status': 'active'
            },
            'overall_health': 'excellent',
            'automation_score': 92,
            'time_saved_this_week': 180  # minutes
        }
        
        return jsonify({
            'success': True,
            'integrations': integration_status
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

# ===== PAYMENT INTEGRATION API ENDPOINTS =====

@app.route('/api/payment/pricing', methods=['GET'])
def get_pricing_plans():
    """Get all pricing plans"""
    try:
        payment_system = get_payment_integration()
        plans = payment_system.get_pricing_plans()
        return jsonify({'success': True, 'plans': plans})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/payment/checkout', methods=['POST'])
def create_checkout_session():
    """Create Stripe checkout session"""
    try:
        data = request.get_json()
        payment_system = get_payment_integration()
        
        result = payment_system.create_checkout_session(
            user_id=data['user_id'],
            tier=data['tier'],
            billing_period=data.get('billing_period', 'monthly')
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/payment/webhook', methods=['POST'])
def handle_payment_webhook():
    """Handle Stripe webhook events"""
    try:
        payment_system = get_payment_integration()
        event_data = request.get_json()
        
        result = payment_system.handle_webhook(event_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/payment/subscription/<user_id>', methods=['GET'])
def get_user_subscription(user_id):
    """Get user's current subscription"""
    try:
        payment_system = get_payment_integration()
        subscription = payment_system.get_user_subscription(user_id)
        return jsonify({'success': True, 'subscription': subscription})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/payment/history/<user_id>', methods=['GET'])
def get_payment_history(user_id):
    """Get user's payment history"""
    try:
        payment_system = get_payment_integration()
        history = payment_system.get_payment_history(user_id)
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== AGENT MANAGEMENT API ENDPOINTS =====

@app.route('/api/agents', methods=['GET'])
def get_all_agents():
    """Get all configured agents"""
    try:
        agent_system = get_agent_management()
        agents = agent_system.get_all_agents()
        return jsonify({'success': True, 'agents': agents})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/agents/<agent_id>', methods=['GET'])
def get_agent_detail(agent_id):
    """Get specific agent configuration"""
    try:
        agent_system = get_agent_management()
        agent = agent_system.get_agent(agent_id)
        
        if agent is None:
            return jsonify({'success': False, 'error': 'Agent not found'}), 404
        
        return jsonify({'success': True, 'agent': agent})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/agents', methods=['POST'])
def create_agent():
    """Create a new agent"""
    try:
        data = request.get_json()
        agent_system = get_agent_management()
        
        result = agent_system.create_agent(data, created_by='admin')
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/agents/<agent_id>', methods=['PUT'])
def update_agent(agent_id):
    """Update agent configuration"""
    try:
        data = request.get_json()
        agent_system = get_agent_management()
        
        result = agent_system.update_agent(agent_id, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/agents/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    """Delete an agent"""
    try:
        agent_system = get_agent_management()
        result = agent_system.delete_agent(agent_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/agents/templates', methods=['GET'])
def get_agent_templates():
    """Get available agent templates"""
    try:
        agent_system = get_agent_management()
        templates = agent_system.get_agent_templates()
        return jsonify({'success': True, 'templates': templates})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/agents/<agent_id>/tasks', methods=['POST'])
def assign_task_to_agent(agent_id):
    """Assign a task to an agent"""
    try:
        data = request.get_json()
        agent_system = get_agent_management()
        
        result = agent_system.assign_task_to_agent(agent_id, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/agents/performance', methods=['GET'])
def get_agent_performance_summary():
    """Get overall agent performance summary"""
    try:
        agent_system = get_agent_management()
        summary = agent_system.get_agent_performance_summary()
        return jsonify({'success': True, 'performance': summary})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== PROJECT INTELLIGENCE API ENDPOINTS =====

@app.route('/api/projects', methods=['GET'])
def get_all_projects():
    """Get all projects with tier-based filtering"""
    try:
        user_tier = request.args.get('tier', 'admin')
        project_system = get_project_intelligence()
        projects = project_system.get_all_projects(user_tier)
        return jsonify({'success': True, 'projects': projects})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/templates', methods=['GET'])
def get_project_templates():
    """Get all available project templates"""
    try:
        project_system = get_project_intelligence()
        templates = project_system.get_project_templates()
        return jsonify({'success': True, 'templates': templates})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/create', methods=['POST'])
def create_project_from_template():
    """Create a new project from a template"""
    try:
        data = request.get_json()
        project_system = get_project_intelligence()
        
        result = project_system.create_project_from_template(
            template_id=data['template_id'],
            project_data=data['project_data'],
            created_by=data.get('created_by', 'admin')
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/intelligence', methods=['GET'])
def get_project_intelligence_summary():
    """Get overall project intelligence summary"""
    try:
        project_system = get_project_intelligence()
        summary = project_system.get_project_intelligence_summary()
        return jsonify({'success': True, 'intelligence': summary})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== SUB-PAGE ROUTING =====

@app.route('/project-overview.html')
def project_overview():
    """Serve project overview page"""
    try:
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'project-overview.html')
        with open(frontend_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Project overview page not found", 404

@app.route('/project-detail.html')
def project_detail():
    """Serve project detail page"""
    try:
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'project-detail.html')
        with open(frontend_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Project detail page not found", 404

@app.route('/task-management.html')
def task_management():
    """Serve task management page"""
    try:
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'task-management.html')
        with open(frontend_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Task management page not found", 404

@app.route('/billing-overview.html')
def billing_overview():
    """Serve billing overview page"""
    try:
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'billing-overview.html')
        with open(frontend_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Billing overview page not found", 404

@app.route('/google-workspace.html')
def google_workspace():
    """Serve Google Workspace integration page"""
    try:
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'google-workspace.html')
        with open(frontend_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Google Workspace page not found", 404

@app.route('/memory-center.html')
def memory_center_page():
    """Serve memory center page"""
    try:
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'memory-center.html')
        with open(frontend_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Memory center page not found", 404


# QuickBooks Billing Integration API Endpoints
@app.route('/api/billing/quickbooks/connect', methods=['POST'])
def connect_quickbooks():
    """Connect to QuickBooks Online API"""
    try:
        from quickbooks_billing_integration import quickbooks_manager
        
        # Get connection parameters from request
        data = request.get_json()
        company_id = data.get('company_id')
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        
        # Establish QuickBooks connection
        result = quickbooks_manager.connect_quickbooks(
            company_id=company_id,
            access_token=access_token,
            refresh_token=refresh_token
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Failed to connect to QuickBooks: {str(e)}"
        }), 400

@app.route('/api/billing/expenses/categorize', methods=['POST'])
def categorize_project_expense():
    """Automatically categorize and sync project expense with QuickBooks"""
    try:
        from quickbooks_billing_integration import quickbooks_manager
        
        data = request.get_json()
        project_id = data.get('project_id')
        expense_data = data.get('expense_data')
        
        # Categorize expense using Trinity Foundation methodology
        result = quickbooks_manager.categorize_project_expense(
            project_id=project_id,
            expense_data=expense_data
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Failed to categorize expense: {str(e)}"
        }), 400

@app.route('/api/billing/invoices/generate', methods=['POST'])
def generate_project_invoice_billing():
    """Generate invoice for project services using QuickBooks integration"""
    try:
        from quickbooks_billing_integration import quickbooks_manager
        
        data = request.get_json()
        project_id = data.get('project_id')
        invoice_data = data.get('invoice_data')
        
        # Generate invoice with Trinity Foundation service categorization
        result = quickbooks_manager.generate_project_invoice(
            project_id=project_id,
            invoice_data=invoice_data
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Failed to generate invoice: {str(e)}"
        }), 400

@app.route('/api/billing/financial-intelligence/<project_id>', methods=['GET'])
def get_project_financial_intelligence(project_id):
    """Get comprehensive financial intelligence for a project"""
    try:
        from quickbooks_billing_integration import quickbooks_manager
        
        # Generate financial intelligence using Trinity Foundation analysis
        result = quickbooks_manager.get_project_financial_intelligence(project_id)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Failed to get financial intelligence: {str(e)}"
        }), 400

@app.route('/api/billing/automation/setup', methods=['POST'])
def setup_billing_automation():
    """Setup automated billing rules and workflows"""
    try:
        from quickbooks_billing_integration import quickbooks_manager
        
        data = request.get_json()
        automation_config = data.get('automation_config')
        
        # Setup automation with agent intelligence
        result = quickbooks_manager.setup_billing_automation(automation_config)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Failed to setup billing automation: {str(e)}"
        }), 400

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)


# Unified Integration Management API Endpoints
@app.route('/api/integrations/initiate', methods=['POST'])
def initiate_integration():
    """Initiate connection to an external service through OBJX platform"""
    try:
        from unified_integration_manager import integration_manager
        
        data = request.get_json()
        user_id = data.get('user_id')
        integration_type = data.get('integration_type')
        connection_config = data.get('config', {})
        
        result = integration_manager.initiate_integration_connection(
            user_id=user_id,
            integration_type=integration_type,
            connection_config=connection_config
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Failed to initiate integration: {str(e)}"
        }), 400

@app.route('/api/integrations/complete', methods=['POST'])
def complete_integration():
    """Complete integration connection with authentication data"""
    try:
        from unified_integration_manager import integration_manager
        
        data = request.get_json()
        connection_id = data.get('connection_id')
        auth_data = data.get('auth_data', {})
        
        result = integration_manager.complete_integration_connection(
            connection_id=connection_id,
            auth_data=auth_data
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Failed to complete integration: {str(e)}"
        }), 400

@app.route('/api/integrations/user/<user_id>', methods=['GET'])
def get_user_integrations(user_id):
    """Get all integrations for a user"""
    try:
        from unified_integration_manager import integration_manager
        
        result = integration_manager.get_user_integrations(user_id)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Failed to get user integrations: {str(e)}"
        }), 400

@app.route('/api/integrations/sync/<connection_id>', methods=['POST'])
def sync_integration_data(connection_id):
    """Synchronize data from an integrated service"""
    try:
        from unified_integration_manager import integration_manager
        
        data = request.get_json() or {}
        sync_config = data.get('sync_config', {})
        
        result = integration_manager.sync_integration_data(
            connection_id=connection_id,
            sync_config=sync_config
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Failed to sync integration data: {str(e)}"
        }), 400

@app.route('/api/integrations/disconnect/<connection_id>', methods=['DELETE'])
def disconnect_integration(connection_id):
    """Disconnect an integration and clean up data"""
    try:
        from unified_integration_manager import integration_manager
        
        data = request.get_json() or {}
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'User ID is required'
            }), 400
        
        result = integration_manager.disconnect_integration(
            connection_id=connection_id,
            user_id=user_id
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Failed to disconnect integration: {str(e)}"
        }), 400

@app.route('/api/integrations/available', methods=['GET'])
def get_available_integrations():
    """Get list of all available integrations"""
    try:
        from unified_integration_manager import integration_manager
        
        available_integrations = []
        for integration_type, info in integration_manager.supported_integrations.items():
            available_integrations.append({
                'type': integration_type,
                'name': info['name'],
                'services': info['services'],
                'auth_type': info['auth_type'],
                'trinity_alignment': info['trinity_alignment']
            })
        
        return jsonify({
            'success': True,
            'available_integrations': available_integrations,
            'total_available': len(available_integrations)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Failed to get available integrations: {str(e)}"
        }), 400

# Agent Intelligence Orchestrator endpoints
@app.route('/api/intelligence/analyze-project', methods=['POST'])
def analyze_project_intelligence():
    """Analyze project for strategic intelligence insights"""
    try:
        from backend.agent_intelligence_orchestrator import AgentIntelligenceOrchestrator
        
        data = request.get_json()
        project_data = data.get('project_data', {})
        
        orchestrator = AgentIntelligenceOrchestrator()
        result = orchestrator.analyze_project_intelligence(project_data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/intelligence/auto-organize', methods=['POST'])
def apply_auto_organization():
    """Apply automatic organization rules to data"""
    try:
        from backend.agent_intelligence_orchestrator import AgentIntelligenceOrchestrator
        
        data = request.get_json()
        input_data = data.get('data', {})
        
        orchestrator = AgentIntelligenceOrchestrator()
        result = orchestrator.apply_auto_organization(input_data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/intelligence/create-rule', methods=['POST'])
def create_auto_organization_rule():
    """Create a new auto-organization rule"""
    try:
        from backend.agent_intelligence_orchestrator import AgentIntelligenceOrchestrator
        
        data = request.get_json()
        rule_data = data.get('rule_data', {})
        
        orchestrator = AgentIntelligenceOrchestrator()
        result = orchestrator.create_auto_organization_rule(rule_data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/intelligence/strategic-report', methods=['POST'])
def generate_strategic_intelligence_report():
    """Generate strategic intelligence report across projects"""
    try:
        from backend.agent_intelligence_orchestrator import AgentIntelligenceOrchestrator
        
        data = request.get_json()
        project_ids = data.get('project_ids', [])
        
        orchestrator = AgentIntelligenceOrchestrator()
        result = orchestrator.generate_strategic_intelligence_report(project_ids)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/intelligence/compound-insights', methods=['GET'])
def get_compound_intelligence_insights():
    """Get compound intelligence insights across the platform"""
    try:
        # Sample compound intelligence data
        insights = {
            'success': True,
            'compound_intelligence_score': 92.5,
            'strategic_patterns': [
                {
                    'pattern': 'Resource Optimization Opportunity',
                    'confidence': 0.89,
                    'trinity_phase': 'compound',
                    'description': 'Cross-project resource sharing could improve efficiency by 23%',
                    'affected_projects': 3,
                    'potential_savings': '$45,000'
                },
                {
                    'pattern': 'Timeline Acceleration Pattern',
                    'confidence': 0.94,
                    'trinity_phase': 'create',
                    'description': 'Parallel task execution could reduce project timelines by 15%',
                    'affected_projects': 2,
                    'time_savings': '18 days'
                }
            ],
            'auto_organization_stats': {
                'active_rules': 12,
                'success_rate': 94.2,
                'data_organized': 1847,
                'time_saved': '23.5 hours'
            },
            'intelligence_evolution': {
                'pattern_recognition_growth': 18.5,
                'automation_adoption': 76.3,
                'strategic_value_increase': 31.2
            }
        }
        
        return jsonify(insights)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

