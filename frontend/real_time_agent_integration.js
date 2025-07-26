/**
 * OBJX Intelligence Platform - Real-time Agent Integration
 * Connects frontend UI to autonomous agents running in backend
 */

class RealTimeAgentIntegration {
    constructor() {
        this.agentStatusEndpoint = '/api/agents/status';
        this.proactiveIntelligenceEndpoint = '/api/intelligence/proactive';
        this.backgroundStatusEndpoint = '/api/background/status';
        this.updateInterval = 5000; // 5 seconds
        this.agents = {};
        this.isConnected = false;
        
        this.init();
    }

    async init() {
        console.log('🚀 Initializing Real-time Agent Integration...');
        
        // Start real-time updates
        this.startRealTimeUpdates();
        
        // Initialize WebSocket connection if available
        this.initWebSocket();
        
        // Set up event listeners for interactive controls
        this.setupEventListeners();
        
        console.log('✅ Real-time Agent Integration initialized');
    }

    async startRealTimeUpdates() {
        // Initial load
        await this.updateAgentStatus();
        await this.updateProactiveIntelligence();
        await this.updateBackgroundStatus();
        
        // Set up periodic updates
        setInterval(async () => {
            await this.updateAgentStatus();
            await this.updateProactiveIntelligence();
        }, this.updateInterval);
        
        // More frequent background status updates
        setInterval(async () => {
            await this.updateBackgroundStatus();
        }, 2000);
    }

    async updateAgentStatus() {
        try {
            const response = await fetch(this.agentStatusEndpoint);
            
            if (response.ok) {
                const data = await response.json();
                this.agents = data;
                this.updateAgentUI(data);
                this.isConnected = true;
            } else {
                // Handle graceful degradation
                this.handleConnectionError();
            }
        } catch (error) {
            console.warn('Agent status update failed:', error);
            this.handleConnectionError();
        }
    }

    async updateProactiveIntelligence() {
        try {
            const response = await fetch(this.proactiveIntelligenceEndpoint + '?user_tier=admin');
            
            if (response.ok) {
                const data = await response.json();
                this.updateProactiveIntelligenceUI(data);
            }
        } catch (error) {
            console.warn('Proactive intelligence update failed:', error);
        }
    }

    async updateBackgroundStatus() {
        try {
            const response = await fetch(this.backgroundStatusEndpoint);
            
            if (response.ok) {
                const data = await response.json();
                this.updateBackgroundStatusUI(data);
            }
        } catch (error) {
            console.warn('Background status update failed:', error);
        }
    }

    updateAgentUI(agentData) {
        // Update agent status indicators
        const agentElements = document.querySelectorAll('[data-agent-id]');
        
        agentElements.forEach(element => {
            const agentId = element.getAttribute('data-agent-id');
            const agent = agentData.agents && agentData.agents[agentId];
            
            if (agent) {
                // Update status indicator
                const statusIndicator = element.querySelector('.agent-status');
                if (statusIndicator) {
                    statusIndicator.className = `agent-status ${agent.status}`;
                    statusIndicator.title = `${agent.name}: ${agent.status} - Last active: ${agent.last_active}`;
                }
                
                // Update activity description
                const activityElement = element.querySelector('.agent-activity');
                if (activityElement && agent.current_activity) {
                    activityElement.textContent = agent.current_activity;
                }
                
                // Update performance metrics
                const metricsElement = element.querySelector('.agent-metrics');
                if (metricsElement && agent.metrics) {
                    metricsElement.innerHTML = `
                        <span class="metric">Tasks: ${agent.metrics.tasks_completed}</span>
                        <span class="metric">Efficiency: ${agent.metrics.efficiency}%</span>
                    `;
                }
            }
        });
        
        // Update overall agent orchestration status
        this.updateOrchestrationStatus(agentData);
    }

    updateOrchestrationStatus(agentData) {
        const orchestrationElement = document.querySelector('.agent-orchestration-status');
        if (orchestrationElement && agentData.system_status) {
            const activeAgents = agentData.active_agents || 0;
            const totalAgents = agentData.total_agents || 7;
            
            orchestrationElement.innerHTML = `
                <div class="orchestration-summary">
                    <span class="active-count">${activeAgents}/${totalAgents}</span>
                    <span class="status-text">Agents Active</span>
                    <div class="status-indicator ${agentData.system_status}"></div>
                </div>
            `;
        }
    }

    updateProactiveIntelligenceUI(intelligenceData) {
        // Update proactive insights display
        const insightsContainer = document.querySelector('.proactive-insights');
        if (insightsContainer && intelligenceData.proactive_insights) {
            insightsContainer.innerHTML = intelligenceData.proactive_insights
                .map(insight => `<div class="insight-item">${insight}</div>`)
                .join('');
        }
        
        // Update strategic recommendations
        const recommendationsContainer = document.querySelector('.strategic-recommendations');
        if (recommendationsContainer && intelligenceData.strategic_recommendations) {
            recommendationsContainer.innerHTML = intelligenceData.strategic_recommendations
                .map(rec => `<div class="recommendation-item">${rec}</div>`)
                .join('');
        }
        
        // Update Trinity Foundation insights
        const trinityContainer = document.querySelector('.trinity-insights');
        if (trinityContainer && intelligenceData.trinity_insights) {
            const trinity = intelligenceData.trinity_insights;
            trinityContainer.innerHTML = `
                <div class="trinity-item clarify">
                    <span class="trinity-label">Clarify:</span>
                    <span class="trinity-content">${trinity.clarify}</span>
                </div>
                <div class="trinity-item compound">
                    <span class="trinity-label">Compound:</span>
                    <span class="trinity-content">${trinity.compound}</span>
                </div>
                <div class="trinity-item create">
                    <span class="trinity-label">Create:</span>
                    <span class="trinity-content">${trinity.create}</span>
                </div>
            `;
        }
    }

    updateBackgroundStatusUI(statusData) {
        // Update background processing indicators
        const processingElement = document.querySelector('.background-processing-status');
        if (processingElement && statusData) {
            const workersActive = statusData.workers_active || 0;
            const tasksProcessed = statusData.tasks_processed || 0;
            
            processingElement.innerHTML = `
                <div class="processing-summary">
                    <span class="workers-count">${workersActive} Workers</span>
                    <span class="tasks-count">${tasksProcessed} Tasks Processed</span>
                    <div class="processing-indicator active"></div>
                </div>
            `;
        }
    }

    setupEventListeners() {
        // Orchestrate button
        const orchestrateBtn = document.querySelector('[data-action="orchestrate"]');
        if (orchestrateBtn) {
            orchestrateBtn.addEventListener('click', () => this.triggerOrchestration());
        }
        
        // New Project button
        const newProjectBtn = document.querySelector('[data-action="new-project"]');
        if (newProjectBtn) {
            newProjectBtn.addEventListener('click', () => this.createNewProject());
        }
        
        // Agent control buttons
        document.querySelectorAll('[data-agent-action]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.getAttribute('data-agent-action');
                const agentId = e.target.getAttribute('data-agent-id');
                this.handleAgentAction(action, agentId);
            });
        });
    }

    async triggerOrchestration() {
        try {
            const response = await fetch('/api/triggers/project-update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: 'orchestrate',
                    timestamp: new Date().toISOString(),
                    user: 'admin'
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                this.showNotification('Orchestration triggered successfully', 'success');
                
                // Force immediate update
                setTimeout(() => this.updateAgentStatus(), 1000);
            } else {
                this.showNotification('Orchestration failed', 'error');
            }
        } catch (error) {
            console.error('Orchestration error:', error);
            this.showNotification('Orchestration error', 'error');
        }
    }

    async createNewProject() {
        // This would open a modal or navigate to project creation
        this.showNotification('New Project creation initiated', 'info');
        
        // Trigger project creation workflow
        try {
            const response = await fetch('/api/triggers/project-update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: 'new_project',
                    timestamp: new Date().toISOString(),
                    user: 'admin'
                })
            });
            
            if (response.ok) {
                // Navigate to project creation or open modal
                window.location.href = '/project-detail.html?action=create';
            }
        } catch (error) {
            console.error('New project error:', error);
        }
    }

    async handleAgentAction(action, agentId) {
        try {
            const response = await fetch(`/api/agents/${agentId}/${action}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                this.showNotification(`Agent ${action} successful`, 'success');
                setTimeout(() => this.updateAgentStatus(), 1000);
            }
        } catch (error) {
            console.error(`Agent ${action} error:`, error);
        }
    }

    initWebSocket() {
        // Initialize WebSocket for real-time updates if available
        try {
            const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${wsProtocol}//${window.location.host}/ws/agents`;
            
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.onopen = () => {
                console.log('✅ WebSocket connected for real-time updates');
            };
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
            };
            
            this.websocket.onerror = () => {
                console.log('⚠️ WebSocket not available, using polling');
            };
        } catch (error) {
            console.log('⚠️ WebSocket not available, using polling');
        }
    }

    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'agent_status':
                this.updateAgentUI(data.payload);
                break;
            case 'proactive_intelligence':
                this.updateProactiveIntelligenceUI(data.payload);
                break;
            case 'notification':
                this.showNotification(data.message, data.level);
                break;
        }
    }

    handleConnectionError() {
        this.isConnected = false;
        
        // Show graceful degradation
        const statusElements = document.querySelectorAll('.agent-status');
        statusElements.forEach(el => {
            el.className = 'agent-status connecting';
            el.title = 'Connecting to autonomous agents...';
        });
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.agentIntegration = new RealTimeAgentIntegration();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RealTimeAgentIntegration;
}

