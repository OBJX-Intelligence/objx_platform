"""
OBJX Intelligence Platform - Memory Command Center
Mem0-integrated memory management system with enterprise-grade controls
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum

class MemoryType(Enum):
    CLIENT = "client"
    PROJECT = "project"
    SYSTEM = "system"
    PATTERN = "pattern"
    INSIGHT = "insight"

class MemoryPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Memory:
    id: str
    content: str
    memory_type: MemoryType
    priority: MemoryPriority
    client_id: Optional[str]
    project_id: Optional[str]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    relevance_score: float
    access_count: int
    metadata: Dict[str, Any]

class MemoryCommandCenter:
    """
    Enterprise-grade memory management system with Mem0 integration
    """
    
    def __init__(self):
        self.mem0_api_key = os.getenv('MEM0_API_KEY')
        self.mem0_base_url = os.getenv('MEM0_API_BASE', 'https://api.mem0.ai')
        self.headers = {
            'Authorization': f'Bearer {self.mem0_api_key}',
            'Content-Type': 'application/json'
        }
    
    def get_all_memories(self, user_id: Optional[str] = None) -> List[Memory]:
        """Retrieve all memories from Mem0 with enhanced metadata"""
        try:
            url = f"{self.mem0_base_url}/v1/memories"
            params = {}
            if user_id:
                params['user_id'] = user_id
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            memories_data = response.json()
            memories = []
            
            for mem_data in memories_data.get('memories', []):
                memory = Memory(
                    id=mem_data.get('id'),
                    content=mem_data.get('memory'),
                    memory_type=MemoryType(mem_data.get('metadata', {}).get('type', 'system')),
                    priority=MemoryPriority(mem_data.get('metadata', {}).get('priority', 'medium')),
                    client_id=mem_data.get('metadata', {}).get('client_id'),
                    project_id=mem_data.get('metadata', {}).get('project_id'),
                    tags=mem_data.get('metadata', {}).get('tags', []),
                    created_at=datetime.fromisoformat(mem_data.get('created_at', datetime.now().isoformat())),
                    updated_at=datetime.fromisoformat(mem_data.get('updated_at', datetime.now().isoformat())),
                    relevance_score=mem_data.get('score', 0.0),
                    access_count=mem_data.get('metadata', {}).get('access_count', 0),
                    metadata=mem_data.get('metadata', {})
                )
                memories.append(memory)
            
            return memories
            
        except Exception as e:
            print(f"Error retrieving memories: {e}")
            return []
    
    def create_memory(self, content: str, user_id: str, memory_type: MemoryType = MemoryType.SYSTEM,
                     priority: MemoryPriority = MemoryPriority.MEDIUM, client_id: Optional[str] = None,
                     project_id: Optional[str] = None, tags: List[str] = None) -> Optional[str]:
        """Create a new memory in Mem0 with enhanced metadata"""
        try:
            url = f"{self.mem0_base_url}/v1/memories"
            
            metadata = {
                'type': memory_type.value,
                'priority': priority.value,
                'created_by': 'admin',
                'access_count': 0,
                'tags': tags or []
            }
            
            if client_id:
                metadata['client_id'] = client_id
            if project_id:
                metadata['project_id'] = project_id
            
            payload = {
                'messages': [{'role': 'user', 'content': content}],
                'user_id': user_id,
                'metadata': metadata
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result.get('id')
            
        except Exception as e:
            print(f"Error creating memory: {e}")
            return None
    
    def update_memory(self, memory_id: str, content: Optional[str] = None,
                     metadata: Optional[Dict] = None) -> bool:
        """Update an existing memory in Mem0"""
        try:
            url = f"{self.mem0_base_url}/v1/memories/{memory_id}"
            
            payload = {}
            if content:
                payload['memory'] = content
            if metadata:
                payload['metadata'] = metadata
            
            response = requests.put(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            return True
            
        except Exception as e:
            print(f"Error updating memory: {e}")
            return False
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory from Mem0"""
        try:
            url = f"{self.mem0_base_url}/v1/memories/{memory_id}"
            
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            
            return True
            
        except Exception as e:
            print(f"Error deleting memory: {e}")
            return False
    
    def search_memories(self, query: str, user_id: Optional[str] = None,
                       memory_type: Optional[MemoryType] = None,
                       client_id: Optional[str] = None) -> List[Memory]:
        """Search memories with advanced filtering"""
        try:
            url = f"{self.mem0_base_url}/v1/memories/search"
            
            payload = {
                'query': query,
                'limit': 50
            }
            
            if user_id:
                payload['user_id'] = user_id
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            results = response.json()
            memories = []
            
            for mem_data in results.get('memories', []):
                # Apply additional filters
                metadata = mem_data.get('metadata', {})
                
                if memory_type and metadata.get('type') != memory_type.value:
                    continue
                if client_id and metadata.get('client_id') != client_id:
                    continue
                
                memory = Memory(
                    id=mem_data.get('id'),
                    content=mem_data.get('memory'),
                    memory_type=MemoryType(metadata.get('type', 'system')),
                    priority=MemoryPriority(metadata.get('priority', 'medium')),
                    client_id=metadata.get('client_id'),
                    project_id=metadata.get('project_id'),
                    tags=metadata.get('tags', []),
                    created_at=datetime.fromisoformat(mem_data.get('created_at', datetime.now().isoformat())),
                    updated_at=datetime.fromisoformat(mem_data.get('updated_at', datetime.now().isoformat())),
                    relevance_score=mem_data.get('score', 0.0),
                    access_count=metadata.get('access_count', 0),
                    metadata=metadata
                )
                memories.append(memory)
            
            return memories
            
        except Exception as e:
            print(f"Error searching memories: {e}")
            return []
    
    def get_memory_analytics(self) -> Dict[str, Any]:
        """Get comprehensive memory analytics"""
        memories = self.get_all_memories()
        
        analytics = {
            'total_memories': len(memories),
            'memory_types': {},
            'priority_distribution': {},
            'client_distribution': {},
            'recent_activity': [],
            'top_accessed': [],
            'memory_health': {
                'outdated_memories': 0,
                'low_relevance': 0,
                'orphaned_memories': 0
            }
        }
        
        # Calculate distributions
        for memory in memories:
            # Memory types
            mem_type = memory.memory_type.value
            analytics['memory_types'][mem_type] = analytics['memory_types'].get(mem_type, 0) + 1
            
            # Priority distribution
            priority = memory.priority.value
            analytics['priority_distribution'][priority] = analytics['priority_distribution'].get(priority, 0) + 1
            
            # Client distribution
            if memory.client_id:
                analytics['client_distribution'][memory.client_id] = analytics['client_distribution'].get(memory.client_id, 0) + 1
            
            # Memory health checks
            days_old = (datetime.now() - memory.created_at).days
            if days_old > 90:
                analytics['memory_health']['outdated_memories'] += 1
            if memory.relevance_score < 0.3:
                analytics['memory_health']['low_relevance'] += 1
            if not memory.client_id and not memory.project_id:
                analytics['memory_health']['orphaned_memories'] += 1
        
        # Recent activity (last 7 days)
        recent_cutoff = datetime.now() - timedelta(days=7)
        analytics['recent_activity'] = [
            {
                'id': mem.id,
                'content': mem.content[:100] + '...' if len(mem.content) > 100 else mem.content,
                'type': mem.memory_type.value,
                'created_at': mem.created_at.isoformat()
            }
            for mem in memories 
            if mem.created_at > recent_cutoff
        ]
        
        # Top accessed memories
        analytics['top_accessed'] = [
            {
                'id': mem.id,
                'content': mem.content[:100] + '...' if len(mem.content) > 100 else mem.content,
                'access_count': mem.access_count,
                'relevance_score': mem.relevance_score
            }
            for mem in sorted(memories, key=lambda x: x.access_count, reverse=True)[:10]
        ]
        
        return analytics
    
    def bulk_update_memories(self, memory_ids: List[str], updates: Dict[str, Any]) -> Dict[str, bool]:
        """Bulk update multiple memories"""
        results = {}
        
        for memory_id in memory_ids:
            success = self.update_memory(memory_id, metadata=updates)
            results[memory_id] = success
        
        return results
    
    def export_memories(self, user_id: Optional[str] = None, 
                       memory_type: Optional[MemoryType] = None) -> Dict[str, Any]:
        """Export memories for backup or migration"""
        memories = self.get_all_memories(user_id)
        
        if memory_type:
            memories = [mem for mem in memories if mem.memory_type == memory_type]
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'total_memories': len(memories),
            'memories': [
                {
                    'id': mem.id,
                    'content': mem.content,
                    'type': mem.memory_type.value,
                    'priority': mem.priority.value,
                    'client_id': mem.client_id,
                    'project_id': mem.project_id,
                    'tags': mem.tags,
                    'created_at': mem.created_at.isoformat(),
                    'updated_at': mem.updated_at.isoformat(),
                    'relevance_score': mem.relevance_score,
                    'access_count': mem.access_count,
                    'metadata': mem.metadata
                }
                for mem in memories
            ]
        }
        
        return export_data

# Initialize the Memory Command Center
memory_center = MemoryCommandCenter()

