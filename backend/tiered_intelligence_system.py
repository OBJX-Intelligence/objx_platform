"""
OBJX Intelligence Platform - Tiered Intelligence System
Strategic Intelligence Multiplier with Trinity Foundation Methodology
Scales across all tiers with intelligent restrictions
"""

class TieredIntelligenceSystem:
    """
    Manages intelligence access and capabilities across all user tiers
    Implements Trinity Foundation methodology with appropriate restrictions
    """
    
    def __init__(self):
        self.tier_capabilities = {
            'tier1': {
                'name': 'Foundation Access',
                'projects_visible': 1,  # Only personal/assigned projects
                'memory_access': False,
                'ai_assistants': ['basic_helper'],
                'dynamic_fields': False,
                'strategic_insights': 'basic',
                'trinity_methodology': 'guided',  # Guided through prompts
                'compound_intelligence': False,
                'features': {
                    'project_overview': 'limited',
                    'task_management': 'personal',
                    'billing_access': False,
                    'team_collaboration': False,
                    'advanced_analytics': False
                }
            },
            'tier2': {
                'name': 'Personal Intelligence',
                'projects_visible': 3,  # Personal + related projects
                'memory_access': 'personal',
                'ai_assistants': ['personal_assistant', 'task_coordinator'],
                'dynamic_fields': 'personal',
                'strategic_insights': 'enhanced',
                'trinity_methodology': 'integrated',  # Seamlessly integrated
                'compound_intelligence': 'personal',
                'features': {
                    'project_overview': 'enhanced',
                    'task_management': 'advanced',
                    'billing_access': 'view_only',
                    'team_collaboration': 'limited',
                    'advanced_analytics': 'personal'
                }
            },
            'tier3': {
                'name': 'Strategic Intelligence',
                'projects_visible': 'assigned',  # All assigned projects
                'memory_access': 'full_personal',
                'ai_assistants': ['strategic_partner', 'project_intelligence', 'client_orchestrator'],
                'dynamic_fields': 'full',
                'strategic_insights': 'advanced',
                'trinity_methodology': 'invisible',  # Completely invisible integration
                'compound_intelligence': 'cross_project',
                'features': {
                    'project_overview': 'full',
                    'task_management': 'strategic',
                    'billing_access': 'full',
                    'team_collaboration': 'advanced',
                    'advanced_analytics': 'strategic'
                }
            },
            'staff': {
                'name': 'Team Intelligence',
                'projects_visible': 'team_assigned',
                'memory_access': 'team_shared',
                'ai_assistants': ['team_coordinator', 'project_intelligence', 'deadline_monitor'],
                'dynamic_fields': 'team_level',
                'strategic_insights': 'team_focused',
                'trinity_methodology': 'invisible',
                'compound_intelligence': 'team_wide',
                'features': {
                    'project_overview': 'team_focused',
                    'task_management': 'team_coordination',
                    'billing_access': 'project_specific',
                    'team_collaboration': 'full',
                    'advanced_analytics': 'team_performance'
                }
            },
            'admin': {
                'name': 'Complete Intelligence Control',
                'projects_visible': 'all',
                'memory_access': 'organizational',
                'ai_assistants': 'all_available',
                'dynamic_fields': 'unlimited',
                'strategic_insights': 'comprehensive',
                'trinity_methodology': 'invisible',
                'compound_intelligence': 'organizational',
                'features': {
                    'project_overview': 'complete',
                    'task_management': 'organizational',
                    'billing_access': 'complete',
                    'team_collaboration': 'complete',
                    'advanced_analytics': 'comprehensive'
                }
            }
        }
        
        self.trinity_integration_levels = {
            'guided': {
                'clarify': 'Prompted questions to help clarify objectives',
                'compound': 'Suggested connections to previous work',
                'create': 'Guided action recommendations'
            },
            'integrated': {
                'clarify': 'Automatic information gathering and organization',
                'compound': 'Pattern recognition across personal projects',
                'create': 'Strategic recommendations based on patterns'
            },
            'invisible': {
                'clarify': 'Seamless intelligence gathering without user awareness',
                'compound': 'Automatic cross-project intelligence multiplication',
                'create': 'Proactive strategic value creation and optimization'
            }
        }
    
    def get_user_capabilities(self, user_tier, user_role=None):
        """Get capabilities for a specific user tier"""
        if user_role == 'admin':
            return self.tier_capabilities['admin']
        return self.tier_capabilities.get(user_tier, self.tier_capabilities['tier1'])
    
    def filter_projects_by_tier(self, projects, user_tier, user_id=None):
        """Filter projects based on user tier and permissions"""
        capabilities = self.get_user_capabilities(user_tier)
        
        if capabilities['projects_visible'] == 'all':
            return projects
        elif capabilities['projects_visible'] == 'team_assigned':
            # Return projects assigned to user's team
            return [p for p in projects if user_id in p.get('team', [])]
        elif capabilities['projects_visible'] == 'assigned':
            # Return projects specifically assigned to user
            return [p for p in projects if user_id in p.get('assigned_users', [])]
        elif isinstance(capabilities['projects_visible'], int):
            # Return limited number of projects
            return projects[:capabilities['projects_visible']]
        else:
            return []
    
    def get_strategic_insights_by_tier(self, insights, user_tier):
        """Filter strategic insights based on user tier"""
        capabilities = self.get_user_capabilities(user_tier)
        insight_level = capabilities['strategic_insights']
        
        if insight_level == 'basic':
            return {
                'personal_productivity': insights.get('personal_productivity', {}),
                'next_actions': insights.get('next_actions', [])[:3]
            }
        elif insight_level == 'enhanced':
            return {
                'personal_productivity': insights.get('personal_productivity', {}),
                'project_patterns': insights.get('project_patterns', {}),
                'next_actions': insights.get('next_actions', [])[:5],
                'optimization_opportunities': insights.get('optimization_opportunities', [])[:2]
            }
        elif insight_level == 'advanced':
            return {
                'personal_productivity': insights.get('personal_productivity', {}),
                'project_patterns': insights.get('project_patterns', {}),
                'cross_project_intelligence': insights.get('cross_project_intelligence', {}),
                'next_actions': insights.get('next_actions', []),
                'optimization_opportunities': insights.get('optimization_opportunities', []),
                'strategic_recommendations': insights.get('strategic_recommendations', [])[:3]
            }
        elif insight_level == 'team_focused':
            return {
                'team_performance': insights.get('team_performance', {}),
                'project_patterns': insights.get('project_patterns', {}),
                'collaboration_insights': insights.get('collaboration_insights', {}),
                'next_actions': insights.get('next_actions', []),
                'optimization_opportunities': insights.get('optimization_opportunities', [])
            }
        else:  # comprehensive
            return insights
    
    def apply_trinity_methodology(self, user_tier, context, user_input=None):
        """Apply Trinity Foundation methodology based on user tier"""
        capabilities = self.get_user_capabilities(user_tier)
        methodology_level = capabilities['trinity_methodology']
        integration = self.trinity_integration_levels[methodology_level]
        
        result = {
            'clarify': self._apply_clarify_phase(integration['clarify'], context, user_input),
            'compound': self._apply_compound_phase(integration['compound'], context, user_tier),
            'create': self._apply_create_phase(integration['create'], context, user_tier)
        }
        
        return result
    
    def _apply_clarify_phase(self, level_description, context, user_input):
        """Apply Clarify phase of Trinity Foundation"""
        if 'Prompted questions' in level_description:
            return {
                'type': 'guided',
                'questions': [
                    "What is the primary objective you want to achieve?",
                    "What information do you need to make progress?",
                    "What obstacles might prevent success?"
                ],
                'guidance': "Let's clarify your objectives step by step"
            }
        elif 'Automatic information' in level_description:
            return {
                'type': 'integrated',
                'auto_gathered_info': context.get('relevant_data', {}),
                'organized_insights': context.get('patterns', []),
                'clarity_score': 85
            }
        else:  # Seamless intelligence
            return {
                'type': 'invisible',
                'comprehensive_analysis': context,
                'hidden_intelligence': "Intelligence gathered and organized seamlessly",
                'clarity_score': 95
            }
    
    def _apply_compound_phase(self, level_description, context, user_tier):
        """Apply Compound phase of Trinity Foundation"""
        if 'Suggested connections' in level_description:
            return {
                'type': 'guided',
                'suggested_connections': [
                    "This relates to your previous project on...",
                    "Consider applying lessons learned from..."
                ],
                'pattern_hints': "Look for patterns in your past work"
            }
        elif 'Pattern recognition' in level_description:
            return {
                'type': 'integrated',
                'identified_patterns': context.get('personal_patterns', []),
                'cross_project_insights': context.get('connections', []),
                'compound_score': 75
            }
        else:  # Automatic cross-project
            return {
                'type': 'invisible',
                'intelligence_multiplication': "Patterns automatically identified and applied",
                'compound_value': context.get('compound_intelligence', {}),
                'compound_score': 92
            }
    
    def _apply_create_phase(self, level_description, context, user_tier):
        """Apply Create phase of Trinity Foundation"""
        if 'Guided action' in level_description:
            return {
                'type': 'guided',
                'recommended_actions': [
                    "Start with the highest priority task",
                    "Schedule time for the most important objective"
                ],
                'guidance': "Here are suggested next steps"
            }
        elif 'Strategic recommendations' in level_description:
            return {
                'type': 'integrated',
                'strategic_actions': context.get('recommended_actions', []),
                'value_creation_opportunities': context.get('opportunities', []),
                'creation_score': 80
            }
        else:  # Proactive strategic
            return {
                'type': 'invisible',
                'proactive_value_creation': "Strategic opportunities identified and prepared",
                'optimization_actions': context.get('optimizations', []),
                'creation_score': 94
            }
    
    def get_ai_assistants_by_tier(self, user_tier):
        """Get available AI assistants based on user tier"""
        capabilities = self.get_user_capabilities(user_tier)
        assistants = capabilities['ai_assistants']
        
        assistant_definitions = {
            'basic_helper': {
                'name': 'OBJX Assistant',
                'description': 'Helps with basic tasks and questions',
                'capabilities': ['task_guidance', 'basic_questions']
            },
            'personal_assistant': {
                'name': 'Personal Intelligence Partner',
                'description': 'Your strategic thinking companion',
                'capabilities': ['personal_optimization', 'task_coordination', 'pattern_recognition']
            },
            'task_coordinator': {
                'name': 'Task Intelligence Coordinator',
                'description': 'Optimizes your task management and workflow',
                'capabilities': ['task_optimization', 'deadline_management', 'workflow_enhancement']
            },
            'strategic_partner': {
                'name': 'Strategic Intelligence Partner',
                'description': 'Advanced strategic thinking and planning companion',
                'capabilities': ['strategic_planning', 'cross_project_analysis', 'value_creation']
            },
            'project_intelligence': {
                'name': 'Project Intelligence Agent',
                'description': 'Analyzes and optimizes project performance',
                'capabilities': ['project_analysis', 'risk_assessment', 'optimization_recommendations']
            },
            'client_orchestrator': {
                'name': 'Client Relationship Orchestrator',
                'description': 'Manages and optimizes client relationships',
                'capabilities': ['client_analysis', 'communication_optimization', 'relationship_intelligence']
            },
            'team_coordinator': {
                'name': 'Team Intelligence Coordinator',
                'description': 'Optimizes team collaboration and performance',
                'capabilities': ['team_optimization', 'collaboration_enhancement', 'performance_analysis']
            },
            'deadline_monitor': {
                'name': 'Deadline Intelligence Monitor',
                'description': 'Tracks and optimizes deadline management',
                'capabilities': ['deadline_tracking', 'timeline_optimization', 'risk_alerts']
            }
        }
        
        if assistants == 'all_available':
            return assistant_definitions
        elif isinstance(assistants, list):
            return {k: v for k, v in assistant_definitions.items() if k in assistants}
        else:
            return {}
    
    def can_access_feature(self, user_tier, feature_name):
        """Check if user tier can access a specific feature"""
        capabilities = self.get_user_capabilities(user_tier)
        return capabilities['features'].get(feature_name, False)
    
    def get_dynamic_field_capabilities(self, user_tier):
        """Get dynamic field creation capabilities by tier"""
        capabilities = self.get_user_capabilities(user_tier)
        field_access = capabilities['dynamic_fields']
        
        if field_access == False:
            return {
                'can_create': False,
                'can_modify': False,
                'templates_available': []
            }
        elif field_access == 'personal':
            return {
                'can_create': True,
                'can_modify': True,
                'scope': 'personal_projects_only',
                'templates_available': ['basic_tracking', 'personal_notes']
            }
        elif field_access == 'team_level':
            return {
                'can_create': True,
                'can_modify': True,
                'scope': 'team_projects',
                'templates_available': ['team_tracking', 'collaboration_fields', 'status_updates']
            }
        elif field_access == 'full':
            return {
                'can_create': True,
                'can_modify': True,
                'scope': 'assigned_projects',
                'templates_available': ['all_templates']
            }
        else:  # unlimited
            return {
                'can_create': True,
                'can_modify': True,
                'scope': 'all_projects',
                'templates_available': ['all_templates'],
                'can_create_templates': True
            }

# Global instance for use across the platform
tiered_intelligence = TieredIntelligenceSystem()

