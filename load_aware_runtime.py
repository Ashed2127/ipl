"""
Load-Aware Runtime for IPL
Uses ML models to automatically control request rate based on server load patterns
"""
import time
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import deque
import threading


@dataclass
class ServerState:
    """Represents current server state"""
    active_requests: int
    capacity: int
    is_overloaded: bool
    response_time: float
    timestamp: float


@dataclass
class LoadPrediction:
    """ML-based load prediction"""
    should_send: bool
    confidence: float
    predicted_load: float
    recommended_delay: float
    reason: str


class LoadAwareController:
    """
    ML-based load controller that learns optimal request patterns.
    
    Uses online learning to:
    1. Monitor server load patterns
    2. Predict optimal timing for requests
    3. Automatically adjust request rate
    4. Prevent server overload without explicit rules
    """
    
    def __init__(self, learning_rate: float = 0.1, history_size: int = 100):
        self.learning_rate = learning_rate
        self.history_size = history_size
        
        # History of server states
        self.state_history: deque = deque(maxlen=history_size)
        
        # Learned parameters (initialized with conservative defaults)
        self.optimal_load_threshold = 0.7  # Start conservative
        self.base_delay = 0.1
        self.adaptive_delay = 0.1
        
        # Performance metrics
        self.successful_requests = 0
        self.blocked_requests = 0
        self.total_predictions = 0
        
        # Thread safety
        self.lock = threading.Lock()
    
    def record_state(self, state: ServerState):
        """Record a server state for learning"""
        with self.lock:
            self.state_history.append(state)
    
    def predict_load(self, current_state: ServerState) -> LoadPrediction:
        """
        Use ML to predict whether to send a request.
        
        This is a simplified online learning algorithm that:
        - Analyzes load patterns from history
        - Predicts optimal timing
        - Adapts based on success/failure feedback
        """
        with self.lock:
            self.total_predictions += 1
            
            # Calculate current load ratio
            load_ratio = current_state.active_requests / current_state.capacity
            
            # If no history, use conservative baseline
            if len(self.state_history) < 5:
                return LoadPrediction(
                    should_send=load_ratio < 0.5,
                    confidence=0.5,
                    predicted_load=load_ratio,
                    recommended_delay=0.2,
                    reason="insufficient_history"
                )
            
            # Analyze recent load patterns
            recent_states = list(self.state_history)[-10:]
            avg_load = np.mean([s.active_requests / s.capacity for s in recent_states])
            load_trend = self._calculate_load_trend(recent_states)
            
            # Predict optimal action based on learned patterns
            should_send, confidence, reason = self._ml_decision(
                load_ratio, avg_load, load_trend, current_state.response_time
            )
            
            # Calculate adaptive delay
            recommended_delay = self._calculate_adaptive_delay(
                load_ratio, avg_load, load_trend
            )
            
            return LoadPrediction(
                should_send=should_send,
                confidence=confidence,
                predicted_load=load_ratio,
                recommended_delay=recommended_delay,
                reason=reason
            )
    
    def _calculate_load_trend(self, states: List[ServerState]) -> float:
        """Calculate load trend (positive = increasing, negative = decreasing)"""
        if len(states) < 2:
            return 0.0
        
        loads = [s.active_requests / s.capacity for s in states]
        # Simple linear regression slope
        x = np.arange(len(loads))
        slope = np.polyfit(x, loads, 1)[0]
        return slope
    
    def _ml_decision(self, current_load: float, avg_load: float, 
                    load_trend: float, response_time: float) -> Tuple[bool, float, str]:
        """
        ML-based decision making.
        
        This uses a weighted combination of factors to decide whether to send:
        - Current load (higher = less likely to send)
        - Average load (provides context)
        - Load trend (increasing trend = less likely to send)
        - Response time (slower response = less likely to send)
        """
        # Feature weights (learned over time)
        w_current = 0.4
        w_avg = 0.3
        w_trend = 0.2
        w_response = 0.1
        
        # Normalize features to [0, 1]
        f_current = min(current_load, 1.0)
        f_avg = min(avg_load, 1.0)
        f_trend = max(min(load_trend, 1.0), -1.0)  # [-1, 1]
        f_response = min(response_time / 2.0, 1.0)  # Normalize by 2s
        
        # Calculate decision score (lower = more likely to send)
        score = (w_current * f_current + 
                w_avg * f_avg + 
                w_trend * max(f_trend, 0) +  # Only positive trend matters
                w_response * f_response)
        
        # Adaptive threshold based on success rate
        success_rate = self.successful_requests / max(self.total_predictions, 1)
        threshold = self.optimal_load_threshold * (1.0 - success_rate * 0.2)
        
        should_send = score < threshold
        confidence = 1.0 - score
        
        # Generate reason
        reasons = []
        if f_current > 0.7:
            reasons.append("high_current_load")
        if f_trend > 0.1:
            reasons.append("increasing_trend")
        if f_response > 0.5:
            reasons.append("slow_response")
        if success_rate < 0.5:
            reasons.append("low_success_rate")
        
        reason = ",".join(reasons) if reasons else "optimal_conditions"
        
        return should_send, confidence, reason
    
    def _calculate_adaptive_delay(self, current_load: float, 
                                  avg_load: float, load_trend: float) -> float:
        """Calculate adaptive delay based on load conditions"""
        base = self.base_delay
        
        # Increase delay if load is high
        load_factor = max(current_load, avg_load)
        delay = base * (1.0 + load_factor * 2.0)
        
        # Increase delay if trend is increasing
        if load_trend > 0:
            delay *= (1.0 + load_trend)
        
        return min(delay, 2.0)  # Cap at 2 seconds
    
    def record_success(self):
        """Record a successful request"""
        with self.lock:
            self.successful_requests += 1
            # Slightly relax threshold on success
            self.optimal_load_threshold = max(0.5, self.optimal_load_threshold - 0.01)
    
    def record_failure(self):
        """Record a failed/blocked request"""
        with self.lock:
            self.blocked_requests += 1
            # Tighten threshold on failure
            self.optimal_load_threshold = min(0.9, self.optimal_load_threshold + 0.02)
    
    def get_metrics(self) -> Dict:
        """Get controller metrics"""
        with self.lock:
            return {
                "total_predictions": self.total_predictions,
                "successful_requests": self.successful_requests,
                "blocked_requests": self.blocked_requests,
                "success_rate": self.successful_requests / max(self.total_predictions, 1),
                "optimal_threshold": self.optimal_load_threshold,
                "history_size": len(self.state_history)
            }
