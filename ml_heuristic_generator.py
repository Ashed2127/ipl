"""
ML-Based Heuristic Generator for IPL
Based on research: "Intelligent Compilers" (Cavazos et al.)
and machine learning for compiler heuristics

This module implements:
- Automatic learning of security check heuristics
- ML-based optimization suggestion generation
- Pattern discovery for compiler decisions
- Heuristic evolution and adaptation
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import pickle


class HeuristicType(Enum):
    """Types of heuristics to generate"""
    SECURITY_CHECK = "security_check"
    OPTIMIZATION_FLAG = "optimization_flag"
    INLINE_DECISION = "inline_decision"
    UNROLL_FACTOR = "unroll_factor"
    PARALLELIZATION = "parallelization"
    TAINT_PROPAGATION = "taint_propagation"


class MLModelType(Enum):
    """Types of ML models for heuristic generation"""
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    LOGISTIC_REGRESSION = "logistic_regression"
    SVM = "svm"
    KMEANS = "kmeans"


@dataclass
class Heuristic:
    """Learned heuristic for compiler decision"""
    name: str
    heuristic_type: HeuristicType
    model_type: MLModelType
    features: List[str]
    condition: str  # Human-readable condition
    confidence: float
    accuracy: float
    model: Any  # Trained ML model
    scaler: Optional[Any] = None
    feature_importance: Optional[Dict[str, float]] = None


@dataclass
class HeuristicDecision:
    """Decision made by a heuristic"""
    heuristic_name: str
    decision: bool  # True/False for binary decisions
    confidence: float
    reasoning: str


class MLHeuristicGenerator:
    """
    Machine learning-based heuristic generator for IPL.

    Automatically learns compiler heuristics from collected statistics,
    replacing hand-tuned rules with data-driven decisions.
    Based on Cavazos et al.'s work on automatic optimization heuristics.
    """

    def __init__(self):
        """Initialize ML heuristic generator"""
        self.heuristics: Dict[str, Heuristic] = {}
        self.feature_vectorizer = DictVectorizer(sparse=False)
        self.scaler = StandardScaler()
        self.is_fitted = False

    def extract_features(self, program_graph, profiling_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract features from program graph and profiling data.

        Args:
            program_graph: ProgramGraph instance
            profiling_data: Profiling statistics

        Returns:
            Feature dictionary
        """
        features = {}

        # Graph structure features
        stats = program_graph.get_statistics()
        features['num_nodes'] = stats['num_nodes']
        features['num_edges'] = stats['num_edges']
        features['avg_degree'] = stats['avg_degree']
        features['node_count_variable'] = stats['node_types'].get('variable', 0)
        features['node_count_sink'] = stats['node_types'].get('sink', 0)
        features['node_count_source'] = stats['node_types'].get('source', 0)
        features['node_count_sanitizer'] = stats['node_types'].get('sanitizer', 0)

        # Profiling features
        if profiling_data:
            features['execution_count'] = profiling_data.get('execution_count', 0)
            features['avg_execution_time_ms'] = profiling_data.get('avg_time_ms', 0)
            features['total_time_ms'] = profiling_data.get('total_time_ms', 0)
            features['security_blocks'] = profiling_data.get('security_blocks', 0)
            features['cache_hit_rate'] = profiling_data.get('cache_hit_rate', 0)

        # Taint features
        features['taint_propagation_steps'] = profiling_data.get('taint_propagation_steps', 0)
        features['has_untrusted_data'] = 1 if features.get('node_count_source', 0) > 0 else 0
        features['has_sanitization'] = 1 if features.get('node_count_sanitizer', 0) > 0 else 0

        # Ratios
        if features['num_nodes'] > 0:
            features['sink_to_node_ratio'] = features['node_count_sink'] / features['num_nodes']
            features['source_to_node_ratio'] = features['node_count_source'] / features['num_nodes']
            features['sanitizer_to_source_ratio'] = (
                features['node_count_sanitizer'] / max(1, features['node_count_source'])
            )
        else:
            features['sink_to_node_ratio'] = 0
            features['source_to_node_ratio'] = 0
            features['sanitizer_to_source_ratio'] = 0

        return features

    def learn_security_check_heuristic(self,
                                      training_data: List[Dict[str, Any]],
                                      labels: List[int],
                                      model_type: MLModelType = MLModelType.RANDOM_FOREST) -> Heuristic:
        """
        Learn a heuristic for security check decisions.

        Args:
            training_data: List of feature dictionaries
            labels: Binary labels (1 = check needed, 0 = check not needed)
            model_type: Type of ML model to use

        Returns:
            Learned heuristic
        """
        # Vectorize features
        X = self.feature_vectorizer.fit_transform(training_data)
        y = np.array(labels)

        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        self.is_fitted = True

        # Train model
        model = self._create_model(model_type)
        model.fit(X_scaled, y)

        # Evaluate model
        scores = cross_val_score(model, X_scaled, y, cv=5)
        accuracy = scores.mean()

        # Get feature importance
        feature_importance = self._get_feature_importance(model, self.feature_vectorizer)

        # Create human-readable condition
        condition = self._generate_condition(feature_importance, model_type)

        # Create heuristic
        heuristic = Heuristic(
            name=f"security_check_{model_type.value}",
            heuristic_type=HeuristicType.SECURITY_CHECK,
            model_type=model_type,
            features=list(self.feature_vectorizer.get_feature_names_out()),
            condition=condition,
            confidence=accuracy,
            accuracy=accuracy,
            model=model,
            scaler=self.scaler,
            feature_importance=feature_importance
        )

        self.heuristics[heuristic.name] = heuristic
        return heuristic

    def learn_optimization_heuristic(self,
                                    training_data: List[Dict[str, Any]],
                                    labels: List[int],
                                    model_type: MLModelType = MLModelType.GRADIENT_BOOSTING) -> Heuristic:
        """
        Learn a heuristic for optimization decisions.

        Args:
            training_data: List of feature dictionaries
            labels: Binary labels (1 = optimize, 0 = don't optimize)
            model_type: Type of ML model to use

        Returns:
            Learned heuristic
        """
        # Vectorize features
        X = self.feature_vectorizer.fit_transform(training_data)
        y = np.array(labels)

        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        self.is_fitted = True

        # Train model
        model = self._create_model(model_type)
        model.fit(X_scaled, y)

        # Evaluate model
        scores = cross_val_score(model, X_scaled, y, cv=5)
        accuracy = scores.mean()

        # Get feature importance
        feature_importance = self._get_feature_importance(model, self.feature_vectorizer)

        # Create human-readable condition
        condition = self._generate_condition(feature_importance, model_type)

        # Create heuristic
        heuristic = Heuristic(
            name=f"optimization_{model_type.value}",
            heuristic_type=HeuristicType.OPTIMIZATION_FLAG,
            model_type=model_type,
            features=list(self.feature_vectorizer.get_feature_names_out()),
            condition=condition,
            confidence=accuracy,
            accuracy=accuracy,
            model=model,
            scaler=self.scaler,
            feature_importance=feature_importance
        )

        self.heuristics[heuristic.name] = heuristic
        return heuristic

    def apply_heuristic(self,
                       heuristic_name: str,
                       features: Dict[str, float]) -> HeuristicDecision:
        """
        Apply a learned heuristic to make a decision.

        Args:
            heuristic_name: Name of heuristic to apply
            features: Feature dictionary

        Returns:
            Heuristic decision
        """
        if heuristic_name not in self.heuristics:
            raise ValueError(f"Heuristic {heuristic_name} not found")

        heuristic = self.heuristics[heuristic_name]

        # Vectorize and scale features
        X = self.feature_vectorizer.transform([features])
        X_scaled = heuristic.scaler.transform(X)

        # Make prediction
        prediction = heuristic.model.predict(X_scaled)[0]
        confidence = self._get_prediction_confidence(heuristic.model, X_scaled)

        # Generate reasoning
        reasoning = f"Based on {heuristic.condition}"

        return HeuristicDecision(
            heuristic_name=heuristic_name,
            decision=bool(prediction),
            confidence=confidence,
            reasoning=reasoning
        )

    def _create_model(self, model_type: MLModelType):
        """Create ML model of specified type"""
        if model_type == MLModelType.RANDOM_FOREST:
            return RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == MLModelType.GRADIENT_BOOSTING:
            return GradientBoostingClassifier(n_estimators=100, random_state=42)
        elif model_type == MLModelType.LOGISTIC_REGRESSION:
            return LogisticRegression(random_state=42, max_iter=1000)
        elif model_type == MLModelType.SVM:
            return SVC(probability=True, random_state=42)
        elif model_type == MLModelType.KMEANS:
            return KMeans(n_clusters=2, random_state=42)
        else:
            raise ValueError(f"Unknown model type: {model_type}")

    def _get_feature_importance(self, model, vectorizer) -> Dict[str, float]:
        """Get feature importance from model"""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            feature_names = vectorizer.get_feature_names_out()
            return dict(zip(feature_names, importances))
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_[0])
            feature_names = vectorizer.get_feature_names_out()
            return dict(zip(feature_names, importances))
        else:
            return {}

    def _get_prediction_confidence(self, model, X) -> float:
        """Get confidence score for prediction"""
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(X)[0]
            return max(probs)
        elif hasattr(model, 'decision_function'):
            # Normalize decision function to [0, 1]
            decision = model.decision_function(X)[0]
            return 1.0 / (1.0 + np.exp(-decision))
        else:
            return 0.5

    def _generate_condition(self, feature_importance: Dict[str, float], model_type: MLModelType) -> str:
        """Generate human-readable condition from feature importance"""
        # Sort features by importance
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)

        # Take top 3 features
        top_features = sorted_features[:3]

        # Generate condition
        conditions = []
        for feature, importance in top_features:
            if importance > 0.5:
                conditions.append(f"high {feature}")
            elif importance > 0.2:
                conditions.append(f"moderate {feature}")
            else:
                conditions.append(f"low {feature}")

        if not conditions:
            return "default heuristic"

        return " AND ".join(conditions)

    def discover_patterns(self,
                         training_data: List[Dict[str, Any]],
                         n_clusters: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Discover patterns in training data using clustering.

        Args:
            training_data: List of feature dictionaries
            n_clusters: Number of clusters to find

        Returns:
            Dictionary of clusters with their members
        """
        # Vectorize features
        X = self.feature_vectorizer.fit_transform(training_data)

        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        self.is_fitted = True

        # Cluster
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)

        # Group by cluster
        clusters_dict = {}
        for i, cluster_id in enumerate(clusters):
            if cluster_id not in clusters_dict:
                clusters_dict[str(cluster_id)] = []
            clusters_dict[str(cluster_id)].append(training_data[i])

        return clusters_dict

    def save_heuristics(self, path: str):
        """Save learned heuristics to file"""
        heuristics_data = {
            name: {
                'name': h.name,
                'heuristic_type': h.heuristic_type.value,
                'model_type': h.model_type.value,
                'features': h.features,
                'condition': h.condition,
                'confidence': h.confidence,
                'accuracy': h.accuracy,
                'model': pickle.dumps(h.model),
                'scaler': pickle.dumps(h.scaler) if h.scaler else None,
                'feature_importance': h.feature_importance
            }
            for name, h in self.heuristics.items()
        }

        with open(path, 'w') as f:
            json.dump(heuristics_data, f, indent=2)

    def load_heuristics(self, path: str):
        """Load learned heuristics from file"""
        with open(path, 'r') as f:
            heuristics_data = json.load(f)

        for name, data in heuristics_data.items():
            model = pickle.loads(data['model'])
            scaler = pickle.loads(data['scaler']) if data['scaler'] else None

            heuristic = Heuristic(
                name=data['name'],
                heuristic_type=HeuristicType(data['heuristic_type']),
                model_type=MLModelType(data['model_type']),
                features=data['features'],
                condition=data['condition'],
                confidence=data['confidence'],
                accuracy=data['accuracy'],
                model=model,
                scaler=scaler,
                feature_importance=data['feature_importance']
            )

            self.heuristics[name] = heuristic

        self.is_fitted = True


# Test the ML heuristic generator
if __name__ == "__main__":
    print("Testing ML Heuristic Generator")

    generator = MLHeuristicGenerator()

    # Generate synthetic training data
    training_data = []
    labels = []

    for i in range(100):
        features = {
            'num_nodes': np.random.randint(5, 50),
            'num_edges': np.random.randint(5, 100),
            'node_count_sink': np.random.randint(0, 5),
            'node_count_source': np.random.randint(0, 5),
            'node_count_sanitizer': np.random.randint(0, 5),
            'execution_count': np.random.randint(0, 1000),
            'avg_execution_time_ms': np.random.uniform(0.1, 10.0),
            'security_blocks': np.random.randint(0, 10),
        }

        # Simple rule for labeling: need security check if has source
        label = 1 if features['node_count_source'] > 0 else 0

        training_data.append(features)
        labels.append(label)

    # Learn security check heuristic
    print("\nLearning security check heuristic...")
    heuristic = generator.learn_security_check_heuristic(
        training_data,
        labels,
        MLModelType.RANDOM_FOREST
    )

    print(f"Heuristic: {heuristic.name}")
    print(f"Condition: {heuristic.condition}")
    print(f"Accuracy: {heuristic.accuracy:.4f}")
    print(f"Top features: {list(heuristic.feature_importance.keys())[:5]}")

    # Apply heuristic to new data
    test_features = {
        'num_nodes': 20,
        'num_edges': 30,
        'node_count_sink': 2,
        'node_count_source': 1,
        'node_count_sanitizer': 0,
        'execution_count': 50,
        'avg_execution_time_ms': 2.5,
        'security_blocks': 0,
    }

    decision = generator.apply_heuristic(heuristic.name, test_features)
    print(f"\nDecision: {decision.decision}")
    print(f"Confidence: {decision.confidence:.4f}")
    print(f"Reasoning: {decision.reasoning}")

    # Discover patterns
    print("\nDiscovering patterns...")
    patterns = generator.discover_patterns(training_data, n_clusters=3)
    for cluster_id, members in patterns.items():
        print(f"Cluster {cluster_id}: {len(members)} programs")

    print("\nML Heuristic Generator test completed!")
