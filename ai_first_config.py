"""
AI-First Configuration for IPL
Prioritizes AI model (qwen2.5-coder:0.5b) over hardcoded patterns
"""
import os
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class AIFirstConfig:
    """Configuration for AI-first IPL operation."""
    
    # Primary AI Model Settings
    primary_model: str = "qwen2.5-coder:0.5b"
    ollama_endpoint: str = "http://localhost:11434"
    
    # AI-First Priority Settings
    ai_priority_mode: bool = True  # Use AI as primary decision engine
    ai_confidence_threshold: float = 0.7  # Minimum confidence to accept AI result
    ai_timeout_seconds: int = 30  # Timeout for AI model calls
    
    # Fallback Settings
    enable_pattern_fallback: bool = True  # Enable hardcoded pattern fallback when AI fails
    pattern_fallback_delay_ms: int = 100  # Delay before falling back to patterns
    
    # Performance Settings
    enable_ai_caching: bool = True  # Cache AI responses
    ai_cache_ttl_seconds: int = 3600  # AI cache time-to-live
    max_ai_cache_size: int = 1000  # Maximum AI cache entries
    
    # Decision Tracking
    track_ai_decisions: bool = True  # Track AI decision quality
    log_ai_failures: bool = True  # Log when AI fails and patterns are used
    
    # Specific Task AI Preferences
    task_ai_preferences: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.task_ai_preferences is None:
            # Default: Use AI for all tasks initially
            self.task_ai_preferences = {
                "type_inference": True,
                "semantic_extraction": True,
                "sentiment_analysis": True,
                "currency_extraction": True,
                "quantity_extraction": True,
                "intent_classification": True,
                "security_analysis": True,
                "error_analysis": True,
                "code_optimization": True
            }
    
    @classmethod
    def from_env(cls) -> 'AIFirstConfig':
        """Create configuration from environment variables."""
        return cls(
            primary_model=os.environ.get("IPL_PRIMARY_MODEL", "qwen2.5-coder:0.5b"),
            ollama_endpoint=os.environ.get("IPL_OLLAMA_ENDPOINT", "http://localhost:11434"),
            ai_priority_mode=os.environ.get("IPL_AI_PRIORITY", "true").lower() == "true",
            ai_confidence_threshold=float(os.environ.get("IPL_AI_CONFIDENCE", "0.7")),
            ai_timeout_seconds=int(os.environ.get("IPL_AI_TIMEOUT", "30")),
            enable_pattern_fallback=os.environ.get("IPL_PATTERN_FALLBACK", "true").lower() == "true",
            pattern_fallback_delay_ms=int(os.environ.get("IPL_FALLBACK_DELAY", "100")),
            enable_ai_caching=os.environ.get("IPL_AI_CACHE", "true").lower() == "true",
            ai_cache_ttl_seconds=int(os.environ.get("IPL_CACHE_TTL", "3600")),
            max_ai_cache_size=int(os.environ.get("IPL_CACHE_SIZE", "1000")),
            track_ai_decisions=os.environ.get("IPL_TRACK_DECISIONS", "true").lower() == "true",
            log_ai_failures=os.environ.get("IPL_LOG_AI_FAILURES", "true").lower() == "true"
        )
    
    def should_use_ai_for_task(self, task_type: str) -> bool:
        """Check if AI should be used for a specific task type."""
        if not self.ai_priority_mode:
            return False
        return self.task_ai_preferences.get(task_type, True)
    
    def get_effective_model(self) -> str:
        """Get the effective model to use."""
        return self.primary_model
    
    def is_ai_first_enabled(self) -> bool:
        """Check if AI-first mode is enabled."""
        return self.ai_priority_mode


class AIDecisionTracker:
    """Track AI decision quality and performance."""
    
    def __init__(self):
        self.total_decisions = 0
        self.ai_decisions = 0
        self.pattern_fallbacks = 0
        self.ai_successes = 0
        self.ai_failures = 0
        self.confidence_scores = []
        self.task_type_stats = {}
    
    def record_ai_decision(self, task_type: str, success: bool, confidence: float, execution_time_ms: float):
        """Record an AI decision."""
        self.total_decisions += 1
        self.ai_decisions += 1
        
        if success:
            self.ai_successes += 1
        else:
            self.ai_failures += 1
        
        self.confidence_scores.append(confidence)
        
        # Track by task type
        if task_type not in self.task_type_stats:
            self.task_type_stats[task_type] = {
                "total": 0,
                "successes": 0,
                "failures": 0,
                "avg_confidence": 0.0,
                "avg_time_ms": 0.0
            }
        
        stats = self.task_type_stats[task_type]
        stats["total"] += 1
        if success:
            stats["successes"] += 1
        else:
            stats["failures"] += 1
        
        # Update running averages
        n = stats["total"]
        stats["avg_confidence"] = ((n - 1) * stats["avg_confidence"] + confidence) / n
        stats["avg_time_ms"] = ((n - 1) * stats["avg_time_ms"] + execution_time_ms) / n
    
    def record_pattern_fallback(self, task_type: str, reason: str):
        """Record a pattern fallback (when AI failed)."""
        self.total_decisions += 1
        self.pattern_fallbacks += 1
        
        if task_type not in self.task_type_stats:
            self.task_type_stats[task_type] = {
                "total": 0,
                "successes": 0,
                "failures": 0,
                "avg_confidence": 0.0,
                "avg_time_ms": 0.0,
                "fallbacks": 0,
                "fallback_reasons": {}
            }
        
        stats = self.task_type_stats[task_type]
        stats["fallbacks"] = stats.get("fallbacks", 0) + 1
        
        if "fallback_reasons" not in stats:
            stats["fallback_reasons"] = {}
        
        stats["fallback_reasons"][reason] = stats["fallback_reasons"].get(reason, 0) + 1
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get decision tracking statistics."""
        ai_success_rate = self.ai_successes / max(self.ai_decisions, 1)
        ai_usage_rate = self.ai_decisions / max(self.total_decisions, 1)
        fallback_rate = self.pattern_fallbacks / max(self.total_decisions, 1)
        avg_confidence = sum(self.confidence_scores) / max(len(self.confidence_scores), 1)
        
        return {
            "total_decisions": self.total_decisions,
            "ai_decisions": self.ai_decisions,
            "pattern_fallbacks": self.pattern_fallbacks,
            "ai_success_rate": round(ai_success_rate, 3),
            "ai_usage_rate": round(ai_usage_rate, 3),
            "fallback_rate": round(fallback_rate, 3),
            "average_ai_confidence": round(avg_confidence, 3),
            "task_type_breakdown": self.task_type_stats
        }
    
    def reset(self):
        """Reset all statistics."""
        self.total_decisions = 0
        self.ai_decisions = 0
        self.pattern_fallbacks = 0
        self.ai_successes = 0
        self.ai_failures = 0
        self.confidence_scores = []
        self.task_type_stats = {}


# Global configuration instance
_global_config: Optional[AIFirstConfig] = None
_global_tracker: Optional[AIDecisionTracker] = None

def get_ai_first_config() -> AIFirstConfig:
    """Get the global AI-first configuration."""
    global _global_config
    if _global_config is None:
        _global_config = AIFirstConfig.from_env()
    return _global_config

def get_ai_decision_tracker() -> AIDecisionTracker:
    """Get the global AI decision tracker."""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = AIDecisionTracker()
    return _global_tracker

def set_ai_first_config(config: AIFirstConfig):
    """Set the global AI-first configuration."""
    global _global_config
    _global_config = config

def reset_ai_decision_tracker():
    """Reset the global AI decision tracker."""
    global _global_tracker
    _global_tracker = AIDecisionTracker()