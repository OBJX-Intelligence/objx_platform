// Universal Chat Component with Permission Filtering
// Single HTML element across all pages with tier-based access control

class UniversalChatComponent {
    constructor() {
        this.isOpen = false;
        this.currentTier = this.detectUserTier();
        this.currentPage = this.detectCurrentPage();
        this.permissions = this.getPermissions();
        this.init();
    }

    detectUserTier() {
        // Detect tier from URL or page context
        const url = window.location.pathname;
        if (url.includes('tier1')) return 'tier1';
        if (url.includes('tier2')) return 'tier2';
        if (url.includes('tier3')) return 'tier3';
        if (url.includes('admin')) return 'admin';
        return 'tier1'; // Default
    }

    detectCurrentPage() {
        const url = window.location.pathname;
        if (url.includes('dashboard')) return 'dashboard';
        if (url.includes('project')) return 'project';
        if (url.includes('billing')) return 'billing';
        if (url.includes('google-workspace')) return 'workspace';
        return 'general';
    }

    getPermissions() {
        const permissions = {
            tier1: {
                features: ['basic_chat', 'systematic_thinking'],
                context: ['current_page'],
                memory: false,
                agents: false
            },
            tier2: {
                features: ['basic_chat', 'systematic_thinking', 'project_context', 'memory_search'],
                context: ['current_page', 'project_data'],
                memory: true,
                agents: false
            },
            tier3: {
                features: ['basic_chat', 'systematic_thinking', 'project_context', 'memory_search', 'agent_orchestration', 'document_generation'],
                context: ['current_page', 'project_data', 'full_dashboard'],
                memory: true,
                agents: true
            },
            admin: {
                features: ['basic_chat', 'systematic_thinking', 'project_context', 'memory_search', 'agent_orchestration', 'document_generation', 'system_admin'],
                context: ['current_page', 'project_data', 'full_dashboard', 'system_metrics'],
                memory: true,
                agents: true
            }
        };
        return permissions[this.currentTier] || permissions.tier1;
    }

    init() {
        this.createChatHTML();
        this.attachEventListeners();
        this.loadInitialContext();
    }

    createChatHTML() {
        const chatHTML = `
            <div id="universal-chat-container" class="chat-container">
                <!-- Chat Toggle Button -->
                <button id="chat-toggle" class="chat-toggle" aria-label="Open Chat">
                    <div class="chat-toggle-icon">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                        </svg>
                    </div>
                    <div class="notification-badge" id="chat-notification" style="display: none;">
                        <span id="notification-count">1</span>
                    </div>
                </button>

                <!-- Chat Window -->
                <div id="chat-window" class="chat-window">
                    <div class="chat-header">
                        <div class="chat-header-content">
                            <h3 class="chat-title">OBJX Intelligence</h3>
                            <p class="chat-subtitle">Strategic Intelligence Partner</p>
                        </div>
                        <div class="chat-tier-badge">${this.currentTier.toUpperCase()}</div>
                        <button id="chat-close" class="chat-close" aria-label="Close Chat">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    </div>

                    <div id="chat-messages" class="chat-messages">
                        <div class="message assistant">
                            <div class="message-content">
                                <div class="message-avatar">
                                    <div class="avatar-circle">AI</div>
                                </div>
                                <div class="message-bubble">
                                    <div class="message-text">
                                        Welcome to OBJX Intelligence! I'm here to enhance your thinking using the Trinity Foundation methodology. How can I help you think through your current challenge or opportunity?
                                    </div>
                                    <div class="message-time">Now</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="chat-input-container">
                        <div class="chat-features">
                            ${this.renderFeatureTags()}
                        </div>
                        <div class="chat-input-wrapper">
                            <textarea 
                                id="chat-input" 
                                placeholder="Share your thoughts, challenges, or opportunities..."
                                rows="1"
                            ></textarea>
                            <button id="chat-send" class="chat-send-button" disabled>
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
        
        // Add HTML to page
        document.body.insertAdjacentHTML('beforeend', chatHTML);
    }

    renderFeatureTags() {
        const features = this.permissions.features;
        const tags = [];
        
        if (features.includes('systematic_thinking')) tags.push('Strategic Thinking');
        if (features.includes('memory_search')) tags.push('Pattern Recognition');
        if (features.includes('project_context')) tags.push('Project Context');
        if (features.includes('agent_orchestration')) tags.push('Agent Orchestration');
        
        return tags.map(tag => `<span class="feature-tag">${tag}</span>`).join('');
    }

    attachEventListeners() {
        const toggleBtn = document.getElementById('chat-toggle');
        const closeBtn = document.getElementById('chat-close');
        const sendBtn = document.getElementById('chat-send');
        const input = document.getElementById('chat-input');

        toggleBtn.addEventListener('click', () => this.toggleChat());
        closeBtn.addEventListener('click', () => this.closeChat());
        sendBtn.addEventListener('click', () => this.sendMessage());
        
        input.addEventListener('input', (e) => {
            this.handleInputChange(e);
            this.autoResize(e.target);
        });
        
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const chatWindow = document.getElementById('chat-window');
        const toggleBtn = document.getElementById('chat-toggle');
        
        if (this.isOpen) {
            chatWindow.classList.add('active');
            toggleBtn.style.transform = 'scale(0.9)';
            document.getElementById('chat-input').focus();
        } else {
            chatWindow.classList.remove('active');
            toggleBtn.style.transform = 'scale(1)';
        }
    }

    closeChat() {
        this.isOpen = false;
        document.getElementById('chat-window').classList.remove('active');
        document.getElementById('chat-toggle').style.transform = 'scale(1)';
    }

    handleInputChange(e) {
        const sendBtn = document.getElementById('chat-send');
        sendBtn.disabled = e.target.value.trim().length === 0;
    }

    autoResize(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        input.value = '';
        input.style.height = 'auto';
        document.getElementById('chat-send').disabled = true;

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Prepare context based on permissions
            const context = await this.gatherContext();
            
            // Send to API
            const response = await fetch('/api/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    context: context,
                    tier: this.currentTier,
                    page: this.currentPage,
                    permissions: this.permissions
                })
            });

            const data = await response.json();
            
            // Remove typing indicator
            this.removeTypingIndicator();
            
            if (data.success) {
                this.addMessage(data.message, 'assistant');
            } else {
                this.addMessage('I\'m having trouble connecting right now. Please try again.', 'assistant', true);
            }
            
        } catch (error) {
            console.error('Chat error:', error);
            this.removeTypingIndicator();
            this.addMessage('I\'m having trouble connecting right now. Please try again.', 'assistant', true);
        }
    }

    async gatherContext() {
        const context = {
            tier: this.currentTier,
            page: this.currentPage,
            timestamp: new Date().toISOString()
        };

        // Add page-specific context based on permissions
        if (this.permissions.context.includes('project_data')) {
            context.projects = this.getProjectData();
        }
        
        if (this.permissions.context.includes('full_dashboard')) {
            context.dashboard = this.getDashboardData();
        }
        
        if (this.permissions.context.includes('system_metrics')) {
            context.system = this.getSystemMetrics();
        }

        return context;
    }

    getProjectData() {
        // Extract project data from current page if available
        try {
            const projectElements = document.querySelectorAll('[data-project-id]');
            return Array.from(projectElements).map(el => ({
                id: el.dataset.projectId,
                name: el.dataset.projectName || 'Unknown',
                status: el.dataset.projectStatus || 'Active'
            }));
        } catch (error) {
            return [];
        }
    }

    getDashboardData() {
        // Extract dashboard metrics if available
        try {
            return {
                revenue: document.querySelector('[data-revenue]')?.textContent || 'N/A',
                projects: document.querySelector('[data-project-count]')?.textContent || 'N/A',
                team: document.querySelector('[data-team-performance]')?.textContent || 'N/A'
            };
        } catch (error) {
            return {};
        }
    }

    getSystemMetrics() {
        // Admin-only system metrics
        return {
            agents_active: 7,
            background_tasks: 12,
            system_health: 'Optimal'
        };
    }

    addMessage(text, sender, isError = false) {
        const messagesContainer = document.getElementById('chat-messages');
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        const messageHTML = `
            <div class="message ${sender} ${isError ? 'error' : ''}">
                <div class="message-content">
                    ${sender === 'assistant' ? '<div class="message-avatar"><div class="avatar-circle">AI</div></div>' : ''}
                    <div class="message-bubble">
                        <div class="message-text">${text}</div>
                        <div class="message-time">${time}</div>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        const typingHTML = `
            <div id="typing-indicator" class="message assistant typing">
                <div class="message-content">
                    <div class="message-avatar"><div class="avatar-circle">AI</div></div>
                    <div class="message-bubble">
                        <div class="typing-dots">
                            <span></span><span></span><span></span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', typingHTML);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }

    loadInitialContext() {
        // Load any initial context based on current page
        console.log(`Universal Chat initialized for ${this.currentTier} on ${this.currentPage}`);
    }

    injectCSS() {
        const css = `
            <style>
                .chat-container {
                    position: fixed;
                    bottom: 24px;
                    right: 24px;
                    z-index: 1000;
                    font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Arial, sans-serif;
                }

                .chat-toggle {
                    width: 64px;
                    height: 64px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
                    border: none;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 8px 32px rgba(139, 92, 246, 0.3);
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    position: relative;
                    color: white;
                }

                .chat-toggle:hover {
                    transform: scale(1.05);
                    box-shadow: 0 12px 40px rgba(139, 92, 246, 0.4);
                }

                .notification-badge {
                    position: absolute;
                    top: -4px;
                    right: -4px;
                    background: #ef4444;
                    color: white;
                    border-radius: 50%;
                    width: 20px;
                    height: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 11px;
                    font-weight: 600;
                }

                .chat-window {
                    position: absolute;
                    bottom: 80px;
                    right: 0;
                    width: 400px;
                    height: 600px;
                    background: white;
                    border-radius: 16px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
                    display: none;
                    flex-direction: column;
                    transform: translateY(20px) scale(0.95);
                    opacity: 0;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    overflow: hidden;
                }

                .chat-window.active {
                    display: flex;
                    transform: translateY(0) scale(1);
                    opacity: 1;
                }

                .chat-header {
                    padding: 20px 24px 16px;
                    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
                    color: white;
                    position: relative;
                }

                .chat-title {
                    font-size: 18px;
                    font-weight: 600;
                    margin: 0 0 4px 0;
                }

                .chat-subtitle {
                    font-size: 13px;
                    opacity: 0.9;
                    margin: 0;
                }

                .chat-tier-badge {
                    position: absolute;
                    top: 16px;
                    right: 50px;
                    background: rgba(255, 255, 255, 0.2);
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: 600;
                }

                .chat-close {
                    position: absolute;
                    top: 16px;
                    right: 20px;
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                    padding: 4px;
                    border-radius: 4px;
                    opacity: 0.8;
                }

                .chat-close:hover {
                    opacity: 1;
                    background: rgba(255, 255, 255, 0.1);
                }

                .chat-messages {
                    flex: 1;
                    padding: 20px;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column;
                    gap: 16px;
                    background: #f8fafc;
                }

                .message {
                    display: flex;
                    flex-direction: column;
                    max-width: 85%;
                }

                .message.user {
                    align-self: flex-end;
                }

                .message.assistant {
                    align-self: flex-start;
                }

                .message-content {
                    display: flex;
                    gap: 12px;
                    align-items: flex-end;
                }

                .message-avatar {
                    flex-shrink: 0;
                }

                .avatar-circle {
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #8B5CF6, #7C3AED);
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    font-weight: 600;
                }

                .message-bubble {
                    background: white;
                    padding: 12px 16px;
                    border-radius: 16px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                }

                .message.user .message-bubble {
                    background: linear-gradient(135deg, #8B5CF6, #7C3AED);
                    color: white;
                }

                .message-text {
                    font-size: 14px;
                    line-height: 1.5;
                    margin-bottom: 4px;
                }

                .message-time {
                    font-size: 11px;
                    opacity: 0.6;
                }

                .chat-features {
                    padding: 12px 20px 8px;
                    display: flex;
                    gap: 8px;
                    flex-wrap: wrap;
                    background: white;
                    border-top: 1px solid #e2e8f0;
                }

                .feature-tag {
                    background: #f1f5f9;
                    color: #64748b;
                    padding: 4px 8px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: 500;
                }

                .chat-input-container {
                    background: white;
                    border-top: 1px solid #e2e8f0;
                }

                .chat-input-wrapper {
                    padding: 16px 20px;
                    display: flex;
                    gap: 12px;
                    align-items: flex-end;
                }

                #chat-input {
                    flex: 1;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 12px 16px;
                    font-size: 14px;
                    resize: none;
                    outline: none;
                    font-family: inherit;
                    min-height: 44px;
                    max-height: 120px;
                }

                #chat-input:focus {
                    border-color: #8B5CF6;
                    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
                }

                .chat-send-button {
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
                }

                .chat-send-button:disabled {
                    opacity: 0.5;
                    cursor: not-allowed;
                }

                .chat-send-button:not(:disabled):hover {
                    transform: scale(1.05);
                }

                .typing-dots {
                    display: flex;
                    gap: 4px;
                    align-items: center;
                }

                .typing-dots span {
                    width: 6px;
                    height: 6px;
                    border-radius: 50%;
                    background: #8B5CF6;
                    animation: typing 1.4s infinite ease-in-out;
                }

                .typing-dots span:nth-child(2) {
                    animation-delay: 0.2s;
                }

                .typing-dots span:nth-child(3) {
                    animation-delay: 0.4s;
                }

                @keyframes typing {
                    0%, 60%, 100% {
                        transform: scale(0.8);
                        opacity: 0.5;
                    }
                    30% {
                        transform: scale(1);
                        opacity: 1;
                    }
                }

                @media (max-width: 480px) {
                    .chat-window {
                        width: calc(100vw - 48px);
                        height: calc(100vh - 120px);
                        bottom: 80px;
                        right: 24px;
                    }
                }
            </style>
        `;
        document.head.insertAdjacentHTML('beforeend', css);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new UniversalChatComponent();
    });
} else {
    new UniversalChatComponent();
}

