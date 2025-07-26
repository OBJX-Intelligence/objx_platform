"""
OBJX Intelligence Platform - Notification System
Enterprise-grade notification management for Staff and Admin levels
"""

import os
import json
import smtplib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import threading
import time

class NotificationType(Enum):
    PROJECT_UPDATE = "project_update"
    MEMORY_ALERT = "memory_alert"
    CLIENT_COMMUNICATION = "client_communication"
    SYSTEM_EVENT = "system_event"
    TEAM_NOTIFICATION = "team_notification"
    DEADLINE_REMINDER = "deadline_reminder"
    BUSINESS_INTELLIGENCE = "business_intelligence"
    SECURITY_ALERT = "security_alert"

class NotificationPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class NotificationChannel(Enum):
    IN_APP = "in_app"
    EMAIL = "email"
    SMS = "sms"
    SLACK = "slack"
    PUSH = "push"

class UserRole(Enum):
    ADMIN = "admin"
    STAFF = "staff"
    CLIENT = "client"

@dataclass
class Notification:
    id: str
    title: str
    message: str
    notification_type: NotificationType
    priority: NotificationPriority
    user_id: str
    user_role: UserRole
    channels: List[NotificationChannel]
    created_at: datetime
    read_at: Optional[datetime]
    action_url: Optional[str]
    action_buttons: List[Dict[str, str]]
    metadata: Dict[str, Any]
    expires_at: Optional[datetime]

@dataclass
class NotificationPreferences:
    user_id: str
    user_role: UserRole
    email_enabled: bool
    sms_enabled: bool
    slack_enabled: bool
    push_enabled: bool
    quiet_hours_start: Optional[str]  # "22:00"
    quiet_hours_end: Optional[str]    # "08:00"
    frequency: str  # "immediate", "hourly", "daily"
    type_preferences: Dict[str, bool]  # notification_type -> enabled

class NotificationSystem:
    """
    Enterprise-grade notification system with multi-channel delivery
    """
    
    def __init__(self, db_path: str = "notifications.db"):
        self.db_path = db_path
        self.init_database()
        self.notification_handlers: Dict[NotificationChannel, Callable] = {
            NotificationChannel.IN_APP: self._handle_in_app,
            NotificationChannel.EMAIL: self._handle_email,
            NotificationChannel.SMS: self._handle_sms,
            NotificationChannel.SLACK: self._handle_slack,
            NotificationChannel.PUSH: self._handle_push
        }
        
        # Start background processor
        self.processor_thread = threading.Thread(target=self._process_notifications, daemon=True)
        self.processor_thread.start()
    
    def init_database(self):
        """Initialize SQLite database for notifications"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Notifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                notification_type TEXT NOT NULL,
                priority TEXT NOT NULL,
                user_id TEXT NOT NULL,
                user_role TEXT NOT NULL,
                channels TEXT NOT NULL,
                created_at TEXT NOT NULL,
                read_at TEXT,
                action_url TEXT,
                action_buttons TEXT,
                metadata TEXT,
                expires_at TEXT
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notification_preferences (
                user_id TEXT PRIMARY KEY,
                user_role TEXT NOT NULL,
                email_enabled BOOLEAN DEFAULT 1,
                sms_enabled BOOLEAN DEFAULT 0,
                slack_enabled BOOLEAN DEFAULT 1,
                push_enabled BOOLEAN DEFAULT 1,
                quiet_hours_start TEXT,
                quiet_hours_end TEXT,
                frequency TEXT DEFAULT 'immediate',
                type_preferences TEXT
            )
        ''')
        
        # Notification queue table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notification_queue (
                id TEXT PRIMARY KEY,
                notification_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                scheduled_at TEXT NOT NULL,
                processed_at TEXT,
                status TEXT DEFAULT 'pending',
                error_message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_notification(self, title: str, message: str, notification_type: NotificationType,
                          priority: NotificationPriority, user_id: str, user_role: UserRole,
                          channels: List[NotificationChannel] = None,
                          action_url: str = None, action_buttons: List[Dict[str, str]] = None,
                          metadata: Dict[str, Any] = None, expires_hours: int = 24) -> str:
        """Create a new notification"""
        
        notification_id = f"notif_{int(datetime.now().timestamp() * 1000)}"
        
        if channels is None:
            channels = self._get_default_channels(user_role, priority)
        
        expires_at = datetime.now() + timedelta(hours=expires_hours)
        
        notification = Notification(
            id=notification_id,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            user_id=user_id,
            user_role=user_role,
            channels=channels,
            created_at=datetime.now(),
            read_at=None,
            action_url=action_url,
            action_buttons=action_buttons or [],
            metadata=metadata or {},
            expires_at=expires_at
        )
        
        # Store notification
        self._store_notification(notification)
        
        # Queue for delivery
        self._queue_notification(notification)
        
        return notification_id
    
    def _get_default_channels(self, user_role: UserRole, priority: NotificationPriority) -> List[NotificationChannel]:
        """Get default notification channels based on role and priority"""
        channels = [NotificationChannel.IN_APP]
        
        if priority in [NotificationPriority.CRITICAL, NotificationPriority.HIGH]:
            channels.extend([NotificationChannel.EMAIL, NotificationChannel.SLACK])
            
            if priority == NotificationPriority.CRITICAL:
                channels.append(NotificationChannel.SMS)
        
        if user_role == UserRole.ADMIN:
            channels.append(NotificationChannel.PUSH)
        
        return channels
    
    def _store_notification(self, notification: Notification):
        """Store notification in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO notifications (
                id, title, message, notification_type, priority, user_id, user_role,
                channels, created_at, read_at, action_url, action_buttons, metadata, expires_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            notification.id,
            notification.title,
            notification.message,
            notification.notification_type.value,
            notification.priority.value,
            notification.user_id,
            notification.user_role.value,
            json.dumps([ch.value for ch in notification.channels]),
            notification.created_at.isoformat(),
            notification.read_at.isoformat() if notification.read_at else None,
            notification.action_url,
            json.dumps(notification.action_buttons),
            json.dumps(notification.metadata),
            notification.expires_at.isoformat() if notification.expires_at else None
        ))
        
        conn.commit()
        conn.close()
    
    def _queue_notification(self, notification: Notification):
        """Queue notification for delivery across channels"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for channel in notification.channels:
            queue_id = f"queue_{notification.id}_{channel.value}_{int(datetime.now().timestamp() * 1000)}"
            
            cursor.execute('''
                INSERT INTO notification_queue (
                    id, notification_id, channel, scheduled_at, status
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                queue_id,
                notification.id,
                channel.value,
                datetime.now().isoformat(),
                'pending'
            ))
        
        conn.commit()
        conn.close()
    
    def _process_notifications(self):
        """Background processor for notification delivery"""
        while True:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Get pending notifications
                cursor.execute('''
                    SELECT id, notification_id, channel, scheduled_at
                    FROM notification_queue
                    WHERE status = 'pending' AND scheduled_at <= ?
                    ORDER BY scheduled_at ASC
                    LIMIT 10
                ''', (datetime.now().isoformat(),))
                
                pending = cursor.fetchall()
                conn.close()
                
                for queue_id, notification_id, channel, scheduled_at in pending:
                    self._deliver_notification(queue_id, notification_id, NotificationChannel(channel))
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                print(f"Error in notification processor: {e}")
                time.sleep(10)
    
    def _deliver_notification(self, queue_id: str, notification_id: str, channel: NotificationChannel):
        """Deliver a single notification through specified channel"""
        try:
            # Get notification details
            notification = self._get_notification(notification_id)
            if not notification:
                return
            
            # Check user preferences
            if not self._should_deliver(notification, channel):
                self._update_queue_status(queue_id, 'skipped', 'User preferences')
                return
            
            # Deliver through channel
            handler = self.notification_handlers.get(channel)
            if handler:
                success = handler(notification)
                status = 'delivered' if success else 'failed'
                self._update_queue_status(queue_id, status)
            else:
                self._update_queue_status(queue_id, 'failed', f'No handler for {channel.value}')
                
        except Exception as e:
            self._update_queue_status(queue_id, 'failed', str(e))
    
    def _get_notification(self, notification_id: str) -> Optional[Notification]:
        """Retrieve notification from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM notifications WHERE id = ?', (notification_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return Notification(
            id=row[0],
            title=row[1],
            message=row[2],
            notification_type=NotificationType(row[3]),
            priority=NotificationPriority(row[4]),
            user_id=row[5],
            user_role=UserRole(row[6]),
            channels=[NotificationChannel(ch) for ch in json.loads(row[7])],
            created_at=datetime.fromisoformat(row[8]),
            read_at=datetime.fromisoformat(row[9]) if row[9] else None,
            action_url=row[10],
            action_buttons=json.loads(row[11]) if row[11] else [],
            metadata=json.loads(row[12]) if row[12] else {},
            expires_at=datetime.fromisoformat(row[13]) if row[13] else None
        )
    
    def _should_deliver(self, notification: Notification, channel: NotificationChannel) -> bool:
        """Check if notification should be delivered based on user preferences"""
        # Get user preferences
        prefs = self._get_user_preferences(notification.user_id)
        if not prefs:
            return True  # Default to deliver if no preferences set
        
        # Check channel preference
        channel_enabled = {
            NotificationChannel.EMAIL: prefs.email_enabled,
            NotificationChannel.SMS: prefs.sms_enabled,
            NotificationChannel.SLACK: prefs.slack_enabled,
            NotificationChannel.PUSH: prefs.push_enabled,
            NotificationChannel.IN_APP: True  # Always enabled
        }.get(channel, True)
        
        if not channel_enabled:
            return False
        
        # Check quiet hours
        if prefs.quiet_hours_start and prefs.quiet_hours_end:
            current_time = datetime.now().strftime("%H:%M")
            if prefs.quiet_hours_start <= current_time <= prefs.quiet_hours_end:
                # Only deliver critical notifications during quiet hours
                return notification.priority == NotificationPriority.CRITICAL
        
        # Check type preferences
        if prefs.type_preferences:
            type_enabled = prefs.type_preferences.get(notification.notification_type.value, True)
            if not type_enabled:
                return False
        
        return True
    
    def _get_user_preferences(self, user_id: str) -> Optional[NotificationPreferences]:
        """Get user notification preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM notification_preferences WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return NotificationPreferences(
            user_id=row[0],
            user_role=UserRole(row[1]),
            email_enabled=bool(row[2]),
            sms_enabled=bool(row[3]),
            slack_enabled=bool(row[4]),
            push_enabled=bool(row[5]),
            quiet_hours_start=row[6],
            quiet_hours_end=row[7],
            frequency=row[8],
            type_preferences=json.loads(row[9]) if row[9] else {}
        )
    
    def _update_queue_status(self, queue_id: str, status: str, error_message: str = None):
        """Update notification queue status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE notification_queue
            SET status = ?, processed_at = ?, error_message = ?
            WHERE id = ?
        ''', (status, datetime.now().isoformat(), error_message, queue_id))
        
        conn.commit()
        conn.close()
    
    # Channel Handlers
    def _handle_in_app(self, notification: Notification) -> bool:
        """Handle in-app notification delivery"""
        # In-app notifications are stored in database and retrieved by frontend
        return True
    
    def _handle_email(self, notification: Notification) -> bool:
        """Handle email notification delivery"""
        try:
            # Email configuration (would be in environment variables)
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            smtp_username = os.getenv('SMTP_USERNAME')
            smtp_password = os.getenv('SMTP_PASSWORD')
            
            if not smtp_username or not smtp_password:
                return False
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = notification.metadata.get('email', f"{notification.user_id}@company.com")
            msg['Subject'] = f"[OBJX] {notification.title}"
            
            # Email body
            body = f"""
            {notification.message}
            
            Priority: {notification.priority.value.upper()}
            Time: {notification.created_at.strftime('%Y-%m-%d %H:%M:%S')}
            
            {f'Action: {notification.action_url}' if notification.action_url else ''}
            
            ---
            OBJX Intelligence Platform
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Email delivery failed: {e}")
            return False
    
    def _handle_sms(self, notification: Notification) -> bool:
        """Handle SMS notification delivery"""
        # SMS implementation would use Twilio or similar service
        print(f"SMS: {notification.title} - {notification.message}")
        return True
    
    def _handle_slack(self, notification: Notification) -> bool:
        """Handle Slack notification delivery"""
        # Slack implementation would use Slack API
        print(f"Slack: {notification.title} - {notification.message}")
        return True
    
    def _handle_push(self, notification: Notification) -> bool:
        """Handle push notification delivery"""
        # Push notification implementation
        print(f"Push: {notification.title} - {notification.message}")
        return True
    
    # Public API Methods
    def get_user_notifications(self, user_id: str, unread_only: bool = False, 
                             limit: int = 50) -> List[Dict[str, Any]]:
        """Get notifications for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT * FROM notifications 
            WHERE user_id = ? AND (expires_at IS NULL OR expires_at > ?)
        '''
        params = [user_id, datetime.now().isoformat()]
        
        if unread_only:
            query += ' AND read_at IS NULL'
        
        query += ' ORDER BY created_at DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        notifications = []
        for row in rows:
            notifications.append({
                'id': row[0],
                'title': row[1],
                'message': row[2],
                'type': row[3],
                'priority': row[4],
                'created_at': row[8],
                'read_at': row[9],
                'action_url': row[10],
                'action_buttons': json.loads(row[11]) if row[11] else [],
                'metadata': json.loads(row[12]) if row[12] else {}
            })
        
        return notifications
    
    def mark_notification_read(self, notification_id: str, user_id: str) -> bool:
        """Mark a notification as read"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE notifications 
            SET read_at = ? 
            WHERE id = ? AND user_id = ?
        ''', (datetime.now().isoformat(), notification_id, user_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def get_notification_stats(self, user_id: str) -> Dict[str, Any]:
        """Get notification statistics for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total notifications
        cursor.execute('SELECT COUNT(*) FROM notifications WHERE user_id = ?', (user_id,))
        total = cursor.fetchone()[0]
        
        # Unread notifications
        cursor.execute('SELECT COUNT(*) FROM notifications WHERE user_id = ? AND read_at IS NULL', (user_id,))
        unread = cursor.fetchone()[0]
        
        # By priority
        cursor.execute('''
            SELECT priority, COUNT(*) 
            FROM notifications 
            WHERE user_id = ? AND read_at IS NULL
            GROUP BY priority
        ''', (user_id,))
        priority_counts = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total': total,
            'unread': unread,
            'priority_counts': priority_counts
        }

# Initialize the notification system
notification_system = NotificationSystem()

# Predefined notification templates for common scenarios
class NotificationTemplates:
    @staticmethod
    def project_deadline_reminder(project_name: str, days_remaining: int, user_id: str, user_role: UserRole):
        priority = NotificationPriority.HIGH if days_remaining <= 2 else NotificationPriority.MEDIUM
        
        return notification_system.create_notification(
            title=f"Project Deadline Approaching: {project_name}",
            message=f"Project '{project_name}' is due in {days_remaining} days. Please review progress and ensure timely completion.",
            notification_type=NotificationType.DEADLINE_REMINDER,
            priority=priority,
            user_id=user_id,
            user_role=user_role,
            action_url=f"/projects/{project_name}",
            action_buttons=[
                {"text": "View Project", "url": f"/projects/{project_name}"},
                {"text": "Update Status", "url": f"/projects/{project_name}/status"}
            ],
            metadata={"project_name": project_name, "days_remaining": days_remaining}
        )
    
    @staticmethod
    def memory_insight_discovered(insight: str, relevance_score: float, user_id: str, user_role: UserRole):
        return notification_system.create_notification(
            title="New Memory Insight Discovered",
            message=f"AI has discovered a new pattern: {insight}",
            notification_type=NotificationType.MEMORY_ALERT,
            priority=NotificationPriority.MEDIUM,
            user_id=user_id,
            user_role=user_role,
            action_url="/admin/memory-center",
            action_buttons=[
                {"text": "View Insight", "url": "/admin/memory-center"},
                {"text": "Apply to Projects", "url": "/projects/apply-insight"}
            ],
            metadata={"insight": insight, "relevance_score": relevance_score}
        )
    
    @staticmethod
    def client_inquiry_received(client_name: str, inquiry_type: str, user_id: str, user_role: UserRole):
        return notification_system.create_notification(
            title=f"New Client Inquiry: {client_name}",
            message=f"Received a new {inquiry_type} inquiry from {client_name}. Requires immediate attention.",
            notification_type=NotificationType.CLIENT_COMMUNICATION,
            priority=NotificationPriority.HIGH,
            user_id=user_id,
            user_role=user_role,
            action_url="/admin/inquiries",
            action_buttons=[
                {"text": "View Inquiry", "url": "/admin/inquiries"},
                {"text": "Respond", "url": f"/admin/inquiries/respond/{client_name}"}
            ],
            metadata={"client_name": client_name, "inquiry_type": inquiry_type}
        )

