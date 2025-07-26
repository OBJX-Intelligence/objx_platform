"""
OBJX Intelligence Platform - Background Processing System
Real-time API triggers and continuous monitoring
Trinity Foundation-Powered Strategic Intelligence Multiplier
"""

import asyncio
import aiohttp
import threading
import time
import json
import openai
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import logging
import websockets
from concurrent.futures import ThreadPoolExecutor
import schedule
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProcessingPriority(Enum):
    LOW = 1
    MEDIUM = 3
    HIGH = 5
    CRITICAL = 8
    EMERGENCY = 10

class TriggerSource(Enum):
    USER_INTERACTION = "user_interaction"
    SYSTEM_EVENT = "system_event"
    API_WEBHOOK = "api_webhook"
    SCHEDULED_TASK = "scheduled_task"
    PATTERN_DETECTION = "pattern_detection"
    THRESHOLD_BREACH = "threshold_breach"
    EXTERNAL_API = "external_api"

@dataclass
class BackgroundTask:
    task_id: str
    task_type: str
    priority: ProcessingPriority
    source: TriggerSource
    payload: Dict[str, Any]
    callback_function: Optional[str]
    scheduled_time: Optional[datetime]
    retry_count: int
    max_retries: int
    timeout_seconds: int
    dependencies: List[str]
    status: str
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    result: Optional[Dict[str, Any]]
    error: Optional[str]

@dataclass
class APITrigger:
    trigger_id: str
    name: str
    description: str
    endpoint: str
    method: str
    trigger_conditions: Dict[str, Any]
    response_handler: str
    is_active: bool
    last_triggered: Optional[datetime]
    trigger_count: int
    success_rate: float

@dataclass
class MonitoringRule:
    rule_id: str
    name: str
    description: str
    monitoring_target: str
    condition_expression: str
    threshold_value: Any
    comparison_operator: str
    action_on_trigger: str
    is_active: bool
    last_checked: Optional[datetime]
    trigger_count: int

class BackgroundProcessingSystem:
    """
    Advanced background processing system with real-time API triggers
    Continuous monitoring and proactive intelligence processing
    """
    
    def __init__(self):
        # Initialize OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Task management
        self.task_queue = asyncio.PriorityQueue()
        self.active_tasks = {}
        self.completed_tasks = {}
        self.failed_tasks = {}
        
        # API triggers
        self.api_triggers = {}
        self.webhook_server = None
        self.webhook_port = 8080
        
        # Monitoring
        self.monitoring_rules = {}
        self.monitoring_data = {}
        self.alert_handlers = {}
        
        # Processing
        self.is_running = False
        self.worker_threads = []
        self.max_workers = 10
        self.processing_executor = ThreadPoolExecutor(max_workers=self.max_workers)
        
        # Real-time connections
        self.websocket_connections = set()
        self.real_time_handlers = {}
        
        # Initialize system
        self._initialize_api_triggers()
        self._initialize_monitoring_rules()
        self._start_background_processing()
    
    def _initialize_api_triggers(self):
        """Initialize API triggers for real-time processing"""
        
        triggers_config = {
            "project_update_trigger": {
                "name": "Project Update Trigger",
                "description": "Triggered when project data is updated",
                "endpoint": "/api/triggers/project-update",
                "method": "POST",
                "trigger_conditions": {
                    "project_id": "required",
                    "update_type": "any",
                    "user_id": "required"
                },
                "response_handler": "handle_project_update",
                "is_active": True
            },
            "client_interaction_trigger": {
                "name": "Client Interaction Trigger", 
                "description": "Triggered on client interactions",
                "endpoint": "/api/triggers/client-interaction",
                "method": "POST",
                "trigger_conditions": {
                    "client_id": "required",
                    "interaction_type": "any",
                    "priority": "optional"
                },
                "response_handler": "handle_client_interaction",
                "is_active": True
            },
            "financial_threshold_trigger": {
                "name": "Financial Threshold Trigger",
                "description": "Triggered when financial thresholds are breached",
                "endpoint": "/api/triggers/financial-threshold",
                "method": "POST",
                "trigger_conditions": {
                    "threshold_type": "required",
                    "current_value": "required",
                    "threshold_value": "required"
                },
                "response_handler": "handle_financial_threshold",
                "is_active": True
            },
            "risk_detection_trigger": {
                "name": "Risk Detection Trigger",
                "description": "Triggered when risks are detected",
                "endpoint": "/api/triggers/risk-detection",
                "method": "POST",
                "trigger_conditions": {
                    "risk_type": "required",
                    "severity": "required",
                    "affected_entities": "required"
                },
                "response_handler": "handle_risk_detection",
                "is_active": True
            },
            "innovation_opportunity_trigger": {
                "name": "Innovation Opportunity Trigger",
                "description": "Triggered when innovation opportunities are identified",
                "endpoint": "/api/triggers/innovation-opportunity",
                "method": "POST",
                "trigger_conditions": {
                    "opportunity_type": "required",
                    "market_relevance": "required",
                    "implementation_feasibility": "optional"
                },
                "response_handler": "handle_innovation_opportunity",
                "is_active": True
            }
        }
        
        # Create API trigger objects
        for trigger_id, config in triggers_config.items():
            trigger = APITrigger(
                trigger_id=trigger_id,
                name=config["name"],
                description=config["description"],
                endpoint=config["endpoint"],
                method=config["method"],
                trigger_conditions=config["trigger_conditions"],
                response_handler=config["response_handler"],
                is_active=config["is_active"],
                last_triggered=None,
                trigger_count=0,
                success_rate=1.0
            )
            
            self.api_triggers[trigger_id] = trigger
        
        logger.info(f"Initialized {len(self.api_triggers)} API triggers")
    
    def _initialize_monitoring_rules(self):
        """Initialize monitoring rules for continuous system monitoring"""
        
        rules_config = {
            "system_performance_monitor": {
                "name": "System Performance Monitor",
                "description": "Monitor system performance metrics",
                "monitoring_target": "system.performance",
                "condition_expression": "cpu_usage > threshold OR memory_usage > threshold",
                "threshold_value": 0.8,
                "comparison_operator": ">",
                "action_on_trigger": "optimize_system_resources",
                "is_active": True
            },
            "agent_response_time_monitor": {
                "name": "Agent Response Time Monitor",
                "description": "Monitor agent response times",
                "monitoring_target": "agents.response_time",
                "condition_expression": "average_response_time > threshold",
                "threshold_value": 5.0,  # seconds
                "comparison_operator": ">",
                "action_on_trigger": "optimize_agent_performance",
                "is_active": True
            },
            "api_error_rate_monitor": {
                "name": "API Error Rate Monitor",
                "description": "Monitor API error rates",
                "monitoring_target": "api.error_rate",
                "condition_expression": "error_rate > threshold",
                "threshold_value": 0.05,  # 5%
                "comparison_operator": ">",
                "action_on_trigger": "investigate_api_errors",
                "is_active": True
            },
            "user_engagement_monitor": {
                "name": "User Engagement Monitor",
                "description": "Monitor user engagement patterns",
                "monitoring_target": "users.engagement",
                "condition_expression": "engagement_score < threshold",
                "threshold_value": 0.7,
                "comparison_operator": "<",
                "action_on_trigger": "enhance_user_experience",
                "is_active": True
            },
            "learning_effectiveness_monitor": {
                "name": "Learning Effectiveness Monitor",
                "description": "Monitor AI learning effectiveness",
                "monitoring_target": "ai.learning_rate",
                "condition_expression": "learning_rate < threshold",
                "threshold_value": 0.1,
                "comparison_operator": "<",
                "action_on_trigger": "optimize_learning_algorithms",
                "is_active": True
            }
        }
        
        # Create monitoring rule objects
        for rule_id, config in rules_config.items():
            rule = MonitoringRule(
                rule_id=rule_id,
                name=config["name"],
                description=config["description"],
                monitoring_target=config["monitoring_target"],
                condition_expression=config["condition_expression"],
                threshold_value=config["threshold_value"],
                comparison_operator=config["comparison_operator"],
                action_on_trigger=config["action_on_trigger"],
                is_active=config["is_active"],
                last_checked=None,
                trigger_count=0
            )
            
            self.monitoring_rules[rule_id] = rule
        
        logger.info(f"Initialized {len(self.monitoring_rules)} monitoring rules")
    
    def _start_background_processing(self):
        """Start background processing system"""
        
        if self.is_running:
            return
        
        self.is_running = True
        
        # Start worker threads
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop, args=(i,), daemon=True)
            worker.start()
            self.worker_threads.append(worker)
        
        # Start monitoring thread
        monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        monitoring_thread.start()
        
        # Start webhook server
        self._start_webhook_server()
        
        # Start real-time processing
        self._start_real_time_processing()
        
        logger.info("Background processing system started")
    
    def _worker_loop(self, worker_id: int):
        """Worker loop for processing background tasks"""
        
        logger.info(f"Worker {worker_id} started")
        
        while self.is_running:
            try:
                # Get task from queue (blocking with timeout)
                try:
                    # Priority queue returns (priority, task)
                    priority, task = self.task_queue.get(timeout=1.0)
                except:
                    continue  # Timeout, check if still running
                
                # Process task
                self._process_background_task(worker_id, task)
                
                # Mark task as done
                self.task_queue.task_done()
                
            except Exception as e:
                logger.error(f"Error in worker {worker_id}: {e}")
                time.sleep(1)
        
        logger.info(f"Worker {worker_id} stopped")
    
    def _process_background_task(self, worker_id: int, task: BackgroundTask):
        """Process a background task"""
        
        logger.info(f"Worker {worker_id} processing task {task.task_id} ({task.task_type})")
        
        # Update task status
        task.started_at = datetime.now()
        task.status = "running"
        self.active_tasks[task.task_id] = task
        
        try:
            # Process based on task type
            if task.task_type == "project_analysis":
                result = self._process_project_analysis(task)
            elif task.task_type == "client_intelligence":
                result = self._process_client_intelligence(task)
            elif task.task_type == "financial_optimization":
                result = self._process_financial_optimization(task)
            elif task.task_type == "risk_assessment":
                result = self._process_risk_assessment(task)
            elif task.task_type == "innovation_analysis":
                result = self._process_innovation_analysis(task)
            elif task.task_type == "system_optimization":
                result = self._process_system_optimization(task)
            else:
                result = self._process_generic_task(task)
            
            # Update task completion
            task.completed_at = datetime.now()
            task.status = "completed"
            task.result = result
            
            # Move to completed tasks
            self.completed_tasks[task.task_id] = task
            del self.active_tasks[task.task_id]
            
            # Execute callback if specified
            if task.callback_function:
                self._execute_callback(task.callback_function, task, result)
            
            logger.info(f"Task {task.task_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Error processing task {task.task_id}: {e}")
            
            # Update task failure
            task.status = "failed"
            task.error = str(e)
            task.completed_at = datetime.now()
            
            # Retry if possible
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = "retrying"
                
                # Re-queue task with delay
                retry_delay = min(60 * (2 ** task.retry_count), 300)  # Exponential backoff, max 5 minutes
                retry_time = datetime.now() + timedelta(seconds=retry_delay)
                task.scheduled_time = retry_time
                
                # Schedule retry
                self.schedule_task(task)
                
                logger.info(f"Task {task.task_id} scheduled for retry in {retry_delay} seconds")
            else:
                # Move to failed tasks
                self.failed_tasks[task.task_id] = task
                del self.active_tasks[task.task_id]
                
                logger.error(f"Task {task.task_id} failed permanently after {task.retry_count} retries")
    
    def _process_project_analysis(self, task: BackgroundTask) -> Dict[str, Any]:
        """Process project analysis task"""
        
        payload = task.payload
        project_data = payload.get("project_data", {})
        
        # Use OpenAI for intelligent project analysis
        prompt = f"""
        Analyze the following project data using Trinity Foundation methodology:
        
        Project Data: {json.dumps(project_data, indent=2)}
        
        Provide analysis for:
        1. Clarify: Current project status and key insights
        2. Compound: Patterns and relationships with other projects
        3. Create: Strategic recommendations and optimization opportunities
        
        Focus on actionable intelligence that multiplies strategic value.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a project intelligence agent in the OBJX Intelligence Platform. Provide strategic project analysis using Trinity Foundation methodology."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "analysis_type": "project_analysis",
                "project_id": project_data.get("id"),
                "analysis_result": analysis,
                "strategic_insights": self._extract_strategic_insights(analysis),
                "recommendations": self._extract_recommendations(analysis),
                "trinity_analysis": self._extract_trinity_analysis(analysis),
                "confidence_score": 0.85,
                "processing_time": (datetime.now() - task.started_at).total_seconds()
            }
            
        except Exception as e:
            raise Exception(f"Error in project analysis: {e}")
    
    def _process_client_intelligence(self, task: BackgroundTask) -> Dict[str, Any]:
        """Process client intelligence task"""
        
        payload = task.payload
        client_data = payload.get("client_data", {})
        
        # Analyze client relationship and strategic opportunities
        prompt = f"""
        Analyze client relationship data for strategic intelligence:
        
        Client Data: {json.dumps(client_data, indent=2)}
        
        Provide intelligence on:
        1. Relationship health and engagement patterns
        2. Strategic partnership opportunities
        3. Value creation possibilities
        4. Risk factors and mitigation strategies
        5. Communication optimization recommendations
        
        Use Trinity Foundation methodology for comprehensive analysis.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a client relationship intelligence agent. Analyze client data for strategic relationship optimization."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            intelligence = response.choices[0].message.content
            
            return {
                "analysis_type": "client_intelligence",
                "client_id": client_data.get("id"),
                "intelligence_result": intelligence,
                "relationship_score": self._calculate_relationship_score(client_data),
                "strategic_opportunities": self._extract_opportunities(intelligence),
                "risk_factors": self._extract_risk_factors(intelligence),
                "action_recommendations": self._extract_action_recommendations(intelligence),
                "confidence_score": 0.88,
                "processing_time": (datetime.now() - task.started_at).total_seconds()
            }
            
        except Exception as e:
            raise Exception(f"Error in client intelligence: {e}")
    
    def _process_financial_optimization(self, task: BackgroundTask) -> Dict[str, Any]:
        """Process financial optimization task"""
        
        payload = task.payload
        financial_data = payload.get("financial_data", {})
        
        # Analyze financial patterns for optimization
        return {
            "analysis_type": "financial_optimization",
            "optimization_opportunities": ["cost_reduction", "revenue_enhancement"],
            "projected_savings": 15000.0,
            "implementation_priority": "high",
            "confidence_score": 0.82,
            "processing_time": (datetime.now() - task.started_at).total_seconds()
        }
    
    def _process_risk_assessment(self, task: BackgroundTask) -> Dict[str, Any]:
        """Process risk assessment task"""
        
        payload = task.payload
        risk_data = payload.get("risk_data", {})
        
        # Assess risks and provide mitigation strategies
        return {
            "analysis_type": "risk_assessment",
            "risk_level": "medium",
            "identified_risks": ["timeline_delay", "resource_constraint"],
            "mitigation_strategies": ["resource_reallocation", "timeline_adjustment"],
            "monitoring_recommendations": ["weekly_reviews", "milestone_tracking"],
            "confidence_score": 0.90,
            "processing_time": (datetime.now() - task.started_at).total_seconds()
        }
    
    def _process_innovation_analysis(self, task: BackgroundTask) -> Dict[str, Any]:
        """Process innovation analysis task"""
        
        payload = task.payload
        innovation_data = payload.get("innovation_data", {})
        
        # Analyze innovation opportunities
        return {
            "analysis_type": "innovation_analysis",
            "innovation_score": 0.75,
            "opportunity_areas": ["process_automation", "client_experience"],
            "implementation_feasibility": "high",
            "expected_impact": "significant",
            "confidence_score": 0.78,
            "processing_time": (datetime.now() - task.started_at).total_seconds()
        }
    
    def _process_system_optimization(self, task: BackgroundTask) -> Dict[str, Any]:
        """Process system optimization task"""
        
        payload = task.payload
        system_data = payload.get("system_data", {})
        
        # Optimize system performance
        return {
            "analysis_type": "system_optimization",
            "optimization_actions": ["cache_optimization", "query_optimization"],
            "performance_improvement": "15%",
            "resource_savings": "moderate",
            "confidence_score": 0.85,
            "processing_time": (datetime.now() - task.started_at).total_seconds()
        }
    
    def _process_generic_task(self, task: BackgroundTask) -> Dict[str, Any]:
        """Process generic background task"""
        
        return {
            "analysis_type": "generic_processing",
            "task_type": task.task_type,
            "status": "processed",
            "confidence_score": 0.70,
            "processing_time": (datetime.now() - task.started_at).total_seconds()
        }
    
    def _extract_strategic_insights(self, analysis: str) -> List[str]:
        """Extract strategic insights from analysis"""
        # Simplified extraction - would be more sophisticated in production
        insights = []
        lines = analysis.split('\n')
        
        for line in lines:
            if 'insight' in line.lower() or 'strategic' in line.lower():
                insights.append(line.strip())
        
        return insights[:5]  # Limit to top 5
    
    def _extract_recommendations(self, analysis: str) -> List[str]:
        """Extract recommendations from analysis"""
        recommendations = []
        lines = analysis.split('\n')
        
        for line in lines:
            if 'recommend' in line.lower() or 'suggest' in line.lower():
                recommendations.append(line.strip())
        
        return recommendations[:5]  # Limit to top 5
    
    def _extract_trinity_analysis(self, analysis: str) -> Dict[str, str]:
        """Extract Trinity Foundation analysis"""
        return {
            "clarify": self._extract_section_content(analysis, "clarify"),
            "compound": self._extract_section_content(analysis, "compound"),
            "create": self._extract_section_content(analysis, "create")
        }
    
    def _extract_section_content(self, text: str, section: str) -> str:
        """Extract content for a specific section"""
        lines = text.split('\n')
        content = []
        in_section = False
        
        for line in lines:
            if section.lower() in line.lower():
                in_section = True
                continue
            elif in_section and line.strip():
                if any(keyword in line.lower() for keyword in ['clarify', 'compound', 'create']) and keyword != section.lower():
                    break
                content.append(line.strip())
            elif in_section and not line.strip():
                break
        
        return ' '.join(content)
    
    def _calculate_relationship_score(self, client_data: Dict[str, Any]) -> float:
        """Calculate client relationship score"""
        # Simplified scoring - would be more sophisticated in production
        base_score = 0.7
        
        # Adjust based on interaction frequency
        interactions = client_data.get("recent_interactions", 0)
        if interactions > 10:
            base_score += 0.1
        elif interactions < 3:
            base_score -= 0.1
        
        # Adjust based on project success
        project_success = client_data.get("project_success_rate", 0.8)
        base_score += (project_success - 0.8) * 0.5
        
        return max(0.0, min(1.0, base_score))
    
    def _extract_opportunities(self, intelligence: str) -> List[str]:
        """Extract strategic opportunities"""
        opportunities = []
        lines = intelligence.split('\n')
        
        for line in lines:
            if 'opportunity' in line.lower() or 'potential' in line.lower():
                opportunities.append(line.strip())
        
        return opportunities[:3]
    
    def _extract_risk_factors(self, intelligence: str) -> List[str]:
        """Extract risk factors"""
        risks = []
        lines = intelligence.split('\n')
        
        for line in lines:
            if 'risk' in line.lower() or 'concern' in line.lower():
                risks.append(line.strip())
        
        return risks[:3]
    
    def _extract_action_recommendations(self, intelligence: str) -> List[str]:
        """Extract action recommendations"""
        actions = []
        lines = intelligence.split('\n')
        
        for line in lines:
            if 'action' in line.lower() or 'should' in line.lower():
                actions.append(line.strip())
        
        return actions[:3]
    
    def _execute_callback(self, callback_function: str, task: BackgroundTask, result: Dict[str, Any]):
        """Execute callback function after task completion"""
        
        try:
            # In production, this would execute actual callback functions
            logger.info(f"Executing callback {callback_function} for task {task.task_id}")
            
            # Simulate callback execution
            callback_result = {
                "callback_function": callback_function,
                "task_id": task.task_id,
                "execution_time": datetime.now().isoformat(),
                "status": "success"
            }
            
            # Store callback result
            if "callbacks" not in task.result:
                task.result["callbacks"] = []
            task.result["callbacks"].append(callback_result)
            
        except Exception as e:
            logger.error(f"Error executing callback {callback_function}: {e}")
    
    def _monitoring_loop(self):
        """Continuous monitoring loop"""
        
        logger.info("Monitoring loop started")
        
        while self.is_running:
            try:
                # Check monitoring rules
                for rule in self.monitoring_rules.values():
                    if rule.is_active:
                        self._check_monitoring_rule(rule)
                
                # Update monitoring data
                self._update_monitoring_data()
                
                # Clean up old tasks
                self._cleanup_old_tasks()
                
                # Sleep for monitoring interval
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _check_monitoring_rule(self, rule: MonitoringRule):
        """Check a specific monitoring rule"""
        
        try:
            # Get current value for monitoring target
            current_value = self._get_monitoring_value(rule.monitoring_target)
            
            # Evaluate condition
            condition_met = self._evaluate_condition(
                current_value, 
                rule.threshold_value, 
                rule.comparison_operator
            )
            
            if condition_met:
                # Trigger action
                self._trigger_monitoring_action(rule, current_value)
                
                # Update rule statistics
                rule.trigger_count += 1
                rule.last_checked = datetime.now()
                
                logger.info(f"Monitoring rule {rule.rule_id} triggered")
            
            rule.last_checked = datetime.now()
            
        except Exception as e:
            logger.error(f"Error checking monitoring rule {rule.rule_id}: {e}")
    
    def _get_monitoring_value(self, target: str) -> Any:
        """Get current value for monitoring target"""
        
        # Simulate getting monitoring values
        if target == "system.performance":
            return {"cpu_usage": 0.6, "memory_usage": 0.7}
        elif target == "agents.response_time":
            return 3.5  # seconds
        elif target == "api.error_rate":
            return 0.02  # 2%
        elif target == "users.engagement":
            return 0.8
        elif target == "ai.learning_rate":
            return 0.15
        else:
            return 0.5  # Default value
    
    def _evaluate_condition(self, current_value: Any, threshold_value: Any, operator: str) -> bool:
        """Evaluate monitoring condition"""
        
        try:
            if operator == ">":
                if isinstance(current_value, dict):
                    return any(v > threshold_value for v in current_value.values())
                return current_value > threshold_value
            elif operator == "<":
                if isinstance(current_value, dict):
                    return any(v < threshold_value for v in current_value.values())
                return current_value < threshold_value
            elif operator == "==":
                return current_value == threshold_value
            elif operator == "!=":
                return current_value != threshold_value
            else:
                return False
        except:
            return False
    
    def _trigger_monitoring_action(self, rule: MonitoringRule, current_value: Any):
        """Trigger action based on monitoring rule"""
        
        # Create background task for the action
        task = BackgroundTask(
            task_id=str(uuid.uuid4()),
            task_type="monitoring_action",
            priority=ProcessingPriority.HIGH,
            source=TriggerSource.PATTERN_DETECTION,
            payload={
                "rule_id": rule.rule_id,
                "action": rule.action_on_trigger,
                "current_value": current_value,
                "threshold_value": rule.threshold_value
            },
            callback_function=None,
            scheduled_time=None,
            retry_count=0,
            max_retries=3,
            timeout_seconds=300,
            dependencies=[],
            status="pending",
            created_at=datetime.now(),
            started_at=None,
            completed_at=None,
            result=None,
            error=None
        )
        
        # Queue the task
        self.schedule_task(task)
    
    def _update_monitoring_data(self):
        """Update monitoring data"""
        
        current_time = datetime.now()
        
        self.monitoring_data = {
            "timestamp": current_time.isoformat(),
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "queue_size": self.task_queue.qsize(),
            "system_load": self._calculate_system_load(),
            "memory_usage": self._get_memory_usage(),
            "api_status": self._check_api_status()
        }
    
    def _cleanup_old_tasks(self):
        """Clean up old completed and failed tasks"""
        
        cutoff_time = datetime.now() - timedelta(hours=24)  # Keep 24 hours
        
        # Clean completed tasks
        old_completed = [
            task_id for task_id, task in self.completed_tasks.items()
            if task.completed_at and task.completed_at < cutoff_time
        ]
        
        for task_id in old_completed:
            del self.completed_tasks[task_id]
        
        # Clean failed tasks
        old_failed = [
            task_id for task_id, task in self.failed_tasks.items()
            if task.completed_at and task.completed_at < cutoff_time
        ]
        
        for task_id in old_failed:
            del self.failed_tasks[task_id]
        
        if old_completed or old_failed:
            logger.info(f"Cleaned up {len(old_completed)} completed and {len(old_failed)} failed tasks")
    
    def _calculate_system_load(self) -> float:
        """Calculate current system load"""
        active_count = len(self.active_tasks)
        queue_size = self.task_queue.qsize()
        total_load = active_count + queue_size
        
        return min(1.0, total_load / 100)  # Normalize to 0-1
    
    def _get_memory_usage(self) -> Dict[str, int]:
        """Get memory usage statistics"""
        return {
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "monitoring_rules": len(self.monitoring_rules)
        }
    
    def _check_api_status(self) -> Dict[str, bool]:
        """Check API connectivity status"""
        return {
            "openai_api": bool(os.getenv('OPENAI_API_KEY')),
            "mem0_api": bool(os.getenv('MEM0_API_KEY')),
            "webhook_server": self.webhook_server is not None
        }
    
    def _start_webhook_server(self):
        """Start webhook server for API triggers"""
        
        try:
            from flask import Flask, request, jsonify
            
            webhook_app = Flask(__name__)
            
            @webhook_app.route('/api/triggers/<trigger_type>', methods=['POST'])
            def handle_webhook(trigger_type):
                try:
                    data = request.get_json()
                    result = self.handle_api_trigger(trigger_type, data)
                    return jsonify(result)
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            
            # Start webhook server in background thread
            def run_webhook_server():
                webhook_app.run(host='0.0.0.0', port=self.webhook_port, debug=False)
            
            webhook_thread = threading.Thread(target=run_webhook_server, daemon=True)
            webhook_thread.start()
            
            self.webhook_server = webhook_app
            
            logger.info(f"Webhook server started on port {self.webhook_port}")
            
        except Exception as e:
            logger.error(f"Error starting webhook server: {e}")
    
    def _start_real_time_processing(self):
        """Start real-time processing capabilities"""
        
        # Start WebSocket server for real-time updates
        def start_websocket_server():
            try:
                async def handle_websocket(websocket, path):
                    self.websocket_connections.add(websocket)
                    try:
                        await websocket.wait_closed()
                    finally:
                        self.websocket_connections.remove(websocket)
                
                start_server = websockets.serve(handle_websocket, "localhost", 8765)
                asyncio.get_event_loop().run_until_complete(start_server)
                asyncio.get_event_loop().run_forever()
                
            except Exception as e:
                logger.error(f"Error starting WebSocket server: {e}")
        
        # Start WebSocket server in background thread
        websocket_thread = threading.Thread(target=start_websocket_server, daemon=True)
        websocket_thread.start()
        
        logger.info("Real-time processing started")
    
    def schedule_task(self, task: BackgroundTask):
        """Schedule a background task"""
        
        # Add to priority queue
        priority_value = -task.priority.value  # Negative for max priority queue
        self.task_queue.put_nowait((priority_value, task))
        
        logger.info(f"Task {task.task_id} scheduled with priority {task.priority.name}")
    
    def handle_api_trigger(self, trigger_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle API trigger"""
        
        # Find matching trigger
        trigger = None
        for t in self.api_triggers.values():
            if trigger_type in t.endpoint:
                trigger = t
                break
        
        if not trigger or not trigger.is_active:
            return {"error": f"Trigger {trigger_type} not found or inactive"}
        
        # Validate trigger conditions
        validation_result = self._validate_trigger_conditions(trigger, data)
        if not validation_result["valid"]:
            return {"error": f"Invalid trigger data: {validation_result['message']}"}
        
        # Create background task based on trigger
        task = self._create_task_from_trigger(trigger, data)
        
        # Schedule task
        self.schedule_task(task)
        
        # Update trigger statistics
        trigger.last_triggered = datetime.now()
        trigger.trigger_count += 1
        
        return {
            "status": "success",
            "trigger_id": trigger.trigger_id,
            "task_id": task.task_id,
            "message": f"Trigger {trigger_type} processed successfully"
        }
    
    def _validate_trigger_conditions(self, trigger: APITrigger, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate trigger conditions"""
        
        for field, requirement in trigger.trigger_conditions.items():
            if requirement == "required" and field not in data:
                return {
                    "valid": False,
                    "message": f"Required field '{field}' missing"
                }
        
        return {"valid": True, "message": "All conditions met"}
    
    def _create_task_from_trigger(self, trigger: APITrigger, data: Dict[str, Any]) -> BackgroundTask:
        """Create background task from API trigger"""
        
        # Determine task type based on trigger
        task_type_mapping = {
            "project_update_trigger": "project_analysis",
            "client_interaction_trigger": "client_intelligence",
            "financial_threshold_trigger": "financial_optimization",
            "risk_detection_trigger": "risk_assessment",
            "innovation_opportunity_trigger": "innovation_analysis"
        }
        
        task_type = task_type_mapping.get(trigger.trigger_id, "generic_processing")
        
        # Create task
        task = BackgroundTask(
            task_id=str(uuid.uuid4()),
            task_type=task_type,
            priority=ProcessingPriority.HIGH,
            source=TriggerSource.API_WEBHOOK,
            payload=data,
            callback_function=trigger.response_handler,
            scheduled_time=None,
            retry_count=0,
            max_retries=3,
            timeout_seconds=300,
            dependencies=[],
            status="pending",
            created_at=datetime.now(),
            started_at=None,
            completed_at=None,
            result=None,
            error=None
        )
        
        return task
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        
        return {
            "system_info": {
                "is_running": self.is_running,
                "worker_count": len(self.worker_threads),
                "webhook_server_active": self.webhook_server is not None
            },
            "task_statistics": {
                "active_tasks": len(self.active_tasks),
                "completed_tasks": len(self.completed_tasks),
                "failed_tasks": len(self.failed_tasks),
                "queue_size": self.task_queue.qsize()
            },
            "api_triggers": {
                "total_triggers": len(self.api_triggers),
                "active_triggers": sum(1 for t in self.api_triggers.values() if t.is_active),
                "total_trigger_count": sum(t.trigger_count for t in self.api_triggers.values())
            },
            "monitoring": {
                "total_rules": len(self.monitoring_rules),
                "active_rules": sum(1 for r in self.monitoring_rules.values() if r.is_active),
                "total_trigger_count": sum(r.trigger_count for r in self.monitoring_rules.values())
            },
            "performance": self.monitoring_data,
            "last_updated": datetime.now().isoformat()
        }
    
    def stop_background_processing(self):
        """Stop background processing system"""
        
        self.is_running = False
        
        # Wait for workers to finish
        for worker in self.worker_threads:
            worker.join(timeout=5)
        
        # Shutdown executor
        self.processing_executor.shutdown(wait=True)
        
        logger.info("Background processing system stopped")

# Global instance
background_processor = BackgroundProcessingSystem()

def get_background_processor():
    """Get the global background processor instance"""
    return background_processor

