"""
Authorization and Context-Aware Security System for IPL.
Implements user authentication, role-based access control, and policy-based security
with token optimization and fast performance.
"""
import hashlib
import time
import json
from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import secrets


class UserRole(Enum):
    """User roles with permission levels."""
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class Permission(Enum):
    """Granular permissions for operations."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    ADMIN = "admin"
    SYSTEM = "system"
    NETWORK = "network"
    FILE_SYSTEM = "file_system"


@dataclass
class SecurityContext:
    """Security context for authorization decisions."""
    user_id: str
    role: UserRole
    permissions: Set[Permission]
    session_id: str
    ip_address: str = "unknown"
    user_agent: str = "unknown"
    timestamp: float = field(default_factory=time.time)
    context_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "role": self.role.value,
            "permissions": [p.value for p in self.permissions],
            "session_id": self.session_id,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp
        }


@dataclass
class SecurityPolicy:
    """Security policy for authorization decisions."""
    policy_id: str
    name: str
    description: str
    allowed_roles: Set[UserRole]
    required_permissions: Set[Permission]
    denied_patterns: List[str] = field(default_factory=list)
    context_requirements: Dict[str, Any] = field(default_factory=dict)
    priority: int = 100  # Higher priority policies override lower ones


@dataclass
class AuthorizationDecision:
    """Result of authorization check."""
    allowed: bool
    reason: str
    confidence: float
    token_usage: int = 0
    decision_time_ms: float = 0.0
    policy_used: Optional[str] = None
    context_verified: bool = False


class TokenOptimizedAuthCache:
    """Optimized cache for authorization decisions with token tracking."""
    
    def __init__(self, max_size: int = 500, ttl_seconds: int = 1800):
        self.cache: Dict[str, Tuple[AuthorizationDecision, float]] = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.hit_count = 0
        self.miss_count = 0
        self.total_tokens_saved = 0
        
    def _generate_key(self, user_id: str, operation: str, context_hash: str) -> str:
        """Generate cache key with user, operation, and context."""
        key_data = f"{user_id}:{operation}:{context_hash}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    def get(self, user_id: str, operation: str, context: SecurityContext) -> Optional[AuthorizationDecision]:
        """Get cached authorization decision."""
        context_hash = self._hash_context(context)
        key = self._generate_key(user_id, operation, context_hash)
        
        if key not in self.cache:
            self.miss_count += 1
            return None
            
        decision, timestamp = self.cache[key]
        
        # Check TTL
        if time.time() - timestamp > self.ttl_seconds:
            del self.cache[key]
            self.miss_count += 1
            return None
            
        self.hit_count += 1
        self.total_tokens_saved += decision.token_usage
        return decision
    
    def set(self, user_id: str, operation: str, context: SecurityContext, decision: AuthorizationDecision):
        """Cache authorization decision."""
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
            
        context_hash = self._hash_context(context)
        key = self._generate_key(user_id, operation, context_hash)
        self.cache[key] = (decision, time.time())
    
    def _hash_context(self, context: SecurityContext) -> str:
        """Hash context for cache key."""
        context_data = {
            "user_id": context.user_id,
            "role": context.role.value,
            "permissions": sorted([p.value for p in context.permissions]),
            "ip_address": context.ip_address
        }
        return hashlib.sha256(json.dumps(context_data, sort_keys=True).encode()).hexdigest()
    
    def _evict_oldest(self):
        """Evict oldest cache entries."""
        if not self.cache:
            return
            
        sorted_items = sorted(self.cache.items(), key=lambda x: x[1][1])
        evict_count = max(1, len(sorted_items) // 10)
        
        for key, _ in sorted_items[:evict_count]:
            del self.cache[key]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.hit_count + self.miss_count
        hit_rate = self.hit_count / total_requests if total_requests > 0 else 0
        
        return {
            "cache_size": len(self.cache),
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": round(hit_rate, 4),
            "total_tokens_saved": self.total_tokens_saved,
            "estimated_cost_saved_usd": self.total_tokens_saved * 0.00001  # Rough estimate
        }


class UserDatabase:
    """Fast in-memory user database with authentication."""
    
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}
        self.sessions: Dict[str, SecurityContext] = {}
        self._initialize_default_users()
    
    def _initialize_default_users(self):
        """Initialize default users for testing."""
        # Super admin with all permissions
        self.users["admin"] = {
            "password_hash": self._hash_password("admin123"),
            "role": UserRole.SUPER_ADMIN,
            "permissions": set(Permission),
            "metadata": {"created_at": time.time()}
        }
        
        # Regular admin
        self.users["moderator"] = {
            "password_hash": self._hash_password("mod123"),
            "role": UserRole.ADMIN,
            "permissions": {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.EXECUTE},
            "metadata": {"created_at": time.time()}
        }
        
        # Regular user
        self.users["user"] = {
            "password_hash": self._hash_password("user123"),
            "role": UserRole.USER,
            "permissions": {Permission.READ, Permission.WRITE},
            "metadata": {"created_at": time.time()}
        }
        
        # Guest
        self.users["guest"] = {
            "password_hash": self._hash_password("guest123"),
            "role": UserRole.GUEST,
            "permissions": {Permission.READ},
            "metadata": {"created_at": time.time()}
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash password for storage."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> Optional[SecurityContext]:
        """Authenticate user and return security context."""
        if username not in self.users:
            return None
            
        user = self.users[username]
        password_hash = self._hash_password(password)
        
        if user["password_hash"] != password_hash:
            return None
        
        # Create session
        session_id = secrets.token_hex(16)
        context = SecurityContext(
            user_id=username,
            role=user["role"],
            permissions=user["permissions"],
            session_id=session_id
        )
        
        self.sessions[session_id] = context
        return context
    
    def get_context_by_session(self, session_id: str) -> Optional[SecurityContext]:
        """Get security context by session ID."""
        return self.sessions.get(session_id)
    
    def create_user(self, username: str, password: str, role: UserRole, permissions: Set[Permission]):
        """Create new user."""
        if username in self.users:
            raise ValueError(f"User {username} already exists")
            
        self.users[username] = {
            "password_hash": self._hash_password(password),
            "role": role,
            "permissions": permissions,
            "metadata": {"created_at": time.time()}
        }
    
    def get_user_permissions(self, username: str) -> Set[Permission]:
        """Get user permissions."""
        if username not in self.users:
            return set()
        return self.users[username]["permissions"]


class PolicyEngine:
    """Fast policy-based security engine with caching."""
    
    def __init__(self):
        self.policies: List[SecurityPolicy] = []
        self.cache = TokenOptimizedAuthCache()
        self._initialize_default_policies()
    
    def _initialize_default_policies(self):
        """Initialize default security policies."""
        # Admin can do system operations
        self.policies.append(SecurityPolicy(
            policy_id="admin_system",
            name="Admin System Operations",
            description="Allow admins to perform system operations",
            allowed_roles={UserRole.ADMIN, UserRole.SUPER_ADMIN},
            required_permissions={Permission.SYSTEM, Permission.ADMIN},
            priority=200
        ))
        
        # Users can read and write their own data
        self.policies.append(SecurityPolicy(
            policy_id="user_data",
            name="User Data Operations",
            description="Allow users to read and write their own data",
            allowed_roles={UserRole.USER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
            required_permissions={Permission.READ, Permission.WRITE},
            priority=100
        ))
        
        # File deletion requires specific permissions
        self.policies.append(SecurityPolicy(
            policy_id="file_deletion",
            name="File Deletion Control",
            description="Control file deletion operations",
            allowed_roles={UserRole.ADMIN, UserRole.SUPER_ADMIN},
            required_permissions={Permission.DELETE, Permission.FILE_SYSTEM},
            denied_patterns=["rm -rf", "delete.*system", "drop.*database"],
            priority=150
        ))
        
        # Network operations require admin
        self.policies.append(SecurityPolicy(
            policy_id="network_ops",
            name="Network Operations",
            description="Control network operations",
            allowed_roles={UserRole.ADMIN, UserRole.SUPER_ADMIN},
            required_permissions={Permission.NETWORK},
            priority=150
        ))
    
    def evaluate_authorization(
        self,
        context: SecurityContext,
        operation: str,
        operation_details: Dict[str, Any] = None
    ) -> AuthorizationDecision:
        """Evaluate authorization using policy engine with caching."""
        start_time = time.time()
        
        # Check cache first
        cached_decision = self.cache.get(context.user_id, operation, context)
        if cached_decision:
            cached_decision.decision_time_ms = (time.time() - start_time) * 1000
            return cached_decision
        
        # Evaluate policies
        decision = self._evaluate_policies(context, operation, operation_details or {})
        decision.decision_time_ms = (time.time() - start_time) * 1000
        
        # Cache the decision
        self.cache.set(context.user_id, operation, context, decision)
        
        return decision
    
    def _evaluate_policies(
        self,
        context: SecurityContext,
        operation: str,
        operation_details: Dict[str, Any]
    ) -> AuthorizationDecision:
        """Evaluate security policies."""
        # Sort policies by priority (highest first)
        sorted_policies = sorted(self.policies, key=lambda p: p.priority, reverse=True)
        
        for policy in sorted_policies:
            # Check if user's role is allowed
            if context.role not in policy.allowed_roles:
                continue
                
            # Check if user has required permissions
            if not policy.required_permissions.issubset(context.permissions):
                continue
                
            # Check denied patterns
            for pattern in policy.denied_patterns:
                if pattern.lower() in operation.lower():
                    return AuthorizationDecision(
                        allowed=False,
                        reason=f"Operation matches denied pattern '{pattern}' in policy '{policy.name}'",
                        confidence=1.0,
                        policy_used=policy.policy_id,
                        context_verified=True
                    )
            
            # Check context requirements
            if policy.context_requirements:
                if not self._check_context_requirements(context, policy.context_requirements):
                    continue
            
            # Policy allows this operation
            return AuthorizationDecision(
                allowed=True,
                reason=f"Allowed by policy '{policy.name}'",
                confidence=1.0,
                policy_used=policy.policy_id,
                context_verified=True
            )
        
        # No policy explicitly allows this operation
        return AuthorizationDecision(
            allowed=False,
            reason="No security policy allows this operation",
            confidence=0.5,
            context_verified=True
        )
    
    def _check_context_requirements(self, context: SecurityContext, requirements: Dict[str, Any]) -> bool:
        """Check if context meets policy requirements."""
        for key, value in requirements.items():
            if key == "min_role_level":
                role_hierarchy = {
                    UserRole.GUEST: 0,
                    UserRole.USER: 1,
                    UserRole.ADMIN: 2,
                    UserRole.SUPER_ADMIN: 3
                }
                if role_hierarchy.get(context.role, 0) < value:
                    return False
            elif key == "allowed_ip_ranges":
                # Simple IP range check
                if context.ip_address not in value:
                    return False
            elif key == "session_age_limit":
                session_age = time.time() - context.timestamp
                if session_age > value:
                    return False
        
        return True
    
    def add_policy(self, policy: SecurityPolicy):
        """Add new security policy."""
        self.policies.append(policy)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get policy engine statistics."""
        return {
            "total_policies": len(self.policies),
            "cache_statistics": self.cache.get_statistics()
        }


class ContextAwareSecurityAnalyzer:
    """AI-powered context-aware security analysis with token optimization."""
    
    def __init__(self, ai_engine=None):
        self.ai_engine = ai_engine
        self.cache = TokenOptimizedAuthCache(max_size=300, ttl_seconds=3600)
        self.security_patterns = self._load_security_patterns()
    
    def _load_security_patterns(self) -> Dict[str, List[str]]:
        """Load security analysis patterns."""
        return {
            "legitimate_admin_ops": [
                "delete.*log.*files",
                "cleanup.*temporary.*files",
                "rotate.*logs",
                "backup.*system",
                "maintenance.*mode"
            ],
            "malicious_patterns": [
                "delete.*system.*files",
                "rm.*-rf.*/",
                "drop.*database",
                "format.*disk",
                "override.*security"
            ],
            "context_indicators": {
                "admin_panel": ["admin", "dashboard", "management"],
                "user_panel": ["profile", "settings", "account"],
                "api_endpoint": ["api", "endpoint", "service"]
            }
        }
    
    def analyze_intent_with_context(
        self,
        intent: str,
        context: SecurityContext,
        operation_type: str = "general"
    ) -> AuthorizationDecision:
        """Analyze intent with context using AI or pattern matching."""
        start_time = time.time()
        
        # Check cache first
        cache_key = f"{context.user_id}:{intent}:{operation_type}"
        cached = self.cache.get(context.user_id, intent, context)
        if cached:
            cached.decision_time_ms = (time.time() - start_time) * 1000
            return cached
        
        # Fast pattern matching (Tier 1 equivalent)
        decision = self._fast_pattern_analysis(intent, context, operation_type)
        
        decision.decision_time_ms = (time.time() - start_time) * 1000
        decision.token_usage = len(intent) // 4  # Estimate tokens
        
        # Cache the decision
        self.cache.set(context.user_id, intent, context, decision)
        
        return decision
    
    def _fast_pattern_analysis(
        self,
        intent: str,
        context: SecurityContext,
        operation_type: str
    ) -> AuthorizationDecision:
        """Fast pattern-based analysis for quick decisions."""
        import re
        
        intent_lower = intent.lower()
        
        # Check for malicious patterns
        for pattern in self.security_patterns["malicious_patterns"]:
            if re.search(pattern, intent_lower):
                # Check if user has admin role and this might be legitimate
                if context.role in {UserRole.ADMIN, UserRole.SUPER_ADMIN}:
                    # Check if it matches legitimate admin patterns
                    for legit_pattern in self.security_patterns["legitimate_admin_ops"]:
                        if re.search(legit_pattern, intent_lower):
                            return AuthorizationDecision(
                                allowed=True,
                                reason="Authorized admin operation matching legitimate pattern",
                                confidence=0.85,
                                context_verified=True
                            )
                
                return AuthorizationDecision(
                    allowed=False,
                    reason=f"Intent matches malicious pattern: {pattern}",
                    confidence=0.95,
                    context_verified=True
                )
        
        # Check for legitimate admin operations
        if context.role in {UserRole.ADMIN, UserRole.SUPER_ADMIN}:
            for pattern in self.security_patterns["legitimate_admin_ops"]:
                if re.search(pattern, intent_lower):
                    return AuthorizationDecision(
                        allowed=True,
                        reason="Authorized admin operation",
                        confidence=0.90,
                        context_verified=True
                    )
        
        # Default decision based on user role
        if context.role in {UserRole.ADMIN, UserRole.SUPER_ADMIN}:
            return AuthorizationDecision(
                allowed=True,
                reason="Admin role allows operation",
                confidence=0.75,
                context_verified=True
            )
        elif context.role == UserRole.USER:
            # Users can do basic operations
            if any(word in intent_lower for word in ["read", "view", "get", "show"]):
                return AuthorizationDecision(
                    allowed=True,
                    reason="User role allows read operations",
                    confidence=0.80,
                    context_verified=True
                )
            return AuthorizationDecision(
                allowed=False,
                reason="User role does not allow this operation",
                confidence=0.70,
                context_verified=True
            )
        else:  # Guest
            return AuthorizationDecision(
                allowed=False,
                reason="Guest role has limited permissions",
                confidence=0.90,
                context_verified=True
            )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get analyzer statistics."""
        return {
            "cache_statistics": self.cache.get_statistics(),
            "security_patterns": len(self.security_patterns["malicious_patterns"])
        }


class AuthorizationSystem:
    """Main authorization system integrating all components."""
    
    def __init__(self, ai_engine=None):
        self.user_db = UserDatabase()
        self.policy_engine = PolicyEngine()
        self.context_analyzer = ContextAwareSecurityAnalyzer(ai_engine)
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.total_authorizations = 0
        self.total_blocked = 0
        self.total_allowed = 0
    
    def authenticate_user(self, username: str, password: str) -> Optional[SecurityContext]:
        """Authenticate user and return security context."""
        return self.user_db.authenticate(username, password)
    
    def authorize_operation(
        self,
        context: SecurityContext,
        operation: str,
        operation_details: Dict[str, Any] = None
    ) -> AuthorizationDecision:
        """Authorize operation using policy engine and context analysis."""
        self.total_authorizations += 1
        
        # First check policy engine
        policy_decision = self.policy_engine.evaluate_authorization(
            context, operation, operation_details
        )
        
        # If policy denies, check context analyzer for nuance
        if not policy_decision.allowed:
            context_decision = self.context_analyzer.analyze_intent_with_context(
                operation, context, "operation"
            )
            
            # Context analyzer might override if it's clearly legitimate
            if context_decision.allowed and context_decision.confidence > 0.85:
                # Use context decision if confidence is high
                if context_decision.confidence > policy_decision.confidence:
                    context_decision.token_usage += policy_decision.token_usage
                    self.total_allowed += 1
                    return context_decision
        
        if policy_decision.allowed:
            self.total_allowed += 1
        else:
            self.total_blocked += 1
        
        return policy_decision
    
    def authorize_intent(
        self,
        context: SecurityContext,
        intent: str,
        target_type: str = None
    ) -> AuthorizationDecision:
        """Authorize intent-based operation with context analysis."""
        self.total_authorizations += 1
        
        decision = self.context_analyzer.analyze_intent_with_context(
            intent, context, "intent"
        )
        
        if decision.allowed:
            self.total_allowed += 1
        else:
            self.total_blocked += 1
        
        return decision
    
    def create_user(self, username: str, password: str, role: UserRole, permissions: Set[Permission]):
        """Create new user."""
        self.user_db.create_user(username, password, role, permissions)
    
    def add_security_policy(self, policy: SecurityPolicy):
        """Add new security policy."""
        self.policy_engine.add_policy(policy)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive authorization statistics."""
        total = self.total_allowed + self.total_blocked
        block_rate = self.total_blocked / total if total > 0 else 0
        
        return {
            "total_authorizations": self.total_authorizations,
            "total_allowed": self.total_allowed,
            "total_blocked": self.total_blocked,
            "block_rate": round(block_rate, 4),
            "allow_rate": round(1 - block_rate, 4),
            "policy_engine_stats": self.policy_engine.get_statistics(),
            "context_analyzer_stats": self.context_analyzer.get_statistics(),
            "user_count": len(self.user_db.users),
            "active_sessions": len(self.user_db.sessions)
        }


# Singleton instance for global access
_auth_system_instance = None

def get_authorization_system(ai_engine=None) -> AuthorizationSystem:
    """Get the global authorization system instance."""
    global _auth_system_instance
    if _auth_system_instance is None:
        _auth_system_instance = AuthorizationSystem(ai_engine)
    return _auth_system_instance