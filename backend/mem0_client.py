#!/usr/bin/env python3
"""
OBJX Platform - MEM0 Client
Implements MEM0 integration with tier structure and local fallback
"""

import os
import json
import time
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

# Import MEM0 SDK
try:
    from mem0 import MemoryClient
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False
    print("MEM0 SDK not available. Install with: pip install mem0ai")

# Import local memory fallback
try:
    from local_memory import LocalMemorySystem
    LOCAL_MEMORY_AVAILABLE = True
except ImportError:
    LOCAL_MEMORY_AVAILABLE = False
    print("Local memory fallback not available.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("OBJX-Memory")

class OBJXMemoryClient:
    """OBJX Memory Client with MEM0 integration and local fallback"""
    
    def __init__(self, api_key=None, user_tier=1, user_id=None):
        """Initialize the memory client
        
        Args:
            api_key: MEM0 API key (optional, will use env var if not provided)
            user_tier: User tier level (1, 2, or 3)
            user_id: User ID for memory segregation
        """
        self.api_key = api_key or os.getenv("MEM0_API_KEY")
        self.user_tier = user_tier
        self.user_id = user_id or str(uuid.uuid4())
        self.mem0_client = None
        self.local_memory = None
        
        # Initialize based on tier
        if self.user_tier == 1:
            # Tier 1 has no memory
            logger.info(f"Initializing Tier 1 memory client for user {self.user_id} (no memory)")
            self.has_memory = False
        else:
            # Tier 2 and 3 have memory
            self.has_memory = True
            
            # Try to initialize MEM0 client
            if MEM0_AVAILABLE and self.api_key:
                try:
                    self.mem0_client = MemoryClient(api_key=self.api_key)
                    logger.info(f"Initialized MEM0 client for user {self.user_id} (Tier {self.user_tier})")
                except Exception as e:
                    logger.error(f"Failed to initialize MEM0 client: {str(e)}")
                    self.mem0_client = None
            
            # Initialize local fallback if needed
            if not self.mem0_client and LOCAL_MEMORY_AVAILABLE:
                storage_dir = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    f"local_memory_store/tier{self.user_tier}/{self.user_id}"
                )
                self.local_memory = LocalMemorySystem(storage_dir=storage_dir)
                logger.info(f"Initialized local memory fallback for user {self.user_id} (Tier {self.user_tier})")
    
    def add_memory(self, messages, metadata=None):
        """Add memory from conversation messages
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            metadata: Additional metadata to store with the memory
        
        Returns:
            Memory ID if successful, None otherwise
        """
        if not self.has_memory:
            logger.info("Memory storage not available for this tier")
            return None
        
        metadata = metadata or {}
        metadata.update({
            "user_id": self.user_id,
            "user_tier": self.user_tier,
            "timestamp": datetime.now().isoformat()
        })
        
        # Try MEM0 first
        if self.mem0_client:
            try:
                result = self.mem0_client.add(messages, user_id=self.user_id, **metadata)
                logger.info(f"Added memory to MEM0 for user {self.user_id}")
                return result
            except Exception as e:
                logger.error(f"Failed to add memory to MEM0: {str(e)}")
        
        # Fall back to local storage
        if self.local_memory:
            try:
                # Convert messages to a single content string for local storage
                content = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
                result = self.local_memory.create_memory(content, metadata)
                logger.info(f"Added memory to local storage for user {self.user_id}")
                return result.get("id") if result else None
            except Exception as e:
                logger.error(f"Failed to add memory to local storage: {str(e)}")
        
        return None
    
    def search_memory(self, query, limit=10):
        """Search memory with a query
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
        
        Returns:
            List of memory results
        """
        if not self.has_memory:
            logger.info("Memory search not available for this tier")
            return []
        
        # Try MEM0 first
        if self.mem0_client:
            try:
                results = self.mem0_client.search(query, user_id=self.user_id, limit=limit)
                logger.info(f"Searched MEM0 for user {self.user_id} with query: {query}")
                return results
            except Exception as e:
                logger.error(f"Failed to search MEM0: {str(e)}")
        
        # Fall back to local storage
        if self.local_memory:
            try:
                results = self.local_memory.search_memories(query, limit)
                logger.info(f"Searched local storage for user {self.user_id} with query: {query}")
                return results
            except Exception as e:
                logger.error(f"Failed to search local storage: {str(e)}")
        
        return []
    
    def get_recent_memories(self, limit=10):
        """Get recent memories
        
        Args:
            limit: Maximum number of memories to return
        
        Returns:
            List of recent memories
        """
        if not self.has_memory:
            logger.info("Memory retrieval not available for this tier")
            return []
        
        # Try MEM0 first (Note: MEM0 API might not have a direct "get recent" method)
        if self.mem0_client:
            try:
                # This is a placeholder - actual implementation would depend on MEM0 API
                # For now, we'll search with an empty query to get recent memories
                results = self.mem0_client.search("", user_id=self.user_id, limit=limit)
                logger.info(f"Retrieved recent memories from MEM0 for user {self.user_id}")
                return results
            except Exception as e:
                logger.error(f"Failed to retrieve recent memories from MEM0: {str(e)}")
        
        # Fall back to local storage
        if self.local_memory:
            try:
                results = self.local_memory.get_recent_memories(limit)
                logger.info(f"Retrieved recent memories from local storage for user {self.user_id}")
                return results
            except Exception as e:
                logger.error(f"Failed to retrieve recent memories from local storage: {str(e)}")
        
        return []
    
    def get_memory_by_id(self, memory_id):
        """Get a specific memory by ID
        
        Args:
            memory_id: ID of the memory to retrieve
        
        Returns:
            Memory object if found, None otherwise
        """
        if not self.has_memory:
            logger.info("Memory retrieval not available for this tier")
            return None
        
        # Try MEM0 first
        if self.mem0_client:
            try:
                # This is a placeholder - actual implementation would depend on MEM0 API
                # MEM0 might not have a direct "get by ID" method
                logger.warning("MEM0 get_memory_by_id not implemented")
                return None
            except Exception as e:
                logger.error(f"Failed to retrieve memory from MEM0: {str(e)}")
        
        # Fall back to local storage
        if self.local_memory:
            try:
                result = self.local_memory.get_memory(memory_id)
                logger.info(f"Retrieved memory {memory_id} from local storage")
                return result
            except Exception as e:
                logger.error(f"Failed to retrieve memory from local storage: {str(e)}")
        
        return None
    
    def delete_memory(self, memory_id):
        """Delete a memory by ID
        
        Args:
            memory_id: ID of the memory to delete
        
        Returns:
            True if successful, False otherwise
        """
        if not self.has_memory:
            logger.info("Memory deletion not available for this tier")
            return False
        
        # Try MEM0 first
        if self.mem0_client:
            try:
                # This is a placeholder - actual implementation would depend on MEM0 API
                logger.warning("MEM0 delete_memory not implemented")
                return False
            except Exception as e:
                logger.error(f"Failed to delete memory from MEM0: {str(e)}")
        
        # Fall back to local storage
        if self.local_memory:
            try:
                result = self.local_memory.delete_memory(memory_id)
                logger.info(f"Deleted memory {memory_id} from local storage")
                return result
            except Exception as e:
                logger.error(f"Failed to delete memory from local storage: {str(e)}")
        
        return False
    
    def clear_all_memories(self):
        """Clear all memories for the current user
        
        Returns:
            True if successful, False otherwise
        """
        if not self.has_memory:
            logger.info("Memory clearing not available for this tier")
            return False
        
        # Try MEM0 first
        if self.mem0_client:
            try:
                # This is a placeholder - actual implementation would depend on MEM0 API
                logger.warning("MEM0 clear_all_memories not implemented")
                return False
            except Exception as e:
                logger.error(f"Failed to clear memories from MEM0: {str(e)}")
        
        # Fall back to local storage
        if self.local_memory:
            try:
                result = self.local_memory.clear_all_memories()
                logger.info(f"Cleared all memories for user {self.user_id} from local storage")
                return result
            except Exception as e:
                logger.error(f"Failed to clear memories from local storage: {str(e)}")
        
        return False

# Factory function to get memory client based on tier
def get_memory_client(user_tier=1, user_id=None, api_key=None):
    """Get a memory client based on user tier
    
    Args:
        user_tier: User tier level (1, 2, or 3)
        user_id: User ID for memory segregation
        api_key: MEM0 API key (optional, will use env var if not provided)
    
    Returns:
        OBJXMemoryClient instance
    """
    return OBJXMemoryClient(
        api_key=api_key or os.getenv("MEM0_API_KEY"),
        user_tier=user_tier,
        user_id=user_id
    )

# Test function
def test_memory_client():
    """Test the memory client with different tiers"""
    print("Testing OBJX Memory Client...")
    
    # Test Tier 1 (no memory)
    tier1_client = get_memory_client(user_tier=1, user_id="test_user_tier1")
    print(f"Tier 1 client has memory: {tier1_client.has_memory}")
    
    # Test Tier 2 (with memory)
    tier2_client = get_memory_client(user_tier=2, user_id="test_user_tier2")
    print(f"Tier 2 client has memory: {tier2_client.has_memory}")
    
    # Test adding memory
    if tier2_client.has_memory:
        messages = [
            {"role": "user", "content": "What is the capital of France?"},
            {"role": "assistant", "content": "The capital of France is Paris."}
        ]
        
        memory_id = tier2_client.add_memory(messages, {"topic": "geography"})
        print(f"Added memory with ID: {memory_id}")
        
        # Test searching memory
        results = tier2_client.search_memory("France")
        print(f"Search results: {len(results)} memories found")
        
        # Test getting recent memories
        recent = tier2_client.get_recent_memories(5)
        print(f"Recent memories: {len(recent)} memories found")
    
    # Test Tier 3 (with memory)
    tier3_client = get_memory_client(user_tier=3, user_id="test_user_tier3")
    print(f"Tier 3 client has memory: {tier3_client.has_memory}")
    
    print("Memory client test completed!")

if __name__ == "__main__":
    test_memory_client()

