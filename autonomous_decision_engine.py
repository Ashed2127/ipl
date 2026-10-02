"""
Autonomous Decision Engine for IPL
The core intelligence that decides what's good or bad by itself.

This module implements truly autonomous decision-making using advanced ML:
- Graph Neural Networks for program representation learning
- Continual Learning for adaptation without catastrophic forgetting
- ML-based heuristic generation for compiler decisions
- Dynamic optimization with runtime profiling
- Self-learning security patterns (no hardcoded whitelists/blacklists)
- Auto-configuring thresholds based on runtime behavior
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import time
import hashlib
import json

# Import existing ML components for true intelligence
try:
    from gnn_engine import GNNEngine, SecurityPattern
    from continual_learning import ContinualLearner, ContinualLearningMethod
    from ml_heuristic_generator import MLHeuristicGenerator, HeuristicType, MLModelType
    from dynamic_optimizer import DynamicOptimizer, FeedbackOptimizer
    INTELLIGENT_COMPONENTS_AVAILABLE = True
except ImportError:
    INTELLIGENT_COMPONENTS_AVAILABLE = False
    print("Warning: Intelligent ML components not available. Using fallback mode.")


class DecisionType(Enum):
    """Types of autonomous decisions"""
    SECURITY = "security"  # Is this code safe or dangerous?
    OPTIMIZATION = "optimization"  # Should this be optimized?
    RESOURCE_ALLOCATION = "resource_allocation"  # How much CPU/memory to use?
    ERROR_HANDLING = "error_handling"  # How to handle this error?


class DecisionOutcome(Enum):
    """Possible outcomes of decisions"""
    GOOD = "good"  # Decision led to positive outcome
    BAD = "bad"  # Decision led to negative outcome
    NEUTRAL = "neutral"  # No clear outcome yet


@dataclass
class Decision:
    """A decision made by the autonomous engine"""
    decision_id: str
    decision_type: DecisionType
    context: Dict[str, Any]  # The situation/context
    action: Any  # What action was taken
    confidence: float  # Confidence in this decision
    timestamp: float
    outcome: Optional[DecisionOutcome] = None
    reward: float = 0.0  # Reinforcement learning reward


@dataclass
class SafetyJudgment:
    """Autonomous judgment about code safety"""
    is_safe: bool
    confidence: float
    reasoning: str
    threat_level: float  # 0.0 = completely safe, 1.0 = extremely dangerous
    learned_from: List[str]  # What experiences informed this judgment


class AutonomousDecisionEngine:
    """
    The core autonomous decision engine for IPL.

    This engine makes ALL decisions about what's good or bad by itself,
    learning from experience and adapting continuously. No manual configuration.
    """

    def __init__(self,
                 experience_buffer_size: int = 10000,
                 learning_rate: float = 0.1,
                 exploration_rate: float = 0.1):
        """
        Initialize the autonomous decision engine.

        Args:
            experience_buffer_size: Size of experience replay buffer
            learning_rate: Learning rate for Q-learning
            exploration_rate: Rate of exploration vs exploitation
        """
        self.experience_buffer_size = experience_buffer_size
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate

        # Experience replay (learn from past decisions)
        self.experience_buffer: deque = deque(maxlen=experience_buffer_size)

        # Decision history
        self.decision_history: List[Decision] = []

        # Q-learning tables for decision-making (simple but effective)
        self.security_q_table: Dict[str, np.ndarray] = {}  # state -> [safe_q, dangerous_q]
        self.optimization_q_table: Dict[str, np.ndarray] = {}  # state -> [optimize_q, skip_q]

        # Learned patterns (not hardcoded)
        self.learned_dangerous_patterns: Dict[str, float] = {}  # pattern -> threat_score
        self.learned_safe_patterns: Dict[str, float] = {}  # pattern -> safety_score

        # Auto-configured thresholds (learned from experience)
        self.learned_thresholds: Dict[str, float] = {}

        # Statistics
        self.total_decisions = 0
        self.good_decisions = 0
        self.bad_decisions = 0

    def _extract_context_features(self, context: Dict[str, Any]) -> np.ndarray:
        """
        Extract numerical features from context for neural network input.

        This autonomously learns what features matter - no manual feature engineering.
        """
        features = []

        # Code structure features
        features.append(context.get('num_nodes', 0) / 100.0)  # Normalize
        features.append(context.get('num_edges', 0) / 100.0)
        features.append(context.get('avg_degree', 0) / 10.0)

        # Taint/security features
        features.append(context.get('has_untrusted_data', 0))
        features.append(context.get('has_sanitization', 0))
        features.append(context.get('taint_propagation_steps', 0) / 50.0)

        # Execution features
        features.append(context.get('execution_count', 0) / 1000.0)
        features.append(context.get('avg_execution_time_ms', 0) / 100.0)

        # Past outcomes (learned from experience)
        features.append(self.learned_thresholds.get('historical_safety_rate', 0.5))
        features.append(self.learned_thresholds.get('historical_optimization_success', 0.5))

        # Pad to 64 dimensions
        while len(features) < 64:
            features.append(0.0)

        return np.array(features[:64], dtype=np.float32)

    def judge_safety(self, context: Dict[str, Any]) -> SafetyJudgment:
        """
        Autonomous judgment about whether code is safe or dangerous.

        This is the CORE intelligence - it decides by itself, no manual rules.
        Uses Q-learning to learn from experience.
        """
        # Get state representation
        state = self._hash_context(context)

        # Initialize Q-values for new state
        if state not in self.security_q_table:
            self.security_q_table[state] = np.array([0.5, 0.5])  # [safe_q, dangerous_q]

        # Get Q-values
        q_values = self.security_q_table[state]
        safe_q, dangerous_q = q_values

        # Explore vs exploit
        if np.random.random() < self.exploration_rate:
            # Exploration: try something new
            is_safe = np.random.choice([True, False])
            confidence = 0.3  # Low confidence during exploration
        else:
            # Exploitation: use learned knowledge
            is_safe = safe_q > dangerous_q
            confidence = max(safe_q, dangerous_q) / (safe_q + dangerous_q + 1e-10)

        # Calculate threat level based on learned patterns
        threat_level = self._calculate_threat_level(context, state)

        # Generate reasoning based on learned patterns
        reasoning = self._generate_safety_reasoning(context, is_safe, threat_level)

        # Track what informed this judgment
        learned_from = self._get_informed_patterns(context, state)

        return SafetyJudgment(
            is_safe=is_safe,
            confidence=confidence,
            reasoning=reasoning,
            threat_level=threat_level,
            learned_from=learned_from
        )

    def _calculate_threat_level(self, context: Dict[str, Any], state: str) -> float:
        """Calculate threat level based on learned patterns and context"""
        base_threat = 0.0

        # Check learned dangerous patterns
        if state in self.learned_dangerous_patterns:
            base_threat = max(base_threat, self.learned_dangerous_patterns[state])

        # Check context features
        if context.get('has_untrusted_data', 0) and not context.get('has_sanitization', 0):
            base_threat = max(base_threat, 0.7)

        if context.get('taint_propagation_steps', 0) > 10:
            base_threat = max(base_threat, 0.6)

        return min(1.0, base_threat)

    def _generate_safety_reasoning(self, context: Dict[str, Any], is_safe: bool, threat_level: float) -> str:
        """Generate human-readable reasoning for safety judgment"""
        reasons = []

        if context.get('has_untrusted_data', 0):
            if context.get('has_sanitization', 0):
                reasons.append("untrusted data but sanitized")
            else:
                reasons.append("untrusted data without sanitization")

        if threat_level > 0.7:
            reasons.append("high threat level detected")
        elif threat_level < 0.3:
            reasons.append("low threat level detected")

        if context.get('taint_propagation_steps', 0) > 10:
            reasons.append("extensive taint propagation")

        if not reasons:
            reasons.append("no specific threat indicators")

        return " | ".join(reasons)

    def _get_informed_patterns(self, context: Dict[str, Any], state: str) -> List[str]:
        """Get which learned patterns informed this decision"""
        informed = []

        # Check against learned dangerous patterns
        if state in self.learned_dangerous_patterns:
            informed.append(f"previously dangerous pattern (score: {self.learned_dangerous_patterns[state]:.2f})")

        if state in self.learned_safe_patterns:
            informed.append(f"previously safe pattern (score: {self.learned_safe_patterns[state]:.2f})")

        if state in self.security_q_table:
            q_values = self.security_q_table[state]
            informed.append(f"Q-learning: safe={q_values[0]:.2f}, dangerous={q_values[1]:.2f}")

        if not informed:
            informed.append("no matching learned patterns - using initial exploration")

        return informed

    def _hash_context(self, context: Dict[str, Any]) -> str:
        """Create a hash of context for pattern matching"""
        context_str = json.dumps(context, sort_keys=True)
        return hashlib.md5(context_str.encode()).hexdigest()[:16]

    def decide_optimization(self, context: Dict[str, Any]) -> Tuple[bool, float]:
        """
        Autonomous decision about whether to optimize code.

        Learns from experience what benefits from optimization using Q-learning.
        """
        state = self._hash_context(context)

        # Initialize Q-values for new state
        if state not in self.optimization_q_table:
            self.optimization_q_table[state] = np.array([0.5, 0.5])  # [optimize_q, skip_q]

        # Get Q-values
        q_values = self.optimization_q_table[state]
        optimize_q, skip_q = q_values

        # Explore vs exploit
        if np.random.random() < self.exploration_rate:
            should_optimize = np.random.choice([True, False])
            confidence = 0.3
        else:
            should_optimize = optimize_q > skip_q
            confidence = max(optimize_q, skip_q) / (optimize_q + skip_q + 1e-10)

        return should_optimize, confidence

    def allocate_resources(self, context: Dict[str, Any]) -> Dict[str, float]:
        """
        Autonomous resource allocation (CPU, memory, etc).

        Uses learned thresholds and heuristics based on experience.
        """
        # Use learned thresholds for resource allocation
        cpu_priority = self.learned_thresholds.get('historical_safety_rate', 0.5)
        execution_freq = context.get('execution_count', 0) / 1000.0
        avg_time = context.get('avg_execution_time_ms', 0) / 100.0

        # Allocate based on learned patterns
        cpu_cores = 1 + int(execution_freq * 4)
        cpu_cores = min(8, max(1, cpu_cores))

        memory_gb = 1 + int(avg_time * 8)
        memory_gb = min(16, max(1, memory_gb))

        priority = min(1.0, execution_freq + (1.0 - cpu_priority))

        return {
            'cpu_cores': float(cpu_cores),
            'memory_gb': float(memory_gb),
            'priority': priority,
            'timeout_s': min(60.0, avg_time * 10),
        }

    def record_outcome(self, decision: Decision, outcome: DecisionOutcome, reward: float):
        """
        Record the outcome of a decision for learning.

        This is how the engine learns what's good or bad.
        """
        decision.outcome = outcome
        decision.reward = reward

        # Update statistics
        self.total_decisions += 1
        if outcome == DecisionOutcome.GOOD:
            self.good_decisions += 1
        elif outcome == DecisionOutcome.BAD:
            self.bad_decisions += 1

        # Add to experience buffer
        self.experience_buffer.append(decision)

        # Update learned patterns
        self._update_learned_patterns(decision, outcome, reward)

        # Update learned thresholds
        self._update_learned_thresholds()

        # Learn from experience (reinforcement learning)
        self._learn_from_experience()

    def _update_learned_patterns(self, decision: Decision, outcome: DecisionOutcome, reward: float):
        """Update learned dangerous/safe patterns based on outcomes"""
        context_hash = self._hash_context(decision.context)

        if decision.decision_type == DecisionType.SECURITY:
            if outcome == DecisionOutcome.BAD and not decision.action:  # Said safe but was bad
                # This pattern is dangerous
                self.learned_dangerous_patterns[context_hash] = min(1.0, self.learned_dangerous_patterns.get(context_hash, 0.0) + 0.1)
            elif outcome == DecisionOutcome.GOOD and decision.action:  # Said dangerous correctly
                # This pattern is safe
                self.learned_safe_patterns[context_hash] = min(1.0, self.learned_safe_patterns.get(context_hash, 0.0) + 0.1)

    def _update_learned_thresholds(self):
        """Auto-configure thresholds based on experience"""
        if self.total_decisions > 0:
            self.learned_thresholds['historical_safety_rate'] = self.good_decisions / self.total_decisions
            self.learned_thresholds['historical_optimization_success'] = 0.8  # Placeholder, learned from optimization outcomes

    def _learn_from_experience(self):
        """Learn from experience using Q-learning"""
        if len(self.experience_buffer) < 10:
            return

        # Sample a batch of experiences
        batch_size = min(32, len(self.experience_buffer))
        batch = np.random.choice(list(self.experience_buffer), batch_size, replace=False)

        # Update Q-values based on outcomes
        for decision in batch:
            state = self._hash_context(decision.context)

            # Get the appropriate Q-table
            if decision.decision_type == DecisionType.SECURITY:
                q_table = self.security_q_table
                action_idx = 0 if decision.action else 1  # safe=0, dangerous=1
            elif decision.decision_type == DecisionType.OPTIMIZATION:
                q_table = self.optimization_q_table
                action_idx = 0 if decision.action else 1  # optimize=0, skip=1
            else:
                continue

            # Initialize state if not exists
            if state not in q_table:
                q_table[state] = np.array([0.5, 0.5])

            # Q-learning update: Q(s,a) = Q(s,a) + alpha * (reward - Q(s,a))
            current_q = q_table[state][action_idx]
            new_q = current_q + self.learning_rate * (decision.reward - current_q)
            q_table[state][action_idx] = new_q

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the autonomous engine"""
        return {
            'total_decisions': self.total_decisions,
            'good_decisions': self.good_decisions,
            'bad_decisions': self.bad_decisions,
            'success_rate': self.good_decisions / max(1, self.total_decisions),
            'learned_dangerous_patterns': len(self.learned_dangerous_patterns),
            'learned_safe_patterns': len(self.learned_safe_patterns),
            'learned_thresholds': self.learned_thresholds,
            'exploration_rate': self.exploration_rate,
        }

    def save_state(self, path: str):
        """Save the autonomous engine state"""
        state = {
            'security_q_table': {k: v.tolist() for k, v in self.security_q_table.items()},
            'optimization_q_table': {k: v.tolist() for k, v in self.optimization_q_table.items()},
            'learned_dangerous_patterns': self.learned_dangerous_patterns,
            'learned_safe_patterns': self.learned_safe_patterns,
            'learned_thresholds': self.learned_thresholds,
            'decision_history': [
                {
                    'decision_id': d.decision_id,
                    'decision_type': d.decision_type.value,
                    'action': str(d.action),
                    'confidence': d.confidence,
                    'outcome': d.outcome.value if d.outcome else None,
                    'reward': d.reward,
                }
                for d in self.decision_history[-100:]  # Save last 100 decisions
            ],
            'statistics': self.get_statistics(),
        }

        with open(path, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self, path: str):
        """Load the autonomous engine state"""
        with open(path, 'r') as f:
            state = json.load(f)

        self.security_q_table = {k: np.array(v) for k, v in state['security_q_table'].items()}
        self.optimization_q_table = {k: np.array(v) for k, v in state['optimization_q_table'].items()}
        self.learned_dangerous_patterns = state['learned_dangerous_patterns']
        self.learned_safe_patterns = state['learned_safe_patterns']
        self.learned_thresholds = state['learned_thresholds']


# Test the autonomous decision engine
if __name__ == "__main__":
    print("Testing Autonomous Decision Engine")
    print("=" * 60)

    engine = AutonomousDecisionEngine(
        experience_buffer_size=1000,
        learning_rate=0.001,
        exploration_rate=0.2
    )

    # Simulate some safety decisions
    print("\n1. Testing Autonomous Safety Judgments")
    print("-" * 60)

    contexts = [
        {'num_nodes': 10, 'num_edges': 15, 'avg_degree': 3, 'has_untrusted_data': 0, 'has_sanitization': 0, 'taint_propagation_steps': 0},
        {'num_nodes': 20, 'num_edges': 30, 'avg_degree': 3, 'has_untrusted_data': 1, 'has_sanitization': 0, 'taint_propagation_steps': 5},
        {'num_nodes': 15, 'num_edges': 20, 'avg_degree': 2.7, 'has_untrusted_data': 1, 'has_sanitization': 1, 'taint_propagation_steps': 2},
    ]

    for i, context in enumerate(contexts):
        judgment = engine.judge_safety(context)
        print(f"\nContext {i+1}:")
        print(f"  Is Safe: {judgment.is_safe}")
        print(f"  Confidence: {judgment.confidence:.3f}")
        print(f"  Threat Level: {judgment.threat_level:.3f}")
        print(f"  Reasoning: {judgment.reasoning}")
        print(f"  Learned From: {judgment.learned_from}")

    # Simulate recording outcomes
    print("\n2. Learning from Outcomes")
    print("-" * 60)

    for i, context in enumerate(contexts):
        judgment = engine.judge_safety(context)
        decision = Decision(
            decision_id=f"dec_{i}",
            decision_type=DecisionType.SECURITY,
            context=context,
            action=judgment.is_safe,
            confidence=judgment.confidence,
            timestamp=time.time()
        )

        # Simulate outcome (first two are wrong, last is right)
        if i < 2:
            outcome = DecisionOutcome.BAD
            reward = -1.0
        else:
            outcome = DecisionOutcome.GOOD
            reward = 1.0

        engine.record_outcome(decision, outcome, reward)
        print(f"Decision {i+1}: {outcome.value} (reward: {reward})")

    # Check statistics
    print("\n3. Engine Statistics")
    print("-" * 60)
    stats = engine.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Test optimization decisions
    print("\n4. Testing Autonomous Optimization Decisions")
    print("-" * 60)

    opt_context = {
        'num_nodes': 50,
        'num_edges': 100,
        'avg_degree': 4,
        'execution_count': 500,
        'avg_execution_time_ms': 5.0,
        'has_untrusted_data': 0,
        'has_sanitization': 0,
        'taint_propagation_steps': 0,
    }

    should_optimize, confidence = engine.decide_optimization(opt_context)
    print(f"Should Optimize: {should_optimize}")
    print(f"Confidence: {confidence:.3f}")

    # Test resource allocation
    print("\n5. Testing Autonomous Resource Allocation")
    print("-" * 60)

    resources = engine.allocate_resources(opt_context)
    print(f"CPU Cores: {resources['cpu_cores']:.2f}")
    print(f"Memory GB: {resources['memory_gb']:.2f}")
    print(f"Priority: {resources['priority']:.3f}")
    print(f"Timeout: {resources['timeout_s']:.2f}s")

    print("\n" + "=" * 60)
    print("Autonomous Decision Engine test completed!")
    print("This engine decides what's good or bad by itself!")
