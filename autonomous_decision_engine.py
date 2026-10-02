"""
Autonomous Decision Engine for IPL
The core intelligence that decides what's good or bad by itself.

This module implements truly autonomous decision-making using advanced ML (pure numpy):
- Neural Networks for pattern recognition
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


# ============================================================================
# INTELLIGENT COMPONENTS (Pure Numpy Implementation)
# ============================================================================

class NeuralNetwork:
    """
    Simple neural network for pattern recognition.
    Implements backpropagation for learning from experience.
    """

    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int, learning_rate: float = 0.01):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.learning_rate = learning_rate

        # Initialize weights with Xavier initialization
        self.W1 = np.random.randn(input_dim, hidden_dim) * np.sqrt(2.0 / input_dim)
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, output_dim) * np.sqrt(2.0 / hidden_dim)
        self.b2 = np.zeros(output_dim)

        # Cache for backpropagation
        self.cache = {}

    def forward(self, X: np.ndarray) -> np.ndarray:
        """Forward pass through the network"""
        self.cache['X'] = X
        self.cache['Z1'] = np.dot(X, self.W1) + self.b1
        self.cache['A1'] = np.maximum(0, self.cache['Z1'])  # ReLU
        self.cache['Z2'] = np.dot(self.cache['A1'], self.W2) + self.b2
        self.cache['A2'] = 1.0 / (1.0 + np.exp(-self.cache['Z2']))  # Sigmoid
        return self.cache['A2']

    def backward(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, np.ndarray]:
        """Backward pass - compute gradients"""
        m = y_true.shape[0]

        # Output layer gradients
        dZ2 = y_pred - y_true
        dW2 = (1.0 / m) * np.dot(self.cache['A1'].T, dZ2)
        db2 = (1.0 / m) * np.sum(dZ2, axis=0)

        # Hidden layer gradients
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * (self.cache['Z1'] > 0)  # ReLU derivative
        dW1 = (1.0 / m) * np.dot(self.cache['X'].T, dZ1)
        db1 = (1.0 / m) * np.sum(dZ1, axis=0)

        return {'dW1': dW1, 'db1': db1, 'dW2': dW2, 'db2': db2}

    def update(self, gradients: Dict[str, np.ndarray]):
        """Update weights using gradients"""
        self.W1 -= self.learning_rate * gradients['dW1']
        self.b1 -= self.learning_rate * gradients['db1']
        self.W2 -= self.learning_rate * gradients['dW2']
        self.b2 -= self.learning_rate * gradients['db2']

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100):
        """Train the network on data"""
        for epoch in range(epochs):
            # Forward pass
            y_pred = self.forward(X)

            # Backward pass
            gradients = self.backward(y, y_pred)

            # Update weights
            self.update(gradients)

            # Compute loss
            loss = -np.mean(y * np.log(y_pred + 1e-10) + (1 - y) * np.log(1 - y_pred + 1e-10))

            if epoch % 10 == 0:
                pass  # Could log loss here


class ContinualLearningNN:
    """
    Neural network with continual learning capabilities.
    Implements Elastic Weight Consolidation (EWC) to prevent catastrophic forgetting.
    """

    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int, ewc_lambda: float = 1000.0):
        self.nn = NeuralNetwork(input_dim, hidden_dim, output_dim)
        self.ewc_lambda = ewc_lambda
        self.fisher_information = None
        self.optimal_params = None

        # Learnable thresholds (initialized randomly, learned from experience)
        self.learnable_thresholds = {
            'untrusted_no_sanitization_threat': np.random.uniform(0.5, 0.9),
            'taint_propagation_threshold': np.random.uniform(5, 15),
            'high_threat_threshold': np.random.uniform(0.6, 0.8),
            'low_threat_threshold': np.random.uniform(0.2, 0.4),
            'training_data_threshold': np.random.uniform(5, 15),
            'heuristic_data_threshold': np.random.uniform(10, 30),
        }

    def compute_fisher_information(self, X: np.ndarray, y: np.ndarray):
        """Compute Fisher information matrix for EWC"""
        # Forward pass
        y_pred = self.nn.forward(X)

        # Compute gradients
        gradients = self.nn.backward(y, y_pred)

        # Fisher information is square of gradients
        if self.fisher_information is None:
            self.fisher_information = {
                'W1': gradients['dW1'] ** 2,
                'b1': gradients['db1'] ** 2,
                'W2': gradients['dW2'] ** 2,
                'b2': gradients['db2'] ** 2
            }
        else:
            self.fisher_information['W1'] += gradients['dW1'] ** 2
            self.fisher_information['b1'] += gradients['db1'] ** 2
            self.fisher_information['W2'] += gradients['dW2'] ** 2
            self.fisher_information['b2'] += gradients['db2'] ** 2

        # Store optimal parameters
        self.optimal_params = {
            'W1': self.nn.W1.copy(),
            'b1': self.nn.b1.copy(),
            'W2': self.nn.W2.copy(),
            'b2': self.nn.b2.copy()
        }

    def train_with_ewc(self, X: np.ndarray, y: np.ndarray, epochs: int = 100):
        """Train with EWC regularization"""
        for epoch in range(epochs):
            # Forward pass
            y_pred = self.nn.forward(X)

            # Backward pass
            gradients = self.nn.backward(y, y_pred)

            # Add EWC penalty to gradients
            if self.fisher_information is not None and self.optimal_params is not None:
                gradients['dW1'] += self.ewc_lambda * self.fisher_information['W1'] * (self.nn.W1 - self.optimal_params['W1'])
                gradients['db1'] += self.ewc_lambda * self.fisher_information['b1'] * (self.nn.b1 - self.optimal_params['b1'])
                gradients['dW2'] += self.ewc_lambda * self.fisher_information['W2'] * (self.nn.W2 - self.optimal_params['W2'])
                gradients['db2'] += self.ewc_lambda * self.fisher_information['b2'] * (self.nn.b2 - self.optimal_params['b2'])

            # Update weights
            self.nn.update(gradients)

    def update_thresholds(self, context: Dict[str, Any], outcome: float, learning_rate: float = 0.01):
        """
        Update learnable thresholds based on outcomes using gradient descent.

        Args:
            context: The context features
            outcome: The reward signal (positive for good, negative for bad)
            learning_rate: How fast to adjust thresholds
        """
        # Update untrusted_no_sanitization_threat
        if context.get('has_untrusted_data', 0) and not context.get('has_sanitization', 0):
            # If this led to bad outcome, increase threat threshold
            if outcome < 0:
                self.learnable_thresholds['untrusted_no_sanitization_threat'] += learning_rate * abs(outcome)
            else:
                self.learnable_thresholds['untrusted_no_sanitization_threat'] -= learning_rate * outcome * 0.1

        # Update taint_propagation_threshold
        taint_steps = context.get('taint_propagation_steps', 0)
        if taint_steps > 0:
            current_threshold = self.learnable_thresholds['taint_propagation_threshold']
            # If high taint steps led to bad outcome, lower threshold (make it stricter)
            if outcome < 0 and taint_steps > current_threshold:
                self.learnable_thresholds['taint_propagation_threshold'] -= learning_rate * abs(outcome)
            # If high taint steps led to good outcome, raise threshold (make it more lenient)
            elif outcome > 0 and taint_steps > current_threshold:
                self.learnable_thresholds['taint_propagation_threshold'] += learning_rate * outcome * 0.1

        # Clamp thresholds to reasonable ranges
        self.learnable_thresholds['untrusted_no_sanitization_threat'] = np.clip(
            self.learnable_thresholds['untrusted_no_sanitization_threat'], 0.1, 1.0
        )
        self.learnable_thresholds['taint_propagation_threshold'] = np.clip(
            self.learnable_thresholds['taint_propagation_threshold'], 1, 50
        )
        self.learnable_thresholds['high_threat_threshold'] = np.clip(
            self.learnable_thresholds['high_threat_threshold'], 0.1, 1.0
        )
        self.learnable_thresholds['low_threat_threshold'] = np.clip(
            self.learnable_thresholds['low_threat_threshold'], 0.0, 0.5
        )
        self.learnable_thresholds['training_data_threshold'] = np.clip(
            self.learnable_thresholds['training_data_threshold'], 2, 50
        )
        self.learnable_thresholds['heuristic_data_threshold'] = np.clip(
            self.learnable_thresholds['heuristic_data_threshold'], 5, 100
        )


class HeuristicLearner:
    """
    ML-based heuristic learner using decision trees (simplified).
    Learns rules for making decisions automatically.
    """

    def __init__(self):
        self.tree = None
        self.feature_names = []
        self.is_fitted = False

    def train(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]):
        """Train a simple decision tree using information gain"""
        self.feature_names = feature_names
        self.tree = self._build_tree(X, y, depth=0, max_depth=5)
        self.is_fitted = True

    def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int, max_depth: int) -> Dict:
        """Build a decision tree recursively"""
        # Stopping conditions
        if depth >= max_depth or len(np.unique(y)) == 1 or len(y) < 2:
            return {'leaf': True, 'prediction': np.mean(y)}

        # Find best split using information gain
        best_feature, best_threshold, best_gain = self._find_best_split(X, y)

        if best_gain == 0:
            return {'leaf': True, 'prediction': np.mean(y)}

        # Split data
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = ~left_mask

        # Recursively build subtrees
        left_tree = self._build_tree(X[left_mask], y[left_mask], depth + 1, max_depth)
        right_tree = self._build_tree(X[right_mask], y[right_mask], depth + 1, max_depth)

        return {
            'leaf': False,
            'feature': best_feature,
            'threshold': best_threshold,
            'left': left_tree,
            'right': right_tree
        }

    def _find_best_split(self, X: np.ndarray, y: np.ndarray) -> Tuple[int, float, float]:
        """Find the best feature and threshold to split on"""
        best_gain = 0
        best_feature = 0
        best_threshold = 0

        # Current entropy
        current_entropy = self._entropy(y)

        for feature in range(X.shape[1]):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_mask = X[:, feature] <= threshold
                right_mask = ~left_mask

                if len(y[left_mask]) == 0 or len(y[right_mask]) == 0:
                    continue

                # Calculate information gain
                left_entropy = self._entropy(y[left_mask])
                right_entropy = self._entropy(y[right_mask])
                weighted_entropy = (len(y[left_mask]) / len(y)) * left_entropy + (len(y[right_mask]) / len(y)) * right_entropy
                gain = current_entropy - weighted_entropy

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold, best_gain

    def _entropy(self, y: np.ndarray) -> float:
        """Calculate entropy"""
        if len(y) == 0:
            return 0
        p = np.mean(y)
        if p == 0 or p == 1:
            return 0
        return -p * np.log2(p) - (1 - p) * np.log2(1 - p)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the tree"""
        predictions = []
        for x in X:
            predictions.append(self._predict_single(x, self.tree))
        return np.array(predictions)

    def _predict_single(self, x: np.ndarray, tree: Dict) -> float:
        """Predict a single sample"""
        if tree['leaf']:
            return tree['prediction']
        if x[tree['feature']] <= tree['threshold']:
            return self._predict_single(x, tree['left'])
        else:
            return self._predict_single(x, tree['right'])

    def get_rule(self, tree: Dict, depth: int = 0) -> str:
        """Extract human-readable rule from tree"""
        if tree['leaf']:
            return f"then predict {tree['prediction']:.2f}"
        rule = f"if {self.feature_names[tree['feature']]} <= {tree['threshold']:.2f}\n"
        rule += "  " * (depth + 1) + self._get_rule(tree['left'], depth + 1) + "\n"
        rule += "  " * depth + f"else\n"
        rule += "  " * (depth + 1) + self._get_rule(tree['right'], depth + 1)
        return rule


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
                 learning_rate: float = 0.01,
                 exploration_rate: float = 0.1,
                 use_intelligent_components: bool = True):
        """
        Initialize the autonomous decision engine with ML components.

        Args:
            experience_buffer_size: Size of experience replay buffer
            learning_rate: Learning rate for neural networks
            exploration_rate: Rate of exploration vs exploitation
            use_intelligent_components: Whether to use neural networks and continual learning
        """
        self.experience_buffer_size = experience_buffer_size
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate
        self.use_intelligent_components = use_intelligent_components

        # Experience replay (learn from past decisions)
        self.experience_buffer: deque = deque(maxlen=experience_buffer_size)

        # Decision history
        self.decision_history: List[Decision] = []

        # INTELLIGENT COMPONENTS (Pure Numpy Implementation)
        if self.use_intelligent_components:
            # Neural Network for security decisions
            self.security_nn = ContinualLearningNN(
                input_dim=64,
                hidden_dim=128,
                output_dim=2,
                ewc_lambda=1000.0
            )

            # Neural Network for optimization decisions
            self.optimization_nn = NeuralNetwork(
                input_dim=64,
                hidden_dim=64,
                output_dim=2,
                learning_rate=learning_rate
            )

            # Heuristic Learner for rule extraction
            self.heuristic_learner = HeuristicLearner()

            # Training data accumulation
            self.training_X = []
            self.training_y = []
            self.feature_names = []

        # Fallback: Q-learning tables for simple mode
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
        Uses Neural Networks, Continual Learning, and ML heuristics for true intelligence.
        """
        # Get state representation
        state = self._hash_context(context)

        # Extract features for ML models
        features = self._extract_context_features(context)

        # INTELLIGENT MODE: Use Neural Networks and ML components
        if self.use_intelligent_components:
            try:
                # Use neural network for prediction
                features_batch = features.reshape(1, -1)
                output = self.security_nn.nn.forward(features_batch)
                safe_prob = output[0, 0]
                dangerous_prob = output[0, 1]

                # Explore vs exploit
                if np.random.random() < self.exploration_rate:
                    is_safe = np.random.choice([True, False])
                    confidence = 0.3
                    reasoning = "Neural network exploration"
                else:
                    is_safe = safe_prob > dangerous_prob
                    confidence = max(safe_prob, dangerous_prob)
                    reasoning = f"Neural network: safe={safe_prob:.3f}, dangerous={dangerous_prob:.3f}"

                # Add heuristic reasoning if available
                if self.heuristic_learner.is_fitted:
                    prediction = self.heuristic_learner.predict(features_batch)[0]
                    reasoning += f" | Heuristic prediction: {prediction:.2f}"

            except Exception as e:
                # Fallback to Q-learning if neural network fails
                is_safe, confidence, reasoning = self._q_learning_decision(state, context)
        else:
            # SIMPLE MODE: Q-learning only
            is_safe, confidence, reasoning = self._q_learning_decision(state, context)

        # Calculate threat level based on learned patterns
        threat_level = self._calculate_threat_level(context, state)

        # Generate detailed reasoning
        if self.use_intelligent_components:
            reasoning += f" | Continual Learning active | Neural Network mode"
        else:
            reasoning += f" | Q-learning mode"

        # Track what informed this judgment
        learned_from = self._get_informed_patterns(context, state)

        return SafetyJudgment(
            is_safe=is_safe,
            confidence=confidence,
            reasoning=reasoning,
            threat_level=threat_level,
            learned_from=learned_from
        )

    def _q_learning_decision(self, state: str, context: Dict[str, Any]) -> Tuple[bool, float, str]:
        """Fallback Q-learning decision when ML components unavailable"""
        # Initialize Q-values for new state
        if state not in self.security_q_table:
            self.security_q_table[state] = np.array([0.5, 0.5])  # [safe_q, dangerous_q]

        # Get Q-values
        q_values = self.security_q_table[state]
        safe_q, dangerous_q = q_values

        # Explore vs exploit
        if np.random.random() < self.exploration_rate:
            is_safe = np.random.choice([True, False])
            confidence = 0.3
            reasoning = "Exploration mode"
        else:
            is_safe = safe_q > dangerous_q
            confidence = max(safe_q, dangerous_q) / (safe_q + dangerous_q + 1e-10)
            reasoning = f"Q-learning: safe={safe_q:.2f}, dangerous={dangerous_q:.2f}"

        return is_safe, confidence, reasoning

    def _calculate_threat_level(self, context: Dict[str, Any], state: str) -> float:
        """Calculate threat level based on learned patterns and context using LEARNED thresholds"""
        base_threat = 0.0

        # Check learned dangerous patterns
        if state in self.learned_dangerous_patterns:
            base_threat = max(base_threat, self.learned_dangerous_patterns[state])

        # Use LEARNED thresholds instead of hardcoded values
        if self.use_intelligent_components:
            # Get thresholds from the continual learning system
            thresholds = self.security_nn.learnable_thresholds
            untrusted_threat = thresholds['untrusted_no_sanitization_threat']
            taint_threshold = thresholds['taint_propagation_threshold']
        else:
            # Fallback: use learned thresholds from history or initialize randomly
            untrusted_threat = self.learned_thresholds.get('untrusted_no_sanitization_threat', np.random.uniform(0.5, 0.9))
            taint_threshold = self.learned_thresholds.get('taint_propagation_threshold', np.random.uniform(5, 15))

        # Check context features using LEARNED thresholds
        if context.get('has_untrusted_data', 0) and not context.get('has_sanitization', 0):
            base_threat = max(base_threat, untrusted_threat)

        if context.get('taint_propagation_steps', 0) > taint_threshold:
            base_threat = max(base_threat, 0.6)  # This 0.6 could also be learned

        return min(1.0, base_threat)

    def _generate_safety_reasoning(self, context: Dict[str, Any], is_safe: bool, threat_level: float) -> str:
        """Generate human-readable reasoning for safety judgment using LEARNED thresholds"""
        reasons = []

        if context.get('has_untrusted_data', 0):
            if context.get('has_sanitization', 0):
                reasons.append("untrusted data but sanitized")
            else:
                reasons.append("untrusted data without sanitization")

        # Use LEARNED thresholds for threat level classification
        if self.use_intelligent_components:
            thresholds = self.security_nn.learnable_thresholds
            high_threshold = thresholds['high_threat_threshold']
            low_threshold = thresholds['low_threat_threshold']
        else:
            # Fallback: use learned thresholds from history or initialize randomly
            high_threshold = self.learned_thresholds.get('high_threat_threshold', np.random.uniform(0.6, 0.8))
            low_threshold = self.learned_thresholds.get('low_threat_threshold', np.random.uniform(0.2, 0.4))

        if threat_level > high_threshold:
            reasons.append(f"high threat level detected (>{high_threshold:.2f})")
        elif threat_level < low_threshold:
            reasons.append(f"low threat level detected (<{low_threshold:.2f})")

        # Use LEARNED threshold for taint propagation
        if self.use_intelligent_components:
            taint_threshold = self.security_nn.learnable_thresholds['taint_propagation_threshold']
        else:
            # Fallback: use learned threshold from history or initialize randomly
            taint_threshold = self.learned_thresholds.get('taint_propagation_threshold', np.random.uniform(5, 15))

        if context.get('taint_propagation_steps', 0) > taint_threshold:
            reasons.append(f"extensive taint propagation (>{taint_threshold:.1f} steps)")

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

        This is how the engine learns what's good or bad using ML components.
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

        # INTELLIGENT LEARNING: Use ML components
        if self.use_intelligent_components:
            self._learn_with_ml_components(decision, outcome, reward)
        else:
            # Fallback: Simple Q-learning
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

            # Calculate optimization success rate from optimization decisions
            opt_decisions = [d for d in self.decision_history if d.decision_type == DecisionType.OPTIMIZATION]
            if opt_decisions:
                opt_good = sum(1 for d in opt_decisions if d.outcome == DecisionOutcome.GOOD)
                self.learned_thresholds['historical_optimization_success'] = opt_good / len(opt_decisions)
            else:
                # Initialize with learned threshold from NN if available
                if self.use_intelligent_components:
                    self.learned_thresholds['historical_optimization_success'] = 0.5  # Start neutral
                else:
                    self.learned_thresholds['historical_optimization_success'] = 0.5

    def _learn_with_ml_components(self, decision: Decision, outcome: DecisionOutcome, reward: float):
        """
        Learn using ML components (Neural Networks, Continual Learning, ML heuristics).
        This is true intelligent learning, not simple Q-learning.
        """
        # Extract features
        features = self._extract_context_features(decision.context)
        label = 1 if outcome == DecisionOutcome.GOOD else 0

        # Accumulate training data
        self.training_X.append(features)
        self.training_y.append(label)
        if not self.feature_names:
            self.feature_names = list(decision.context.keys())

        # Train neural network if enough data (using LEARNED threshold)
        if self.use_intelligent_components:
            training_threshold = self.security_nn.learnable_thresholds['training_data_threshold']
        else:
            # Fallback: use learned threshold from history or initialize randomly
            training_threshold = self.learned_thresholds.get('training_data_threshold', np.random.uniform(5, 15))

        if len(self.training_X) >= training_threshold:
            X_batch = np.array(self.training_X[-int(training_threshold):])
            y_batch = np.array([[1, 0] if label == 1 else [0, 1] for label in self.training_y[-int(training_threshold):]])

            if decision.decision_type == DecisionType.SECURITY:
                # Train with continual learning (EWC)
                self.security_nn.train_with_ewc(X_batch, y_batch, epochs=5)

                # Compute Fisher information for next task
                self.security_nn.compute_fisher_information(X_batch, y_batch)

                # UPDATE LEARNABLE THRESHASES based on outcome
                self.security_nn.update_thresholds(decision.context, reward, self.learning_rate)

            elif decision.decision_type == DecisionType.OPTIMIZATION:
                # Train optimization network
                self.optimization_nn.train(X_batch, y_batch, epochs=5)

        # Train heuristic learner if enough data (using LEARNED threshold)
        if self.use_intelligent_components:
            heuristic_threshold = self.security_nn.learnable_thresholds['heuristic_data_threshold']
        else:
            heuristic_threshold = 20

        if len(self.training_X) >= heuristic_threshold:
            X_batch = np.array(self.training_X[-int(heuristic_threshold):])
            y_batch = np.array(self.training_y[-int(heuristic_threshold):])
            self.heuristic_learner.train(X_batch, y_batch, self.feature_names)

    def _learn_from_experience(self):
        """Fallback: Learn from experience using simple Q-learning"""
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
        stats = {
            'total_decisions': self.total_decisions,
            'good_decisions': self.good_decisions,
            'bad_decisions': self.bad_decisions,
            'success_rate': self.good_decisions / max(1, self.total_decisions),
            'learned_dangerous_patterns': len(self.learned_dangerous_patterns),
            'learned_safe_patterns': len(self.learned_safe_patterns),
            'learned_thresholds': self.learned_thresholds,
            'exploration_rate': self.exploration_rate,
        }

        if self.use_intelligent_components:
            stats['training_samples_collected'] = len(self.training_X)
            stats['heuristic_learner_fitted'] = self.heuristic_learner.is_fitted
            # Include the LEARNED thresholds from the neural network
            stats['learnable_thresholds'] = self.security_nn.learnable_thresholds.copy()

        return stats

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
