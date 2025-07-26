"""
OBJX Intelligence Platform - Project Intelligence System
Advanced project management with systematic thinking methodology integration
Invisible framework application for strategic intelligence multiplication
"""

import os
import json
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from flask import current_app

class ProjectType(Enum):
    """Project type definitions aligned with OBJX methodology"""
    MUNICIPAL_DEVELOPMENT = "municipal_development"
    COMMERCIAL_BUILD = "commercial_build"
    RESIDENTIAL_PROJECT = "residential_project"
    INFRASTRUCTURE = "infrastructure"
    ENVIRONMENTAL_REVIEW = "environmental_review"
    COMPLIANCE_AUDIT = "compliance_audit"
    STRATEGIC_PLANNING = "strategic_planning"
    CUSTOM = "custom"

class ProjectPhase(Enum):
    """Project phases following systematic thinking approach"""
    CLARIFY = "clarify"           # Understanding current state and desired outcome
    COMPOUND = "compound"         # Building intelligence and gathering resources
    CREATE = "create"             # Executing and delivering results
    COMPLETE = "complete"         # Project completion and knowledge capture

class ProjectStatus(Enum):
    """Project status definitions"""
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    AT_RISK = "at_risk"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    MEDIUM = 3
    HIGH = 5
    CRITICAL = 7
    URGENT = 9

@dataclass
class ProjectTemplate:
    """Project template for systematic approach"""
    template_id: str
    name: str
    description: str
    project_type: ProjectType
    phases: List[Dict[str, Any]]
    default_tasks: List[Dict[str, Any]]
    required_roles: List[str]
    estimated_duration: int  # in days
    complexity_score: int    # 1-10
    methodology_focus: str   # clarify, compound, or create emphasis

@dataclass
class ProjectMilestone:
    """Project milestone with strategic thinking integration"""
    milestone_id: str
    name: str
    description: str
    phase: ProjectPhase
    due_date: datetime
    completion_criteria: List[str]
    strategic_outcome: str  # What intelligence is multiplied
    dependencies: List[str]
    status: str
    completed_at: Optional[datetime] = None

@dataclass
class ProjectTask:
    """Enhanced task with systematic thinking context"""
    task_id: str
    title: str
    description: str
    phase: ProjectPhase
    priority: TaskPriority
    assigned_to: Optional[str]
    due_date: Optional[datetime]
    estimated_hours: int
    actual_hours: int
    status: str
    dependencies: List[str]
    strategic_context: str  # How this task contributes to intelligence multiplication
    methodology_step: str   # Which part of X+Y=Z this addresses
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

@dataclass
class ProjectIntelligence:
    """Project intelligence metrics and insights"""
    project_id: str
    clarity_score: float        # How well current state is understood (0-100)
    compound_score: float       # How effectively intelligence is being built (0-100)
    creation_score: float       # How well outcomes are being delivered (0-100)
    overall_health: float       # Overall project health (0-100)
    risk_factors: List[str]
    success_indicators: List[str]
    strategic_insights: List[str]
    next_actions: List[str]
    updated_at: datetime

@dataclass
class ProjectConfiguration:
    """Comprehensive project configuration"""
    project_id: str
    name: str
    description: str
    project_type: ProjectType
    client_id: str
    project_manager_id: str
    team_members: List[str]
    status: ProjectStatus
    current_phase: ProjectPhase
    
    # Strategic thinking integration
    current_state: str          # X in X+Y=Z
    desired_outcome: str        # Z in X+Y=Z
    change_required: str        # Y in X+Y=Z
    strategic_context: str
    
    # Timeline and scheduling
    start_date: datetime
    target_end_date: datetime
    actual_end_date: Optional[datetime]
    
    # Financial tracking
    budget: float
    actual_cost: float
    billing_rate: float
    
    # Configuration and customization
    custom_fields: Dict[str, Any]
    workflow_rules: List[Dict[str, Any]]
    notification_settings: Dict[str, Any]
    
    # Intelligence and insights
    milestones: List[ProjectMilestone]
    tasks: List[ProjectTask]
    intelligence: ProjectIntelligence
    
    # Metadata
    created_at: datetime
    updated_at: datetime
    created_by: str

class ProjectIntelligenceSystem:
    """Advanced project management with systematic thinking methodology"""
    
    def __init__(self):
        self.projects: Dict[str, ProjectConfiguration] = {}
        self.project_templates: Dict[str, ProjectTemplate] = {}
        self.custom_fields: Dict[str, Dict[str, Any]] = {}
        self.workflow_rules: Dict[str, List[Dict[str, Any]]] = {}
        self._initialize_project_templates()
        self._initialize_demo_projects()
    
    def _initialize_project_templates(self):
        """Initialize project templates aligned with OBJX methodology"""
        templates = [
            {
                'name': 'Municipal Development Project',
                'description': 'Systematic approach to municipal development with compliance focus',
                'project_type': ProjectType.MUNICIPAL_DEVELOPMENT,
                'methodology_focus': 'clarify',
                'phases': [
                    {
                        'phase': ProjectPhase.CLARIFY,
                        'name': 'Project Clarification',
                        'description': 'Understand current zoning, requirements, and desired outcomes',
                        'duration_days': 14,
                        'key_activities': [
                            'Site analysis and current state assessment',
                            'Stakeholder identification and requirements gathering',
                            'Regulatory framework analysis',
                            'Desired outcome definition'
                        ]
                    },
                    {
                        'phase': ProjectPhase.COMPOUND,
                        'name': 'Intelligence Building',
                        'description': 'Gather permits, approvals, and build project intelligence',
                        'duration_days': 45,
                        'key_activities': [
                            'Permit application and tracking',
                            'Environmental impact assessment',
                            'Community engagement and feedback',
                            'Design development and refinement'
                        ]
                    },
                    {
                        'phase': ProjectPhase.CREATE,
                        'name': 'Project Execution',
                        'description': 'Execute construction and deliver outcomes',
                        'duration_days': 120,
                        'key_activities': [
                            'Construction management',
                            'Quality assurance and compliance monitoring',
                            'Stakeholder communication and updates',
                            'Issue resolution and adaptation'
                        ]
                    },
                    {
                        'phase': ProjectPhase.COMPLETE,
                        'name': 'Project Completion',
                        'description': 'Finalize deliverables and capture knowledge',
                        'duration_days': 7,
                        'key_activities': [
                            'Final inspections and approvals',
                            'Documentation and knowledge capture',
                            'Client handover and training',
                            'Project retrospective and lessons learned'
                        ]
                    }
                ],
                'default_tasks': [
                    {
                        'title': 'Conduct Site Analysis',
                        'phase': ProjectPhase.CLARIFY,
                        'priority': TaskPriority.HIGH,
                        'estimated_hours': 16,
                        'strategic_context': 'Understanding current state for systematic planning',
                        'methodology_step': 'Defining X (current state)'
                    },
                    {
                        'title': 'Submit Permit Applications',
                        'phase': ProjectPhase.COMPOUND,
                        'priority': TaskPriority.CRITICAL,
                        'estimated_hours': 24,
                        'strategic_context': 'Building regulatory intelligence and approvals',
                        'methodology_step': 'Implementing Y (change required)'
                    },
                    {
                        'title': 'Begin Construction Phase',
                        'phase': ProjectPhase.CREATE,
                        'priority': TaskPriority.HIGH,
                        'estimated_hours': 200,
                        'strategic_context': 'Executing systematic plan to achieve desired outcome',
                        'methodology_step': 'Delivering Z (desired outcome)'
                    }
                ],
                'required_roles': ['Project Manager', 'Site Engineer', 'Compliance Specialist'],
                'estimated_duration': 186,
                'complexity_score': 8
            },
            {
                'name': 'Strategic Planning Initiative',
                'description': 'Systematic thinking approach to organizational strategy development',
                'project_type': ProjectType.STRATEGIC_PLANNING,
                'methodology_focus': 'compound',
                'phases': [
                    {
                        'phase': ProjectPhase.CLARIFY,
                        'name': 'Current State Analysis',
                        'description': 'Understand organizational current state and challenges',
                        'duration_days': 21,
                        'key_activities': [
                            'Organizational assessment',
                            'Stakeholder interviews',
                            'Market analysis',
                            'SWOT analysis'
                        ]
                    },
                    {
                        'phase': ProjectPhase.COMPOUND,
                        'name': 'Strategic Intelligence Development',
                        'description': 'Build comprehensive strategic intelligence and options',
                        'duration_days': 35,
                        'key_activities': [
                            'Scenario planning',
                            'Strategic option development',
                            'Risk assessment',
                            'Resource requirement analysis'
                        ]
                    },
                    {
                        'phase': ProjectPhase.CREATE,
                        'name': 'Strategy Implementation',
                        'description': 'Execute strategic initiatives and monitor progress',
                        'duration_days': 90,
                        'key_activities': [
                            'Implementation planning',
                            'Change management',
                            'Progress monitoring',
                            'Adaptive adjustments'
                        ]
                    },
                    {
                        'phase': ProjectPhase.COMPLETE,
                        'name': 'Strategy Institutionalization',
                        'description': 'Embed strategy in organizational processes',
                        'duration_days': 14,
                        'key_activities': [
                            'Process documentation',
                            'Training and knowledge transfer',
                            'Performance measurement setup',
                            'Continuous improvement framework'
                        ]
                    }
                ],
                'default_tasks': [
                    {
                        'title': 'Conduct Organizational Assessment',
                        'phase': ProjectPhase.CLARIFY,
                        'priority': TaskPriority.HIGH,
                        'estimated_hours': 40,
                        'strategic_context': 'Understanding organizational current state',
                        'methodology_step': 'Defining X (current organizational state)'
                    },
                    {
                        'title': 'Develop Strategic Options',
                        'phase': ProjectPhase.COMPOUND,
                        'priority': TaskPriority.HIGH,
                        'estimated_hours': 60,
                        'strategic_context': 'Building strategic intelligence and alternatives',
                        'methodology_step': 'Developing Y (strategic changes required)'
                    },
                    {
                        'title': 'Execute Strategic Initiatives',
                        'phase': ProjectPhase.CREATE,
                        'priority': TaskPriority.CRITICAL,
                        'estimated_hours': 120,
                        'strategic_context': 'Implementing systematic strategy for desired outcomes',
                        'methodology_step': 'Achieving Z (strategic objectives)'
                    }
                ],
                'required_roles': ['Strategy Consultant', 'Change Manager', 'Business Analyst'],
                'estimated_duration': 160,
                'complexity_score': 9
            }
        ]
        
        for template_config in templates:
            template_id = str(uuid.uuid4())
            template = ProjectTemplate(
                template_id=template_id,
                name=template_config['name'],
                description=template_config['description'],
                project_type=template_config['project_type'],
                phases=template_config['phases'],
                default_tasks=template_config['default_tasks'],
                required_roles=template_config['required_roles'],
                estimated_duration=template_config['estimated_duration'],
                complexity_score=template_config['complexity_score'],
                methodology_focus=template_config['methodology_focus']
            )
            self.project_templates[template_id] = template
    
    def _initialize_demo_projects(self):
        """Initialize demo projects with realistic data"""
        demo_projects = [
            {
                'name': 'City Hall Renovation Project',
                'description': 'Complete renovation of municipal building with accessibility upgrades',
                'project_type': ProjectType.MUNICIPAL_DEVELOPMENT,
                'client_id': 'client_001',
                'current_state': 'Aging city hall building with accessibility issues and outdated systems',
                'desired_outcome': 'Fully renovated, ADA-compliant municipal building with modern systems',
                'change_required': 'Comprehensive renovation including structural, electrical, and accessibility upgrades',
                'budget': 2500000.0,
                'actual_cost': 1875000.0,
                'status': ProjectStatus.ACTIVE,
                'current_phase': ProjectPhase.CREATE,
                'progress_percentage': 75
            },
            {
                'name': 'Downtown Parking Structure',
                'description': 'New 500-space parking structure with retail ground floor',
                'project_type': ProjectType.COMMERCIAL_BUILD,
                'client_id': 'client_002',
                'current_state': 'Vacant lot in downtown core with parking shortage',
                'desired_outcome': '500-space parking structure with retail space and revenue generation',
                'change_required': 'Design and construct multi-level parking with mixed-use components',
                'budget': 8500000.0,
                'actual_cost': 3200000.0,
                'status': ProjectStatus.ACTIVE,
                'current_phase': ProjectPhase.COMPOUND,
                'progress_percentage': 45
            },
            {
                'name': 'Residential Complex Phase 1',
                'description': '120-unit affordable housing development',
                'project_type': ProjectType.RESIDENTIAL_PROJECT,
                'client_id': 'client_003',
                'current_state': 'Housing shortage with need for affordable options',
                'desired_outcome': '120 affordable housing units with community amenities',
                'change_required': 'Develop affordable housing with sustainable design and community focus',
                'budget': 15000000.0,
                'actual_cost': 2800000.0,
                'status': ProjectStatus.ACTIVE,
                'current_phase': ProjectPhase.COMPOUND,
                'progress_percentage': 35
            }
        ]
        
        for i, project_config in enumerate(demo_projects):
            project_id = f"project_{str(uuid.uuid4())[:8]}"
            
            # Create milestones based on project phase
            milestones = self._generate_project_milestones(project_config)
            
            # Create tasks based on current phase
            tasks = self._generate_project_tasks(project_config)
            
            # Calculate project intelligence
            intelligence = self._calculate_project_intelligence(project_config, tasks)
            
            project = ProjectConfiguration(
                project_id=project_id,
                name=project_config['name'],
                description=project_config['description'],
                project_type=project_config['project_type'],
                client_id=project_config['client_id'],
                project_manager_id=f"pm_{i+1}",
                team_members=[f"member_{j}" for j in range(3, 8)],
                status=project_config['status'],
                current_phase=project_config['current_phase'],
                current_state=project_config['current_state'],
                desired_outcome=project_config['desired_outcome'],
                change_required=project_config['change_required'],
                strategic_context=f"Strategic intelligence multiplication through systematic {project_config['project_type'].value.replace('_', ' ')}",
                start_date=datetime.now() - timedelta(days=60),
                target_end_date=datetime.now() + timedelta(days=120),
                actual_end_date=None,
                budget=project_config['budget'],
                actual_cost=project_config['actual_cost'],
                billing_rate=150.0,
                custom_fields={},
                workflow_rules=[],
                notification_settings={},
                milestones=milestones,
                tasks=tasks,
                intelligence=intelligence,
                created_at=datetime.now() - timedelta(days=60),
                updated_at=datetime.now(),
                created_by='system'
            )
            
            self.projects[project_id] = project
    
    def _generate_project_milestones(self, project_config: Dict[str, Any]) -> List[ProjectMilestone]:
        """Generate realistic milestones for a project"""
        milestones = []
        base_date = datetime.now() - timedelta(days=60)
        
        milestone_templates = [
            {
                'name': 'Project Initiation Complete',
                'phase': ProjectPhase.CLARIFY,
                'days_offset': 14,
                'strategic_outcome': 'Clear understanding of current state and desired outcomes'
            },
            {
                'name': 'Permits and Approvals Secured',
                'phase': ProjectPhase.COMPOUND,
                'days_offset': 45,
                'strategic_outcome': 'Regulatory intelligence built and approvals obtained'
            },
            {
                'name': 'Construction 50% Complete',
                'phase': ProjectPhase.CREATE,
                'days_offset': 120,
                'strategic_outcome': 'Systematic execution delivering measurable progress'
            },
            {
                'name': 'Project Delivery',
                'phase': ProjectPhase.COMPLETE,
                'days_offset': 180,
                'strategic_outcome': 'Desired outcomes achieved and knowledge captured'
            }
        ]
        
        for template in milestone_templates:
            milestone_id = str(uuid.uuid4())
            milestone = ProjectMilestone(
                milestone_id=milestone_id,
                name=template['name'],
                description=f"{template['name']} for {project_config['name']}",
                phase=template['phase'],
                due_date=base_date + timedelta(days=template['days_offset']),
                completion_criteria=[
                    'All deliverables completed',
                    'Quality standards met',
                    'Stakeholder approval received'
                ],
                strategic_outcome=template['strategic_outcome'],
                dependencies=[],
                status='completed' if template['days_offset'] < 75 else 'active'
            )
            milestones.append(milestone)
        
        return milestones
    
    def _generate_project_tasks(self, project_config: Dict[str, Any]) -> List[ProjectTask]:
        """Generate realistic tasks for a project"""
        tasks = []
        base_date = datetime.now() - timedelta(days=60)
        
        task_templates = [
            {
                'title': 'Site Survey and Analysis',
                'phase': ProjectPhase.CLARIFY,
                'priority': TaskPriority.HIGH,
                'estimated_hours': 24,
                'days_offset': 7,
                'status': 'completed',
                'strategic_context': 'Understanding current site conditions for systematic planning',
                'methodology_step': 'Defining X (current site state)'
            },
            {
                'title': 'Permit Application Submission',
                'phase': ProjectPhase.COMPOUND,
                'priority': TaskPriority.CRITICAL,
                'estimated_hours': 16,
                'days_offset': 30,
                'status': 'completed',
                'strategic_context': 'Building regulatory intelligence and securing approvals',
                'methodology_step': 'Implementing Y (regulatory compliance)'
            },
            {
                'title': 'Foundation Work',
                'phase': ProjectPhase.CREATE,
                'priority': TaskPriority.HIGH,
                'estimated_hours': 80,
                'days_offset': 90,
                'status': 'active',
                'strategic_context': 'Executing systematic construction plan',
                'methodology_step': 'Creating Z (physical infrastructure)'
            },
            {
                'title': 'Electrical Systems Installation',
                'phase': ProjectPhase.CREATE,
                'priority': TaskPriority.MEDIUM,
                'estimated_hours': 60,
                'days_offset': 110,
                'status': 'pending',
                'strategic_context': 'Installing modern systems for desired functionality',
                'methodology_step': 'Creating Z (operational capability)'
            }
        ]
        
        for template in task_templates:
            task_id = str(uuid.uuid4())
            task = ProjectTask(
                task_id=task_id,
                title=template['title'],
                description=f"{template['title']} for {project_config['name']}",
                phase=template['phase'],
                priority=template['priority'],
                assigned_to=f"team_member_{hash(template['title']) % 5 + 1}",
                due_date=base_date + timedelta(days=template['days_offset']),
                estimated_hours=template['estimated_hours'],
                actual_hours=template['estimated_hours'] if template['status'] == 'completed' else 0,
                status=template['status'],
                dependencies=[],
                strategic_context=template['strategic_context'],
                methodology_step=template['methodology_step'],
                created_at=base_date,
                updated_at=datetime.now(),
                completed_at=base_date + timedelta(days=template['days_offset']) if template['status'] == 'completed' else None
            )
            tasks.append(task)
        
        return tasks
    
    def _calculate_project_intelligence(self, project_config: Dict[str, Any], tasks: List[ProjectTask]) -> ProjectIntelligence:
        """Calculate project intelligence metrics"""
        # Calculate clarity score (how well current state is understood)
        clarity_score = 85.0 if project_config['current_phase'] != ProjectPhase.CLARIFY else 95.0
        
        # Calculate compound score (how effectively intelligence is being built)
        completed_tasks = len([t for t in tasks if t.status == 'completed'])
        total_tasks = len(tasks)
        compound_score = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Calculate creation score (how well outcomes are being delivered)
        creation_score = project_config.get('progress_percentage', 0)
        
        # Overall health score
        overall_health = (clarity_score + compound_score + creation_score) / 3
        
        return ProjectIntelligence(
            project_id=project_config.get('project_id', ''),
            clarity_score=clarity_score,
            compound_score=compound_score,
            creation_score=creation_score,
            overall_health=overall_health,
            risk_factors=[
                'Weather delays possible',
                'Material cost fluctuations'
            ] if overall_health < 80 else [],
            success_indicators=[
                'On-time milestone completion',
                'Budget adherence',
                'Quality standards met'
            ],
            strategic_insights=[
                'Systematic approach enabling efficient progress',
                'Clear X+Y=Z framework driving decision-making'
            ],
            next_actions=[
                'Continue systematic execution',
                'Monitor critical path dependencies'
            ],
            updated_at=datetime.now()
        )
    
    def get_all_projects(self, user_tier: str = 'admin') -> List[Dict[str, Any]]:
        """Get all projects with tier-based filtering"""
        projects_list = []
        
        for project_id, project in self.projects.items():
            # Apply tier-based filtering
            if user_tier == 'tier_1':
                # Tier 1 sees limited project info
                project_dict = {
                    'project_id': project.project_id,
                    'name': project.name,
                    'status': project.status.value,
                    'progress': project.intelligence.creation_score,
                    'upgrade_required': True
                }
            else:
                # Full project information for higher tiers
                project_dict = asdict(project)
                project_dict['active_tasks'] = len([t for t in project.tasks if t.status == 'active'])
                project_dict['completed_tasks'] = len([t for t in project.tasks if t.status == 'completed'])
                project_dict['budget_utilization'] = (project.actual_cost / project.budget * 100) if project.budget > 0 else 0
                project_dict['days_remaining'] = (project.target_end_date - datetime.now()).days
            
            projects_list.append(project_dict)
        
        return projects_list
    
    def get_project_detail(self, project_id: str, user_tier: str = 'admin') -> Optional[Dict[str, Any]]:
        """Get detailed project information"""
        if project_id not in self.projects:
            return None
        
        project = self.projects[project_id]
        
        if user_tier == 'tier_1':
            return {
                'project_id': project.project_id,
                'name': project.name,
                'description': 'Upgrade to Tier 2 for full project access',
                'upgrade_required': True,
                'upgrade_url': '/upgrade?tier=2'
            }
        
        # Full project details for higher tiers
        project_dict = asdict(project)
        
        # Add calculated metrics
        project_dict['metrics'] = {
            'budget_utilization': (project.actual_cost / project.budget * 100) if project.budget > 0 else 0,
            'schedule_performance': project.intelligence.creation_score,
            'team_utilization': 87.5,  # Mock team utilization
            'client_satisfaction': 92.0,  # Mock client satisfaction
            'risk_level': 'Low' if project.intelligence.overall_health > 80 else 'Medium'
        }
        
        # Add recent activity
        project_dict['recent_activity'] = [
            {
                'timestamp': datetime.now() - timedelta(hours=2),
                'activity': 'Task completed: Foundation inspection',
                'user': 'Site Engineer'
            },
            {
                'timestamp': datetime.now() - timedelta(hours=6),
                'activity': 'Milestone achieved: 75% construction complete',
                'user': 'Project Manager'
            },
            {
                'timestamp': datetime.now() - timedelta(days=1),
                'activity': 'Client meeting scheduled for progress review',
                'user': 'Client Communicator Agent'
            }
        ]
        
        return project_dict
    
    def create_project_from_template(self, template_id: str, project_data: Dict[str, Any], created_by: str) -> Dict[str, Any]:
        """Create a new project from a template"""
        try:
            if template_id not in self.project_templates:
                return {'success': False, 'error': 'Template not found'}
            
            template = self.project_templates[template_id]
            project_id = str(uuid.uuid4())
            
            # Generate milestones from template
            milestones = []
            for phase in template.phases:
                milestone_id = str(uuid.uuid4())
                milestone = ProjectMilestone(
                    milestone_id=milestone_id,
                    name=f"{phase['name']} Complete",
                    description=phase['description'],
                    phase=ProjectPhase(phase['phase']),
                    due_date=datetime.now() + timedelta(days=phase['duration_days']),
                    completion_criteria=['Phase deliverables completed', 'Quality review passed'],
                    strategic_outcome=f"Strategic intelligence multiplied through {phase['name'].lower()}",
                    dependencies=[],
                    status='pending'
                )
                milestones.append(milestone)
            
            # Generate tasks from template
            tasks = []
            for task_template in template.default_tasks:
                task_id = str(uuid.uuid4())
                task = ProjectTask(
                    task_id=task_id,
                    title=task_template['title'],
                    description=f"{task_template['title']} for {project_data['name']}",
                    phase=task_template['phase'],
                    priority=task_template['priority'],
                    assigned_to=None,
                    due_date=None,
                    estimated_hours=task_template['estimated_hours'],
                    actual_hours=0,
                    status='pending',
                    dependencies=[],
                    strategic_context=task_template['strategic_context'],
                    methodology_step=task_template['methodology_step'],
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                tasks.append(task)
            
            # Calculate initial intelligence
            intelligence = ProjectIntelligence(
                project_id=project_id,
                clarity_score=0.0,
                compound_score=0.0,
                creation_score=0.0,
                overall_health=0.0,
                risk_factors=[],
                success_indicators=[],
                strategic_insights=[],
                next_actions=['Begin project clarification phase'],
                updated_at=datetime.now()
            )
            
            # Create project
            project = ProjectConfiguration(
                project_id=project_id,
                name=project_data['name'],
                description=project_data['description'],
                project_type=template.project_type,
                client_id=project_data['client_id'],
                project_manager_id=project_data.get('project_manager_id', ''),
                team_members=project_data.get('team_members', []),
                status=ProjectStatus.PLANNING,
                current_phase=ProjectPhase.CLARIFY,
                current_state=project_data.get('current_state', ''),
                desired_outcome=project_data.get('desired_outcome', ''),
                change_required=project_data.get('change_required', ''),
                strategic_context=f"Strategic intelligence multiplication through systematic {template.project_type.value.replace('_', ' ')}",
                start_date=datetime.now(),
                target_end_date=datetime.now() + timedelta(days=template.estimated_duration),
                actual_end_date=None,
                budget=project_data.get('budget', 0.0),
                actual_cost=0.0,
                billing_rate=project_data.get('billing_rate', 150.0),
                custom_fields=project_data.get('custom_fields', {}),
                workflow_rules=[],
                notification_settings={},
                milestones=milestones,
                tasks=tasks,
                intelligence=intelligence,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                created_by=created_by
            )
            
            self.projects[project_id] = project
            
            return {'success': True, 'project_id': project_id}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_project_templates(self) -> List[Dict[str, Any]]:
        """Get all available project templates"""
        return [asdict(template) for template in self.project_templates.values()]
    
    def get_project_intelligence_summary(self) -> Dict[str, Any]:
        """Get overall project intelligence summary"""
        total_projects = len(self.projects)
        active_projects = len([p for p in self.projects.values() if p.status == ProjectStatus.ACTIVE])
        
        total_budget = sum(p.budget for p in self.projects.values())
        total_actual = sum(p.actual_cost for p in self.projects.values())
        
        avg_health = sum(p.intelligence.overall_health for p in self.projects.values()) / total_projects if total_projects > 0 else 0
        
        return {
            'total_projects': total_projects,
            'active_projects': active_projects,
            'completed_projects': len([p for p in self.projects.values() if p.status == ProjectStatus.COMPLETED]),
            'total_budget': total_budget,
            'total_actual_cost': total_actual,
            'budget_utilization': (total_actual / total_budget * 100) if total_budget > 0 else 0,
            'average_project_health': avg_health,
            'projects_on_track': len([p for p in self.projects.values() if p.intelligence.overall_health > 80]),
            'projects_at_risk': len([p for p in self.projects.values() if p.intelligence.overall_health < 60])
        }

# Global project intelligence system instance
project_intelligence = ProjectIntelligenceSystem()

def get_project_intelligence():
    """Get the global project intelligence instance"""
    return project_intelligence

