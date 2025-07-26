"""
OBJX Intelligence Platform - Agent Management System
Comprehensive agent configuration, orchestration, and management
"""

import os
import json
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from flask import current_app

class AgentType(Enum):
    """Agent type definitions"""
    PROJECT_MANAGER = "project_manager"
    TASK_COORDINATOR = "task_coordinator"
    DEADLINE_MONITOR = "deadline_monitor"
    RESOURCE_OPTIMIZER = "resource_optimizer"
    CLIENT_COMMUNICATOR = "client_communicator"
    BILLING_MANAGER = "billing_manager"
    QUALITY_ASSURANCE = "quality_assurance"
    LEGAL_COMPLIANCE = "legal_compliance"
    ENVIRONMENTAL_REVIEW = "environmental_review"
    CUSTOM = "custom"

class AgentStatus(Enum):
    """Agent status definitions"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PAUSED = "paused"
    ERROR = "error"
    LEARNING = "learning"

class AgentCapability(Enum):
    """Agent capability definitions"""
    PROJECT_PLANNING = "project_planning"
    TASK_MANAGEMENT = "task_management"
    DEADLINE_TRACKING = "deadline_tracking"
    RESOURCE_ALLOCATION = "resource_allocation"
    CLIENT_COMMUNICATION = "client_communication"
    FINANCIAL_MANAGEMENT = "financial_management"
    QUALITY_CONTROL = "quality_control"
    COMPLIANCE_CHECKING = "compliance_checking"
    DOCUMENT_GENERATION = "document_generation"
    DATA_ANALYSIS = "data_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    WORKFLOW_AUTOMATION = "workflow_automation"
    INTEGRATION_MANAGEMENT = "integration_management"
    NOTIFICATION_HANDLING = "notification_handling"
    REPORTING = "reporting"

@dataclass
class AgentConfiguration:
    """Agent configuration structure"""
    agent_id: str
    name: str
    type: AgentType
    description: str
    capabilities: List[AgentCapability]
    status: AgentStatus
    priority_level: int  # 1-10, higher = more priority
    max_concurrent_tasks: int
    response_time_target: int  # in seconds
    escalation_threshold: int  # in minutes
    created_at: datetime
    updated_at: datetime
    created_by: str
    
    # Configuration parameters
    parameters: Dict[str, Any]
    
    # Workflow configuration
    triggers: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    
    # Performance metrics
    performance_metrics: Dict[str, Any]
    
    # Integration settings
    integrations: Dict[str, Any]

@dataclass
class AgentTask:
    """Agent task structure"""
    task_id: str
    agent_id: str
    title: str
    description: str
    priority: int
    status: str
    assigned_at: datetime
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    context: Dict[str, Any]
    result: Optional[Dict[str, Any]]

@dataclass
class AgentPerformance:
    """Agent performance metrics"""
    agent_id: str
    tasks_completed: int
    tasks_failed: int
    average_response_time: float
    success_rate: float
    efficiency_score: float
    last_activity: datetime
    uptime_percentage: float

class AgentManagementSystem:
    """Comprehensive agent management and orchestration system"""
    
    def __init__(self):
        self.agents: Dict[str, AgentConfiguration] = {}
        self.agent_tasks: Dict[str, List[AgentTask]] = {}
        self.agent_performance: Dict[str, AgentPerformance] = {}
        self.agent_templates: Dict[str, Dict[str, Any]] = {}
        self._initialize_default_agents()
        self._initialize_agent_templates()
    
    def _initialize_default_agents(self):
        """Initialize the default 7 agents"""
        default_agents = [
            {
                'name': 'Project Manager',
                'type': AgentType.PROJECT_MANAGER,
                'description': 'Oversees project lifecycle, coordinates teams, and ensures deliverables',
                'capabilities': [
                    AgentCapability.PROJECT_PLANNING,
                    AgentCapability.TASK_MANAGEMENT,
                    AgentCapability.RESOURCE_ALLOCATION,
                    AgentCapability.RISK_ASSESSMENT,
                    AgentCapability.REPORTING
                ],
                'priority_level': 9,
                'max_concurrent_tasks': 5,
                'response_time_target': 300,  # 5 minutes
                'escalation_threshold': 60,   # 1 hour
                'parameters': {
                    'project_types': ['municipal', 'commercial', 'residential'],
                    'team_size_limit': 10,
                    'budget_authority': 50000,
                    'approval_required_above': 25000
                },
                'triggers': [
                    {'event': 'project_created', 'condition': 'budget > 10000'},
                    {'event': 'milestone_missed', 'condition': 'critical_path = true'},
                    {'event': 'resource_conflict', 'condition': 'priority > 7'}
                ],
                'actions': [
                    {'type': 'create_project_plan', 'template': 'standard_project'},
                    {'type': 'assign_team_members', 'criteria': 'skill_match'},
                    {'type': 'schedule_status_meeting', 'frequency': 'weekly'}
                ]
            },
            {
                'name': 'Task Coordinator',
                'type': AgentType.TASK_COORDINATOR,
                'description': 'Manages task dependencies, assignments, and workflow optimization',
                'capabilities': [
                    AgentCapability.TASK_MANAGEMENT,
                    AgentCapability.WORKFLOW_AUTOMATION,
                    AgentCapability.DEADLINE_TRACKING,
                    AgentCapability.NOTIFICATION_HANDLING
                ],
                'priority_level': 8,
                'max_concurrent_tasks': 15,
                'response_time_target': 120,  # 2 minutes
                'escalation_threshold': 30,   # 30 minutes
                'parameters': {
                    'auto_assign_tasks': True,
                    'dependency_checking': True,
                    'workload_balancing': True,
                    'skill_matching': True
                },
                'triggers': [
                    {'event': 'task_created', 'condition': 'auto_assign = true'},
                    {'event': 'task_blocked', 'condition': 'dependency_issue = true'},
                    {'event': 'workload_imbalance', 'condition': 'variance > 20%'}
                ],
                'actions': [
                    {'type': 'assign_task', 'method': 'skill_and_availability'},
                    {'type': 'resolve_dependency', 'escalate_after': 60},
                    {'type': 'rebalance_workload', 'threshold': 80}
                ]
            },
            {
                'name': 'Deadline Monitor',
                'type': AgentType.DEADLINE_MONITOR,
                'description': 'Tracks deadlines, identifies risks, and sends proactive alerts',
                'capabilities': [
                    AgentCapability.DEADLINE_TRACKING,
                    AgentCapability.RISK_ASSESSMENT,
                    AgentCapability.NOTIFICATION_HANDLING,
                    AgentCapability.REPORTING
                ],
                'priority_level': 9,
                'max_concurrent_tasks': 20,
                'response_time_target': 60,   # 1 minute
                'escalation_threshold': 15,   # 15 minutes
                'parameters': {
                    'early_warning_days': 3,
                    'critical_warning_hours': 24,
                    'auto_escalate': True,
                    'weekend_monitoring': True
                },
                'triggers': [
                    {'event': 'deadline_approaching', 'condition': 'days_left <= 3'},
                    {'event': 'deadline_missed', 'condition': 'overdue = true'},
                    {'event': 'risk_detected', 'condition': 'probability > 70%'}
                ],
                'actions': [
                    {'type': 'send_warning', 'recipients': ['assignee', 'manager']},
                    {'type': 'escalate_to_manager', 'delay_hours': 2},
                    {'type': 'suggest_mitigation', 'auto_apply': False}
                ]
            },
            {
                'name': 'Resource Optimizer',
                'type': AgentType.RESOURCE_OPTIMIZER,
                'description': 'Optimizes resource allocation, capacity planning, and cost efficiency',
                'capabilities': [
                    AgentCapability.RESOURCE_ALLOCATION,
                    AgentCapability.DATA_ANALYSIS,
                    AgentCapability.WORKFLOW_AUTOMATION,
                    AgentCapability.REPORTING
                ],
                'priority_level': 7,
                'max_concurrent_tasks': 10,
                'response_time_target': 600,  # 10 minutes
                'escalation_threshold': 120,  # 2 hours
                'parameters': {
                    'optimization_frequency': 'daily',
                    'cost_threshold': 1000,
                    'efficiency_target': 85,
                    'auto_reallocation': False
                },
                'triggers': [
                    {'event': 'resource_shortage', 'condition': 'availability < 20%'},
                    {'event': 'cost_overrun', 'condition': 'budget_variance > 10%'},
                    {'event': 'efficiency_drop', 'condition': 'efficiency < 80%'}
                ],
                'actions': [
                    {'type': 'reallocate_resources', 'approval_required': True},
                    {'type': 'suggest_alternatives', 'cost_limit': 5000},
                    {'type': 'generate_efficiency_report', 'frequency': 'weekly'}
                ]
            },
            {
                'name': 'Client Communicator',
                'type': AgentType.CLIENT_COMMUNICATOR,
                'description': 'Manages client communications, updates, and relationship building',
                'capabilities': [
                    AgentCapability.CLIENT_COMMUNICATION,
                    AgentCapability.DOCUMENT_GENERATION,
                    AgentCapability.NOTIFICATION_HANDLING,
                    AgentCapability.REPORTING
                ],
                'priority_level': 8,
                'max_concurrent_tasks': 12,
                'response_time_target': 240,  # 4 minutes
                'escalation_threshold': 60,   # 1 hour
                'parameters': {
                    'communication_frequency': 'weekly',
                    'auto_status_updates': True,
                    'personalization_level': 'high',
                    'approval_required': False
                },
                'triggers': [
                    {'event': 'milestone_completed', 'condition': 'client_facing = true'},
                    {'event': 'issue_detected', 'condition': 'severity >= medium'},
                    {'event': 'scheduled_update', 'condition': 'frequency_met = true'}
                ],
                'actions': [
                    {'type': 'send_status_update', 'template': 'milestone_completion'},
                    {'type': 'schedule_meeting', 'urgency': 'medium'},
                    {'type': 'generate_progress_report', 'format': 'executive_summary'}
                ]
            },
            {
                'name': 'Billing Manager',
                'type': AgentType.BILLING_MANAGER,
                'description': 'Handles invoicing, payments, and financial tracking',
                'capabilities': [
                    AgentCapability.FINANCIAL_MANAGEMENT,
                    AgentCapability.DOCUMENT_GENERATION,
                    AgentCapability.INTEGRATION_MANAGEMENT,
                    AgentCapability.NOTIFICATION_HANDLING
                ],
                'priority_level': 9,
                'max_concurrent_tasks': 8,
                'response_time_target': 180,  # 3 minutes
                'escalation_threshold': 45,   # 45 minutes
                'parameters': {
                    'auto_invoicing': True,
                    'payment_terms': 30,
                    'late_fee_percentage': 1.5,
                    'quickbooks_sync': True
                },
                'triggers': [
                    {'event': 'milestone_billing', 'condition': 'invoice_ready = true'},
                    {'event': 'payment_overdue', 'condition': 'days_overdue > 5'},
                    {'event': 'expense_submitted', 'condition': 'amount > 100'}
                ],
                'actions': [
                    {'type': 'generate_invoice', 'send_immediately': True},
                    {'type': 'send_payment_reminder', 'escalation_sequence': True},
                    {'type': 'sync_with_quickbooks', 'frequency': 'daily'}
                ]
            },
            {
                'name': 'Quality Assurance',
                'type': AgentType.QUALITY_ASSURANCE,
                'description': 'Ensures quality standards, compliance, and deliverable review',
                'capabilities': [
                    AgentCapability.QUALITY_CONTROL,
                    AgentCapability.COMPLIANCE_CHECKING,
                    AgentCapability.DOCUMENT_GENERATION,
                    AgentCapability.RISK_ASSESSMENT
                ],
                'priority_level': 8,
                'max_concurrent_tasks': 6,
                'response_time_target': 480,  # 8 minutes
                'escalation_threshold': 180,  # 3 hours
                'parameters': {
                    'quality_standards': ['ISO_9001', 'municipal_codes'],
                    'review_required': True,
                    'auto_compliance_check': True,
                    'documentation_level': 'comprehensive'
                },
                'triggers': [
                    {'event': 'deliverable_ready', 'condition': 'review_required = true'},
                    {'event': 'compliance_issue', 'condition': 'severity >= medium'},
                    {'event': 'quality_metric_drop', 'condition': 'score < 85%'}
                ],
                'actions': [
                    {'type': 'conduct_quality_review', 'checklist': 'standard_qa'},
                    {'type': 'flag_compliance_issue', 'escalate_immediately': True},
                    {'type': 'generate_quality_report', 'include_recommendations': True}
                ]
            }
        ]
        
        for agent_config in default_agents:
            agent_id = str(uuid.uuid4())
            agent = AgentConfiguration(
                agent_id=agent_id,
                name=agent_config['name'],
                type=agent_config['type'],
                description=agent_config['description'],
                capabilities=agent_config['capabilities'],
                status=AgentStatus.ACTIVE,
                priority_level=agent_config['priority_level'],
                max_concurrent_tasks=agent_config['max_concurrent_tasks'],
                response_time_target=agent_config['response_time_target'],
                escalation_threshold=agent_config['escalation_threshold'],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                created_by='system',
                parameters=agent_config['parameters'],
                triggers=agent_config['triggers'],
                actions=agent_config['actions'],
                performance_metrics={},
                integrations={}
            )
            
            self.agents[agent_id] = agent
            self.agent_tasks[agent_id] = []
            self.agent_performance[agent_id] = AgentPerformance(
                agent_id=agent_id,
                tasks_completed=0,
                tasks_failed=0,
                average_response_time=0.0,
                success_rate=100.0,
                efficiency_score=85.0,
                last_activity=datetime.now(),
                uptime_percentage=99.5
            )
    
    def _initialize_agent_templates(self):
        """Initialize agent templates for common business functions"""
        self.agent_templates = {
            'legal_compliance': {
                'name': 'Legal Compliance Agent',
                'type': AgentType.LEGAL_COMPLIANCE,
                'description': 'Ensures legal compliance and regulatory adherence',
                'capabilities': [
                    AgentCapability.COMPLIANCE_CHECKING,
                    AgentCapability.RISK_ASSESSMENT,
                    AgentCapability.DOCUMENT_GENERATION
                ],
                'parameters': {
                    'jurisdictions': ['federal', 'state', 'local'],
                    'compliance_frameworks': ['OSHA', 'EPA', 'ADA'],
                    'auto_check': True
                }
            },
            'environmental_review': {
                'name': 'Environmental Review Agent',
                'type': AgentType.ENVIRONMENTAL_REVIEW,
                'description': 'Conducts environmental impact assessments and reviews',
                'capabilities': [
                    AgentCapability.COMPLIANCE_CHECKING,
                    AgentCapability.DATA_ANALYSIS,
                    AgentCapability.DOCUMENT_GENERATION,
                    AgentCapability.RISK_ASSESSMENT
                ],
                'parameters': {
                    'assessment_types': ['NEPA', 'CEQA', 'wetlands'],
                    'auto_screening': True,
                    'report_templates': ['standard', 'detailed', 'summary']
                }
            },
            'custom_specialist': {
                'name': 'Custom Specialist Agent',
                'type': AgentType.CUSTOM,
                'description': 'Customizable agent for specific business needs',
                'capabilities': [
                    AgentCapability.TASK_MANAGEMENT,
                    AgentCapability.DATA_ANALYSIS,
                    AgentCapability.NOTIFICATION_HANDLING
                ],
                'parameters': {
                    'specialization': 'custom',
                    'configurable': True
                }
            }
        }
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get all configured agents"""
        agents_list = []
        for agent_id, agent in self.agents.items():
            performance = self.agent_performance.get(agent_id)
            agent_dict = asdict(agent)
            agent_dict['performance'] = asdict(performance) if performance else None
            agent_dict['active_tasks'] = len([t for t in self.agent_tasks.get(agent_id, []) if t.status == 'active'])
            agents_list.append(agent_dict)
        
        return agents_list
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get specific agent configuration"""
        if agent_id not in self.agents:
            return None
        
        agent = self.agents[agent_id]
        performance = self.agent_performance.get(agent_id)
        tasks = self.agent_tasks.get(agent_id, [])
        
        agent_dict = asdict(agent)
        agent_dict['performance'] = asdict(performance) if performance else None
        agent_dict['tasks'] = [asdict(task) for task in tasks]
        
        return agent_dict
    
    def create_agent(self, agent_config: Dict[str, Any], created_by: str) -> Dict[str, Any]:
        """Create a new agent"""
        try:
            agent_id = str(uuid.uuid4())
            
            # Validate required fields
            required_fields = ['name', 'type', 'description', 'capabilities']
            for field in required_fields:
                if field not in agent_config:
                    return {'success': False, 'error': f'Missing required field: {field}'}
            
            # Create agent configuration
            agent = AgentConfiguration(
                agent_id=agent_id,
                name=agent_config['name'],
                type=AgentType(agent_config['type']),
                description=agent_config['description'],
                capabilities=[AgentCapability(cap) for cap in agent_config['capabilities']],
                status=AgentStatus.ACTIVE,
                priority_level=agent_config.get('priority_level', 5),
                max_concurrent_tasks=agent_config.get('max_concurrent_tasks', 5),
                response_time_target=agent_config.get('response_time_target', 300),
                escalation_threshold=agent_config.get('escalation_threshold', 60),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                created_by=created_by,
                parameters=agent_config.get('parameters', {}),
                triggers=agent_config.get('triggers', []),
                actions=agent_config.get('actions', []),
                performance_metrics={},
                integrations=agent_config.get('integrations', {})
            )
            
            self.agents[agent_id] = agent
            self.agent_tasks[agent_id] = []
            self.agent_performance[agent_id] = AgentPerformance(
                agent_id=agent_id,
                tasks_completed=0,
                tasks_failed=0,
                average_response_time=0.0,
                success_rate=100.0,
                efficiency_score=85.0,
                last_activity=datetime.now(),
                uptime_percentage=100.0
            )
            
            return {'success': True, 'agent_id': agent_id}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def update_agent(self, agent_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update agent configuration"""
        try:
            if agent_id not in self.agents:
                return {'success': False, 'error': 'Agent not found'}
            
            agent = self.agents[agent_id]
            
            # Update allowed fields
            updateable_fields = [
                'name', 'description', 'capabilities', 'status', 'priority_level',
                'max_concurrent_tasks', 'response_time_target', 'escalation_threshold',
                'parameters', 'triggers', 'actions', 'integrations'
            ]
            
            for field, value in updates.items():
                if field in updateable_fields:
                    if field == 'capabilities':
                        value = [AgentCapability(cap) for cap in value]
                    elif field == 'status':
                        value = AgentStatus(value)
                    elif field == 'type':
                        value = AgentType(value)
                    
                    setattr(agent, field, value)
            
            agent.updated_at = datetime.now()
            
            return {'success': True}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_agent(self, agent_id: str) -> Dict[str, Any]:
        """Delete an agent (only custom agents can be deleted)"""
        try:
            if agent_id not in self.agents:
                return {'success': False, 'error': 'Agent not found'}
            
            agent = self.agents[agent_id]
            
            # Prevent deletion of system agents
            if agent.created_by == 'system':
                return {'success': False, 'error': 'Cannot delete system agents'}
            
            # Check for active tasks
            active_tasks = [t for t in self.agent_tasks.get(agent_id, []) if t.status == 'active']
            if active_tasks:
                return {'success': False, 'error': f'Agent has {len(active_tasks)} active tasks'}
            
            # Delete agent
            del self.agents[agent_id]
            del self.agent_tasks[agent_id]
            del self.agent_performance[agent_id]
            
            return {'success': True}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_agent_templates(self) -> Dict[str, Any]:
        """Get available agent templates"""
        return self.agent_templates
    
    def assign_task_to_agent(self, agent_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assign a task to an agent"""
        try:
            if agent_id not in self.agents:
                return {'success': False, 'error': 'Agent not found'}
            
            agent = self.agents[agent_id]
            
            # Check if agent can handle more tasks
            active_tasks = len([t for t in self.agent_tasks[agent_id] if t.status == 'active'])
            if active_tasks >= agent.max_concurrent_tasks:
                return {'success': False, 'error': 'Agent at maximum capacity'}
            
            # Create task
            task_id = str(uuid.uuid4())
            task = AgentTask(
                task_id=task_id,
                agent_id=agent_id,
                title=task_data['title'],
                description=task_data['description'],
                priority=task_data.get('priority', 5),
                status='active',
                assigned_at=datetime.now(),
                due_date=datetime.fromisoformat(task_data['due_date']) if task_data.get('due_date') else None,
                completed_at=None,
                context=task_data.get('context', {}),
                result=None
            )
            
            self.agent_tasks[agent_id].append(task)
            
            return {'success': True, 'task_id': task_id}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_agent_performance_summary(self) -> Dict[str, Any]:
        """Get overall agent performance summary"""
        total_agents = len(self.agents)
        active_agents = len([a for a in self.agents.values() if a.status == AgentStatus.ACTIVE])
        total_tasks = sum(len(tasks) for tasks in self.agent_tasks.values())
        completed_tasks = sum(len([t for t in tasks if t.status == 'completed']) for tasks in self.agent_tasks.values())
        
        avg_success_rate = sum(p.success_rate for p in self.agent_performance.values()) / len(self.agent_performance) if self.agent_performance else 0
        avg_efficiency = sum(p.efficiency_score for p in self.agent_performance.values()) / len(self.agent_performance) if self.agent_performance else 0
        
        return {
            'total_agents': total_agents,
            'active_agents': active_agents,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            'average_success_rate': avg_success_rate,
            'average_efficiency': avg_efficiency,
            'system_uptime': 99.8  # Mock system uptime
        }

# Global agent management system instance
agent_management = AgentManagementSystem()

def get_agent_management():
    """Get the global agent management instance"""
    return agent_management

