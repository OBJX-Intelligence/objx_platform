"""
OBJX Intelligence Platform - Role-Based Memory Manager
Implements proper Mem0 memory permissions with user isolation and tier-based access
"""

from enum import Enum
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json

class UserTier(Enum):
    TIER_1 = "tier_1"  # NO memory access
    TIER_2 = "tier_2"  # Basic memory access
    TIER_3 = "tier_3"  # Full memory access
    STAFF = "staff"    # Project-specific memory
    ADMIN = "admin"    # Complete memory control

class MemoryScope(Enum):
    PERSONAL = "personal"      # User's own memories
    PROJECT = "project"        # Project-specific memories
    TEAM = "team"             # Team collaboration memories
    ORGANIZATION = "organization"  # Organization-wide memories
    SYSTEM = "system"         # System-level memories

class MemoryType(Enum):
    FACTUAL = "factual"       # Long-term factual knowledge
    EPISODIC = "episodic"     # Past interactions and experiences
    SEMANTIC = "semantic"     # Conceptual understanding
    WORKING = "working"       # Short-term session memory
    PREFERENCE = "preference" # User preferences and settings

@dataclass
class MemoryPermission:
    """Defines what memory operations a user tier can perform"""
    can_read: bool = False
    can_write: bool = False
    can_delete: bool = False
    can_search: bool = False
    can_analytics: bool = False
    scopes: List[MemoryScope] = None
    memory_types: List[MemoryType] = None
    
    def __post_init__(self):
        if self.scopes is None:
            self.scopes = []
        if self.memory_types is None:
            self.memory_types = []

class RoleBasedMemoryManager:
    """
    Manages memory access based on user roles and tiers
    Implements proper Mem0 patterns with enterprise security
    """
    
    def __init__(self, mem0_api_key: str):
        self.mem0_api_key = mem0_api_key
        self.permissions = self._initialize_permissions()
        
    def _initialize_permissions(self) -> Dict[UserTier, MemoryPermission]:
        """Initialize role-based memory permissions"""
        return {
            # Tier 1: NO memory access (stateless only)
            UserTier.TIER_1: MemoryPermission(
                can_read=False,
                can_write=False,
                can_delete=False,
                can_search=False,
                can_analytics=False,
                scopes=[],
                memory_types=[]
            ),
            
            # Tier 2: Basic memory access (personal only)
            UserTier.TIER_2: MemoryPermission(
                can_read=True,
                can_write=True,
                can_delete=False,  # Cannot delete memories
                can_search=True,
                can_analytics=False,
                scopes=[MemoryScope.PERSONAL],
                memory_types=[MemoryType.FACTUAL, MemoryType.PREFERENCE]
            ),
            
            # Tier 3: Full memory access (personal + advanced)
            UserTier.TIER_3: MemoryPermission(
                can_read=True,
                can_write=True,
                can_delete=True,
                can_search=True,
                can_analytics=True,
                scopes=[MemoryScope.PERSONAL],
                memory_types=[MemoryType.FACTUAL, MemoryType.EPISODIC, 
                             MemoryType.SEMANTIC, MemoryType.PREFERENCE]
            ),
            
            # Staff: Project-specific + team collaboration
            UserTier.STAFF: MemoryPermission(
                can_read=True,
                can_write=True,
                can_delete=True,
                can_search=True,
                can_analytics=True,
                scopes=[MemoryScope.PERSONAL, MemoryScope.PROJECT, MemoryScope.TEAM],
                memory_types=[MemoryType.FACTUAL, MemoryType.EPISODIC, 
                             MemoryType.SEMANTIC, MemoryType.PREFERENCE]
            ),
            
            # Admin: Complete memory control
            UserTier.ADMIN: MemoryPermission(
                can_read=True,
                can_write=True,
                can_delete=True,
                can_search=True,
                can_analytics=True,
                scopes=[MemoryScope.PERSONAL, MemoryScope.PROJECT, 
                       MemoryScope.TEAM, MemoryScope.ORGANIZATION, MemoryScope.SYSTEM],
                memory_types=[MemoryType.FACTUAL, MemoryType.EPISODIC, 
                             MemoryType.SEMANTIC, MemoryType.WORKING, MemoryType.PREFERENCE]
            )
        }
    
    def check_permission(self, user_tier: UserTier, operation: str, 
                        scope: MemoryScope = None, memory_type: MemoryType = None) -> bool:
        """Check if user has permission for specific memory operation"""
        if user_tier not in self.permissions:
            return False
            
        perm = self.permissions[user_tier]
        
        # Check operation permission
        if operation == "read" and not perm.can_read:
            return False
        elif operation == "write" and not perm.can_write:
            return False
        elif operation == "delete" and not perm.can_delete:
            return False
        elif operation == "search" and not perm.can_search:
            return False
        elif operation == "analytics" and not perm.can_analytics:
            return False
            
        # Check scope permission
        if scope and scope not in perm.scopes:
            return False
            
        # Check memory type permission
        if memory_type and memory_type not in perm.memory_types:
            return False
            
        return True
    
    def get_user_memory_id(self, user_id: str, scope: MemoryScope = MemoryScope.PERSONAL) -> str:
        """Generate isolated memory ID for user and scope"""
        return f"{user_id}_{scope.value}"
    
    def create_memory(self, user_id: str, user_tier: UserTier, content: str, 
                     memory_type: MemoryType, scope: MemoryScope = MemoryScope.PERSONAL,
                     metadata: Dict = None) -> Optional[str]:
        """Create memory with role-based permissions"""
        
        # Check permissions
        if not self.check_permission(user_tier, "write", scope, memory_type):
            raise PermissionError(f"User tier {user_tier.value} cannot create {memory_type.value} memory in {scope.value} scope")
        
        # Generate isolated memory ID
        memory_id = self.get_user_memory_id(user_id, scope)
        
        # Prepare memory data with metadata
        memory_data = {
            "content": content,
            "user_id": user_id,
            "memory_type": memory_type.value,
            "scope": scope.value,
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        # Here you would integrate with actual Mem0 API
        # For now, return a mock memory ID
        return f"mem_{user_id}_{datetime.now().timestamp()}"
    
    def search_memories(self, user_id: str, user_tier: UserTier, query: str,
                       scope: MemoryScope = MemoryScope.PERSONAL,
                       memory_type: MemoryType = None) -> List[Dict]:
        """Search memories with role-based filtering"""
        
        # Check permissions
        if not self.check_permission(user_tier, "search", scope, memory_type):
            raise PermissionError(f"User tier {user_tier.value} cannot search memories in {scope.value} scope")
        
        # Generate isolated memory ID for search
        memory_id = self.get_user_memory_id(user_id, scope)
        
        # Here you would integrate with actual Mem0 search API
        # For now, return mock results
        return [
            {
                "id": f"mem_{user_id}_1",
                "content": f"Sample memory for {query}",
                "memory_type": memory_type.value if memory_type else "factual",
                "scope": scope.value,
                "relevance_score": 0.95,
                "created_at": datetime.now().isoformat()
            }
        ]
    
    def get_memory_analytics(self, user_id: str, user_tier: UserTier) -> Dict:
        """Get memory analytics based on user permissions"""
        
        if not self.check_permission(user_tier, "analytics"):
            raise PermissionError(f"User tier {user_tier.value} cannot access memory analytics")
        
        # Return analytics based on user tier
        if user_tier == UserTier.ADMIN:
            # Admin gets full analytics
            return {
                "total_memories": 150,
                "client_memories": 45,
                "project_memories": 67,
                "team_memories": 23,
                "system_memories": 15,
                "health_score": "98%",
                "user_breakdown": {
                    "tier_1_users": 12,
                    "tier_2_users": 8,
                    "tier_3_users": 5,
                    "staff_users": 3,
                    "admin_users": 2
                }
            }
        elif user_tier == UserTier.STAFF:
            # Staff gets project-focused analytics
            return {
                "total_memories": 89,
                "project_memories": 67,
                "team_memories": 22,
                "health_score": "95%",
                "active_projects": 12
            }
        else:
            # Tier 3 gets personal analytics
            return {
                "total_memories": 25,
                "personal_memories": 25,
                "health_score": "92%"
            }
    
    def get_accessible_scopes(self, user_tier: UserTier) -> List[MemoryScope]:
        """Get all memory scopes accessible to user tier"""
        if user_tier in self.permissions:
            return self.permissions[user_tier].scopes
        return []
    
    def get_accessible_memory_types(self, user_tier: UserTier) -> List[MemoryType]:
        """Get all memory types accessible to user tier"""
        if user_tier in self.permissions:
            return self.permissions[user_tier].memory_types
        return []

# Global instance
role_based_memory = RoleBasedMemoryManager(mem0_api_key="your_mem0_api_key")

