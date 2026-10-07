# IPL ML Structure - How Machine Learning Works in IPL

## Overview

IPL uses **4 main ML components** that work together to make autonomous decisions without hardcoded rules:

```
┌─────────────────────────────────────────────────────────────────┐
│                    IPL ML ARCHITECTURE                          │
│        Autonomous Decision Engine (Pure Numpy Implementation)    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. NEURAL NETWORK (autonomous_decision_engine.py)

### Structure
```
Input Layer (64 features)
    │
    ▼
Hidden Layer (128 neurons) + ReLU Activation
    │
    ▼
Output Layer (2 neurons) + Sigmoid Activation
    │
    ├─→ Neuron 1: SAFE probability
    └─→ Neuron 2: DANGEROUS probability
```

### How It Works

**Forward Pass:**
```python
# Input: Context features (64-dimensional vector)
X = extract_context_features(context)

# Layer 1: Input → Hidden
Z1 = X · W1 + b1          # Matrix multiplication
A1 = max(0, Z1)           # ReLU activation

# Layer 2: Hidden → Output
Z2 = A1 · W2 + b2
A2 = sigmoid(Z2)          # Sigmoid: outputs probabilities [0, 1]

# Output: [safe_prob, dangerous_prob]
return A2
```

**Backpropagation (Learning):**
```python
# Compute gradients from error
dZ2 = y_pred - y_true                # Output error
dW2 = (1/m) · A1^T · dZ2            # Gradient for W2
dA1 = dZ2 · W2^T                    # Backprop to hidden
dZ1 = dA1 · (Z1 > 0)                # ReLU derivative
dW1 = (1/m) · X^T · dZ1             # Gradient for W1

# Update weights (gradient descent)
W1 -= learning_rate · dW1
W2 -= learning_rate · dW2
```

**Features Extracted (64 total):**
- Code structure: num_nodes, num_edges, avg_degree
- Taint info: has_untrusted_data, has_sanitization, taint_propagation_steps
- Sink types: sql_sink, html_sink, shell_sink counts
- Threat levels: untrusted_threat, sanitized_threat
- Pattern info: pattern_match_score, pattern_confidence
- + 50+ more contextual features

---

## 2. CONTINUAL LEARNING (continual_learning.py)

### Problem: Catastrophic Forgetting
When neural networks learn new tasks, they forget old ones.

### Solution: Elastic Weight Consolidation (EWC)

**EWC Algorithm:**
```python
# 1. After learning Task A, compute Fisher Information
gradients = compute_gradients(data_A)
fisher_information = gradients^2      # Importance of each weight
optimal_params = current_weights      # Save optimal weights

# 2. When learning Task B, add EWC penalty
loss = cross_entropy_loss(y_pred, y_true)

# Add penalty for changing important weights
ewc_penalty = lambda · fisher_information · (current_weights - optimal_params)^2
total_loss = loss + ewc_penalty

# 3. Backprop with EWC
total_loss.backward()
```

**What This Does:**
- High Fisher Information = weight is important for Task A
- EWC penalty prevents changing important weights
- Network learns Task B without forgetting Task A

**Implementation in IPL:**
```python
class ContinualLearningNN:
    def __init__(self, input_dim, hidden_dim, output_dim, ewc_lambda=1000.0):
        self.nn = NeuralNetwork(input_dim, hidden_dim, output_dim)
        self.ewc_lambda = ewc_lambda          # Regularization strength
        self.fisher_information = None       # Track importance
        self.optimal_params = None           # Track optimal weights

    def compute_fisher_information(self, X, y):
        # Forward pass
        y_pred = self.nn.forward(X)

        # Compute gradients
        gradients = self.nn.backward(y, y_pred)

        # Fisher info = squared gradients (importance)
        self.fisher_information = {
            'W1': gradients['dW1'] ** 2,
            'b1': gradients['db1'] ** 2,
            'W2': gradients['dW2'] ** 2,
            'b2': gradients['db2'] ** 2
        }

        # Save optimal parameters
        self.optimal_params = {
            'W1': self.nn.W1.copy(),
            'b1': self.nn.b1.copy(),
            'W2': self.nn.W2.copy(),
            'b2': self.nn.b2.copy()
        }

    def train_with_ewc(self, X, y, epochs=100):
        for epoch in range(epochs):
            y_pred = self.nn.forward(X)
            gradients = self.nn.backward(y, y_pred)

            # Add EWC penalty to gradients
            if self.fisher_information is not None:
                gradients['dW1'] += self.ewc_lambda * self.fisher_information['W1'] * (self.nn.W1 - self.optimal_params['W1'])
                gradients['dW2'] += self.ewc_lambda * self.fisher_information['W2'] * (self.nn.W2 - self.optimal_params['W2'])

            # Update weights
            self.nn.update(gradients)
```

---

## 3. LEARNABLE THRESHOLDS (autonomous_decision_engine.py)

### Problem: Traditional compilers use hardcoded thresholds
```python
# Traditional (BAD):
if threat_level > 0.7:          # Hardcoded!
    block_execution()
```

### Solution: Learn thresholds from experience

**Learnable Thresholds:**
```python
self.learnable_thresholds = {
    'untrusted_no_sanitization_threat': 0.5,      # Initial: random
    'taint_propagation_threshold': 7.0,           # Initial: random
    'high_threat_threshold': 0.7,                 # Initial: random
    'low_threat_threshold': 0.3,                 # Initial: random
    'sanitization_reduction_factor': 0.1,         # Initial: random
    'sanitized_taint_propagation_threat': 0.3,     # Initial: random
}
```

**Learning Algorithm (Gradient Descent):**
```python
def update_thresholds(context, outcome, learning_rate=0.01):
    # If untrusted data without sanitization led to bad outcome
    if context['has_untrusted_data'] and not context['has_sanitization']:
        if outcome < 0:  # Bad outcome
            # Increase threat threshold (be more strict)
            self.learnable_thresholds['untrusted_no_sanitization_threat'] += learning_rate * abs(outcome)
        else:  # Good outcome
            # Decrease threat threshold (be more lenient)
            self.learnable_thresholds['untrusted_no_sanitization_threat'] -= learning_rate * outcome * 0.1

    # If sanitization was used
    if context['has_sanitization']:
        if outcome < 0:  # Blocked incorrectly
            # Reduce threat from sanitized data
            self.learnable_thresholds['sanitization_reduction_factor'] -= learning_rate * abs(outcome) * 0.5

    # Clamp to reasonable ranges
    self.learnable_thresholds['untrusted_no_sanitization_threat'] = np.clip(
        self.learnable_thresholds['untrusted_no_sanitization_threat'], 0.1, 1.0
    )
```

**Example Learning:**
```
Initial: untrusted_no_sanitization_threat = 0.5

Experience 1: SQL injection (no sanitization) → BAD
  → Update: 0.5 + 0.01 * 1.0 = 0.51

Experience 2: SQL injection (no sanitization) → BAD
  → Update: 0.51 + 0.01 * 1.0 = 0.52

Experience 3: User input (sanitized) → GOOD
  → Update: 0.52 - 0.01 * 1.0 * 0.1 = 0.519

Final: untrusted_no_sanitization_threat = 0.519 (learned from experience)
```

---

## 4. HEURISTIC LEARNNER (autonomous_decision_engine.py)

### Problem: Neural networks are black boxes
We need explainable rules.

### Solution: Decision Tree for rule extraction

**Decision Tree Structure:**
```
                    Root
                has_untrusted_data?
                   /      \
              Yes/          \No
                /              \
         has_sanitization?    SAFE
            /      \
       Yes/          \No
         /              \
    SAFE        taint_propagation_steps > threshold?
                      /      \
                 Yes/          \No
                   /              \
              DANGEROUS        SAFE
```

**Learning Algorithm (Information Gain):**
```python
def _find_best_split(X, y):
    """Find best feature and threshold to split on"""
    best_gain = 0
    best_feature = 0
    best_threshold = 0

    current_entropy = _entropy(y)

    for feature in range(X.shape[1]):
        for threshold in unique_values(X[:, feature]):
            # Split data
            left_mask = X[:, feature] <= threshold
            right_mask = ~left_mask

            # Calculate information gain
            left_entropy = _entropy(y[left_mask])
            right_entropy = _entropy(y[right_mask])
            gain = current_entropy - weighted_average(left_entropy, right_entropy)

            if gain > best_gain:
                best_gain = gain
                best_feature = feature
                best_threshold = threshold

    return best_feature, best_threshold, best_gain
```

**Output: Human-readable rules**
```python
if has_untrusted_data and not has_sanitization:
    if taint_propagation_steps > 7.5:
        return DANGEROUS
    else:
        return SAFE
else:
    return SAFE
```

---

## 5. INTELLIGENT LOAD CONTROLLER (intelligent_load_controller.py)

### ML Model: Logistic Regression (pure numpy)

**Structure:**
```python
# Feature vector: [load_ratio, is_overloaded, response_time, timestamp]
features = [0.8, 1.0, 0.5, 123]

# Learned weights (from training)
model_weights = [-0.059, -0.025, -0.028, -28.5]
model_bias = -0.0589

# Decision: z = features · weights + bias
z = np.dot(features, model_weights) + model_bias

# Sigmoid: probability = 1 / (1 + exp(-z))
probability = sigmoid(z)

# Decision
if probability > 0.5:
    should_send = True
else:
    should_send = False
```

**Learning from Experience:**
```python
def record_experience(state, action, outcome):
    # Extract features
    features = {
        "load_ratio": state.active_requests / state.capacity,
        "is_overloaded": 1.0 if state.is_overloaded else 0.0,
        "response_time": state.response_time,
        "timestamp": state.timestamp
    }

    # Label: good = 1, bad = 0
    label = 1.0 if outcome else 0.0

    # Store in experience buffer
    experience_buffer.append({
        "features": features,
        "label": label
    })

    # Retrain if enough data
    if len(experience_buffer) >= 50:
        _train_ml_model()

def _train_ml_model():
    # Train logistic regression using gradient descent
    X = extract_features(experience_buffer)
    y = extract_labels(experience_buffer)

    # Initialize weights
    weights = np.random.randn(4)
    bias = 0.0

    # Gradient descent
    for epoch in range(100):
        z = np.dot(X, weights) + bias
        y_pred = sigmoid(z)

        # Compute gradients
        dz = y_pred - y
        dw = (1/m) * np.dot(X.T, dz)
        db = (1/m) * np.sum(dz)

        # Update weights
        weights -= learning_rate * dw
        bias -= learning_rate * db

    self.model_weights = weights
    self.model_bias = bias
    self.is_trained = True
```

---

## 6. ML HEURISTIC GENERATOR (ml_heuristic_generator.py)

### Uses sklearn models (Random Forest, Gradient Boosting, etc.)

**Models Available:**
- Random Forest Classifier
- Gradient Boosting Classifier
- Logistic Regression
- SVM
- K-Means Clustering

**Learning Compiler Heuristics:**
```python
class MLHeuristicGenerator:
    def extract_features(program_graph, profiling_data):
        """Extract features for ML"""
        features = {
            # Graph structure
            "num_nodes": len(program_graph.nodes),
            "num_edges": len(program_graph.edges),
            "avg_degree": 2 * num_edges / num_nodes,

            # Code complexity
            "cyclomatic_complexity": num_edges - num_nodes + 2,
            "nesting_depth": max_nesting_level,

            # Profiling data
            "execution_time": profiling_data["avg_time"],
            "memory_usage": profiling_data["avg_memory"],
            "cache_misses": profiling_data["cache_miss_rate"],
        }
        return features

    def train_heuristic(X, y, model_type="random_forest"):
        """Train ML model to learn heuristic"""
        if model_type == "random_forest":
            model = RandomForestClassifier(n_estimators=100)
        elif model_type == "gradient_boosting":
            model = GradientBoostingClassifier(n_estimators=100)

        model.fit(X, y)

        # Extract feature importance
        importance = dict(zip(feature_names, model.feature_importances_))

        return Heuristic(
            name="security_check_heuristic",
            model_type=model_type,
            features=feature_names,
            condition=_extract_rule(model),  # Extract human-readable rule
            confidence=model.score(X, y),
            model=model,
            feature_importance=importance
        )
```

---

## COMPLETE ML WORKFLOW IN IPL

```
┌─────────────────────────────────────────────────────────────────┐
│                    IPL DECISION FLOW                             │
└─────────────────────────────────────────────────────────────────┘

1. CODE INPUT
   ↓
2. EXTRACT CONTEXT FEATURES (64-dimensional vector)
   ↓
3. NEURAL NETWORK FORWARD PASS
   Input → Hidden (ReLU) → Output (Sigmoid)
   Output: [safe_prob=0.52, dangerous_prob=0.48]
   ↓
4. COMPARE WITH LEARNED THRESHOLDS
   threat_level = computed from context
   if threat_level > learned_thresholds['high_threat_threshold']:
       decision = DANGEROUS
   else:
       decision = SAFE
   ↓
5. MAKE DECISION
   ↓
6. RECORD OUTCOME (after execution)
   - If code was safe: reward = +1.0
   - If code was dangerous: reward = -1.0
   ↓
7. BACKPROPAGATION (LEARNING)
   - Compute gradients from error
   - Update neural network weights
   - Compute Fisher Information for EWC
   ↓
8. UPDATE THRESHOLDS
   - Adjust learnable thresholds via gradient descent
   - Clamp to reasonable ranges
   ↓
9. TRAIN HEURISTIC LEARNER
   - Accumulate (features, decision) pairs
   - Build decision tree for explainable rules
   ↓
10. SAVE STATE
    - Neural network weights
    - Fisher Information matrix
    - Learned thresholds
    - Experience buffer
    → Saved to .ipl_data/autonomous_engine_state.json
```

---

## PERSISTENCE & STATE MANAGEMENT

**What Gets Saved:**
```json
{
  "neural_network_weights": {
    "W1": [[...], [...]],
    "b1": [...],
    "W2": [[...], [...]],
    "b2": [...]
  },
  "fisher_information": {
    "W1": [[...], [...]],
    "b1": [...],
    "W2": [[...], [...]],
    "b2": [...]
  },
  "optimal_params": {
    "W1": [[...], [...]],
    "b1": [...],
    "W2": [[...], [...]],
    "b2": [...]
  },
  "learned_thresholds": {
    "untrusted_no_sanitization_threat": 0.5181,
    "taint_propagation_threshold": 11.8612,
    "high_threat_threshold": 0.7244,
    "low_threat_threshold": 0.2764,
    "sanitization_reduction_factor": 0.1190
  },
  "experience_buffer": [
    {"features": [...], "label": 1.0, "timestamp": "..."},
    {"features": [...], "label": 0.0, "timestamp": "..."}
  ],
  "statistics": {
    "total_decisions": 13,
    "good_decisions": 6,
    "bad_decisions": 7,
    "success_rate": 0.4615
  }
}
```

**Auto-Save Triggers:**
- After every decision outcome
- After neural network weight update
- After threshold adjustment
- Before program exit

---

## KEY INNOVATIONS

1. **No Hardcoded Rules**: All thresholds learned from experience
2. **Continual Learning**: EWC prevents catastrophic forgetting
3. **Explainable AI**: Decision trees extract human-readable rules
4. **Pure Numpy**: No ML framework dependencies (except sklearn for heuristics)
5. **Persistence**: Learned state survives program restarts
6. **Auto-Configuration**: Thresholds adapt to runtime behavior

---

## CURRENT STATUS (from test results)

**Neural Network Performance:**
- 13 total decisions
- 46.15% success rate
- Needs more training data

**Learned Thresholds (actual values from .ipl_data/):**
```
untrusted_no_sanitization_threat: 0.5181  (learned from experience)
taint_propagation_threshold: 11.8612
high_threat_threshold: 0.7244
low_threat_threshold: 0.2764
sanitization_reduction_factor: 0.1190
```

**Persistence:** ✅ Working (weights, thresholds, experience buffer saved)

**ML Components Status:**
- ✅ Neural Network (forward/backprop working)
- ✅ Continual Learning (EWC implemented)
- ✅ Learnable Thresholds (gradient descent working)
- ✅ Heuristic Learner (decision tree implemented)
- ✅ Load Controller (logistic regression working)
- ⚠️ Accuracy low (needs more training data)
