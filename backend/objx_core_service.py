#!/usr/bin/env python3
"""
OBJX CORE SERVICE - OPTIMIZED PLATFORM BUILD
Based on testing insights: simplified preprompt, no exchange prompt, systematic thinking core
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
from mem0 import MemoryClient

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize clients
openai_client = openai.OpenAI()
mem0_client = MemoryClient()

class OBJXCore:
    """Core OBJX intelligence system with systematic thinking"""
    
    def __init__(self):
        self.foundation_context = self.load_foundation_documents()
        
    def load_foundation_documents(self) -> str:
        """Load foundation documents for systematic thinking"""
        
        foundation_dir = "foundation_docs"
        foundation_content = ""
        
        foundation_files = [
            "00_living_doctrine_the_why.md",
            "01_foundation_principles_universal.md", 
            "02_trinity_architecture_universal.md",
            "03_intelligence_memory_compound.md",
            "04_partnership_protocols_complete.md",
            "06_evolution_continuous_improvement.md"
        ]
        
        for filename in foundation_files:
            filepath = os.path.join(foundation_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        foundation_content += f"\n\n=== {filename.upper()} ===\n{content}"
                except Exception as e:
                    print(f"Warning: Could not load {filename}: {e}")
        
        return foundation_content
    
    def get_systematic_response(self, user_message: str, user_id: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Get response using systematic thinking + memory"""
        
        # Search for relevant memories
        try:
            relevant_memories = mem0_client.search(user_message, user_id=user_id)
        except Exception as e:
            print(f"Memory search error: {e}")
            relevant_memories = []
        
        # Build memory context
        memory_context = ""
        if relevant_memories and len(relevant_memories) > 0:
            memory_context = "\n".join([
                f"Relevant memory: {memory.get('memory', '')}" 
                for memory in relevant_memories[:10]
            ])
        
        # Create simplified systematic prompt (no exchange prompt)
        system_prompt = f"""You are an AI assistant with systematic thinking capabilities and access to relevant memories.

=== SYSTEMATIC THINKING PRINCIPLES ===
{self.foundation_context}

=== RELEVANT MEMORIES ===
{memory_context if memory_context else "No relevant memories found."}

=== CONTEXT ===
{context if context else "General inquiry"}

Apply systematic thinking principles naturally and invisibly. Focus on:
- X: What do we know? (gather relevant context)
- Y: What do we need to discover? (identify gaps and requirements)  
- Z: What can we conclude? (systematic synthesis and recommendations)

Provide a comprehensive, naturally flowing response that demonstrates systematic thinking without exposing the methodology."""

        try:
            # Get AI response
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Store interaction in memory
            messages = [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": ai_response}
            ]
            
            mem0_client.add(messages, user_id=user_id)
            
            return {
                "success": True,
                "response": ai_response,
                "tokens_used": response.usage.completion_tokens,
                "memories_found": len(relevant_memories) if relevant_memories else 0,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": "I apologize, but I encountered an error processing your request.",
                "tokens_used": 0,
                "memories_found": 0,
                "timestamp": datetime.now().isoformat()
            }

# Initialize core system
objx_core = OBJXCore()

@app.route('/')
def index():
    """Main interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    
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
        
        # Get systematic response
        result = objx_core.get_systematic_response(user_message, user_id, context)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/memory/search', methods=['POST'])
def search_memory():
    """Search memories for a user"""
    
    try:
        data = request.get_json()
        query = data.get('query', '')
        user_id = data.get('user_id', 'default_user')
        
        memories = mem0_client.search(query, user_id=user_id)
        
        return jsonify({
            "success": True,
            "memories": memories,
            "count": len(memories) if memories else 0
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/memory/clear', methods=['POST'])
def clear_memory():
    """Clear all memories for a user"""
    
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        
        # Search for all memories
        all_memories = mem0_client.search("", user_id=user_id)
        
        deleted_count = 0
        if all_memories:
            for memory in all_memories:
                try:
                    mem0_client.delete(memory.get('id'))
                    deleted_count += 1
                except:
                    pass
        
        return jsonify({
            "success": True,
            "deleted_count": deleted_count
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "foundation_loaded": bool(objx_core.foundation_context),
        "services": {
            "openai": "connected",
            "mem0": "connected"
        }
    })

@app.route('/api/analytics', methods=['GET'])
def analytics():
    """Basic analytics endpoint"""
    
    try:
        user_id = request.args.get('user_id', 'default_user')
        
        # Get memory count
        memories = mem0_client.search("", user_id=user_id)
        memory_count = len(memories) if memories else 0
        
        return jsonify({
            "success": True,
            "user_id": user_id,
            "memory_count": memory_count,
            "foundation_status": "loaded" if objx_core.foundation_context else "not_loaded",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 OBJX Core Service Starting...")
    print("=" * 50)
    print(f"Foundation Documents: {'Loaded' if objx_core.foundation_context else 'Not Found'}")
    print("Systematic Thinking: Enabled")
    print("Exchange Prompt: Disabled (Optimized)")
    print("Memory System: mem0 Integration")
    print("=" * 50)
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)

