#!/usr/bin/env python3
"""
OBJX Platform - Agent API
Implements API endpoints for agent orchestration
"""

from flask import request, jsonify
from agents import get_agent_manager

def initialize_agent_api(app, objx_platform=None):
    """Initialize agent API endpoints for the Flask app"""
    
    # Get agent manager
    agent_manager = get_agent_manager()
    
    @app.route('/api/agents/status', methods=['GET'])
    def api_agents_status():
        """Get status of all agents"""
        try:
            statuses = agent_manager.get_all_agent_statuses()
            
            return jsonify({
                "success": True,
                "agents": statuses
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/agents/status/<agent_id>', methods=['GET'])
    def api_agent_status(agent_id):
        """Get status of a specific agent"""
        try:
            status = agent_manager.get_agent_status(agent_id)
            
            if status is None:
                return jsonify({
                    "success": False,
                    "error": f"Agent with ID {agent_id} not found"
                }), 404
            
            return jsonify({
                "success": True,
                "agent": status
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/agents/task', methods=['POST'])
    def api_add_task():
        """Add a task to an agent's queue"""
        try:
            data = request.get_json()
            agent_id = data.get('agent_id')
            task = data.get('task')
            
            if not agent_id:
                return jsonify({
                    "success": False,
                    "error": "agent_id is required"
                }), 400
            
            if not task:
                return jsonify({
                    "success": False,
                    "error": "task is required"
                }), 400
            
            task_id = agent_manager.add_task(agent_id, task)
            
            if task_id is None:
                return jsonify({
                    "success": False,
                    "error": f"Agent with ID {agent_id} not found"
                }), 404
            
            return jsonify({
                "success": True,
                "task_id": task_id
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/agents/orchestrate', methods=['POST'])
    def api_orchestrate_agents():
        """Orchestrate multiple agents to complete a complex task"""
        try:
            data = request.get_json()
            task = data.get('task')
            
            if not task:
                return jsonify({
                    "success": False,
                    "error": "task is required"
                }), 400
            
            result = agent_manager.orchestrate_agents(task)
            
            return jsonify({
                "success": True,
                "result": result
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/analysis/run', methods=['POST'])
    def api_run_analysis():
        """Run an analysis task"""
        try:
            data = request.get_json()
            analysis_type = data.get('type', 'general')
            parameters = data.get('parameters', {})
            
            task = {
                "type": analysis_type,
                "description": f"Run {analysis_type} analysis",
                "parameters": parameters
            }
            
            task_id = agent_manager.add_task("analysis-agent", task)
            
            return jsonify({
                "success": True,
                "task_id": task_id,
                "message": f"{analysis_type.capitalize()} analysis task added to queue"
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/documents/generate', methods=['POST'])
    def api_generate_document():
        """Generate a document"""
        try:
            data = request.get_json()
            document_type = data.get('type', 'report')
            title = data.get('title', 'Generated Document')
            parameters = data.get('parameters', {})
            
            task = {
                "document_type": document_type,
                "title": title,
                "description": f"Generate {document_type}: {title}",
                "parameters": parameters
            }
            
            task_id = agent_manager.add_task("document-agent", task)
            
            return jsonify({
                "success": True,
                "task_id": task_id,
                "message": f"{document_type.capitalize()} generation task added to queue"
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/documents/templates', methods=['GET'])
    def api_document_templates():
        """Get available document templates"""
        try:
            # In a real implementation, this would fetch templates from a database
            templates = [
                {
                    "id": "business-proposal",
                    "name": "Business Proposal",
                    "description": "A comprehensive business proposal template",
                    "type": "proposal",
                    "sections": ["Executive Summary", "Problem Statement", "Proposed Solution", "Implementation Plan", "Budget and Timeline"]
                },
                {
                    "id": "market-analysis",
                    "name": "Market Analysis Report",
                    "description": "A detailed market analysis report template",
                    "type": "report",
                    "sections": ["Executive Summary", "Market Overview", "Competitive Landscape", "SWOT Analysis", "Market Trends", "Recommendations"]
                },
                {
                    "id": "project-presentation",
                    "name": "Project Presentation",
                    "description": "A professional project presentation template",
                    "type": "presentation",
                    "sections": ["Title Slide", "Agenda", "Introduction", "Key Points", "Data Visualization", "Conclusions", "Next Steps", "Q&A"]
                },
                {
                    "id": "code-review",
                    "name": "Code Review Report",
                    "description": "A technical code review report template",
                    "type": "report",
                    "sections": ["Executive Summary", "Code Quality Metrics", "Issues Found", "Best Practices", "Recommendations", "Appendix"]
                },
                {
                    "id": "risk-assessment",
                    "name": "Risk Assessment",
                    "description": "A comprehensive risk assessment template",
                    "type": "report",
                    "sections": ["Executive Summary", "Risk Identification", "Risk Analysis", "Risk Evaluation", "Risk Treatment", "Monitoring and Review"]
                }
            ]
            
            return jsonify({
                "success": True,
                "templates": templates
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/workflow/optimize', methods=['POST'])
    def api_optimize_workflow():
        """Optimize a workflow"""
        try:
            data = request.get_json()
            workflow_name = data.get('workflow_name', 'General Workflow')
            workflow_type = data.get('type', 'optimize')
            parameters = data.get('parameters', {})
            
            task = {
                "type": workflow_type,
                "workflow_name": workflow_name,
                "description": f"{workflow_type.capitalize()} workflow: {workflow_name}",
                "parameters": parameters
            }
            
            task_id = agent_manager.add_task("workflow-agent", task)
            
            return jsonify({
                "success": True,
                "task_id": task_id,
                "message": f"Workflow {workflow_type} task added to queue"
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/memory/search', methods=['POST'])
    def api_search_memory():
        """Search memory"""
        try:
            data = request.get_json()
            query = data.get('query', '')
            limit = data.get('limit', 10)
            
            task = {
                "type": "search",
                "query": query,
                "limit": limit,
                "description": f"Search memory for: {query}"
            }
            
            task_id = agent_manager.add_task("memory-agent", task)
            
            return jsonify({
                "success": True,
                "task_id": task_id,
                "message": "Memory search task added to queue"
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    return agent_manager

