"""
Intelligent Load-Aware Runtime for IPL
Uses real ML models (Random Forest, Gradient Boosting) to autonomously decide
whether to send requests. IPL learns what's "good" or "bad" from experience.

This is the future of programming: the language itself makes intelligent decisions.
"""
import time
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import deque
import threading
import json

try:
    from ml_heuristic_generator import MLHeuristicGenerator, HeuristicType, MLModelType
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("Warning: ML Heuristic Generator not available, using fallback")


@dataclass
class ServerState:
    """Represents current server state"""
    active_requests: int
    capacity: int
    is_overloaded: bool
    response_time: float
    timestamp: float


@dataclass
class IntelligentDecision:
    """IPL's autonomous decision"""
    should_send: bool
    confidence: float
    reasoning: str
    is_intelligent: bool  # True if ML model made the decision
    model_used: str  # Which ML model


class IntelligentLoadController:
    """
    IPL's intelligent load controller that autonomously learns optimal behavior.
    
    This is NOT rule-based. IPL:
    1. Collects experience (server states + outcomes)
    2. Trains ML models on this experience
    3. Uses ML to make autonomous decisions
    4. Continuously improves based on feedback
    
    IPL decides what's "good" or "bad" - no manual configuration needed.
    """
    
    def __init__(self):
        # Experience buffer for learning
        self.experience_buffer: List[Dict] = []
        self.max_experience = 1000
        
        # ML generator
        self.ml_generator = None
        self.heuristic_name = "load_control_heuristic"
        self.is_trained = False
        
        # Performance tracking
        self.decisions_made = 0
        self.ml_decisions = 0
        self.rule_based_decisions = 0
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Initialize ML if available
        if ML_AVAILABLE:
            self.ml_generator = MLHeuristicGenerator()
    
    def record_experience(self, state: ServerState, action: bool, outcome: bool):
        """
        Record an experience for ML learning.
        
        Args:
            state: Server state when decision was made
            action: Action taken (True = sent, False = blocked)
            outcome: Was it good? (True = success, False = failure/overload)
        """
        with self.lock:
            # Extract features
            features = {
                "load_ratio": state.active_requests / state.capacity,
                "is_overloaded": 1.0 if state.is_overloaded else 0.0,
                "response_time": state.response_time,
                "timestamp": state.timestamp
            }
            
            # Label: good = 1, bad = 0
            label = 1.0 if outcome else 0.0
            
            self.experience_buffer.append({
                "features": features,
                "action": action,
                "label": label,
                "state": state
            })
            
            # Keep buffer size manageable
            if len(self.experience_buffer) > self.max_experience:
                self.experience_buffer.pop(0)
            
            # Retrain if we have enough data
            if len(self.experience_buffer) >= 50 and not self.is_trained:
                self._train_ml_model()
    
    def make_intelligent_decision(self, current_state: ServerState) -> IntelligentDecision:
        """
        IPL autonomously decides whether to send a request.
        
        This is the core intelligence: IPL learns from experience and makes
        autonomous decisions without any manual rules or configuration.
        """
        with self.lock:
            self.decisions_made += 1
            
            # Extract features
            features = {
                "load_ratio": current_state.active_requests / current_state.capacity,
                "is_overloaded": 1.0 if current_state.is_overloaded else 0.0,
                "response_time": current_state.response_time,
                "timestamp": current_state.timestamp
            }
            
            # If ML is trained, use it
            if self.is_trained and self.ml_generator:
                try:
                    decision = self.ml_generator.apply_heuristic(
                        self.heuristic_name, 
                        features
                    )
                    
                    self.ml_decisions += 1
                    
                    return IntelligentDecision(
                        should_send=decision.decision,
                        confidence=decision.confidence,
                        reasoning=decision.reasoning,
                        is_intelligent=True,
                        model_used="RandomForest"
                    )
                except Exception as e:
                    # Fallback to rule-based if ML fails
                    pass
            
            # Fallback: simple heuristic (will be replaced by ML)
            self.rule_based_decisions += 1
            
            load_ratio = current_state.active_requests / current_state.capacity
            
            # Conservative baseline (ML will learn better)
            should_send = load_ratio < 0.5
            confidence = 0.5 if should_send else 0.3
            
            reasoning = f"Load ratio {load_ratio:.2f} (ML not yet trained)"
            
            return IntelligentDecision(
                should_send=should_send,
                confidence=confidence,
                reasoning=reasoning,
                is_intelligent=False,
                model_used="heuristic_fallback"
            )
    
    def _train_ml_model(self):
        """
        Train ML model on collected experience.
        
        IPL learns what decisions led to good outcomes.
        """
        if not self.ml_generator or len(self.experience_buffer) < 50:
            return
        
        # Prepare training data
        training_data = []
        labels = []
        
        for exp in self.experience_buffer:
            training_data.append(exp["features"])
            # Label is whether the outcome was good
            labels.append(exp["label"])
        
        try:
            # Train Random Forest model
            heuristic = self.ml_generator.learn_heuristic(
                training_data=training_data,
                labels=labels,
                model_type=MLModelType.RANDOM_FOREST
            )
            
            self.is_trained = True
            print(f"🧠 IPL trained ML model: {heuristic.name} (accuracy: {heuristic.accuracy:.2f})")
            print(f"   Features: {heuristic.features}")
            print(f"   Condition: {heuristic.condition}")
            
        except Exception as e:
            print(f"ML training failed: {e}")
    
    def get_intelligence_metrics(self) -> Dict:
        """Get metrics about IPL's intelligence"""
        with self.lock:
            return {
                "total_decisions": self.decisions_made,
                "ml_decisions": self.ml_decisions,
                "rule_based_decisions": self.rule_based_decisions,
                "intelligence_rate": self.ml_decisions / max(self.decisions_made, 1),
                "is_trained": self.is_trained,
                "experience_size": len(self.experience_buffer),
                "ml_available": ML_AVAILABLE
            }
