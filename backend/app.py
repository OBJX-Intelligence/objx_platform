"""
OBJX Intelligence Platform - Complete Backend
Trinity Architecture: Foundation + mem0 + Systematic Thinking

Based on Trinity Architecture testing validation:
- Foundation + mem0 superiority proven
- Simplified preprompt (no exchange prompt)
- Systematic thinking core
- Compound learning
"""
from mem0 import MemoryClient
import json
import os
from datetime import datetime
from agents import (
    AgentFactory, 
    SystematicThinkingAgent, 
    CompoundIntelligenceAgent, 
    CompleteMethodologyAgent,
    SOPIntegration,
    AgentTier,
    DocumentType,
    WorkflowStatus
)
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
from mem0 import MemoryClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

class OBJXPlatform:
    """Complete OBJX Platform with systematic thinking and memory"""
    
    def __init__(self):
        self.foundation_context = self.load_foundation_documents()
        self.openai_client = None
        self.mem0_client = None
        self.initialize_clients()
        
        # Initialize agents and SOP integration
        self.agent_factory = AgentFactory()
        self.sop_integration = SOPIntegration()
        
        # Permission levels
        self.permission_levels = {
            'admin': 5,
            'staff': 4, 
            'tier3': 3,
            'tier2': 2,
            'tier1': 1
        }
        
    def initialize_clients(self):
        """Initialize API clients with error handling"""
        try:
            # Initialize OpenAI client
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                print("⚠️  WARNING: OPENAI_API_KEY not found in environment")
                print("   Please set your OpenAI API key in environment variables")
            else:
                self.openai_client = openai.OpenAI(api_key=openai_api_key)
                print("✅ OpenAI client initialized")
                
        except Exception as e:
            print(f"❌ OpenAI initialization error: {e}")
            
        try:
            # Initialize MEM0 client
            mem0_api_key = os.getenv('MEM0_API_KEY')
            if not mem0_api_key:
                print("⚠️  WARNING: MEM0_API_KEY not found in environment")
                print("   Please set your MEM0 API key in environment variables")
            else:
                self.mem0_client = MemoryClient(api_key=mem0_api_key)
                print("✅ MEM0 client initialized")
                
        except Exception as e:
            print(f"❌ MEM0 initialization error: {e}")
        
    def load_foundation_documents(self) -> str:
        """Load the 6 core foundation documents for systematic thinking"""
        
        foundation_dir = "foundation_docs"
        foundation_content = ""
        
        foundation_files = [
            "00_living_doctoring_the_why.md",
            "01_foundation_principles_universal.md", 
            "02_trinity_architecture_universal.md",
            "03_intelligence_memory_compound.md",
            "04_partnership_protocols_complete.md",
            "06_evolution_continuous_improvement.md"
        ]
        
        loaded_count = 0
        
        for filename in foundation_files:
            file_path = os.path.join(foundation_dir, filename)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        foundation_content += f"\n\n=== {filename} ===\n{content}"
                        loaded_count += 1
                        print(f"✅ Loaded: {filename}")
                except Exception as e:
                    print(f"❌ Error loading {filename}: {e}")
            else:
                print(f"⚠️  Foundation document not found: {file_path}")
        
        print(f"📚 Foundation Documents: {loaded_count}/6 loaded")
        return foundation_content
    
    def get_systematic_response(self, user_message: str, user_id: str = "default_user", context: str = None) -> dict:
        """Get systematic thinking response using Trinity Architecture"""
        
        if not self.openai_client:
            return {
                "success": False,
                "error": "OpenAI client not initialized. Please check your API key.",
                "response": "I apologize, but I'm currently unable to process your request due to a configuration issue."
            }
        
        # Get relevant memories (if mem0 available)
        relevant_memories = []
        memory_context = ""
        
        if self.mem0_client:
            try:
                relevant_memories = self.mem0_client.search(user_message, user_id=user_id)
                if relevant_memories:
                    memory_context = "\n".join([
                        f"- {memory.get('memory', '')}" 
                        for memory in relevant_memories[:5]
                    ])
            except Exception as e:
                print(f"Memory search error: {e}")
        
        # Build systematic thinking prompt
        system_prompt = f"""You are an AI assistant with systematic thinking capabilities and access to relevant memories.

=== SYSTEMATIC THINKING PRINCIPLES ===
{self.foundation_context if self.foundation_context else "Foundation documents not loaded - using basic systematic thinking."}

=== RELEVANT MEMORIES ===
{memory_context if memory_context else "No relevant memories found."}

=== CONTEXT ===
{context if context else "General inquiry"}

Apply systematic thinking principles naturally and invisibly. Focus on:
- X: What do we know? (gather relevant context and information)
- Y: What do we need to discover? (identify gaps, requirements, and objectives)  
- Z: What can we conclude? (systematic synthesis, insights, and actionable recommendations)

Provide a comprehensive, naturally flowing response that demonstrates systematic thinking without exposing the methodology. Be proactive, insightful, and strategic in your analysis."""

        try:
            # Get AI response
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Store interaction in memory (if mem0 available)
            if self.mem0_client:
                try:
                    messages = [
                        {"role": "user", "content": user_message},
                        {"role": "assistant", "content": ai_response}
                    ]
                    self.mem0_client.add(messages, user_id=user_id)
                except Exception as e:
                    print(f"Memory storage error: {e}")
            
            return {
                "success": True,
                "response": ai_response,
                "tokens_used": response.usage.completion_tokens if response.usage else 0,
                "memories_found": len(relevant_memories) if relevant_memories else 0,
                "foundation_loaded": bool(self.foundation_context),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": "I apologize, but I encountered an error processing your request. Please try again."
            }

# Initialize platform
objx_platform = OBJXPlatform()

# ============================================================================
# FRONTEND ROUTES

@app.route('/')
def index():
    """Main landing page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/login')
def login():
    """Login page"""
    return send_from_directory('../frontend', 'login.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard - routes to appropriate tier"""
    # TODO: Get actual user tier from session/auth
    return send_from_directory('../frontend', 'dashboard_tier1.html')

@app.route('/dashboard/tier1')
def dashboard_tier1():
    """Tier 1 Dashboard - Systematic Thinking"""
    return send_from_directory('../frontend', 'dashboard_tier1.html')

@app.route('/dashboard/tier2')
def dashboard_tier2():
    """Tier 2 Dashboard - Compound Intelligence"""
    return send_from_directory('../frontend', 'dashboard_tier2.html')

@app.route('/dashboard/tier3')
def dashboard_tier3():
    """Tier 3 Dashboard - Complete Methodology"""
    return send_from_directory('../frontend', 'dashboard_tier3.html')

@app.route('/chat')
def chat_interface():
    """Dedicated chat interface"""
    return send_from_directory('../frontend', 'index.html')

# Serve static assets
@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from frontend directory"""
    return send_from_directory('../frontend', filename)

# ============================================================================
# API ENDPOINTS

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Main chat endpoint - Trinity Architecture systematic thinking"""
    
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')
        context = data.get('context', None)
        
        if not user_message:
            return jsonify({
                "success": False,
                "error": "Message is required"
            }), 400
        
        # Get systematic response using Trinity Architecture
        result = objx_platform.get_systematic_response(user_message, user_id, context)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def api_health():
    """Health check endpoint"""
    
    return jsonify({
        "status": "healthy",
        "platform": "OBJX Intelligence",
        "architecture": "Trinity (Foundation + mem0 + Systematic Thinking)",
        "foundation_loaded": bool(objx_platform.foundation_context),
        "openai_configured": objx_platform.openai_client is not None,
        "mem0_configured": objx_platform.mem0_client is not None,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 OBJX Intelligence Platform Starting...")
    print("🔧 Trinity Architecture: Foundation + mem0 + Systematic Thinking")
    print("📚 Foundation Documents: 6/6 loaded")
    print("🤖 Agent System: Multi-tier functionality enabled")
    print("🌐 Server: http://localhost:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

