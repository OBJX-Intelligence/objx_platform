#!/usr/bin/env python3
"""
OBJX Platform - Local Memory System
Implements a local memory system with MEM0 fallback
"""

import os
import json
import time
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import threading
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("OBJX-LocalMemory")

class LocalMemorySystem:
    """Local memory system with MEM0 fallback"""
    
    def __init__(self, storage_dir: str = "local_memory_store"):
        """Initialize the local memory system"""
        self.storage_dir = storage_dir
        self.mem0_client = None
        self.use_mem0 = False
        self.lock = threading.Lock()
        
        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Initialize memory index
        self.index_file = os.path.join(self.storage_dir, "memory_index.json")
        self.memory_index = self._load_index()
        
        logger.info(f"LocalMemorySystem initialized with storage at: {os.path.abspath(self.storage_dir)}")
    
    def _load_index(self) -> Dict[str, Dict[str, Any]]:
        """Load the memory index from disk"""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading memory index: {str(e)}")
                return {}
        return {}
    
    def _save_index(self):
        """Save the memory index to disk"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory_index, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving memory index: {str(e)}")
    
    def _get_memory_file(self, memory_id: str) -> str:
        """Get the file path for a memory"""
        return os.path.join(self.storage_dir, f"{memory_id}.json")
    
    def create_memory(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new memory"""
        with self.lock:
            # Try MEM0 first if available
            if self.use_mem0 and self.mem0_client:
                try:
                    # Format for MEM0
                    memory_data = {
                        "content": content,
                        "metadata": metadata or {}
                    }
                    
                    # Add to MEM0
                    result = self.mem0_client.add(
                        messages=[{"role": "system", "content": content}],
                        user_id=metadata.get("user_id", "default_user") if metadata else "default_user"
                    )
                    
                    return {
                        "id": result.get("id", str(uuid.uuid4())),
                        "content": content,
                        "metadata": metadata or {},
                        "created_at": datetime.now().isoformat(),
                        "source": "mem0"
                    }
                except Exception as e:
                    logger.error(f"Error creating memory in MEM0: {str(e)}")
                    # Fall back to local storage
            
            # Use local storage
            memory_id = str(uuid.uuid4())
            created_at = datetime.now().isoformat()
            
            memory = {
                "id": memory_id,
                "content": content,
                "metadata": metadata or {},
                "created_at": created_at,
                "source": "local"
            }
            
            # Save memory to file
            memory_file = self._get_memory_file(memory_id)
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory, f, indent=2)
            
            # Update index
            self.memory_index[memory_id] = {
                "content_preview": content[:100] + "..." if len(content) > 100 else content,
                "metadata": metadata or {},
                "created_at": created_at
            }
            self._save_index()
            
            return memory
    
    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Get a memory by ID"""
        # Try MEM0 first if available
        if self.use_mem0 and self.mem0_client:
            try:
                # Try to get from MEM0
                result = self.mem0_client.get(memory_id)
                if result:
                    return {
                        "id": memory_id,
                        "content": result.get("content", ""),
                        "metadata": result.get("metadata", {}),
                        "created_at": result.get("created_at", datetime.now().isoformat()),
                        "source": "mem0"
                    }
            except Exception as e:
                logger.error(f"Error getting memory from MEM0: {str(e)}")
                # Fall back to local storage
        
        # Use local storage
        if memory_id in self.memory_index:
            memory_file = self._get_memory_file(memory_id)
            if os.path.exists(memory_file):
                try:
                    with open(memory_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception as e:
                    logger.error(f"Error loading memory {memory_id}: {str(e)}")
        
        return None
    
    def update_memory(self, memory_id: str, content: str = None, metadata: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Update an existing memory"""
        with self.lock:
            # Try MEM0 first if available
            if self.use_mem0 and self.mem0_client:
                try:
                    # Try to update in MEM0
                    # Note: MEM0 doesn't support direct updates, so we'd need to implement this differently
                    pass
                except Exception as e:
                    logger.error(f"Error updating memory in MEM0: {str(e)}")
                    # Fall back to local storage
            
            # Use local storage
            memory = self.get_memory(memory_id)
            if not memory:
                return None
            
            if content is not None:
                memory["content"] = content
            
            if metadata is not None:
                memory["metadata"].update(metadata)
            
            memory["updated_at"] = datetime.now().isoformat()
            
            # Save updated memory
            memory_file = self._get_memory_file(memory_id)
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory, f, indent=2)
            
            # Update index
            self.memory_index[memory_id] = {
                "content_preview": memory["content"][:100] + "..." if len(memory["content"]) > 100 else memory["content"],
                "metadata": memory["metadata"],
                "created_at": memory["created_at"],
                "updated_at": memory["updated_at"]
            }
            self._save_index()
            
            return memory
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory"""
        with self.lock:
            # Try MEM0 first if available
            if self.use_mem0 and self.mem0_client:
                try:
                    # Try to delete from MEM0
                    # Note: MEM0 might not support direct deletion
                    pass
                except Exception as e:
                    logger.error(f"Error deleting memory from MEM0: {str(e)}")
                    # Fall back to local storage
            
            # Use local storage
            if memory_id in self.memory_index:
                # Remove from index
                del self.memory_index[memory_id]
                self._save_index()
                
                # Delete file
                memory_file = self._get_memory_file(memory_id)
                if os.path.exists(memory_file):
                    os.remove(memory_file)
                
                return True
            
            return False
    
    def search_memories(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memories by content and metadata"""
        # Try MEM0 first if available
        if self.use_mem0 and self.mem0_client:
            try:
                # Search in MEM0
                results = self.mem0_client.search(query, limit=limit)
                if results:
                    return [
                        {
                            "id": item.get("id", ""),
                            "content": item.get("content", ""),
                            "metadata": item.get("metadata", {}),
                            "created_at": item.get("created_at", ""),
                            "source": "mem0",
                            "score": item.get("score", 0)
                        }
                        for item in results
                    ]
            except Exception as e:
                logger.error(f"Error searching memories in MEM0: {str(e)}")
                # Fall back to local storage
        
        # Use local storage (simple keyword search)
        query = query.lower()
        results = []
        
        for memory_id, info in self.memory_index.items():
            memory = self.get_memory(memory_id)
            if not memory:
                continue
            
            # Check if query is in content
            content = memory.get("content", "").lower()
            if query in content:
                # Calculate a simple relevance score
                score = content.count(query) / len(content) if len(content) > 0 else 0
                results.append({
                    **memory,
                    "score": score
                })
                continue
            
            # Check if query is in metadata values
            for key, value in memory.get("metadata", {}).items():
                if isinstance(value, str) and query in value.lower():
                    results.append({
                        **memory,
                        "score": 0.5  # Lower score for metadata matches
                    })
                    break
        
        # Sort by score and limit results
        results.sort(key=lambda x: x.get("score", 0), reverse=True)
        return results[:limit]
    
    def get_recent_memories(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent memories"""
        # Try MEM0 first if available
        if self.use_mem0 and self.mem0_client:
            try:
                # Get recent memories from MEM0
                # Note: MEM0 might have a different API for this
                pass
            except Exception as e:
                logger.error(f"Error getting recent memories from MEM0: {str(e)}")
                # Fall back to local storage
        
        # Use local storage
        memories = []
        
        for memory_id in self.memory_index:
            memory = self.get_memory(memory_id)
            if memory:
                memories.append(memory)
        
        # Sort by created_at (newest first)
        memories.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return memories[:limit]
    
    def clear_all_memories(self) -> bool:
        """Clear all memories (use with caution)"""
        with self.lock:
            try:
                # Clear index
                self.memory_index = {}
                self._save_index()
                
                # Delete all memory files
                for filename in os.listdir(self.storage_dir):
                    if filename.endswith('.json') and filename != "memory_index.json":
                        os.remove(os.path.join(self.storage_dir, filename))
                
                return True
            except Exception as e:
                logger.error(f"Error clearing memories: {str(e)}")
                return False
    
    def set_mem0_client(self, mem0_client):
        """Set the MEM0 client for fallback"""
        self.mem0_client = mem0_client
        self.use_mem0 = mem0_client is not None
        logger.info(f"Using {'MEM0' if self.use_mem0 else 'local storage'} for memory")

# Create a singleton instance
memory_system = None

def get_memory_manager(use_mem0: bool = False, mem0_api_key: str = None):
    """Get the memory manager singleton instance"""
    global memory_system
    if memory_system is None:
        memory_system = LocalMemorySystem()
        
        # Try to set up MEM0 client if requested
        if use_mem0 and mem0_api_key:
            try:
                import mem0ai
                mem0_client = mem0ai.MemoryClient(api_key=mem0_api_key)
                memory_system.set_mem0_client(mem0_client)
            except Exception as e:
                logger.error(f"Error initializing MEM0 client: {str(e)}")
                logger.info("Using local storage for memory (MEM0 fallback)")
    
    return memory_system

# Test function
def test_memory_system():
    """Test the memory system"""
    print("Testing memory system...")
    
    # Get memory manager
    memory = get_memory_manager()
    
    # Create some test memories
    print("Creating test memories...")
    memory1 = memory.create_memory(
        content="This is a test memory about OBJX platform",
        metadata={"type": "test", "category": "platform"}
    )
    print(f"Created memory: {memory1['id']}")
    
    memory2 = memory.create_memory(
        content="Another test memory about AI agents",
        metadata={"type": "test", "category": "agents"}
    )
    print(f"Created memory: {memory2['id']}")
    
    # Get a memory
    print(f"Getting memory {memory1['id']}...")
    retrieved = memory.get_memory(memory1['id'])
    print(f"Retrieved: {retrieved['content']}")
    
    # Update a memory
    print(f"Updating memory {memory1['id']}...")
    updated = memory.update_memory(
        memory1['id'],
        content="Updated test memory about OBJX platform",
        metadata={"updated": True}
    )
    print(f"Updated: {updated['content']}")
    
    # Search memories
    print("Searching for 'OBJX'...")
    results = memory.search_memories("OBJX")
    print(f"Found {len(results)} results")
    for result in results:
        print(f"  {result['id']}: {result['content']}")
    
    # Get recent memories
    print("Getting recent memories...")
    recent = memory.get_recent_memories()
    print(f"Found {len(recent)} recent memories")
    
    # Delete a memory
    print(f"Deleting memory {memory2['id']}...")
    deleted = memory.delete_memory(memory2['id'])
    print(f"Deleted: {deleted}")
    
    print("Memory system test completed!")

if __name__ == "__main__":
    test_memory_system()

