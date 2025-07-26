"""
OBJX Intelligence Platform - Autonomous Agent Activation System
Real-time API connectivity with background processing and proactive intelligence
Trinity Foundation-Powered Strategic Intelligence Multiplier
"""

import asyncio
import threading
import time
import json
import openai
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import logging
from concurrent.futures import ThreadPoolExecutor
import schedule

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    INACTIVE = "inactive"
    ACTIVATING = "activating"
    ACTIVE = "active"
    PROCESSING = "processing"
    LEARNING = "learning"
    OPTIMIZING = "optimizing"

class TriggerType(Enum):
    TIME_BASED = "time_based"
    EVENT_BASED = "event_based"
    PATTERN_BASED = "pattern_based"
    THRESHOLD_BASED = "threshold_based"
    USER_INTERACTION = "user_interaction"
    SYSTEM_CHANGE = "system_change"

@dataclass
class AutonomousTask:
    task_id: str
    agent_id: str
    task_type: str
    priority: int
    context: Dict[str, Any]
    trigger_type: TriggerType
    scheduled_time: Optional[datetime]
    dependencies: List[str]
    expected_duration: int  # seconds
    retry_count: int
    max_retries: int
    status: str
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    result: Optional[Dict[str, Any]]

@dataclass
class AgentPerformanceMetrics:
    agent_id: str
    tasks_completed: int
    success_rate: float
    average_response_time: float
    intelligence_score: float
    learning_rate: float
    proactive_actions: int
    value_created: float
    last_updated: datetime

class AutonomousAgentActivator:
    """
    Activates and manages autonomous AI agents with real-time processing
    Implements proactive intelligence and continuous learning
    """
    
    def __init__(self):
        # Initialize OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Agent management
        self.active_agents = {}
        self.agent_tasks = {}
        self.task_queue = asyncio.Queue()
        self.performance_metrics = {}
        
        # Background processing
        self.background_executor = ThreadPoolExecutor(max_workers=10)
        self.is_running = False
        self.monitoring_thread = None
        
        # Proactive intelligence
        self.intelligence_patterns = {}
        self.learning_data = {}
        self.optimization_rules = {}
        
        # Initialize specialized agents
        self._initialize_autonomous_agents()
        
        # Start background processing
        self._start_background_processing()
    
    def _initialize_autonomous_agents(self):
        """Initialize all 7 specialized autonomous agents"""
        
        agents_config = {
            "strategic_thinking_partner": {
                "name": "Strategic Thinking Partner",
                "description": "Invisible strategic thinking enhancement using Trinity Foundation",
                "capabilities": ["invisible_trinity_guidance", "strategic_pattern_recognition", "decision_enhancement"],
                "proactive_triggers": ["decision_point", "problem_solving", "strategic_planning"],
                "monitoring_interval": 30,  # seconds
                "intelligence_level": "invisible",
                "auto_activate": True
            },
            "project_intelligence_agent": {
                "name": "Project Intelligence Agent", 
                "description": "Cross-project pattern analysis and optimization",
                "capabilities": ["cross_project_analysis", "predictive_optimization", "timeline_intelligence"],
                "proactive_triggers": ["project_update", "milestone_approach", "risk_detection"],
                "monitoring_interval": 60,
                "intelligence_level": "advanced",
                "auto_activate": True
            },
            "client_relationship_orchestrator": {
                "name": "Client Relationship Orchestrator",
                "description": "Strategic relationship intelligence and partnership development",
                "capabilities": ["relationship_analysis", "partnership_development", "communication_optimization"],
                "proactive_triggers": ["client_interaction", "relationship_milestone", "opportunity_detection"],
                "monitoring_interval": 120,
                "intelligence_level": "strategic",
                "auto_activate": True
            },
            "financial_intelligence_optimizer": {
                "name": "Financial Intelligence Optimizer",
                "description": "Financial pattern analysis and optimization recommendations",
                "capabilities": ["financial_analysis", "cost_optimization", "revenue_enhancement"],
                "proactive_triggers": ["financial_threshold", "budget_variance", "opportunity_identification"],
                "monitoring_interval": 300,  # 5 minutes
                "intelligence_level": "strategic",
                "auto_activate": True
            },
            "risk_intelligence_predictor": {
                "name": "Risk Intelligence Predictor",
                "description": "Predictive risk analysis and mitigation strategies",
                "capabilities": ["risk_prediction", "mitigation_planning", "early_warning_system"],
                "proactive_triggers": ["risk_indicator", "pattern_anomaly", "threshold_breach"],
                "monitoring_interval": 180,  # 3 minutes
                "intelligence_level": "predictive",
                "auto_activate": True
            },
            "innovation_opportunity_identifier": {
                "name": "Innovation Opportunity Identifier",
                "description": "Innovation pattern recognition and opportunity identification",
                "capabilities": ["innovation_analysis", "opportunity_identification", "trend_prediction"],
                "proactive_triggers": ["market_change", "technology_advancement", "pattern_emergence"],
                "monitoring_interval": 600,  # 10 minutes
                "intelligence_level": "strategic",
                "auto_activate": True
            },
            "competitive_intelligence_orchestrator": {
                "name": "Competitive Intelligence Orchestrator",
                "description": "Competitive analysis and strategic positioning",
                "capabilities": ["competitive_analysis", "market_positioning", "strategic_advantage"],
                "proactive_triggers": ["market_change", "competitor_action", "positioning_opportunity"],
                "monitoring_interval": 900,  # 15 minutes
                "intelligence_level": "strategic",
                "auto_activate": True
            }
        }
        
        # Activate each agent
        for agent_id, config in agents_config.items():
            self._activate_agent(agent_id, config)
    
    def _activate_agent(self, agent_id: str, config: Dict[str, Any]):
        """Activate an individual autonomous agent"""
        
        logger.info(f"Activating autonomous agent: {agent_id}")
        
        # Create agent instance
        agent = {
            "agent_id": agent_id,
            "config": config,
            "status": AgentStatus.ACTIVATING,
            "last_activity": datetime.now(),
            "task_count": 0,
            "learning_data": {},
            "performance_metrics": AgentPerformanceMetrics(
                agent_id=agent_id,
                tasks_completed=0,
                success_rate=1.0,
                average_response_time=0.0,
                intelligence_score=0.8,
                learning_rate=0.1,
                proactive_actions=0,
                value_created=0.0,
                last_updated=datetime.now()
            )
        }
        
        # Store agent
        self.active_agents[agent_id] = agent
        self.agent_tasks[agent_id] = []
        
        # Schedule proactive monitoring
        if config.get("auto_activate", False):
            self._schedule_proactive_monitoring(agent_id, config["monitoring_interval"])
        
        # Update status to active
        agent["status"] = AgentStatus.ACTIVE
        
        logger.info(f"Agent {agent_id} activated successfully")
    
    def _schedule_proactive_monitoring(self, agent_id: str, interval_seconds: int):
        """Schedule proactive monitoring for an agent"""
        
        def monitor_agent():
            """Proactive monitoring function"""
            try:
                self._execute_proactive_monitoring(agent_id)
            except Exception as e:
                logger.error(f"Error in proactive monitoring for {agent_id}: {e}")
        
        # Schedule recurring monitoring
        schedule.every(interval_seconds).seconds.do(monitor_agent)
        
        logger.info(f"Scheduled proactive monitoring for {agent_id} every {interval_seconds} seconds")
    
    def _execute_proactive_monitoring(self, agent_id: str):
        """Execute proactive monitoring for an agent"""
        
        agent = self.active_agents.get(agent_id)
        if not agent or agent["status"] != AgentStatus.ACTIVE:
            return
        
        logger.info(f"Executing proactive monitoring for {agent_id}")
        
        # Update agent status
        agent["status"] = AgentStatus.PROCESSING
        agent["last_activity"] = datetime.now()
        
        try:
            # Get agent configuration
            config = agent["config"]
            
            # Analyze current context for proactive opportunities
            context = self._analyze_proactive_context(agent_id, config)
            
            # Generate proactive insights
            insights = self._generate_proactive_insights(agent_id, context)
            
            # Execute proactive actions if needed
            if insights.get("actions_recommended"):
                self._execute_proactive_actions(agent_id, insights)
            
            # Update learning data
            self._update_agent_learning(agent_id, context, insights)
            
            # Update performance metrics
            self._update_performance_metrics(agent_id, True, time.time())
            
            logger.info(f"Proactive monitoring completed for {agent_id}")
            
        except Exception as e:
            logger.error(f"Error in proactive monitoring for {agent_id}: {e}")
            self._update_performance_metrics(agent_id, False, time.time())
        
        finally:
            # Reset agent status
            agent["status"] = AgentStatus.ACTIVE
    
    def _analyze_proactive_context(self, agent_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current context for proactive opportunities"""
        
        context = {
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "system_state": self._get_system_state(),
            "recent_activities": self._get_recent_activities(),
            "performance_trends": self._get_performance_trends(agent_id),
            "trigger_analysis": {}
        }
        
        # Analyze each proactive trigger
        for trigger in config.get("proactive_triggers", []):
            context["trigger_analysis"][trigger] = self._analyze_trigger(trigger)
        
        return context
    
    def _get_system_state(self) -> Dict[str, Any]:
        """Get current system state for analysis"""
        return {
            "active_agents": len(self.active_agents),
            "total_tasks": sum(len(tasks) for tasks in self.agent_tasks.values()),
            "system_load": self._calculate_system_load(),
            "memory_usage": self._get_memory_usage(),
            "api_status": self._check_api_status()
        }
    
    def _get_recent_activities(self) -> List[Dict[str, Any]]:
        """Get recent system activities for pattern analysis"""
        # This would integrate with actual system logs and activities
        return [
            {
                "activity_type": "user_interaction",
                "timestamp": datetime.now().isoformat(),
                "details": "Strategic chat interaction"
            },
            {
                "activity_type": "project_update", 
                "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
                "details": "Project progress updated"
            }
        ]
    
    def _get_performance_trends(self, agent_id: str) -> Dict[str, Any]:
        """Get performance trends for the agent"""
        metrics = self.performance_metrics.get(agent_id, {})
        return {
            "success_rate_trend": "stable",
            "response_time_trend": "improving",
            "intelligence_score_trend": "increasing",
            "learning_rate": metrics.get("learning_rate", 0.1)
        }
    
    def _analyze_trigger(self, trigger: str) -> Dict[str, Any]:
        """Analyze a specific proactive trigger"""
        
        trigger_analysis = {
            "trigger_type": trigger,
            "activation_probability": 0.0,
            "context_relevance": 0.0,
            "recommended_action": None,
            "priority": 0
        }
        
        # Analyze different trigger types
        if trigger == "decision_point":
            trigger_analysis.update({
                "activation_probability": 0.7,
                "context_relevance": 0.8,
                "recommended_action": "provide_strategic_guidance",
                "priority": 8
            })
        elif trigger == "project_update":
            trigger_analysis.update({
                "activation_probability": 0.6,
                "context_relevance": 0.9,
                "recommended_action": "analyze_project_patterns",
                "priority": 7
            })
        elif trigger == "risk_indicator":
            trigger_analysis.update({
                "activation_probability": 0.8,
                "context_relevance": 0.95,
                "recommended_action": "assess_risk_mitigation",
                "priority": 9
            })
        
        return trigger_analysis
    
    def _generate_proactive_insights(self, agent_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate proactive insights using OpenAI API"""
        
        try:
            # Prepare prompt for proactive analysis
            prompt = self._build_proactive_prompt(agent_id, context)
            
            # Call OpenAI API for intelligent analysis
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a proactive AI agent in the OBJX Intelligence Platform. Analyze the context and provide strategic insights and recommendations using Trinity Foundation methodology (clarify, compound, create) invisibly."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse response
            insights_text = response.choices[0].message.content
            
            # Structure insights
            insights = {
                "agent_id": agent_id,
                "timestamp": datetime.now().isoformat(),
                "raw_insights": insights_text,
                "structured_insights": self._parse_insights(insights_text),
                "actions_recommended": self._extract_recommended_actions(insights_text),
                "priority_score": self._calculate_priority_score(context),
                "confidence_level": 0.85
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating proactive insights for {agent_id}: {e}")
            return {
                "agent_id": agent_id,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "actions_recommended": False,
                "priority_score": 0,
                "confidence_level": 0.0
            }
    
    def _build_proactive_prompt(self, agent_id: str, context: Dict[str, Any]) -> str:
        """Build prompt for proactive analysis"""
        
        agent = self.active_agents[agent_id]
        config = agent["config"]
        
        prompt = f"""
        As the {config['name']}, analyze the current context and provide proactive strategic insights.
        
        Agent Capabilities: {', '.join(config.get('capabilities', []))}
        
        Current Context:
        - System State: {json.dumps(context['system_state'], indent=2)}
        - Recent Activities: {json.dumps(context['recent_activities'], indent=2)}
        - Performance Trends: {json.dumps(context['performance_trends'], indent=2)}
        - Trigger Analysis: {json.dumps(context['trigger_analysis'], indent=2)}
        
        Please provide:
        1. Strategic insights based on current patterns
        2. Proactive recommendations for optimization
        3. Potential risks or opportunities identified
        4. Suggested actions with priority levels
        5. Trinity Foundation analysis (clarify what's happening, compound insights from patterns, create strategic value)
        
        Focus on actionable intelligence that multiplies strategic thinking capability.
        """
        
        return prompt
    
    def _parse_insights(self, insights_text: str) -> Dict[str, Any]:
        """Parse structured insights from AI response"""
        
        # This would use more sophisticated parsing in production
        return {
            "strategic_insights": self._extract_section(insights_text, "strategic insights"),
            "recommendations": self._extract_section(insights_text, "recommendations"),
            "risks_opportunities": self._extract_section(insights_text, "risks"),
            "trinity_analysis": self._extract_section(insights_text, "trinity")
        }
    
    def _extract_section(self, text: str, section_keyword: str) -> List[str]:
        """Extract specific section from insights text"""
        # Simplified extraction - would be more sophisticated in production
        lines = text.split('\n')
        section_lines = []
        in_section = False
        
        for line in lines:
            if section_keyword.lower() in line.lower():
                in_section = True
                continue
            elif in_section and line.strip().startswith(('1.', '2.', '3.', '-', '*')):
                section_lines.append(line.strip())
            elif in_section and not line.strip():
                break
        
        return section_lines
    
    def _extract_recommended_actions(self, insights_text: str) -> bool:
        """Check if actions are recommended"""
        action_keywords = ["recommend", "suggest", "should", "action", "implement"]
        return any(keyword in insights_text.lower() for keyword in action_keywords)
    
    def _calculate_priority_score(self, context: Dict[str, Any]) -> int:
        """Calculate priority score for insights"""
        score = 5  # Base score
        
        # Increase based on trigger analysis
        for trigger_data in context.get("trigger_analysis", {}).values():
            score += trigger_data.get("priority", 0)
        
        # Increase based on system load
        system_load = context.get("system_state", {}).get("system_load", 0)
        if system_load > 0.8:
            score += 3
        
        return min(score, 10)  # Cap at 10
    
    def _execute_proactive_actions(self, agent_id: str, insights: Dict[str, Any]):
        """Execute proactive actions based on insights"""
        
        logger.info(f"Executing proactive actions for {agent_id}")
        
        # Create proactive task
        task = AutonomousTask(
            task_id=str(uuid.uuid4()),
            agent_id=agent_id,
            task_type="proactive_action",
            priority=insights.get("priority_score", 5),
            context={"insights": insights},
            trigger_type=TriggerType.PATTERN_BASED,
            scheduled_time=None,
            dependencies=[],
            expected_duration=60,
            retry_count=0,
            max_retries=3,
            status="pending",
            created_at=datetime.now(),
            started_at=None,
            completed_at=None,
            result=None
        )
        
        # Add to task queue
        self.agent_tasks[agent_id].append(task)
        
        # Execute task asynchronously
        self.background_executor.submit(self._execute_autonomous_task, task)
    
    def _execute_autonomous_task(self, task: AutonomousTask):
        """Execute an autonomous task"""
        
        logger.info(f"Executing autonomous task {task.task_id} for agent {task.agent_id}")
        
        task.started_at = datetime.now()
        task.status = "running"
        
        try:
            # Execute task based on type
            if task.task_type == "proactive_action":
                result = self._execute_proactive_task(task)
            else:
                result = {"status": "unknown_task_type"}
            
            # Update task
            task.completed_at = datetime.now()
            task.status = "completed"
            task.result = result
            
            # Update agent metrics
            agent = self.active_agents[task.agent_id]
            agent["task_count"] += 1
            
            logger.info(f"Task {task.task_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Error executing task {task.task_id}: {e}")
            task.status = "failed"
            task.result = {"error": str(e)}
            
            # Retry if possible
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = "retrying"
                # Schedule retry
                self.background_executor.submit(self._execute_autonomous_task, task)
    
    def _execute_proactive_task(self, task: AutonomousTask) -> Dict[str, Any]:
        """Execute a proactive task"""
        
        insights = task.context.get("insights", {})
        
        # Simulate proactive action execution
        # In production, this would perform actual system actions
        
        result = {
            "action_type": "proactive_intelligence",
            "insights_processed": len(insights.get("structured_insights", {})),
            "recommendations_generated": len(insights.get("structured_insights", {}).get("recommendations", [])),
            "value_created": self._calculate_value_created(insights),
            "execution_time": (datetime.now() - task.started_at).total_seconds() if task.started_at else 0
        }
        
        return result
    
    def _calculate_value_created(self, insights: Dict[str, Any]) -> float:
        """Calculate value created by proactive action"""
        # Simplified value calculation
        base_value = 10.0
        
        # Increase based on insights quality
        confidence = insights.get("confidence_level", 0.5)
        priority = insights.get("priority_score", 5)
        
        value = base_value * confidence * (priority / 10)
        
        return round(value, 2)
    
    def _update_agent_learning(self, agent_id: str, context: Dict[str, Any], insights: Dict[str, Any]):
        """Update agent learning data"""
        
        agent = self.active_agents[agent_id]
        
        # Update learning data
        if "learning_data" not in agent:
            agent["learning_data"] = {}
        
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "context_analyzed": context,
            "insights_generated": insights,
            "success_indicators": self._calculate_success_indicators(insights)
        }
        
        # Store learning entry
        learning_key = f"learning_{int(time.time())}"
        agent["learning_data"][learning_key] = learning_entry
        
        # Limit learning data size
        if len(agent["learning_data"]) > 100:
            # Remove oldest entries
            oldest_keys = sorted(agent["learning_data"].keys())[:10]
            for key in oldest_keys:
                del agent["learning_data"][key]
    
    def _calculate_success_indicators(self, insights: Dict[str, Any]) -> Dict[str, float]:
        """Calculate success indicators for learning"""
        return {
            "insight_quality": insights.get("confidence_level", 0.5),
            "actionability": 0.8 if insights.get("actions_recommended") else 0.3,
            "strategic_value": insights.get("priority_score", 5) / 10,
            "trinity_alignment": 0.9  # Assuming good Trinity Foundation alignment
        }
    
    def _update_performance_metrics(self, agent_id: str, success: bool, execution_time: float):
        """Update agent performance metrics"""
        
        if agent_id not in self.performance_metrics:
            self.performance_metrics[agent_id] = AgentPerformanceMetrics(
                agent_id=agent_id,
                tasks_completed=0,
                success_rate=1.0,
                average_response_time=0.0,
                intelligence_score=0.8,
                learning_rate=0.1,
                proactive_actions=0,
                value_created=0.0,
                last_updated=datetime.now()
            )
        
        metrics = self.performance_metrics[agent_id]
        
        # Update metrics
        metrics.tasks_completed += 1
        metrics.proactive_actions += 1
        
        # Update success rate
        total_tasks = metrics.tasks_completed
        current_successes = metrics.success_rate * (total_tasks - 1)
        if success:
            current_successes += 1
        metrics.success_rate = current_successes / total_tasks
        
        # Update response time
        if metrics.average_response_time == 0:
            metrics.average_response_time = execution_time
        else:
            metrics.average_response_time = (metrics.average_response_time + execution_time) / 2
        
        # Update intelligence score based on performance
        if success:
            metrics.intelligence_score = min(1.0, metrics.intelligence_score + 0.01)
        else:
            metrics.intelligence_score = max(0.5, metrics.intelligence_score - 0.02)
        
        metrics.last_updated = datetime.now()
    
    def _start_background_processing(self):
        """Start background processing for autonomous agents"""
        
        if self.is_running:
            return
        
        self.is_running = True
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self._background_monitor, daemon=True)
        self.monitoring_thread.start()
        
        logger.info("Background processing started for autonomous agents")
    
    def _background_monitor(self):
        """Background monitoring loop"""
        
        while self.is_running:
            try:
                # Run scheduled tasks
                schedule.run_pending()
                
                # Process task queue
                self._process_task_queue()
                
                # Update system metrics
                self._update_system_metrics()
                
                # Sleep for a short interval
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in background monitoring: {e}")
                time.sleep(5)  # Wait longer on error
    
    def _process_task_queue(self):
        """Process pending tasks in the queue"""
        # This would process tasks from the async queue
        # For now, tasks are processed directly by the executor
        pass
    
    def _update_system_metrics(self):
        """Update overall system metrics"""
        # Update system-wide performance metrics
        pass
    
    def _calculate_system_load(self) -> float:
        """Calculate current system load"""
        # Simplified system load calculation
        active_tasks = sum(len(tasks) for tasks in self.agent_tasks.values())
        return min(1.0, active_tasks / 100)  # Normalize to 0-1
    
    def _get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        return {
            "agents_in_memory": len(self.active_agents),
            "tasks_in_memory": sum(len(tasks) for tasks in self.agent_tasks.values()),
            "learning_data_size": sum(len(agent.get("learning_data", {})) for agent in self.active_agents.values())
        }
    
    def _check_api_status(self) -> Dict[str, bool]:
        """Check API connectivity status"""
        return {
            "openai_api": bool(os.getenv('OPENAI_API_KEY')),
            "mem0_api": bool(os.getenv('MEM0_API_KEY')),
            "system_apis": True
        }
    
    def get_agent_status(self, agent_id: str = None) -> Dict[str, Any]:
        """Get status of agents"""
        
        if agent_id:
            agent = self.active_agents.get(agent_id)
            if not agent:
                return {"error": f"Agent {agent_id} not found"}
            
            return {
                "agent_id": agent_id,
                "status": agent["status"].value if hasattr(agent["status"], 'value') else str(agent["status"]),
                "last_activity": agent["last_activity"].isoformat(),
                "task_count": agent["task_count"],
                "performance_metrics": asdict(self.performance_metrics.get(agent_id, {}))
            }
        else:
            # Return all agents status
            return {
                "total_agents": len(self.active_agents),
                "active_agents": [
                    {
                        "agent_id": aid,
                        "name": agent["config"]["name"],
                        "status": agent["status"].value if hasattr(agent["status"], 'value') else str(agent["status"]),
                        "task_count": agent["task_count"]
                    }
                    for aid, agent in self.active_agents.items()
                ],
                "system_metrics": {
                    "total_tasks": sum(len(tasks) for tasks in self.agent_tasks.values()),
                    "system_load": self._calculate_system_load(),
                    "api_status": self._check_api_status()
                }
            }
    
    def stop_autonomous_processing(self):
        """Stop autonomous processing"""
        self.is_running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        logger.info("Autonomous processing stopped")

# Global instance
autonomous_activator = AutonomousAgentActivator()

def get_autonomous_activator():
    """Get the global autonomous activator instance"""
    return autonomous_activator

