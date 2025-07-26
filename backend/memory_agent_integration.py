"""
OBJX PROJECT MANAGEMENT - MEMORY SYSTEM & AGENT INTEGRATION
Advanced mem0 integration with multi-agent orchestration for comprehensive business operations

Features:
- Persistent project/task memory across sessions
- Pattern recognition and compound learning
- Multi-agent orchestration for Admin level
- Single-agent intelligence for Staff level
- Proactive business operations monitoring
- Systematic thinking integration with all operations
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import schedule
import time

from mem0 import MemoryClient
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AgentType(Enum):
    PROJECT_MANAGER = "project_manager"
    TASK_COORDINATOR = "task_coordinator"
    DEADLINE_MONITOR = "deadline_monitor"
    RESOURCE_OPTIMIZER = "resource_optimizer"
    CLIENT_COMMUNICATOR = "client_communicator"
    BILLING_MANAGER = "billing_manager"
    QUALITY_ASSURANCE = "quality_assurance"

class MemoryCategory(Enum):
    PROJECT_PATTERNS = "project_patterns"
    TEAM_DYNAMICS = "team_dynamics"
    CLIENT_PREFERENCES = "client_preferences"
    RESOURCE_UTILIZATION = "resource_utilization"
    DEADLINE_PATTERNS = "deadline_patterns"
    BILLING_HISTORY = "billing_history"
    QUALITY_METRICS = "quality_metrics"

@dataclass
class AgentSession:
    id: str
    agent_type: AgentType
    user_id: str
    is_active: bool
    last_activity: datetime
    memory_context: Dict[str, Any]
    task_queue: List[Dict[str, Any]]
    performance_metrics: Dict[str, float]

@dataclass
class MemoryInsight:
    category: MemoryCategory
    content: str
    confidence: float
    relevance_score: float
    created_at: datetime
    related_entities: List[str]

class AdvancedMemorySystem:
    """Advanced memory system with pattern recognition and compound learning"""
    
    def __init__(self, mem0_client: MemoryClient, openai_client):
        self.mem0_client = mem0_client
        self.openai_client = openai_client
        self.memory_cache = {}
        self.pattern_database = {}
        
    def store_project_memory(self, project_data: Dict[str, Any], user_id: str) -> bool:
        """Store project information with systematic analysis in memory"""
        
        try:
            # Create comprehensive memory entry
            memory_content = {
                "type": "project_creation",
                "project_name": project_data.get('name', ''),
                "project_description": project_data.get('description', ''),
                "team_size": len(project_data.get('team_members', [])),
                "budget": project_data.get('budget'),
                "timeline": {
                    "start_date": project_data.get('start_date'),
                    "due_date": project_data.get('due_date')
                },
                "systematic_analysis": project_data.get('systematic_analysis', ''),
                "timestamp": datetime.now().isoformat()
            }
            
            # Store in mem0
            messages = [{
                "role": "system",
                "content": f"Project Memory: {json.dumps(memory_content, indent=2)}"
            }]
            
            self.mem0_client.add(messages, user_id=user_id)
            
            # Update pattern database
            self._update_project_patterns(project_data, user_id)
            
            return True
            
        except Exception as e:
            print(f"Error storing project memory: {e}")
            return False
    
    def store_task_memory(self, task_data: Dict[str, Any], user_id: str) -> bool:
        """Store task information with context and patterns"""
        
        try:
            memory_content = {
                "type": "task_creation",
                "task_name": task_data.get('name', ''),
                "project_id": task_data.get('project_id'),
                "assignee": task_data.get('assignee_id'),
                "priority": task_data.get('priority'),
                "estimated_hours": task_data.get('estimated_hours'),
                "dependencies": task_data.get('dependencies', []),
                "systematic_analysis": task_data.get('systematic_analysis', ''),
                "timestamp": datetime.now().isoformat()
            }
            
            messages = [{
                "role": "system", 
                "content": f"Task Memory: {json.dumps(memory_content, indent=2)}"
            }]
            
            self.mem0_client.add(messages, user_id=user_id)
            
            # Update task patterns
            self._update_task_patterns(task_data, user_id)
            
            return True
            
        except Exception as e:
            print(f"Error storing task memory: {e}")
            return False
    
    def get_relevant_memories(self, query: str, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve relevant memories with context scoring"""
        
        try:
            memories = self.mem0_client.search(query, user_id=user_id, limit=limit)
            
            # Enhance memories with pattern insights
            enhanced_memories = []
            for memory in memories:
                enhanced_memory = {
                    "content": memory.get('memory', ''),
                    "relevance_score": memory.get('score', 0.0),
                    "timestamp": memory.get('created_at', ''),
                    "patterns": self._extract_memory_patterns(memory, user_id)
                }
                enhanced_memories.append(enhanced_memory)
            
            return enhanced_memories
            
        except Exception as e:
            print(f"Error retrieving memories: {e}")
            return []
    
    def generate_memory_insights(self, user_id: str) -> List[MemoryInsight]:
        """Generate insights from accumulated memories using systematic thinking"""
        
        try:
            # Get recent memories
            recent_memories = self.mem0_client.search("project task", user_id=user_id, limit=50)
            
            if not recent_memories:
                return []
            
            # Apply systematic thinking to generate insights
            memory_context = "\n".join([
                f"- {memory.get('memory', '')}" 
                for memory in recent_memories[:20]
            ])
            
            system_prompt = f"""
            Analyze the following project and task memories to generate systematic insights:
            
            {memory_context}
            
            Apply X+Y=Z methodology to identify:
            X: What patterns exist in the project/task data?
            Y: What insights can improve future project management?
            Z: What specific recommendations should be made?
            
            Generate insights in these categories:
            1. Project Patterns: Common project characteristics and outcomes
            2. Team Dynamics: Team performance and collaboration patterns
            3. Resource Utilization: How resources are being used effectively
            4. Deadline Patterns: Timeline accuracy and risk factors
            5. Quality Metrics: Success factors and improvement areas
            
            Provide specific, actionable insights with confidence scores.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Generate systematic insights from project memories."}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            insights_text = response.choices[0].message.content
            
            # Parse insights into structured format
            insights = self._parse_insights(insights_text, user_id)
            
            return insights
            
        except Exception as e:
            print(f"Error generating memory insights: {e}")
            return []
    
    def _update_project_patterns(self, project_data: Dict[str, Any], user_id: str):
        """Update project patterns in pattern database"""
        
        if user_id not in self.pattern_database:
            self.pattern_database[user_id] = {
                "project_patterns": [],
                "success_factors": [],
                "risk_indicators": []
            }
        
        # Extract patterns
        pattern = {
            "budget_range": self._categorize_budget(project_data.get('budget', 0)),
            "team_size": len(project_data.get('team_members', [])),
            "timeline_days": self._calculate_timeline_days(project_data),
            "priority": project_data.get('priority', 'medium'),
            "timestamp": datetime.now().isoformat()
        }
        
        self.pattern_database[user_id]["project_patterns"].append(pattern)
    
    def _update_task_patterns(self, task_data: Dict[str, Any], user_id: str):
        """Update task patterns in pattern database"""
        
        if user_id not in self.pattern_database:
            self.pattern_database[user_id] = {"task_patterns": []}
        
        pattern = {
            "estimated_hours": task_data.get('estimated_hours', 0),
            "priority": task_data.get('priority', 'medium'),
            "has_dependencies": len(task_data.get('dependencies', [])) > 0,
            "timestamp": datetime.now().isoformat()
        }
        
        if "task_patterns" not in self.pattern_database[user_id]:
            self.pattern_database[user_id]["task_patterns"] = []
        
        self.pattern_database[user_id]["task_patterns"].append(pattern)
    
    def _extract_memory_patterns(self, memory: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Extract patterns from individual memory"""
        
        patterns = {
            "frequency": 1,  # How often similar memories appear
            "success_correlation": 0.5,  # Correlation with successful outcomes
            "risk_indicators": []  # Potential risk factors identified
        }
        
        # Analyze memory content for patterns
        memory_content = memory.get('memory', '').lower()
        
        # Check for common success/risk indicators
        success_keywords = ['completed', 'successful', 'on time', 'under budget']
        risk_keywords = ['delayed', 'over budget', 'blocked', 'issues']
        
        for keyword in success_keywords:
            if keyword in memory_content:
                patterns["success_correlation"] += 0.1
        
        for keyword in risk_keywords:
            if keyword in memory_content:
                patterns["risk_indicators"].append(keyword)
                patterns["success_correlation"] -= 0.1
        
        return patterns
    
    def _parse_insights(self, insights_text: str, user_id: str) -> List[MemoryInsight]:
        """Parse AI-generated insights into structured format"""
        
        insights = []
        
        # Simple parsing - in production, would use more sophisticated NLP
        lines = insights_text.split('\n')
        current_category = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for category headers
            if any(cat.value.replace('_', ' ').title() in line for cat in MemoryCategory):
                if current_category and current_content:
                    # Save previous insight
                    insight = MemoryInsight(
                        category=current_category,
                        content='\n'.join(current_content),
                        confidence=0.8,  # Default confidence
                        relevance_score=0.9,  # Default relevance
                        created_at=datetime.now(),
                        related_entities=[user_id]
                    )
                    insights.append(insight)
                
                # Start new category
                for cat in MemoryCategory:
                    if cat.value.replace('_', ' ').title() in line:
                        current_category = cat
                        current_content = []
                        break
            else:
                if current_category:
                    current_content.append(line)
        
        # Add final insight
        if current_category and current_content:
            insight = MemoryInsight(
                category=current_category,
                content='\n'.join(current_content),
                confidence=0.8,
                relevance_score=0.9,
                created_at=datetime.now(),
                related_entities=[user_id]
            )
            insights.append(insight)
        
        return insights
    
    def _categorize_budget(self, budget: float) -> str:
        """Categorize budget into ranges"""
        if budget < 10000:
            return "small"
        elif budget < 50000:
            return "medium"
        elif budget < 100000:
            return "large"
        else:
            return "enterprise"
    
    def _calculate_timeline_days(self, project_data: Dict[str, Any]) -> int:
        """Calculate project timeline in days"""
        try:
            start_date = datetime.fromisoformat(project_data.get('start_date', ''))
            due_date = datetime.fromisoformat(project_data.get('due_date', ''))
            return (due_date - start_date).days
        except:
            return 0

class MultiAgentOrchestrator:
    """Multi-agent orchestration system for Admin level users"""
    
    def __init__(self, memory_system: AdvancedMemorySystem, openai_client):
        self.memory_system = memory_system
        self.openai_client = openai_client
        self.active_agents = {}
        self.agent_scheduler = schedule
        
        # Start background monitoring
        self.monitoring_thread = threading.Thread(target=self._run_monitoring, daemon=True)
        self.monitoring_thread.start()
    
    def initialize_admin_agents(self, user_id: str) -> Dict[str, AgentSession]:
        """Initialize all agents for Admin level user"""
        
        agents = {}
        
        for agent_type in AgentType:
            agent_session = AgentSession(
                id=f"{agent_type.value}_{user_id}_{int(time.time())}",
                agent_type=agent_type,
                user_id=user_id,
                is_active=True,
                last_activity=datetime.now(),
                memory_context={},
                task_queue=[],
                performance_metrics={"efficiency": 0.8, "accuracy": 0.9}
            )
            agents[agent_type.value] = agent_session
        
        self.active_agents[user_id] = agents
        
        # Schedule proactive monitoring
        self._schedule_proactive_tasks(user_id)
        
        return agents
    
    def initialize_staff_agent(self, user_id: str) -> AgentSession:
        """Initialize single agent for Staff level user"""
        
        agent_session = AgentSession(
            id=f"staff_agent_{user_id}_{int(time.time())}",
            agent_type=AgentType.PROJECT_MANAGER,
            user_id=user_id,
            is_active=True,
            last_activity=datetime.now(),
            memory_context={},
            task_queue=[],
            performance_metrics={"efficiency": 0.8, "accuracy": 0.9}
        )
        
        self.active_agents[user_id] = {"staff_agent": agent_session}
        
        return agent_session
    
    def process_agent_task(self, user_id: str, agent_type: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process task through specific agent with systematic thinking"""
        
        if user_id not in self.active_agents:
            return {"error": "No active agents for user"}
        
        if agent_type not in self.active_agents[user_id]:
            return {"error": f"Agent {agent_type} not found"}
        
        agent = self.active_agents[user_id][agent_type]
        
        # Get relevant memories
        relevant_memories = self.memory_system.get_relevant_memories(
            task_data.get('description', ''), user_id
        )
        
        # Apply systematic thinking through agent
        result = self._execute_agent_task(agent, task_data, relevant_memories)
        
        # Update agent activity
        agent.last_activity = datetime.now()
        
        return result
    
    def get_proactive_insights(self, user_id: str) -> Dict[str, Any]:
        """Get proactive insights from all active agents"""
        
        if user_id not in self.active_agents:
            return {"insights": [], "recommendations": []}
        
        insights = []
        recommendations = []
        
        # Collect insights from memory system
        memory_insights = self.memory_system.generate_memory_insights(user_id)
        
        for insight in memory_insights:
            insights.append({
                "category": insight.category.value,
                "content": insight.content,
                "confidence": insight.confidence,
                "timestamp": insight.created_at.isoformat()
            })
        
        # Generate proactive recommendations
        recommendations = self._generate_proactive_recommendations(user_id, memory_insights)
        
        return {
            "insights": insights,
            "recommendations": recommendations,
            "agent_status": self._get_agent_status(user_id),
            "timestamp": datetime.now().isoformat()
        }
    
    def _execute_agent_task(self, agent: AgentSession, task_data: Dict[str, Any], 
                           memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute task through agent with systematic thinking"""
        
        # Build context from memories
        memory_context = "\n".join([
            f"- {memory['content']}" 
            for memory in memories[:5]
        ])
        
        # Agent-specific system prompt
        agent_prompts = {
            AgentType.PROJECT_MANAGER: "You are a project management agent focused on planning, coordination, and delivery.",
            AgentType.TASK_COORDINATOR: "You are a task coordination agent focused on task assignment and workflow optimization.",
            AgentType.DEADLINE_MONITOR: "You are a deadline monitoring agent focused on timeline management and risk assessment.",
            AgentType.RESOURCE_OPTIMIZER: "You are a resource optimization agent focused on efficient resource allocation.",
            AgentType.CLIENT_COMMUNICATOR: "You are a client communication agent focused on stakeholder management.",
            AgentType.BILLING_MANAGER: "You are a billing management agent focused on financial tracking and invoicing.",
            AgentType.QUALITY_ASSURANCE: "You are a quality assurance agent focused on deliverable quality and standards."
        }
        
        system_prompt = f"""
        {agent_prompts.get(agent.agent_type, "You are a business operations agent.")}
        
        Apply systematic thinking (X+Y=Z methodology) to this task:
        
        Relevant Memory Context:
        {memory_context}
        
        Task Data:
        {json.dumps(task_data, indent=2)}
        
        Provide systematic analysis and actionable recommendations.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Process this {agent.agent_type.value} task systematically."}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return {
                "agent_type": agent.agent_type.value,
                "analysis": response.choices[0].message.content,
                "methodology": "X+Y=Z Systematic Thinking",
                "memory_context_used": len(memories),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "agent_type": agent.agent_type.value,
                "error": str(e),
                "analysis": "Error processing agent task"
            }
    
    def _schedule_proactive_tasks(self, user_id: str):
        """Schedule proactive monitoring tasks for agents"""
        
        # Schedule different monitoring tasks
        self.agent_scheduler.every(15).minutes.do(
            self._check_deadlines, user_id
        )
        
        self.agent_scheduler.every(1).hour.do(
            self._analyze_resource_utilization, user_id
        )
        
        self.agent_scheduler.every(4).hours.do(
            self._generate_status_updates, user_id
        )
    
    def _check_deadlines(self, user_id: str):
        """Proactive deadline monitoring"""
        # Implementation for deadline checking
        pass
    
    def _analyze_resource_utilization(self, user_id: str):
        """Proactive resource utilization analysis"""
        # Implementation for resource analysis
        pass
    
    def _generate_status_updates(self, user_id: str):
        """Generate proactive status updates"""
        # Implementation for status updates
        pass
    
    def _generate_proactive_recommendations(self, user_id: str, 
                                          insights: List[MemoryInsight]) -> List[Dict[str, Any]]:
        """Generate proactive recommendations based on insights"""
        
        recommendations = []
        
        for insight in insights:
            if insight.confidence > 0.7:
                recommendation = {
                    "type": "proactive_suggestion",
                    "category": insight.category.value,
                    "suggestion": f"Based on patterns, consider: {insight.content[:100]}...",
                    "priority": "medium" if insight.confidence > 0.8 else "low",
                    "timestamp": datetime.now().isoformat()
                }
                recommendations.append(recommendation)
        
        return recommendations
    
    def _get_agent_status(self, user_id: str) -> Dict[str, Any]:
        """Get status of all agents for user"""
        
        if user_id not in self.active_agents:
            return {}
        
        status = {}
        for agent_name, agent in self.active_agents[user_id].items():
            status[agent_name] = {
                "is_active": agent.is_active,
                "last_activity": agent.last_activity.isoformat(),
                "task_queue_size": len(agent.task_queue),
                "performance_metrics": agent.performance_metrics
            }
        
        return status
    
    def _run_monitoring(self):
        """Background monitoring thread"""
        while True:
            try:
                self.agent_scheduler.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(60)

class PrepromptSystem:
    """Preprompt system for systematic thinking integration"""
    
    def __init__(self, foundation_context: str):
        self.foundation_context = foundation_context
        self.preprompts = self._load_preprompts()
    
    def _load_preprompts(self) -> Dict[str, str]:
        """Load preprompts for different contexts"""
        
        return {
            "project_creation": f"""
            Apply systematic thinking to project creation:
            
            Foundation Context:
            {self.foundation_context}
            
            X: What do we know about this project request?
            Y: What do we need to clarify or plan?
            Z: What systematic approach should we take?
            
            Focus on comprehensive planning, risk assessment, and resource allocation.
            """,
            
            "task_assignment": f"""
            Apply systematic thinking to task assignment:
            
            Foundation Context:
            {self.foundation_context}
            
            X: What do we know about the task and available resources?
            Y: What factors should influence assignment decisions?
            Z: What is the optimal assignment strategy?
            
            Consider skills, workload, dependencies, and timeline factors.
            """,
            
            "deadline_analysis": f"""
            Apply systematic thinking to deadline analysis:
            
            Foundation Context:
            {self.foundation_context}
            
            X: What do we know about current progress and timeline?
            Y: What risks or opportunities exist?
            Z: What actions should be taken?
            
            Focus on realistic assessment and proactive risk mitigation.
            """
        }
    
    def get_preprompt(self, context: str) -> str:
        """Get preprompt for specific context"""
        return self.preprompts.get(context, self.preprompts["project_creation"])

# Integration class for the main system
class MemoryAgentIntegration:
    """Main integration class for memory system and agents"""
    
    def __init__(self, openai_client, mem0_client, foundation_context: str):
        self.memory_system = AdvancedMemorySystem(mem0_client, openai_client)
        self.agent_orchestrator = MultiAgentOrchestrator(self.memory_system, openai_client)
        self.preprompt_system = PrepromptSystem(foundation_context)
        
    def initialize_user_agents(self, user_id: str, permission_level: int) -> Dict[str, Any]:
        """Initialize agents based on user permission level"""
        
        if permission_level >= 5:  # Admin
            agents = self.agent_orchestrator.initialize_admin_agents(user_id)
            return {"type": "multi_agent", "agents": agents}
        elif permission_level >= 4:  # Staff
            agent = self.agent_orchestrator.initialize_staff_agent(user_id)
            return {"type": "single_agent", "agent": agent}
        else:
            return {"type": "basic", "message": "Basic tier - no dedicated agents"}
    
    def process_project_with_memory(self, project_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Process project creation with memory integration"""
        
        # Store in memory
        self.memory_system.store_project_memory(project_data, user_id)
        
        # Get relevant insights
        insights = self.memory_system.generate_memory_insights(user_id)
        
        # Process through appropriate agent
        agent_result = self.agent_orchestrator.process_agent_task(
            user_id, "project_manager", project_data
        )
        
        return {
            "project_processed": True,
            "memory_stored": True,
            "insights_generated": len(insights),
            "agent_analysis": agent_result,
            "methodology": "Trinity Architecture with Memory Integration"
        }
    
    def get_comprehensive_status(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive status including memory insights and agent status"""
        
        # Get proactive insights
        proactive_insights = self.agent_orchestrator.get_proactive_insights(user_id)
        
        # Get memory insights
        memory_insights = self.memory_system.generate_memory_insights(user_id)
        
        return {
            "proactive_insights": proactive_insights,
            "memory_insights": [asdict(insight) for insight in memory_insights],
            "system_status": "operational",
            "timestamp": datetime.now().isoformat()
        }

# Export main integration class
__all__ = ['MemoryAgentIntegration', 'AdvancedMemorySystem', 'MultiAgentOrchestrator', 'PrepromptSystem']

