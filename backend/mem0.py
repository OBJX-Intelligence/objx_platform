#!/usr/bin/env python3
"""
MEM0 Client - Memory System for OBJX Platform
Simplified implementation for the OBJX Platform
"""

import os
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

class MemoryClient:
    """
    Client for interacting with the MEM0 memory system
    This is a simplified implementation that stores memories locally
    In production, this would connect to a proper memory service
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the memory client"""
        self.api_key = api_key or os.getenv('MEM0_API_KEY', 'default_key')
        self.memories = {}  # In-memory storage for memories
    
    def add(self, messages: List[Dict[str, str]], user_id: str = 'default_user') -> Dict[str, Any]:
        """Add a memory from messages"""
        
        # Extract content from messages
        content = ""
        for message in messages:
            role = message.get('role', 'unknown')
            message_content = message.get('content', '')
            content += f"{role}: {message_content}\n"
        
        # Create memory object
        memory_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        memory = {
            'id': memory_id,
            'user_id': user_id,
            'memory': content,
            'created_at': timestamp,
            'metadata': {
                'source': 'conversation',
                'message_count': len(messages)
            }
        }
        
        # Store memory
        if user_id not in self.memories:
            self.memories[user_id] = []
        
        self.memories[user_id].append(memory)
        
        return {
            'id': memory_id,
            'created_at': timestamp
        }
    
    def search(self, query: str, user_id: str = 'default_user', limit: int = 10) -> List[Dict[str, Any]]:
        """Search for memories"""
        
        # Get memories for the user
        user_memories = self.memories.get(user_id, [])
        
        # If query is empty, return all memories
        if not query:
            return user_memories[:limit]
        
        # Simple search implementation
        # In production, this would use proper semantic search
        results = []
        for memory in user_memories:
            memory_content = memory.get('memory', '').lower()
            if query.lower() in memory_content:
                # Calculate a mock relevance score
                relevance = 0.5 + (memory_content.count(query.lower()) * 0.1)
                memory_copy = memory.copy()
                memory_copy['relevance_score'] = min(relevance, 0.99)
                results.append(memory_copy)
        
        # Sort by relevance
        results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return results[:limit]
    
    def get(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific memory by ID"""
        
        # Search all users' memories
        for user_id, memories in self.memories.items():
            for memory in memories:
                if memory.get('id') == memory_id:
                    return memory
        
        return None
    
    def delete(self, memory_id: str) -> bool:
        """Delete a memory by ID"""
        
        # Search all users' memories
        for user_id, memories in self.memories.items():
            for i, memory in enumerate(memories):
                if memory.get('id') == memory_id:
                    # Remove the memory
                    self.memories[user_id].pop(i)
                    return True
        
        return False
    
    def clear(self, user_id: str = 'default_user') -> int:
        """Clear all memories for a user"""
        
        if user_id not in self.memories:
            return 0
        
        count = len(self.memories[user_id])
        self.memories[user_id] = []
        
        return count

