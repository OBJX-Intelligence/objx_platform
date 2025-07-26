"""
Dynamic Project Field System for OBJX Intelligence Platform
Enables agents to add, organize, and manage project fields dynamically
Aligned with Trinity Foundation methodology: clarify • compound • create
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import re

class DynamicProjectFieldManager:
    """
    Manages dynamic project fields with agent-driven organization
    Integrates with Trinity Foundation methodology for systematic thinking
    """
    
    def __init__(self):
        self.field_types = {
            'text': {'validation': 'string', 'display': 'input'},
            'textarea': {'validation': 'string', 'display': 'textarea'},
            'number': {'validation': 'numeric', 'display': 'number'},
            'currency': {'validation': 'currency', 'display': 'currency'},
            'date': {'validation': 'date', 'display': 'date'},
            'datetime': {'validation': 'datetime', 'display': 'datetime'},
            'email': {'validation': 'email', 'display': 'email'},
            'phone': {'validation': 'phone', 'display': 'tel'},
            'url': {'validation': 'url', 'display': 'url'},
            'select': {'validation': 'options', 'display': 'select'},
            'multiselect': {'validation': 'options', 'display': 'multiselect'},
            'checkbox': {'validation': 'boolean', 'display': 'checkbox'},
            'file': {'validation': 'file', 'display': 'file'},
            'address': {'validation': 'address', 'display': 'address'},
            'contact': {'validation': 'contact', 'display': 'contact'},
            'timeline': {'validation': 'timeline', 'display': 'timeline'},
            'progress': {'validation': 'percentage', 'display': 'progress'},
            'priority': {'validation': 'priority', 'display': 'priority'},
            'status': {'validation': 'status', 'display': 'status'},
            'tags': {'validation': 'array', 'display': 'tags'},
            'relationship': {'validation': 'relationship', 'display': 'relationship'}
        }
        
        # Trinity Foundation field categories
        self.trinity_categories = {
            'clarify': {
                'name': 'Clarify - Current State',
                'description': 'Fields that help clarify the current situation and requirements',
                'color': '#FBBF24',
                'icon': '🎯',
                'fields': ['scope', 'requirements', 'constraints', 'current_status', 'stakeholders']
            },
            'compound': {
                'name': 'Compound - Intelligence Building',
                'description': 'Fields that build intelligence and compound understanding',
                'color': '#8B5CF6',
                'icon': '🧠',
                'fields': ['analysis', 'patterns', 'insights', 'connections', 'dependencies']
            },
            'create': {
                'name': 'Create - Strategic Outcomes',
                'description': 'Fields that drive creation and strategic outcomes',
                'color': '#22C55E',
                'icon': '🚀',
                'fields': ['deliverables', 'milestones', 'outcomes', 'next_steps', 'success_metrics']
            },
            'complete': {
                'name': 'Complete - Execution & Delivery',
                'description': 'Fields that ensure completion and delivery',
                'color': '#EF4444',
                'icon': '✅',
                'fields': ['tasks', 'deadlines', 'resources', 'quality_checks', 'delivery']
            }
        }
    
    def create_dynamic_field(self, project_id: str, field_data: Dict[str, Any], agent_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a new dynamic field for a project
        Agent-driven with automatic organization and validation
        """
        try:
            field_id = f"field_{uuid.uuid4().hex[:8]}"
            
            # Extract field information
            field_name = field_data.get('name', '').strip()
            field_type = field_data.get('type', 'text')
            field_value = field_data.get('value', '')
            field_description = field_data.get('description', '')
            
            # Agent-driven field categorization using Trinity Foundation
            trinity_category = self._categorize_field_by_trinity(field_name, field_description, field_value, agent_context)
            
            # Auto-generate field properties based on content analysis
            field_properties = self._analyze_field_properties(field_name, field_value, field_type)
            
            # Create field structure
            dynamic_field = {
                'id': field_id,
                'name': field_name,
                'type': field_type,
                'value': field_value,
                'description': field_description,
                'trinity_category': trinity_category,
                'properties': field_properties,
                'metadata': {
                    'created_at': datetime.now().isoformat(),
                    'created_by_agent': agent_context.get('agent_name', 'system') if agent_context else 'system',
                    'auto_organized': True,
                    'intelligence_score': self._calculate_field_intelligence_score(field_name, field_value, field_description),
                    'connections': self._identify_field_connections(field_name, field_value, project_id),
                    'suggested_integrations': self._suggest_integrations(field_name, field_value, field_type)
                },
                'validation': self._get_field_validation(field_type),
                'display_config': self._get_display_config(field_type, field_properties),
                'agent_insights': self._generate_agent_insights(field_name, field_value, field_description, agent_context)
            }
            
            return {
                'success': True,
                'field': dynamic_field,
                'organization_suggestions': self._get_organization_suggestions(dynamic_field, project_id),
                'integration_opportunities': self._identify_integration_opportunities(dynamic_field, project_id)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to create dynamic field: {str(e)}"
            }
    
    def _categorize_field_by_trinity(self, field_name: str, description: str, value: str, agent_context: Dict = None) -> str:
        """
        Automatically categorize field using Trinity Foundation methodology
        Uses AI-driven analysis to determine clarify/compound/create/complete category
        """
        field_text = f"{field_name} {description} {str(value)}".lower()
        
        # Trinity Foundation keyword analysis
        clarify_keywords = ['requirement', 'scope', 'current', 'existing', 'status', 'constraint', 'stakeholder', 'problem', 'issue', 'need', 'goal', 'objective']
        compound_keywords = ['analysis', 'insight', 'pattern', 'connection', 'relationship', 'dependency', 'impact', 'risk', 'opportunity', 'intelligence', 'understanding']
        create_keywords = ['deliverable', 'outcome', 'result', 'solution', 'strategy', 'plan', 'design', 'proposal', 'recommendation', 'next', 'action']
        complete_keywords = ['task', 'deadline', 'milestone', 'resource', 'assignment', 'completion', 'delivery', 'quality', 'review', 'approval', 'final']
        
        # Score each category
        scores = {
            'clarify': sum(1 for keyword in clarify_keywords if keyword in field_text),
            'compound': sum(1 for keyword in compound_keywords if keyword in field_text),
            'create': sum(1 for keyword in create_keywords if keyword in field_text),
            'complete': sum(1 for keyword in complete_keywords if keyword in field_text)
        }
        
        # Agent context influence
        if agent_context:
            agent_type = agent_context.get('agent_type', '').lower()
            if 'analysis' in agent_type or 'intelligence' in agent_type:
                scores['compound'] += 2
            elif 'project' in agent_type or 'task' in agent_type:
                scores['complete'] += 2
            elif 'strategy' in agent_type or 'planning' in agent_type:
                scores['create'] += 2
            elif 'compliance' in agent_type or 'review' in agent_type:
                scores['clarify'] += 2
        
        # Return highest scoring category
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def _analyze_field_properties(self, field_name: str, field_value: str, field_type: str) -> Dict[str, Any]:
        """
        Analyze field content to determine properties and behavior
        """
        properties = {
            'required': False,
            'searchable': True,
            'sortable': True,
            'filterable': True,
            'auto_update': False,
            'integration_ready': False
        }
        
        # Analyze field importance
        important_keywords = ['critical', 'urgent', 'deadline', 'budget', 'cost', 'client', 'contact', 'address', 'phone', 'email']
        if any(keyword in field_name.lower() for keyword in important_keywords):
            properties['required'] = True
            properties['priority'] = 'high'
        
        # Detect integration opportunities
        if field_type in ['email', 'phone', 'address', 'currency', 'date']:
            properties['integration_ready'] = True
        
        # Auto-update detection
        if 'status' in field_name.lower() or 'progress' in field_name.lower():
            properties['auto_update'] = True
        
        return properties
    
    def _calculate_field_intelligence_score(self, field_name: str, field_value: str, description: str) -> int:
        """
        Calculate intelligence score for field based on content richness and strategic value
        """
        score = 50  # Base score
        
        # Content richness
        if len(str(field_value)) > 100:
            score += 20
        elif len(str(field_value)) > 50:
            score += 10
        
        # Strategic keywords
        strategic_keywords = ['strategy', 'goal', 'objective', 'outcome', 'impact', 'value', 'roi', 'benefit']
        score += sum(5 for keyword in strategic_keywords if keyword in f"{field_name} {description}".lower())
        
        # Relationship indicators
        relationship_keywords = ['connect', 'link', 'relate', 'depend', 'impact', 'influence']
        score += sum(3 for keyword in relationship_keywords if keyword in f"{field_name} {description}".lower())
        
        return min(100, max(0, score))
    
    def _identify_field_connections(self, field_name: str, field_value: str, project_id: str) -> List[Dict[str, Any]]:
        """
        Identify potential connections to other fields, projects, or external systems
        """
        connections = []
        
        # Email connections
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, str(field_value))
        for email in emails:
            connections.append({
                'type': 'email',
                'value': email,
                'integration': 'gmail',
                'confidence': 0.95
            })
        
        # Phone connections
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, str(field_value))
        for phone in phones:
            connections.append({
                'type': 'phone',
                'value': phone,
                'integration': 'contacts',
                'confidence': 0.90
            })
        
        # Currency connections
        currency_pattern = r'\$[\d,]+\.?\d*'
        currencies = re.findall(currency_pattern, str(field_value))
        for currency in currencies:
            connections.append({
                'type': 'currency',
                'value': currency,
                'integration': 'quickbooks',
                'confidence': 0.85
            })
        
        return connections
    
    def _suggest_integrations(self, field_name: str, field_value: str, field_type: str) -> List[Dict[str, Any]]:
        """
        Suggest integration opportunities based on field content and type
        """
        suggestions = []
        
        # Email integration suggestions
        if field_type == 'email' or '@' in str(field_value):
            suggestions.append({
                'integration': 'gmail',
                'type': 'email_sync',
                'description': 'Sync with Gmail for automatic email tracking',
                'confidence': 0.95,
                'setup_complexity': 'low'
            })
        
        # Financial integration suggestions
        if field_type == 'currency' or '$' in str(field_value) or 'cost' in field_name.lower() or 'budget' in field_name.lower():
            suggestions.append({
                'integration': 'quickbooks',
                'type': 'financial_sync',
                'description': 'Connect to QuickBooks for automatic expense tracking',
                'confidence': 0.90,
                'setup_complexity': 'medium'
            })
        
        # File integration suggestions
        if field_type == 'file' or 'document' in field_name.lower() or 'file' in field_name.lower():
            suggestions.append({
                'integration': 'google_drive',
                'type': 'file_sync',
                'description': 'Sync with Google Drive for automatic file management',
                'confidence': 0.85,
                'setup_complexity': 'low'
            })
        
        # Calendar integration suggestions
        if field_type == 'date' or field_type == 'datetime' or 'deadline' in field_name.lower() or 'meeting' in field_name.lower():
            suggestions.append({
                'integration': 'google_calendar',
                'type': 'calendar_sync',
                'description': 'Add to Google Calendar for automatic scheduling',
                'confidence': 0.80,
                'setup_complexity': 'low'
            })
        
        return suggestions
    
    def _get_field_validation(self, field_type: str) -> Dict[str, Any]:
        """
        Get validation rules for field type
        """
        validations = {
            'text': {'min_length': 0, 'max_length': 255},
            'textarea': {'min_length': 0, 'max_length': 5000},
            'number': {'type': 'numeric'},
            'currency': {'type': 'currency', 'min': 0},
            'email': {'type': 'email', 'pattern': r'^[^\s@]+@[^\s@]+\.[^\s@]+$'},
            'phone': {'type': 'phone', 'pattern': r'^\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}$'},
            'url': {'type': 'url', 'pattern': r'^https?://'},
            'date': {'type': 'date'},
            'datetime': {'type': 'datetime'}
        }
        
        return validations.get(field_type, {'type': 'string'})
    
    def _get_display_config(self, field_type: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get display configuration for field type
        """
        base_config = {
            'component': self.field_types.get(field_type, {}).get('display', 'input'),
            'width': 'full',
            'label_position': 'top',
            'show_help': True,
            'show_validation': True
        }
        
        # Adjust based on properties
        if properties.get('priority') == 'high':
            base_config['highlight'] = True
            base_config['border_color'] = '#EF4444'
        
        if properties.get('integration_ready'):
            base_config['show_integration_icon'] = True
        
        return base_config
    
    def _generate_agent_insights(self, field_name: str, field_value: str, description: str, agent_context: Dict = None) -> Dict[str, Any]:
        """
        Generate agent insights for the field
        """
        insights = {
            'strategic_value': 'medium',
            'automation_potential': 'low',
            'integration_opportunities': [],
            'optimization_suggestions': [],
            'risk_factors': []
        }
        
        # Strategic value analysis
        strategic_keywords = ['critical', 'important', 'key', 'primary', 'main', 'core', 'essential']
        if any(keyword in f"{field_name} {description}".lower() for keyword in strategic_keywords):
            insights['strategic_value'] = 'high'
        
        # Automation potential
        automation_keywords = ['status', 'progress', 'update', 'sync', 'calculate', 'generate']
        if any(keyword in field_name.lower() for keyword in automation_keywords):
            insights['automation_potential'] = 'high'
            insights['optimization_suggestions'].append('Consider automating this field with agent updates')
        
        # Risk factor analysis
        risk_keywords = ['deadline', 'budget', 'cost', 'critical', 'urgent', 'compliance']
        if any(keyword in f"{field_name} {description}".lower() for keyword in risk_keywords):
            insights['risk_factors'].append('High-impact field requiring careful monitoring')
        
        return insights
    
    def _identify_integration_opportunities(self, field: Dict[str, Any], project_id: str) -> List[Dict[str, Any]]:
        """
        Identify integration opportunities for the field with external systems
        """
        opportunities = []
        
        field_name = field.get('name', '').lower()
        field_value = str(field.get('value', ''))
        field_type = field.get('type', '')
        connections = field.get('properties', {}).get('connections', [])
        
        # Email integration opportunities
        email_connections = [c for c in connections if c.get('type') == 'email']
        if email_connections:
            opportunities.append({
                'system': 'Gmail',
                'type': 'email_integration',
                'description': f"Automatically track emails with {', '.join([c['value'] for c in email_connections])}",
                'setup_complexity': 'low',
                'benefit_score': 85,
                'automation_potential': 'high',
                'setup_steps': [
                    'Connect Gmail API',
                    'Set up email filtering rules',
                    'Enable automatic project tagging'
                ]
            })
        
        # Phone/Contact integration
        phone_connections = [c for c in connections if c.get('type') == 'phone']
        if phone_connections or field_type == 'contact':
            opportunities.append({
                'system': 'Google Contacts',
                'type': 'contact_integration',
                'description': 'Sync contact information with Google Contacts',
                'setup_complexity': 'low',
                'benefit_score': 75,
                'automation_potential': 'medium',
                'setup_steps': [
                    'Connect Google Contacts API',
                    'Create contact synchronization rules',
                    'Enable automatic updates'
                ]
            })
        
        # Financial integration
        currency_connections = [c for c in connections if c.get('type') == 'currency']
        if currency_connections or 'cost' in field_name or 'budget' in field_name or 'expense' in field_name:
            opportunities.append({
                'system': 'QuickBooks',
                'type': 'financial_integration',
                'description': 'Automatically track project expenses and billing',
                'setup_complexity': 'medium',
                'benefit_score': 90,
                'automation_potential': 'high',
                'setup_steps': [
                    'Connect QuickBooks API',
                    'Set up expense categorization',
                    'Enable automatic invoice generation'
                ]
            })
        
        # Date/Calendar integration
        if field_type == 'date' or 'deadline' in field_name or 'schedule' in field_name:
            opportunities.append({
                'system': 'Google Calendar',
                'type': 'calendar_integration',
                'description': 'Create calendar events and reminders for important dates',
                'setup_complexity': 'low',
                'benefit_score': 80,
                'automation_potential': 'high',
                'setup_steps': [
                    'Connect Google Calendar API',
                    'Set up event creation rules',
                    'Configure reminder notifications'
                ]
            })
        
        # Document integration
        if 'document' in field_name or 'file' in field_name or 'attachment' in field_name:
            opportunities.append({
                'system': 'Google Drive',
                'type': 'document_integration',
                'description': 'Automatically organize and share project documents',
                'setup_complexity': 'medium',
                'benefit_score': 85,
                'automation_potential': 'high',
                'setup_steps': [
                    'Connect Google Drive API',
                    'Set up folder organization rules',
                    'Enable automatic file sharing'
                ]
            })
        
        # Task management integration
        if 'task' in field_name or 'todo' in field_name or 'action' in field_name:
            opportunities.append({
                'system': 'OBJX Task Manager',
                'type': 'task_integration',
                'description': 'Convert field content into actionable tasks',
                'setup_complexity': 'low',
                'benefit_score': 75,
                'automation_potential': 'medium',
                'setup_steps': [
                    'Parse field content for action items',
                    'Create task assignments',
                    'Set up progress tracking'
                ]
            })
        
        # Communication integration
        if any(keyword in field_name for keyword in ['communication', 'message', 'note', 'update']):
            opportunities.append({
                'system': 'Communication Hub',
                'type': 'communication_integration',
                'description': 'Automatically distribute updates to stakeholders',
                'setup_complexity': 'medium',
                'benefit_score': 70,
                'automation_potential': 'medium',
                'setup_steps': [
                    'Set up stakeholder notification lists',
                    'Configure communication templates',
                    'Enable automatic distribution'
                ]
            })
        
        # Sort by benefit score
        opportunities.sort(key=lambda x: x['benefit_score'], reverse=True)
        
        return opportunities

    def _get_organization_suggestions(self, field: Dict[str, Any], project_id: str) -> List[Dict[str, Any]]:
        """
        Generate organization suggestions for the field
        """
        suggestions = []
        
        field_name = field.get('name', '').lower()
        field_type = field.get('type', '')
        trinity_category = field.get('trinity_category', '')
        
        # Category-specific suggestions
        if trinity_category == 'clarify':
            suggestions.append({
                'type': 'categorization',
                'description': f"Field '{field['name']}' helps clarify project requirements and current state",
                'action': 'Place in project requirements section',
                'priority': 'high'
            })
        elif trinity_category == 'compound':
            suggestions.append({
                'type': 'intelligence',
                'description': f"Field '{field['name']}' builds compound intelligence and insights",
                'action': 'Connect to analysis and pattern recognition systems',
                'priority': 'high'
            })
        elif trinity_category == 'create':
            suggestions.append({
                'type': 'outcomes',
                'description': f"Field '{field['name']}' drives strategic outcomes and deliverables",
                'action': 'Link to milestone tracking and success metrics',
                'priority': 'critical'
            })
        elif trinity_category == 'complete':
            suggestions.append({
                'type': 'execution',
                'description': f"Field '{field['name']}' ensures completion and delivery",
                'action': 'Integrate with task management and quality control',
                'priority': 'critical'
            })
        
        # Type-specific suggestions
        if field_type == 'contact':
            suggestions.append({
                'type': 'integration',
                'description': 'Contact information can be synced with Google Contacts',
                'action': 'Enable automatic contact synchronization',
                'priority': 'medium'
            })
        elif field_type == 'date':
            suggestions.append({
                'type': 'scheduling',
                'description': 'Date field can be integrated with Google Calendar',
                'action': 'Create calendar events and reminders',
                'priority': 'high'
            })
        elif field_type == 'currency':
            suggestions.append({
                'type': 'financial',
                'description': 'Financial data can be synced with QuickBooks',
                'action': 'Enable automatic expense tracking',
                'priority': 'high'
            })
        
        # Intelligence-based suggestions
        intelligence_score = field.get('metadata', {}).get('intelligence_score', 0)
        if intelligence_score > 80:
            suggestions.append({
                'type': 'priority',
                'description': 'High-value field should be prominently displayed',
                'action': 'Feature in project dashboard summary',
                'priority': 'high'
            })
        
        return suggestions
    
    def _generate_organization_recommendations(self, organized_fields: Dict, insights: Dict) -> List[Dict[str, Any]]:
        """
        Generate recommendations for field organization optimization
        """
        recommendations = []
        
        # Check category balance
        total_fields = insights['total_fields']
        if total_fields > 0:
            clarify_ratio = len(organized_fields['clarify']) / total_fields
            if clarify_ratio > 0.5:
                recommendations.append({
                    'type': 'balance',
                    'description': 'High concentration of clarification fields',
                    'suggestion': 'Consider moving project to compound intelligence phase',
                    'priority': 'medium'
                })
            
            create_ratio = len(organized_fields['create']) / total_fields
            if create_ratio > 0.4:
                recommendations.append({
                    'type': 'execution',
                    'description': 'Strong focus on creation and outcomes',
                    'suggestion': 'Ensure adequate completion tracking fields',
                    'priority': 'high'
                })
        
        # High-value field recommendations
        if len(insights['high_value_fields']) > 5:
            recommendations.append({
                'type': 'optimization',
                'description': 'Multiple high-value fields detected',
                'suggestion': 'Create executive summary dashboard for key insights',
                'priority': 'high'
            })
        
        # Integration recommendations
        if len(insights['integration_ready_fields']) > 3:
            recommendations.append({
                'type': 'automation',
                'description': 'Several fields ready for system integration',
                'suggestion': 'Enable automated data synchronization',
                'priority': 'high'
            })
        
        return recommendations

    def organize_project_fields(self, project_id: str, fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Organize all project fields using Trinity Foundation methodology
        """
        try:
            organized_fields = {
                'clarify': [],
                'compound': [],
                'create': [],
                'complete': []
            }
            
            # Organize fields by Trinity category
            for field in fields:
                category = field.get('trinity_category', 'clarify')
                organized_fields[category].append(field)
            
            # Sort fields within each category by intelligence score
            for category in organized_fields:
                organized_fields[category].sort(
                    key=lambda x: x.get('metadata', {}).get('intelligence_score', 0),
                    reverse=True
                )
            
            # Generate organization insights
            organization_insights = {
                'total_fields': len(fields),
                'category_distribution': {cat: len(fields) for cat, fields in organized_fields.items()},
                'high_value_fields': [f for f in fields if f.get('metadata', {}).get('intelligence_score', 0) > 80],
                'integration_ready_fields': [f for f in fields if f.get('properties', {}).get('integration_ready', False)],
                'automation_candidates': [f for f in fields if f.get('agent_insights', {}).get('automation_potential') == 'high']
            }
            
            return {
                'success': True,
                'organized_fields': organized_fields,
                'insights': organization_insights,
                'recommendations': self._generate_organization_recommendations(organized_fields, organization_insights)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to organize project fields: {str(e)}"
            }

# Initialize the dynamic field manager
dynamic_field_manager = DynamicProjectFieldManager()

