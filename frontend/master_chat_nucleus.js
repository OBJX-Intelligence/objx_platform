/**
 * MASTER CHAT NUCLEUS
 * Single intelligent chat connector for all frontend-to-backend communication
 * Handles: Mem0 integration, 5-tier permissions, agent orchestration, Trinity Foundation
 * 
 * This is the ONLY chat system - all others are deprecated
 */

class MasterChatNucleus {
    constructor() {
        this.isInitialized = false;
        this.isOpen = false;
        this.currentTier = this.detectUserTier();
        this.currentPage = this.detectCurrentPage();
        this.permissions = this.getTierPermissions();
        this.agentCapabilities = this.getAgentCapabilities();
        this.memoryContext = [];
        this.sessionId = this.generateSessionId();
        
        console.log(`🧠 Master Chat Nucleus initializing for ${this.currentTier} on ${this.currentPage}`);
        this.init();
    }

    // TIER DETECTION & PERMISSIONS
    detectUserTier() {
        const url = window.location.pathname;
        if (url.includes('admin')) return 'admin';
        if (url.includes('staff')) return 'staff';
        if (url.includes('tier3')) return 'tier3';
        if (url.includes('tier2')) return 'tier2';
        if (url.includes('tier1')) return 'tier1';
        
        // Default based on page complexity
        if (url.includes('dashboard_admin')) return 'admin';
        return 'tier1';
    }

    detectCurrentPage() {
        const url = window.location.pathname;
        const page = url.split('/').pop().replace('.html', '') || 'index';
        return page;
    }

    getTierPermissions() {
        const permissions = {
            tier1: {
                chat: true,
                memory: false,
                agents: [],
                context: ['basic'],
                features: ['systematic_thinking', 'basic_analysis'],
                maxTokens: 500,
                priority: 'low'
            },
            tier2: {
                chat: true,
                memory: true,
                agents: ['project_manager'],
                context: ['basic', 'project_data'],
                features: ['systematic_thinking', 'basic_analysis', 'project_context', 'memory_search'],
                maxTokens: 1000,
                priority: 'medium'
            },
            tier3: {
                chat: true,
                memory: true,
                agents: ['project_manager', 'task_coordinator', 'deadline_monitor'],
                context: ['basic', 'project_data', 'dashboard_metrics'],
                features: ['systematic_thinking', 'advanced_analysis', 'project_context', 'memory_search', 'document_generation'],
                maxTokens: 1500,
                priority: 'high'
            },
            staff: {
                chat: true,
                memory: true,
                agents: ['project_manager', 'task_coordinator', 'deadline_monitor', 'client_communicator', 'billing_manager'],
                context: ['basic', 'project_data', 'dashboard_metrics', 'team_data'],
                features: ['systematic_thinking', 'advanced_analysis', 'project_context', 'memory_search', 'document_generation', 'team_coordination'],
                maxTokens: 2000,
                priority: 'high'
            },
            admin: {
                chat: true,
                memory: true,
                agents: ['project_manager', 'task_coordinator', 'deadline_monitor', 'client_communicator', 'billing_manager', 'resource_optimizer', 'quality_assurance'],
                context: ['basic', 'project_data', 'dashboard_metrics', 'team_data', 'system_admin'],
                features: ['systematic_thinking', 'advanced_analysis', 'project_context', 'memory_search', 'document_generation', 'team_coordination', 'system_admin', 'agent_orchestration'],
                maxTokens: 3000,
                priority: 'critical'
            }
        };
        
        return permissions[this.currentTier] || permissions.tier1;
    }

    getAgentCapabilities() {
        const allAgents = {
            project_manager: {
                name: 'Project Manager',
                capabilities: ['project_tracking', 'deadline_management', 'resource_allocation'],
                active: this.permissions.agents.includes('project_manager')
            },
            task_coordinator: {
                name: 'Task Coordinator',
                capabilities: ['workflow_optimization', 'task_prioritization', 'team_coordination'],
                active: this.permissions.agents.includes('task_coordinator')
            },
            deadline_monitor: {
                name: 'Deadline Monitor',
                capabilities: ['timeline_tracking', 'risk_assessment', 'alert_management'],
                active: this.permissions.agents.includes('deadline_monitor')
            },
            client_communicator: {
                name: 'Client Communicator',
                capabilities: ['client_updates', 'communication_drafting', 'relationship_management'],
                active: this.permissions.agents.includes('client_communicator')
            },
            billing_manager: {
                name: 'Billing Manager',
                capabilities: ['invoice_processing', 'financial_tracking', 'payment_monitoring'],
                active: this.permissions.agents.includes('billing_manager')
            },
            resource_optimizer: {
                name: 'Resource Optimizer',
                capabilities: ['capacity_analysis', 'resource_planning', 'efficiency_optimization'],
                active: this.permissions.agents.includes('resource_optimizer')
            },
            quality_assurance: {
                name: 'Quality Assurance',
                capabilities: ['deliverable_review', 'quality_metrics', 'process_improvement'],
                active: this.permissions.agents.includes('quality_assurance')
            }
        };

        return allAgents;
    }

    generateSessionId() {
        return `chat_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    // INITIALIZATION
    init() {
        this.createChatInterface();
        this.attachEventListeners();
        this.loadMemoryContext();
        this.initializeAgents();
        this.isInitialized = true;
        console.log(`✅ Master Chat Nucleus ready - ${Object.keys(this.agentCapabilities).filter(k => this.agentCapabilities[k].active).length} agents active`);
    }

    createChatInterface() {
        // Remove any existing chat interfaces first
        this.removeExistingChats();
        
        const chatHTML = `
            <div id="master-chat-nucleus" class="chat-nucleus">
                <!-- Chat Toggle Button -->
                <button id="chat-toggle" class="chat-toggle" aria-label="Open OBJX Intelligence">
                    <div class="chat-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                        </svg>
                    </div>
                    <div class="tier-indicator">${this.currentTier.toUpperCase()}</div>
                    <div class="agent-count">${Object.keys(this.agentCapabilities).filter(k => this.agentCapabilities[k].active).length}</div>
                </button>

                <!-- Chat Window -->
                <div id="chat-window" class="chat-window">
                    <!-- Header -->
                    <div class="chat-header">
                        <div class="header-content">
                            <div class="title-section">
                                <h3 class="chat-title">OBJX Intelligence</h3>
                                <p class="chat-subtitle">Strategic Intelligence Multiplier</p>
                            </div>
                            <div class="status-section">
                                <div class="tier-badge">${this.currentTier.toUpperCase()}</div>
                                <div class="memory-status ${this.permissions.memory ? 'active' : 'inactive'}">
                                    ${this.permissions.memory ? 'MEM0 ACTIVE' : 'SESSION ONLY'}
                                </div>
                            </div>
                        </div>
                        <button id="chat-close" class="chat-close">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    </div>

                    <!-- Active Agents Display -->
                    ${this.renderActiveAgents()}

                    <!-- Messages Container -->
                    <div id="chat-messages" class="chat-messages">
                        ${this.renderWelcomeMessage()}
                    </div>

                    <!-- Feature Tags -->
                    <div class="feature-tags">
                        ${this.renderFeatureTags()}
                    </div>

                    <!-- Input Section -->
                    <div class="chat-input-section">
                        <div class="input-wrapper">
                            <textarea 
                                id="chat-input" 
                                placeholder="Share your thoughts, challenges, or opportunities..."
                                rows="1"
                            ></textarea>
                            <button id="chat-send" class="send-button" disabled>
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <line x1="22" y1="2" x2="11" y2="13"></line>
                                    <polygon points="22,2 15,22 11,13 2,9"></polygon>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Inject CSS
        this.injectCSS();
        
        // Add to page
        document.body.insertAdjacentHTML('beforeend', chatHTML);
    }

    removeExistingChats() {
        // Remove any existing chat interfaces to prevent conflicts
        const existingChats = document.querySelectorAll('[id*="chat"], .chat-container, .chat-nucleus');
        existingChats.forEach(chat => chat.remove());
    }

    renderActiveAgents() {
        const activeAgents = Object.entries(this.agentCapabilities)
            .filter(([key, agent]) => agent.active)
            .map(([key, agent]) => agent.name);

        if (activeAgents.length === 0) return '';

        return `
            <div class="active-agents">
                <div class="agents-label">Active Agents:</div>
                <div class="agents-list">
                    ${activeAgents.map(name => `<span class="agent-tag">${name}</span>`).join('')}
                </div>
            </div>
        `;
    }

    renderWelcomeMessage() {
        const capabilities = this.permissions.features.join(', ');
        const agentCount = Object.keys(this.agentCapabilities).filter(k => this.agentCapabilities[k].active).length;
        
        return `
            <div class="message assistant welcome">
                <div class="message-content">
                    <div class="avatar">AI</div>
                    <div class="bubble">
                        <div class="text">
                            Welcome to OBJX Intelligence! I'm your Strategic Intelligence Partner, enhanced with the Trinity Foundation methodology.
                            <br><br>
                            <strong>Your Access Level:</strong> ${this.currentTier.toUpperCase()}<br>
                            <strong>Active Agents:</strong> ${agentCount}<br>
                            <strong>Memory System:</strong> ${this.permissions.memory ? 'Compound Learning Active' : 'Session-Based'}<br>
                            <br>
                            How can I help you think through your current challenge or opportunity?
                        </div>
                        <div class="time">Now</div>
                    </div>
                </div>
            </div>
        `;
    }

    renderFeatureTags() {
        return this.permissions.features
            .map(feature => `<span class="feature-tag">${this.formatFeatureName(feature)}</span>`)
            .join('');
    }

    formatFeatureName(feature) {
        return feature.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }

    // EVENT HANDLING
    attachEventListeners() {
        const toggleBtn = document.getElementById('chat-toggle');
        const closeBtn = document.getElementById('chat-close');
        const sendBtn = document.getElementById('chat-send');
        const input = document.getElementById('chat-input');

        toggleBtn.addEventListener('click', () => this.toggleChat());
        closeBtn.addEventListener('click', () => this.closeChat());
        sendBtn.addEventListener('click', () => this.sendMessage());
        
        input.addEventListener('input', (e) => this.handleInputChange(e));
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        input.addEventListener('input', () => this.autoResizeTextarea(input));
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const chatWindow = document.getElementById('chat-window');
        
        if (this.isOpen) {
            chatWindow.classList.add('active');
            document.getElementById('chat-input').focus();
        } else {
            chatWindow.classList.remove('active');
        }
    }

    closeChat() {
        this.isOpen = false;
        document.getElementById('chat-window').classList.remove('active');
    }

    handleInputChange(e) {
        const sendBtn = document.getElementById('chat-send');
        sendBtn.disabled = e.target.value.trim().length === 0;
    }

    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    // CORE MESSAGING SYSTEM
    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;

        // Add user message
        this.addMessage(message, 'user');
        input.value = '';
        input.style.height = 'auto';
        document.getElementById('chat-send').disabled = true;

        // Show thinking indicator
        this.showThinkingIndicator();

        try {
            // Gather comprehensive context
            const context = await this.gatherIntelligentContext(message);
            
            // Send to master API endpoint
            const response = await fetch('/api/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    context: context,
                    tier: this.currentTier,
                    permissions: this.permissions,
                    agents: this.agentCapabilities,
                    sessionId: this.sessionId,
                    memoryEnabled: this.permissions.memory,
                    page: this.currentPage
                })
            });

            const data = await response.json();
            
            this.removeThinkingIndicator();
            
            if (data.success) {
                this.addMessage(data.message, 'assistant');
                
                // Update memory context if available
                if (data.memoryUpdated && this.permissions.memory) {
                    this.updateMemoryContext(data.memoryContext);
                }
                
                // Handle agent actions if any
                if (data.agentActions) {
                    this.processAgentActions(data.agentActions);
                }
            } else {
                this.addMessage('I\'m having trouble connecting right now. Please try again.', 'assistant', true);
            }
            
        } catch (error) {
            console.error('Master Chat Nucleus error:', error);
            this.removeThinkingIndicator();
            this.addMessage('I\'m experiencing a connection issue. Please try again.', 'assistant', true);
        }
    }

    async gatherIntelligentContext(message) {
        const context = {
            tier: this.currentTier,
            page: this.currentPage,
            permissions: this.permissions,
            activeAgents: Object.keys(this.agentCapabilities).filter(k => this.agentCapabilities[k].active),
            timestamp: new Date().toISOString(),
            sessionId: this.sessionId,
            messageIntent: this.analyzeMessageIntent(message)
        };

        // Add context based on permissions
        if (this.permissions.context.includes('project_data')) {
            context.projects = this.extractProjectData();
        }
        
        if (this.permissions.context.includes('dashboard_metrics')) {
            context.dashboard = this.extractDashboardMetrics();
        }
        
        if (this.permissions.context.includes('team_data')) {
            context.team = this.extractTeamData();
        }
        
        if (this.permissions.context.includes('system_admin')) {
            context.system = this.extractSystemMetrics();
        }

        // Add memory context if enabled
        if (this.permissions.memory && this.memoryContext.length > 0) {
            context.memory = this.memoryContext.slice(-5); // Last 5 memory items
        }

        return context;
    }

    analyzeMessageIntent(message) {
        const intents = {
            question: message.includes('?'),
            project_related: /project|task|deadline|client/i.test(message),
            financial: /budget|cost|invoice|billing|revenue/i.test(message),
            strategic: /strategy|plan|goal|objective|vision/i.test(message),
            urgent: /urgent|asap|immediately|critical/i.test(message),
            agent_request: /agent|automate|schedule|monitor/i.test(message)
        };
        
        return Object.entries(intents)
            .filter(([key, value]) => value)
            .map(([key]) => key);
    }

    extractProjectData() {
        try {
            const projectElements = document.querySelectorAll('[data-project-id], .project-item, .project-card');
            return Array.from(projectElements).map(el => ({
                id: el.dataset.projectId || 'unknown',
                name: el.dataset.projectName || el.textContent?.trim().substring(0, 50) || 'Unknown Project',
                status: el.dataset.projectStatus || 'Active'
            })).slice(0, 10); // Limit to 10 projects
        } catch (error) {
            return [];
        }
    }

    extractDashboardMetrics() {
        try {
            return {
                revenue: this.extractMetric('[data-revenue]', 'revenue'),
                projects: this.extractMetric('[data-project-count]', 'projects'),
                team: this.extractMetric('[data-team-performance]', 'team'),
                clients: this.extractMetric('[data-client-count]', 'clients')
            };
        } catch (error) {
            return {};
        }
    }

    extractMetric(selector, fallback) {
        const element = document.querySelector(selector);
        return element?.textContent?.trim() || `No ${fallback} data available`;
    }

    extractTeamData() {
        return {
            utilization: '87%',
            activeMembers: 5,
            currentCapacity: 'High'
        };
    }

    extractSystemMetrics() {
        return {
            agentsActive: Object.keys(this.agentCapabilities).filter(k => this.agentCapabilities[k].active).length,
            systemHealth: 'Optimal',
            memoryStatus: this.permissions.memory ? 'Active' : 'Disabled'
        };
    }

    // MESSAGE DISPLAY
    addMessage(text, sender, isError = false) {
        const messagesContainer = document.getElementById('chat-messages');
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        const messageHTML = `
            <div class="message ${sender} ${isError ? 'error' : ''}">
                <div class="message-content">
                    ${sender === 'assistant' ? '<div class="avatar">AI</div>' : ''}
                    <div class="bubble">
                        <div class="text">${text}</div>
                        <div class="time">${time}</div>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    showThinkingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        const thinkingHTML = `
            <div id="thinking-indicator" class="message assistant thinking">
                <div class="message-content">
                    <div class="avatar">AI</div>
                    <div class="bubble">
                        <div class="thinking-animation">
                            <span></span><span></span><span></span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', thinkingHTML);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    removeThinkingIndicator() {
        const indicator = document.getElementById('thinking-indicator');
        if (indicator) indicator.remove();
    }

    // MEMORY & AGENT MANAGEMENT
    updateMemoryContext(newContext) {
        if (Array.isArray(newContext)) {
            this.memoryContext = [...this.memoryContext, ...newContext].slice(-20); // Keep last 20
        }
    }

    processAgentActions(actions) {
        actions.forEach(action => {
            console.log(`🤖 Agent Action: ${action.agent} - ${action.action}`);
            // Handle agent-specific actions here
        });
    }

    loadMemoryContext() {
        if (this.permissions.memory) {
            // Load existing memory context from session storage
            const stored = sessionStorage.getItem(`memory_${this.sessionId}`);
            if (stored) {
                this.memoryContext = JSON.parse(stored);
            }
        }
    }

    initializeAgents() {
        const activeAgents = Object.entries(this.agentCapabilities)
            .filter(([key, agent]) => agent.active);
        
        console.log(`🚀 Initializing ${activeAgents.length} agents:`, activeAgents.map(([k, a]) => a.name));
    }

    // CSS INJECTION
    injectCSS() {
        const css = `
            <style>
                .chat-nucleus {
                    position: fixed;
                    bottom: 24px;
                    right: 24px;
                    z-index: 10000;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                }

                .chat-toggle {
                    width: 72px;
                    height: 72px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
                    border: none;
                    cursor: pointer;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 8px 32px rgba(139, 92, 246, 0.4);
                    transition: all 0.3s ease;
                    color: white;
                    position: relative;
                    overflow: hidden;
                }

                .chat-toggle::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 50%);
                    border-radius: 50%;
                }

                .chat-toggle:hover {
                    transform: scale(1.05);
                    box-shadow: 0 12px 40px rgba(139, 92, 246, 0.5);
                }

                .chat-icon {
                    position: relative;
                    z-index: 1;
                }

                .tier-indicator {
                    position: absolute;
                    top: 4px;
                    right: 4px;
                    background: rgba(255,255,255,0.9);
                    color: #7C3AED;
                    font-size: 8px;
                    font-weight: 700;
                    padding: 2px 4px;
                    border-radius: 6px;
                    line-height: 1;
                }

                .agent-count {
                    position: absolute;
                    bottom: 4px;
                    left: 4px;
                    background: #10B981;
                    color: white;
                    font-size: 10px;
                    font-weight: 600;
                    width: 16px;
                    height: 16px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    line-height: 1;
                }

                .chat-window {
                    position: absolute;
                    bottom: 88px;
                    right: 0;
                    width: 420px;
                    height: 650px;
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.15);
                    display: none;
                    flex-direction: column;
                    transform: translateY(20px) scale(0.95);
                    opacity: 0;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    overflow: hidden;
                    border: 1px solid rgba(139, 92, 246, 0.1);
                }

                .chat-window.active {
                    display: flex;
                    transform: translateY(0) scale(1);
                    opacity: 1;
                }

                .chat-header {
                    padding: 20px 24px;
                    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
                    color: white;
                    position: relative;
                }

                .header-content {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                }

                .chat-title {
                    font-size: 20px;
                    font-weight: 700;
                    margin: 0 0 4px 0;
                    letter-spacing: -0.5px;
                }

                .chat-subtitle {
                    font-size: 14px;
                    opacity: 0.9;
                    margin: 0;
                    font-weight: 400;
                }

                .status-section {
                    display: flex;
                    flex-direction: column;
                    align-items: flex-end;
                    gap: 4px;
                }

                .tier-badge {
                    background: rgba(255,255,255,0.2);
                    padding: 4px 8px;
                    border-radius: 8px;
                    font-size: 10px;
                    font-weight: 700;
                    letter-spacing: 0.5px;
                }

                .memory-status {
                    font-size: 9px;
                    padding: 2px 6px;
                    border-radius: 6px;
                    font-weight: 600;
                    letter-spacing: 0.3px;
                }

                .memory-status.active {
                    background: rgba(16, 185, 129, 0.2);
                    color: #10B981;
                }

                .memory-status.inactive {
                    background: rgba(255,255,255,0.1);
                    color: rgba(255,255,255,0.7);
                }

                .chat-close {
                    position: absolute;
                    top: 16px;
                    right: 20px;
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                    padding: 6px;
                    border-radius: 6px;
                    opacity: 0.8;
                    transition: all 0.2s;
                }

                .chat-close:hover {
                    opacity: 1;
                    background: rgba(255,255,255,0.1);
                }

                .active-agents {
                    padding: 12px 20px;
                    background: #f8fafc;
                    border-bottom: 1px solid #e2e8f0;
                }

                .agents-label {
                    font-size: 11px;
                    font-weight: 600;
                    color: #64748b;
                    margin-bottom: 6px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }

                .agents-list {
                    display: flex;
                    gap: 6px;
                    flex-wrap: wrap;
                }

                .agent-tag {
                    background: linear-gradient(135deg, #8B5CF6, #7C3AED);
                    color: white;
                    padding: 3px 8px;
                    border-radius: 8px;
                    font-size: 10px;
                    font-weight: 600;
                    letter-spacing: 0.3px;
                }

                .chat-messages {
                    flex: 1;
                    padding: 20px;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column;
                    gap: 16px;
                    background: #fafbfc;
                }

                .chat-messages::-webkit-scrollbar {
                    width: 4px;
                }

                .chat-messages::-webkit-scrollbar-track {
                    background: transparent;
                }

                .chat-messages::-webkit-scrollbar-thumb {
                    background: rgba(139, 92, 246, 0.3);
                    border-radius: 2px;
                }

                .message {
                    display: flex;
                    max-width: 85%;
                    animation: messageSlide 0.3s ease-out;
                }

                @keyframes messageSlide {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }

                .message.user {
                    align-self: flex-end;
                }

                .message.assistant {
                    align-self: flex-start;
                }

                .message-content {
                    display: flex;
                    gap: 10px;
                    align-items: flex-end;
                    width: 100%;
                }

                .avatar {
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #8B5CF6, #7C3AED);
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    font-weight: 700;
                    flex-shrink: 0;
                }

                .bubble {
                    background: white;
                    padding: 12px 16px;
                    border-radius: 16px;
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
                    border: 1px solid rgba(0, 0, 0, 0.05);
                    flex: 1;
                }

                .message.user .bubble {
                    background: linear-gradient(135deg, #8B5CF6, #7C3AED);
                    color: white;
                    border: none;
                }

                .text {
                    font-size: 14px;
                    line-height: 1.5;
                    margin-bottom: 6px;
                }

                .time {
                    font-size: 11px;
                    opacity: 0.6;
                    font-weight: 500;
                }

                .feature-tags {
                    padding: 12px 20px;
                    background: white;
                    border-top: 1px solid #e2e8f0;
                    display: flex;
                    gap: 6px;
                    flex-wrap: wrap;
                }

                .feature-tag {
                    background: #f1f5f9;
                    color: #475569;
                    padding: 4px 8px;
                    border-radius: 8px;
                    font-size: 11px;
                    font-weight: 500;
                    letter-spacing: 0.2px;
                }

                .chat-input-section {
                    background: white;
                    border-top: 1px solid #e2e8f0;
                    padding: 16px 20px;
                }

                .input-wrapper {
                    display: flex;
                    gap: 12px;
                    align-items: flex-end;
                }

                #chat-input {
                    flex: 1;
                    border: 2px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 12px 16px;
                    font-size: 14px;
                    resize: none;
                    outline: none;
                    font-family: inherit;
                    min-height: 44px;
                    max-height: 120px;
                    transition: border-color 0.2s;
                }

                #chat-input:focus {
                    border-color: #8B5CF6;
                    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
                }

                .send-button {
                    width: 44px;
                    height: 44px;
                    border-radius: 12px;
                    background: linear-gradient(135deg, #8B5CF6, #7C3AED);
                    border: none;
                    color: white;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.2s;
                    flex-shrink: 0;
                }

                .send-button:disabled {
                    opacity: 0.5;
                    cursor: not-allowed;
                }

                .send-button:not(:disabled):hover {
                    transform: scale(1.05);
                    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
                }

                .thinking-animation {
                    display: flex;
                    gap: 4px;
                    align-items: center;
                    padding: 8px 0;
                }

                .thinking-animation span {
                    width: 6px;
                    height: 6px;
                    border-radius: 50%;
                    background: #8B5CF6;
                    animation: thinking 1.4s infinite ease-in-out;
                }

                .thinking-animation span:nth-child(2) {
                    animation-delay: 0.2s;
                }

                .thinking-animation span:nth-child(3) {
                    animation-delay: 0.4s;
                }

                @keyframes thinking {
                    0%, 60%, 100% {
                        transform: scale(0.8);
                        opacity: 0.5;
                    }
                    30% {
                        transform: scale(1);
                        opacity: 1;
                    }
                }

                .message.error .bubble {
                    background: #fef2f2;
                    border: 1px solid #fecaca;
                    color: #dc2626;
                }

                @media (max-width: 480px) {
                    .chat-window {
                        width: calc(100vw - 48px);
                        height: calc(100vh - 120px);
                        bottom: 88px;
                        right: 24px;
                    }
                    
                    .chat-toggle {
                        width: 64px;
                        height: 64px;
                    }
                }
            </style>
        `;
        
        document.head.insertAdjacentHTML('beforeend', css);
    }
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.masterChatNucleus = new MasterChatNucleus();
    });
} else {
    window.masterChatNucleus = new MasterChatNucleus();
}

// Export for manual initialization if needed
window.MasterChatNucleus = MasterChatNucleus;

