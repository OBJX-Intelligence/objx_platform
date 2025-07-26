"""
OBJX Intelligence Platform - Universal Chat System
Agent-foundation architecture with invisible methodology and tier-based permissions
"""

import os
import json
import openai
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum
from memory_command_center import memory_center, MemoryType, MemoryPriority
from notification_system import notification_system, NotificationType, NotificationPriority, UserRole

class UserTier(Enum):
    TIER_1 = "tier_1"  # Foundation only, no memory
    TIER_2 = "tier_2"  # Foundation + basic memory
    TIER_3 = "tier_3"  # Foundation + full memory + advanced features
    STAFF = "staff"    # Foundation + memory + project management
    ADMIN = "admin"    # Foundation + memory + full system access

@dataclass
class ChatMessage:
    id: str
    user_id: str
    user_tier: UserTier
    message: str
    response: str
    timestamp: datetime
    context_used: List[str]
    memory_accessed: List[str]
    agent_type: str

class UniversalChatSystem:
    """
    Universal chat interface with invisible X+Y=Z methodology
    Tier-based permissions for foundation and memory access
    """
    
    def __init__(self):
        # Initialize OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Load foundation documents
        self.foundation_docs = self._load_foundation_docs()
        
        # Universal preprompt
        self.universal_preprompt = self._load_universal_preprompt()
        
        # Tier-based agent configurations
        self.tier_agents = {
            UserTier.TIER_1: "systematic_thinking_agent",
            UserTier.TIER_2: "compound_intelligence_agent", 
            UserTier.TIER_3: "complete_methodology_agent",
            UserTier.STAFF: "project_management_agent",
            UserTier.ADMIN: "admin_command_agent"
        }
    
    def _load_foundation_docs(self) -> Dict[str, str]:
        """Load all foundation documents for context"""
        foundation_files = [
            "00_living_doctoring_the_why.md",
            "01_foundation_principles_universal.md", 
            "02_trinity_architecture_universal.md",
            "03_intelligence_memory_compound.md",
            "04_partnership_protocols_complete.md",
            "06_evolution_continuous_improvement.md"
        ]
        
        docs = {}
        for filename in foundation_files:
            try:
                with open(f"/home/ubuntu/upload/{filename}", 'r') as f:
                    docs[filename] = f.read()
            except FileNotFoundError:
                print(f"Foundation document not found: {filename}")
                docs[filename] = ""
        
        return docs
    
    def _load_universal_preprompt(self) -> str:
        """Load the universal preprompt"""
        try:
            with open("/home/ubuntu/objx_platform/UNIVERSAL-PREPROMPT.MD", 'r') as f:
                return f.read()
        except FileNotFoundError:
            return """You are a strategic thinking partner operating within the OBJX Intelligence Platform. 
            Communicate naturally and empathetically while invisibly applying systematic thinking methodology. 
            Never explicitly mention frameworks or methodologies. Help users clarify, compound insights, and create solutions 
            through natural conversation and genuine curiosity."""
    
    def _get_tier_permissions(self, user_tier: UserTier) -> Dict[str, bool]:
        """Get permissions based on user tier"""
        permissions = {
            "foundation_access": True,  # All tiers have foundation
            "memory_access": False,
            "memory_creation": False,
            "advanced_agents": False,
            "system_management": False,
            "project_management": False,
            "client_memory": False,
            "admin_functions": False
        }
        
        if user_tier == UserTier.TIER_1:
            # Only foundation access
            pass
        
        elif user_tier == UserTier.TIER_2:
            permissions.update({
                "memory_access": True,
                "memory_creation": True
            })
        
        elif user_tier == UserTier.TIER_3:
            permissions.update({
                "memory_access": True,
                "memory_creation": True,
                "advanced_agents": True,
                "client_memory": True
            })
        
        elif user_tier == UserTier.STAFF:
            permissions.update({
                "memory_access": True,
                "memory_creation": True,
                "project_management": True,
                "client_memory": True
            })
        
        elif user_tier == UserTier.ADMIN:
            permissions.update({
                "memory_access": True,
                "memory_creation": True,
                "advanced_agents": True,
                "system_management": True,
                "project_management": True,
                "client_memory": True,
                "admin_functions": True
            })
        
        return permissions
    
    def _build_context(self, user_id: str, user_tier: UserTier, message: str) -> str:
        """Build context based on tier permissions"""
        permissions = self._get_tier_permissions(user_tier)
        context_parts = []
        
        # Always include universal preprompt
        context_parts.append("UNIVERSAL METHODOLOGY:")
        context_parts.append(self.universal_preprompt)
        
        # Always include foundation documents
        context_parts.append("\nFOUNDATION DOCUMENTS:")
        for doc_name, content in self.foundation_docs.items():
            if content:
                context_parts.append(f"\n{doc_name.upper()}:")
                context_parts.append(content[:2000])  # Limit length
        
        # Add memory context if permitted
        if permissions["memory_access"]:
            relevant_memories = self._get_relevant_memories(user_id, message, user_tier)
            if relevant_memories:
                context_parts.append("\nRELEVANT MEMORIES:")
                for memory in relevant_memories[:5]:  # Limit to top 5
                    context_parts.append(f"- {memory.content}")
        
        # Add tier-specific instructions
        context_parts.append(f"\nUSER TIER: {user_tier.value.upper()}")
        context_parts.append(self._get_tier_instructions(user_tier))
        
        return "\n".join(context_parts)
    
    def _get_relevant_memories(self, user_id: str, message: str, user_tier: UserTier) -> List:
        """Get relevant memories based on tier permissions"""
        if user_tier == UserTier.TIER_1:
            return []  # No memory access for Tier 1
        
        try:
            # Search memories based on message content
            memories = memory_center.search_memories(
                query=message,
                user_id=user_id if user_tier in [UserTier.TIER_2, UserTier.TIER_3] else None
            )
            
            # Filter memories based on tier permissions
            filtered_memories = []
            for memory in memories:
                if self._can_access_memory(memory, user_tier, user_id):
                    filtered_memories.append(memory)
            
            return filtered_memories
            
        except Exception as e:
            print(f"Error retrieving memories: {e}")
            return []
    
    def _can_access_memory(self, memory, user_tier: UserTier, user_id: str) -> bool:
        """Check if user can access specific memory based on tier"""
        permissions = self._get_tier_permissions(user_tier)
        
        # Admin can access all memories
        if permissions["admin_functions"]:
            return True
        
        # Staff can access project and system memories
        if permissions["project_management"]:
            if memory.memory_type in [MemoryType.PROJECT, MemoryType.SYSTEM]:
                return True
        
        # Client memory access for Tier 3 and Staff
        if permissions["client_memory"]:
            if memory.client_id == user_id or memory.memory_type == MemoryType.PATTERN:
                return True
        
        # Basic memory access for Tier 2+
        if permissions["memory_access"]:
            if memory.memory_type == MemoryType.SYSTEM and memory.priority != MemoryPriority.CRITICAL:
                return True
        
        return False
    
    def _get_tier_instructions(self, user_tier: UserTier) -> str:
        """Get specific instructions based on user tier"""
        instructions = {
            UserTier.TIER_1: """
            TIER 1 - SYSTEMATIC THINKING ACCESS:
            - Focus on foundation principles and systematic thinking methodology
            - Help with basic problem-solving using X+Y=Z framework
            - No access to memory or advanced features
            - Provide clear, actionable guidance based on universal principles
            """,
            
            UserTier.TIER_2: """
            TIER 2 - COMPOUND INTELLIGENCE:
            - Access to foundation principles plus basic memory system
            - Can reference past conversations and learned patterns
            - Focus on project organization and pattern recognition
            - Provide memory-enhanced insights and recommendations
            """,
            
            UserTier.TIER_3: """
            TIER 3 - COMPLETE METHODOLOGY:
            - Full access to foundation, memory, and advanced features
            - Can orchestrate multiple agents and create comprehensive outputs
            - Access to client-specific memories and advanced analytics
            - Provide complete methodology solutions with full context
            """,
            
            UserTier.STAFF: """
            STAFF - PROJECT MANAGEMENT:
            - Foundation and memory access focused on project management
            - Can access project memories and team collaboration features
            - Focus on workflow optimization and team coordination
            - Provide project-specific insights and management recommendations
            """,
            
            UserTier.ADMIN: """
            ADMIN - FULL SYSTEM ACCESS:
            - Complete access to all foundation documents and memories
            - Can manage system-wide settings and configurations
            - Access to all client data and business intelligence
            - Provide comprehensive system management and strategic insights
            """
        }
        
        return instructions.get(user_tier, "")
    
    async def process_message(self, user_id: str, user_tier: UserTier, message: str, 
                            context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a chat message with tier-based permissions"""
        
        # Build context based on tier permissions
        system_context = self._build_context(user_id, user_tier, message)
        
        # Get agent type for this tier
        agent_type = self.tier_agents.get(user_tier, "basic_agent")
        
        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": system_context},
            {"role": "user", "content": message}
        ]
        
        # Add conversation history if available
        if context and "conversation_history" in context:
            for hist_msg in context["conversation_history"][-5:]:  # Last 5 messages
                messages.insert(-1, {"role": "user", "content": hist_msg["user"]})
                messages.insert(-1, {"role": "assistant", "content": hist_msg["assistant"]})
        
        try:
            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=messages,
                max_tokens=1500,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Create memory if permitted
            memories_created = []
            if self._get_tier_permissions(user_tier)["memory_creation"]:
                memory_id = self._create_conversation_memory(
                    user_id, user_tier, message, assistant_response
                )
                if memory_id:
                    memories_created.append(memory_id)
            
            # Log conversation
            chat_message = ChatMessage(
                id=f"chat_{int(datetime.now().timestamp() * 1000)}",
                user_id=user_id,
                user_tier=user_tier,
                message=message,
                response=assistant_response,
                timestamp=datetime.now(),
                context_used=[doc for doc in self.foundation_docs.keys()],
                memory_accessed=[],  # Would track which memories were used
                agent_type=agent_type
            )
            
            return {
                "response": assistant_response,
                "agent_type": agent_type,
                "memories_created": memories_created,
                "permissions": self._get_tier_permissions(user_tier),
                "chat_id": chat_message.id
            }
            
        except Exception as e:
            print(f"Error processing message: {e}")
            return {
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again.",
                "error": str(e),
                "agent_type": agent_type
            }
    
    def _create_conversation_memory(self, user_id: str, user_tier: UserTier, 
                                  user_message: str, assistant_response: str) -> Optional[str]:
        """Create memory from conversation if permitted"""
        try:
            # Determine memory type based on tier
            memory_type = MemoryType.CLIENT if user_tier in [UserTier.TIER_2, UserTier.TIER_3] else MemoryType.SYSTEM
            
            # Create memory content
            memory_content = f"User Query: {user_message}\nInsight: {assistant_response}"
            
            # Create memory
            memory_id = memory_center.create_memory(
                content=memory_content,
                user_id=user_id,
                memory_type=memory_type,
                priority=MemoryPriority.MEDIUM,
                client_id=user_id if memory_type == MemoryType.CLIENT else None,
                tags=["conversation", "chat", user_tier.value]
            )
            
            return memory_id
            
        except Exception as e:
            print(f"Error creating conversation memory: {e}")
            return None
    
    def get_chat_history(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get chat history for a user"""
        # This would typically be stored in a database
        # For now, return empty list
        return []
    
    def get_available_agents(self, user_tier: UserTier) -> List[Dict[str, str]]:
        """Get available agents based on user tier"""
        base_agents = [
            {
                "id": "systematic_thinking",
                "name": "Systematic Thinking",
                "description": "Foundation-based problem solving with X+Y=Z methodology"
            }
        ]
        
        if user_tier in [UserTier.TIER_2, UserTier.TIER_3, UserTier.STAFF, UserTier.ADMIN]:
            base_agents.extend([
                {
                    "id": "memory_enhanced",
                    "name": "Memory Enhanced",
                    "description": "Compound intelligence with memory-driven insights"
                }
            ])
        
        if user_tier in [UserTier.TIER_3, UserTier.ADMIN]:
            base_agents.extend([
                {
                    "id": "document_creation",
                    "name": "Document Creation",
                    "description": "Complete methodology with document generation"
                },
                {
                    "id": "visual_analytics",
                    "name": "Visual Analytics", 
                    "description": "Advanced analytics with visual intelligence"
                }
            ])
        
        if user_tier == UserTier.STAFF:
            base_agents.append({
                "id": "project_management",
                "name": "Project Management",
                "description": "Team coordination and workflow optimization"
            })
        
        if user_tier == UserTier.ADMIN:
            base_agents.extend([
                {
                    "id": "system_management",
                    "name": "System Management",
                    "description": "Complete system administration and business intelligence"
                },
                {
                    "id": "multi_agent_orchestration",
                    "name": "Multi-Agent Orchestration",
                    "description": "Coordinate multiple specialized agents"
                }
            ])
        
        return base_agents
    
    async def process_chat_message(self, user_id: str, user_tier: UserTier, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process chat message with invisible methodology integration
        Returns natural, empathetic response without explicit framework mentions
        """
        try:
            # Build context with universal preprompt and tier permissions
            full_context = self._build_context(user_id, user_tier, message)
            
            # Get relevant memories if user has access
            relevant_memories = []
            permissions = self._get_tier_permissions(user_tier)
            if permissions["memory_access"]:
                relevant_memories = memory_center.search_memories(
                    query=message,
                    user_id=user_id,
                    limit=5
                )
            
            # Build the conversation prompt
            conversation_prompt = self._build_conversation_prompt(
                message=message,
                context=full_context,
                memories=relevant_memories,
                user_tier=user_tier
            )
            
            # Generate response using OpenAI
            response = await self._generate_response(conversation_prompt)
            
            # Create conversation memory if user has access
            memory_id = None
            if permissions["memory_creation"]:
                memory_id = self._create_conversation_memory(
                    user_id=user_id,
                    message=message,
                    response=response,
                    user_tier=user_tier
                )
            
            # Create chat message record
            chat_message = ChatMessage(
                id=f"chat_{datetime.now().timestamp()}",
                user_id=user_id,
                user_tier=user_tier,
                message=message,
                response=response,
                timestamp=datetime.now(),
                context_used=[],
                memory_accessed=[m.id for m in relevant_memories] if relevant_memories else [],
                agent_type=self.tier_agents[user_tier]
            )
            
            return {
                "success": True,
                "response": response,
                "message_id": chat_message.id,
                "memory_id": memory_id,
                "agent_type": chat_message.agent_type,
                "memories_accessed": len(relevant_memories) if relevant_memories else 0
            }
            
        except Exception as e:
            print(f"Error processing chat message: {e}")
            return {
                "success": False,
                "error": "I'm having trouble processing your message right now. Please try again.",
                "response": "I apologize, but I'm experiencing some technical difficulties. Could you please rephrase your question?"
            }
    
    def _build_conversation_prompt(self, message: str, context: str, memories: List[Any], user_tier: UserTier) -> str:
        """Build the conversation prompt with invisible methodology"""
        
        # Start with universal preprompt (invisible to user)
        prompt_parts = [self.universal_preprompt]
        
        # Add tier-specific context without mentioning tiers
        tier_context = self._get_natural_tier_context(user_tier)
        if tier_context:
            prompt_parts.append(tier_context)
        
        # Add relevant memories naturally
        if memories:
            memory_context = "RELEVANT CONTEXT FROM PREVIOUS CONVERSATIONS:\n"
            for memory in memories[:3]:  # Limit to most relevant
                memory_context += f"- {memory.content}\n"
            prompt_parts.append(memory_context)
        
        # Add the current conversation
        prompt_parts.append(f"\nUSER MESSAGE: {message}")
        
        # Add response guidelines
        prompt_parts.append("""
RESPONSE GUIDELINES:
- Respond naturally and conversationally, like a trusted advisor
- Show genuine curiosity and ask thoughtful follow-up questions
- Help the user see patterns and connections they might miss
- Provide practical insights and next steps
- Never mention frameworks, methodologies, or systematic processes
- Be empathetic and supportive while being strategically helpful
- Keep responses concise but complete
- Use natural language formatting with proper paragraphs and spacing
""")
        
        return "\n\n".join(prompt_parts)
    
    def _get_natural_tier_context(self, user_tier: UserTier) -> str:
        """Get natural context based on tier without mentioning tier system"""
        contexts = {
            UserTier.TIER_1: "Focus on foundational thinking and clear problem-solving approaches.",
            UserTier.TIER_2: "You can reference our previous conversations and learned patterns to provide enhanced insights.",
            UserTier.TIER_3: "You have access to comprehensive context and can provide complete strategic guidance.",
            UserTier.STAFF: "Focus on project coordination, team dynamics, and workflow optimization.",
            UserTier.ADMIN: "Provide executive-level insights with business intelligence and system-wide perspective."
        }
        return contexts.get(user_tier, "")
    
    async def _generate_response(self, prompt: str) -> str:
        """Generate response using OpenAI with natural formatting"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "Please provide a helpful, natural response."}
                ],
                max_tokens=800,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm here to help you think through this systematically. Could you tell me more about what you're working on?"

# Initialize the universal chat system
universal_chat = UniversalChatSystem()

