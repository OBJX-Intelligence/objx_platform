"""
OBJX Intelligence Platform - Universal Dynamic Field System
Trinity Foundation-Powered Agent-Driven Field Creation
Strategic Intelligence Multiplier for Business Operations
"""

import json
import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
import uuid
from enum import Enum

class FieldType(Enum):
    """Dynamic field types with Trinity Foundation categorization"""
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    BOOLEAN = "boolean"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    FILE = "file"
    CURRENCY = "currency"
    PERCENTAGE = "percentage"
    TIMELINE = "timeline"
    RELATIONSHIP = "relationship"
    INTELLIGENCE_SCORE = "intelligence_score"
    STRATEGIC_METRIC = "strategic_metric"
    COMPOUND_TRACKER = "compound_tracker"

class TrinityCategory(Enum):
    """Trinity Foundation categories for field organization"""
    CLARIFY = "clarify"  # Fields that help clarify objectives and context
    COMPOUND = "compound"  # Fields that build compound intelligence
    CREATE = "create"  # Fields that track value creation and outcomes

@dataclass
class DynamicField:
    """Intelligent dynamic field with Trinity Foundation integration"""
    field_id: str
    name: str
    description: str
    field_type: FieldType
    trinity_category: TrinityCategory
    project_types: List[str]  # Which project types this field applies to
    user_tiers: List[str]  # Which user tiers can access this field
    intelligence_weight: float  # How much this field contributes to intelligence score
    compound_factor: float  # How much this field contributes to compound learning
    auto_populate: bool  # Whether this field can be auto-populated by AI
    validation_rules: Dict[str, Any]
    options: Optional[List[str]]  # For select fields
    relationships: List[str]  # Related field IDs for compound intelligence
    created_by: str
    created_at: str
    usage_count: int
    success_correlation: float  # Correlation with project success
    evolution_data: Dict[str, Any]  # How this field has evolved over time

@dataclass
class FieldCreationRequest:
    """Natural language field creation request"""
    request_text: str
    user_id: str
    project_context: str
    business_need: str
    expected_outcome: str

@dataclass
class FieldIntelligence:
    """Intelligence analysis for field usage and optimization"""
    field_id: str
    usage_patterns: Dict[str, Any]
    correlation_analysis: Dict[str, Any]
    optimization_suggestions: List[str]
    compound_insights: Dict[str, Any]
    strategic_value: float
    evolution_recommendations: List[str]

class TrinityFieldAnalyzer:
    """
    Analyzes field requests and usage through Trinity Foundation methodology
    """
    
    def __init__(self):
        self.trinity_patterns = {
            'clarify': {
                'keywords': ['track', 'monitor', 'identify', 'analyze', 'understand', 'clarify', 'define'],
                'purposes': ['information_gathering', 'context_building', 'requirement_analysis'],
                'intelligence_focus': 'systematic_understanding'
            },
            'compound': {
                'keywords': ['pattern', 'relationship', 'connection', 'history', 'trend', 'compare'],
                'purposes': ['pattern_recognition', 'relationship_building', 'intelligence_multiplication'],
                'intelligence_focus': 'compound_learning'
            },
            'create': {
                'keywords': ['outcome', 'result', 'value', 'impact', 'achievement', 'success', 'deliver'],
                'purposes': ['value_creation', 'outcome_tracking', 'strategic_results'],
                'intelligence_focus': 'strategic_value_generation'
            }
        }
    
    def analyze_field_request(self, request: FieldCreationRequest) -> Dict[str, Any]:
        """Analyze natural language field request using Trinity methodology"""
        
        # Parse the request text for Trinity patterns
        trinity_analysis = self._identify_trinity_category(request.request_text)
        
        # Determine field type based on request context
        field_type = self._determine_field_type(request.request_text, request.business_need)
        
        # Analyze intelligence potential
        intelligence_analysis = self._analyze_intelligence_potential(request, trinity_analysis)
        
        # Generate field specifications
        field_specs = self._generate_field_specifications(request, trinity_analysis, field_type, intelligence_analysis)
        
        return {
            'trinity_analysis': trinity_analysis,
            'field_type': field_type,
            'intelligence_analysis': intelligence_analysis,
            'field_specifications': field_specs,
            'creation_confidence': self._calculate_creation_confidence(trinity_analysis, intelligence_analysis)
        }
    
    def _identify_trinity_category(self, request_text: str) -> Dict[str, Any]:
        """Identify Trinity Foundation category from request text"""
        text_lower = request_text.lower()
        
        category_scores = {}
        for category, patterns in self.trinity_patterns.items():
            score = 0
            matched_keywords = []
            
            for keyword in patterns['keywords']:
                if keyword in text_lower:
                    score += 1
                    matched_keywords.append(keyword)
            
            category_scores[category] = {
                'score': score,
                'matched_keywords': matched_keywords,
                'confidence': min(100, score * 20)  # Max 100% confidence
            }
        
        # Determine primary category
        primary_category = max(category_scores.keys(), key=lambda k: category_scores[k]['score'])
        
        return {
            'primary_category': primary_category,
            'category_scores': category_scores,
            'intelligence_focus': self.trinity_patterns[primary_category]['intelligence_focus']
        }
    
    def _determine_field_type(self, request_text: str, business_need: str) -> FieldType:
        """Determine appropriate field type based on request context"""
        text_combined = f"{request_text} {business_need}".lower()
        
        # Field type patterns
        type_patterns = {
            FieldType.DATE: ['date', 'deadline', 'schedule', 'timeline', 'when', 'permit date'],
            FieldType.CURRENCY: ['cost', 'budget', 'price', 'fee', 'payment', 'invoice', '$'],
            FieldType.PERCENTAGE: ['percent', '%', 'completion', 'progress', 'rate'],
            FieldType.BOOLEAN: ['yes/no', 'true/false', 'approved', 'completed', 'active'],
            FieldType.SELECT: ['status', 'type', 'category', 'priority', 'phase'],
            FieldType.MULTI_SELECT: ['tags', 'categories', 'multiple', 'team members'],
            FieldType.FILE: ['document', 'file', 'attachment', 'upload', 'permit'],
            FieldType.RELATIONSHIP: ['related to', 'connected', 'linked', 'associated'],
            FieldType.INTELLIGENCE_SCORE: ['intelligence', 'score', 'rating', 'assessment'],
            FieldType.STRATEGIC_METRIC: ['strategic', 'kpi', 'metric', 'performance'],
            FieldType.COMPOUND_TRACKER: ['pattern', 'trend', 'compound', 'evolution']
        }
        
        # Score each field type
        type_scores = {}
        for field_type, keywords in type_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_combined)
            if score > 0:
                type_scores[field_type] = score
        
        # Return highest scoring type, default to TEXT
        if type_scores:
            return max(type_scores.keys(), key=lambda k: type_scores[k])
        else:
            return FieldType.TEXT
    
    def _analyze_intelligence_potential(self, request: FieldCreationRequest, trinity_analysis: Dict) -> Dict[str, Any]:
        """Analyze the intelligence multiplication potential of the field"""
        
        intelligence_factors = {
            'strategic_value': self._calculate_strategic_value(request, trinity_analysis),
            'compound_potential': self._calculate_compound_potential(request, trinity_analysis),
            'automation_opportunity': self._calculate_automation_opportunity(request),
            'pattern_recognition_value': self._calculate_pattern_value(request, trinity_analysis),
            'cross_project_applicability': self._calculate_cross_project_value(request)
        }
        
        overall_intelligence_score = sum(intelligence_factors.values()) / len(intelligence_factors)
        
        return {
            'intelligence_factors': intelligence_factors,
            'overall_score': overall_intelligence_score,
            'multiplication_potential': overall_intelligence_score * 1.5,  # Compound factor
            'strategic_classification': self._classify_strategic_importance(overall_intelligence_score)
        }
    
    def _generate_field_specifications(self, request: FieldCreationRequest, trinity_analysis: Dict, 
                                     field_type: FieldType, intelligence_analysis: Dict) -> Dict[str, Any]:
        """Generate complete field specifications"""
        
        # Generate field name from request
        field_name = self._generate_field_name(request.request_text)
        
        # Generate description
        description = self._generate_field_description(request, trinity_analysis)
        
        # Determine validation rules
        validation_rules = self._generate_validation_rules(field_type, request)
        
        # Generate options for select fields
        options = self._generate_field_options(field_type, request) if field_type in [FieldType.SELECT, FieldType.MULTI_SELECT] else None
        
        # Calculate intelligence weights
        intelligence_weight = intelligence_analysis['overall_score'] / 100
        compound_factor = intelligence_analysis['multiplication_potential'] / 100
        
        return {
            'name': field_name,
            'description': description,
            'field_type': field_type,
            'trinity_category': TrinityCategory(trinity_analysis['primary_category']),
            'validation_rules': validation_rules,
            'options': options,
            'intelligence_weight': intelligence_weight,
            'compound_factor': compound_factor,
            'auto_populate': intelligence_analysis['intelligence_factors']['automation_opportunity'] > 0.7,
            'strategic_importance': intelligence_analysis['strategic_classification']
        }

class UniversalDynamicFieldSystem:
    """
    Universal Dynamic Field System with Trinity Foundation methodology
    Agent-driven field creation that multiplies intelligence across all business operations
    """
    
    def __init__(self):
        self.trinity_analyzer = TrinityFieldAnalyzer()
        self.dynamic_fields = {}  # field_id -> DynamicField
        self.field_intelligence = {}  # field_id -> FieldIntelligence
        self.field_templates = {}  # Pre-built field templates
        self.usage_analytics = {}  # Field usage analytics
        
        # Initialize with core Trinity Foundation fields
        self._initialize_trinity_foundation_fields()
    
    def _initialize_trinity_foundation_fields(self):
        """Initialize core Trinity Foundation fields"""
        
        core_fields = [
            # Clarify Fields
            {
                'name': 'Strategic Objective',
                'description': 'Primary strategic objective this project aims to achieve',
                'field_type': FieldType.TEXT,
                'trinity_category': TrinityCategory.CLARIFY,
                'intelligence_weight': 0.9,
                'compound_factor': 0.8
            },
            {
                'name': 'Stakeholder Impact Analysis',
                'description': 'Analysis of how this project impacts key stakeholders',
                'field_type': FieldType.TEXT,
                'trinity_category': TrinityCategory.CLARIFY,
                'intelligence_weight': 0.8,
                'compound_factor': 0.7
            },
            
            # Compound Fields
            {
                'name': 'Pattern Recognition Score',
                'description': 'Score indicating how well this project fits established success patterns',
                'field_type': FieldType.INTELLIGENCE_SCORE,
                'trinity_category': TrinityCategory.COMPOUND,
                'intelligence_weight': 0.95,
                'compound_factor': 0.95
            },
            {
                'name': 'Cross-Project Intelligence',
                'description': 'Insights and patterns identified from similar projects',
                'field_type': FieldType.COMPOUND_TRACKER,
                'trinity_category': TrinityCategory.COMPOUND,
                'intelligence_weight': 0.9,
                'compound_factor': 1.0
            },
            
            # Create Fields
            {
                'name': 'Strategic Value Created',
                'description': 'Quantified strategic value created beyond project deliverables',
                'field_type': FieldType.STRATEGIC_METRIC,
                'trinity_category': TrinityCategory.CREATE,
                'intelligence_weight': 1.0,
                'compound_factor': 0.9
            },
            {
                'name': 'Intelligence Multiplication Factor',
                'description': 'How much this project multiplied organizational intelligence',
                'field_type': FieldType.PERCENTAGE,
                'trinity_category': TrinityCategory.CREATE,
                'intelligence_weight': 0.95,
                'compound_factor': 1.0
            }
        ]
        
        for field_data in core_fields:
            field_id = str(uuid.uuid4())
            dynamic_field = DynamicField(
                field_id=field_id,
                name=field_data['name'],
                description=field_data['description'],
                field_type=field_data['field_type'],
                trinity_category=field_data['trinity_category'],
                project_types=['all'],
                user_tiers=['tier2', 'tier3', 'staff', 'admin'],
                intelligence_weight=field_data['intelligence_weight'],
                compound_factor=field_data['compound_factor'],
                auto_populate=True,
                validation_rules={},
                options=None,
                relationships=[],
                created_by='system',
                created_at=datetime.datetime.now().isoformat(),
                usage_count=0,
                success_correlation=0.0,
                evolution_data={}
            )
            self.dynamic_fields[field_id] = dynamic_field
    
    def create_field_from_natural_language(self, request: FieldCreationRequest) -> Dict[str, Any]:
        """
        Create dynamic field from natural language request
        Example: "Track permit dates for historic reviews"
        """
        
        # Analyze the request using Trinity methodology
        analysis = self.trinity_analyzer.analyze_field_request(request)
        
        if analysis['creation_confidence'] < 0.7:
            return {
                'success': False,
                'message': 'Need more context to create field',
                'suggestions': self._generate_clarification_questions(request, analysis)
            }
        
        # Create the dynamic field
        field_id = str(uuid.uuid4())
        field_specs = analysis['field_specifications']
        
        dynamic_field = DynamicField(
            field_id=field_id,
            name=field_specs['name'],
            description=field_specs['description'],
            field_type=field_specs['field_type'],
            trinity_category=field_specs['trinity_category'],
            project_types=[request.project_context] if request.project_context else ['all'],
            user_tiers=['tier2', 'tier3', 'staff', 'admin'],  # Default access
            intelligence_weight=field_specs['intelligence_weight'],
            compound_factor=field_specs['compound_factor'],
            auto_populate=field_specs['auto_populate'],
            validation_rules=field_specs['validation_rules'],
            options=field_specs.get('options'),
            relationships=[],
            created_by=request.user_id,
            created_at=datetime.datetime.now().isoformat(),
            usage_count=0,
            success_correlation=0.0,
            evolution_data={'creation_analysis': analysis}
        )
        
        # Store the field
        self.dynamic_fields[field_id] = dynamic_field
        
        # Initialize field intelligence tracking
        self.field_intelligence[field_id] = FieldIntelligence(
            field_id=field_id,
            usage_patterns={},
            correlation_analysis={},
            optimization_suggestions=[],
            compound_insights={},
            strategic_value=field_specs['intelligence_weight'],
            evolution_recommendations=[]
        )
        
        return {
            'success': True,
            'field_id': field_id,
            'field': dynamic_field,
            'analysis': analysis,
            'message': f"Successfully created field '{field_specs['name']}' with {field_specs['strategic_importance']} strategic importance"
        }
    
    def get_fields_for_project_type(self, project_type: str, user_tier: str) -> List[DynamicField]:
        """Get all applicable fields for a specific project type and user tier"""
        applicable_fields = []
        
        for field in self.dynamic_fields.values():
            # Check project type applicability
            if 'all' in field.project_types or project_type in field.project_types:
                # Check user tier access
                if user_tier in field.user_tiers:
                    applicable_fields.append(field)
        
        # Sort by intelligence weight (most important first)
        applicable_fields.sort(key=lambda f: f.intelligence_weight, reverse=True)
        
        return applicable_fields
    
    def get_trinity_organized_fields(self, project_type: str, user_tier: str) -> Dict[str, List[DynamicField]]:
        """Get fields organized by Trinity Foundation categories"""
        fields = self.get_fields_for_project_type(project_type, user_tier)
        
        organized_fields = {
            'clarify': [],
            'compound': [],
            'create': []
        }
        
        for field in fields:
            category = field.trinity_category.value
            organized_fields[category].append(field)
        
        return organized_fields
    
    def update_field_intelligence(self, field_id: str, usage_data: Dict[str, Any]):
        """Update field intelligence based on usage patterns"""
        if field_id not in self.field_intelligence:
            return
        
        field_intel = self.field_intelligence[field_id]
        field = self.dynamic_fields[field_id]
        
        # Update usage count
        field.usage_count += 1
        
        # Analyze usage patterns
        self._analyze_usage_patterns(field_intel, usage_data)
        
        # Update correlation analysis
        self._update_correlation_analysis(field_intel, usage_data)
        
        # Generate optimization suggestions
        field_intel.optimization_suggestions = self._generate_optimization_suggestions(field, field_intel)
        
        # Update compound insights
        self._update_compound_insights(field_intel, usage_data)
        
        # Calculate strategic value evolution
        field_intel.strategic_value = self._calculate_evolved_strategic_value(field, field_intel)
    
    def suggest_field_improvements(self, field_id: str) -> List[str]:
        """Suggest improvements for a field based on usage intelligence"""
        if field_id not in self.field_intelligence:
            return []
        
        field = self.dynamic_fields[field_id]
        field_intel = self.field_intelligence[field_id]
        
        suggestions = []
        
        # Usage-based suggestions
        if field.usage_count > 50 and field_intel.strategic_value < 0.5:
            suggestions.append("Consider refining field definition for better strategic alignment")
        
        # Correlation-based suggestions
        if field_intel.correlation_analysis.get('success_correlation', 0) > 0.8:
            suggestions.append("High success correlation - consider making this field required")
        
        # Compound intelligence suggestions
        if field.compound_factor > 0.8 and len(field.relationships) == 0:
            suggestions.append("High compound potential - consider linking to related fields")
        
        return suggestions
    
    def get_field_creation_templates(self, industry: str = None) -> Dict[str, List[Dict]]:
        """Get pre-built field templates organized by Trinity categories"""
        
        templates = {
            'clarify': [
                {
                    'name': 'Permit Requirements Analysis',
                    'description': 'Comprehensive analysis of all permit requirements',
                    'field_type': FieldType.TEXT,
                    'example_request': 'Track all permit requirements and their current status'
                },
                {
                    'name': 'Stakeholder Communication Preferences',
                    'description': 'How each stakeholder prefers to receive updates',
                    'field_type': FieldType.SELECT,
                    'example_request': 'Track how each stakeholder wants to be updated'
                }
            ],
            'compound': [
                {
                    'name': 'Similar Project Patterns',
                    'description': 'Patterns identified from similar successful projects',
                    'field_type': FieldType.COMPOUND_TRACKER,
                    'example_request': 'Track patterns from similar projects that led to success'
                },
                {
                    'name': 'Client Relationship Evolution',
                    'description': 'How the client relationship has evolved over time',
                    'field_type': FieldType.RELATIONSHIP,
                    'example_request': 'Track how our relationship with this client has developed'
                }
            ],
            'create': [
                {
                    'name': 'Strategic Value Delivered',
                    'description': 'Quantified strategic value beyond project deliverables',
                    'field_type': FieldType.STRATEGIC_METRIC,
                    'example_request': 'Track the strategic value we created beyond the basic deliverables'
                },
                {
                    'name': 'Innovation Opportunities Identified',
                    'description': 'New opportunities discovered during project execution',
                    'field_type': FieldType.MULTI_SELECT,
                    'example_request': 'Track new opportunities we discovered while working on this project'
                }
            ]
        }
        
        return templates
    
    def _generate_clarification_questions(self, request: FieldCreationRequest, analysis: Dict) -> List[str]:
        """Generate questions to clarify field creation request"""
        questions = []
        
        if analysis['creation_confidence'] < 0.5:
            questions.append("What specific information do you want to track?")
            questions.append("How will this information help with project success?")
        
        if analysis['trinity_analysis']['primary_category'] == 'clarify':
            questions.append("What decisions will this information help you make?")
        elif analysis['trinity_analysis']['primary_category'] == 'compound':
            questions.append("How should this information connect to other project data?")
        else:  # create
            questions.append("What strategic outcomes should this information help achieve?")
        
        return questions
    
    def _analyze_usage_patterns(self, field_intel: FieldIntelligence, usage_data: Dict):
        """Analyze field usage patterns for intelligence"""
        # Implementation would analyze actual usage patterns
        pass
    
    def _update_correlation_analysis(self, field_intel: FieldIntelligence, usage_data: Dict):
        """Update correlation analysis between field usage and project success"""
        # Implementation would perform statistical correlation analysis
        pass
    
    def _generate_optimization_suggestions(self, field: DynamicField, field_intel: FieldIntelligence) -> List[str]:
        """Generate field optimization suggestions"""
        suggestions = []
        
        if field.usage_count > 100 and field_intel.strategic_value > 0.8:
            suggestions.append("Consider creating related fields to capture more intelligence")
        
        if field.compound_factor > 0.9:
            suggestions.append("High compound potential - explore cross-project applications")
        
        return suggestions
    
    def _update_compound_insights(self, field_intel: FieldIntelligence, usage_data: Dict):
        """Update compound insights from field usage"""
        # Implementation would analyze compound intelligence patterns
        pass
    
    def _calculate_evolved_strategic_value(self, field: DynamicField, field_intel: FieldIntelligence) -> float:
        """Calculate evolved strategic value based on usage intelligence"""
        base_value = field.intelligence_weight
        usage_factor = min(1.5, field.usage_count / 100)  # Usage boost up to 50%
        correlation_factor = field_intel.correlation_analysis.get('success_correlation', 0.5)
        
        return min(1.0, base_value * usage_factor * (1 + correlation_factor))

# Global instance for use across the platform
universal_dynamic_field_system = UniversalDynamicFieldSystem()

