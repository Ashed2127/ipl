"""
Continual Learning System for IPL
Based on research: "Intelligent Compilers" (Cavazos et al.)
and continual learning methodologies (Chen et al., Parisi et al.)

This module implements:
- Continual learning for model updates without catastrophic forgetting
- Experience replay for maintaining knowledge
- Elastic weight consolidation for protecting important weights
- Model versioning and rollback
- Transfer learning across tasks
"""

import torch
import torch.nn as nn
import torch.optim as optim
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np
import json
import hashlib
from collections import deque
import pickle


class ContinualLearningMethod(Enum):
    """Continual learning methods"""
    EXPERIENCE_REPLAY = "experience_replay"
    ELASTIC_WEIGHT_CONSOLIDATION = "elastic_weight_consolidation"
    SYNTHETIC_DATA_GENERATION = "synthetic_data_generation"
    GRADIENT_EPISODIC_MEMORY = "gradient_episodic_memory"
    HYBRID = "hybrid"


@dataclass
class ModelVersion:
    """Version information for a model"""
    version_id: str
    timestamp: str
    accuracy: float
    training_data_size: int
    method: ContinualLearningMethod
    model_state: Dict[str, Any]
    performance_metrics: Dict[str, float]


@dataclass
class Experience:
    """Stored experience for replay"""
    features: np.ndarray
    label: int
    task_id: str
    timestamp: str
    importance: float


class ContinualLearner:
    """
    Continual learning system for IPL models.

    Implements multiple continual learning strategies to prevent
    catastrophic forgetting while allowing models to learn from new data.
    Based on research by Chen et al. and Parisi et al.
    """

    def __init__(self,
                 model: nn.Module,
                 method: ContinualLearningMethod = ContinualLearningMethod.EXPERIENCE_REPLAY,
                 replay_buffer_size: int = 1000,
                 ewc_lambda: float = 1000.0,
                 gamma: float = 0.9):
        """
        Initialize continual learner.

        Args:
            model: PyTorch model to continually train
            method: Continual learning method to use
            replay_buffer_size: Size of experience replay buffer
            ewc_lambda: EWC regularization strength
            gamma: Discount factor for importance weighting
        """
        self.model = model
        self.method = method
        self.replay_buffer_size = replay_buffer_size
        self.ewc_lambda = ewc_lambda
        self.gamma = gamma

        # Experience replay buffer
        self.replay_buffer: deque = deque(maxlen=replay_buffer_size)

        # EWC parameters
        self.fisher_information: Optional[Dict[str, torch.Tensor]] = None
        self.optimal_params: Optional[Dict[str, torch.Tensor]] = None

        # Model versioning
        self.versions: List[ModelVersion] = []
        self.current_version_id = self._generate_version_id()

        # Task tracking
        self.task_performance: Dict[str, List[float]] = {}

    def _generate_version_id(self) -> str:
        """Generate unique version ID"""
        return hashlib.md5(str(time.time()).encode()).hexdigest()[:8]

    def add_experience(self, features: np.ndarray, label: int, task_id: str, importance: float = 1.0):
        """
        Add experience to replay buffer.

        Args:
            features: Feature vector
            label: Label
            task_id: Task identifier
            importance: Importance weight for this experience
        """
        experience = Experience(
            features=features,
            label=label,
            task_id=task_id,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            importance=importance
        )
        self.replay_buffer.append(experience)

    def train_with_continual_learning(self,
                                    new_data: List[Tuple[np.ndarray, int]],
                                    task_id: str,
                                    num_epochs: int = 10,
                                    learning_rate: float = 0.001) -> Dict[str, float]:
        """
        Train model with continual learning.

        Args:
            new_data: New training data (features, labels)
            task_id: Task identifier
            num_epochs: Number of training epochs
            learning_rate: Learning rate

        Returns:
            Training metrics
        """
        # Prepare training data
        if self.method in [ContinualLearningMethod.EXPERIENCE_REPLAY,
                          ContinualLearningMethod.HYBRID]:
            # Mix new data with replay buffer
            train_data = self._prepare_replay_data(new_data)
        else:
            train_data = new_data

        # Train model
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        criterion = nn.CrossEntropyLoss()

        metrics = {
            'loss': [],
            'accuracy': []
        }

        for epoch in range(num_epochs):
            epoch_loss = 0.0
            correct = 0
            total = 0

            for features, label in train_data:
                # Convert to tensors
                x = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
                y = torch.tensor([label], dtype=torch.long)

                # Forward pass
                optimizer.zero_grad()

                # Add EWC penalty if using EWC
                loss = criterion(self.model(x), y)

                if self.method in [ContinualLearningMethod.ELASTIC_WEIGHT_CONSOLIDATION,
                                  ContinualLearningMethod.HYBRID]:
                    loss = self._add_ewc_penalty(loss)

                # Backward pass
                loss.backward()
                optimizer.step()

                # Statistics
                epoch_loss += loss.item()
                predicted = self.model(x).argmax(dim=1)
                correct += (predicted == y).sum().item()
                total += y.size(0)

            # Record metrics
            epoch_loss = epoch_loss / len(train_data)
            epoch_acc = correct / max(1, total)
            metrics['loss'].append(epoch_loss)
            metrics['accuracy'].append(epoch_acc)

        # Update Fisher information for EWC
        if self.method in [ContinualLearningMethod.ELASTIC_WEIGHT_CONSOLIDATION,
                          ContinualLearningMethod.HYBRID]:
            self._update_fisher_information(train_data)

        # Store experiences from new data
        if self.method in [ContinualLearningMethod.EXPERIENCE_REPLAY,
                          ContinualLearningMethod.HYBRID]:
            for features, label in new_data:
                self.add_experience(features, label, task_id)

        # Track task performance
        if task_id not in self.task_performance:
            self.task_performance[task_id] = []
        self.task_performance[task_id].append(metrics['accuracy'][-1])

        # Save version
        self._save_version(metrics['accuracy'][-1], len(new_data))

        return {
            'final_loss': metrics['loss'][-1],
            'final_accuracy': metrics['accuracy'][-1],
            'avg_loss': np.mean(metrics['loss']),
            'avg_accuracy': np.mean(metrics['accuracy'])
        }

    def _prepare_replay_data(self, new_data: List[Tuple[np.ndarray, int]]) -> List[Tuple[np.ndarray, int]]:
        """Prepare training data with experience replay"""
        # Get experiences from buffer
        replay_data = [
            (exp.features, exp.label)
            for exp in self.replay_buffer
        ]

        # Combine with new data
        combined_data = replay_data + new_data

        # Shuffle
        np.random.shuffle(combined_data)

        return combined_data

    def _add_ewc_penalty(self, loss: torch.Tensor) -> torch.Tensor:
        """Add EWC regularization penalty to loss"""
        if self.fisher_information is None or self.optimal_params is None:
            return loss

        ewc_penalty = 0
        for name, param in self.model.named_parameters():
            if name in self.fisher_information:
                ewc_penalty += (self.fisher_information[name] *
                               (param - self.optimal_params[name]) ** 2).sum()

        return loss + (self.ewc_lambda / 2) * ewc_penalty

    def _update_fisher_information(self, data: List[Tuple[np.ndarray, int]]):
        """Update Fisher information matrix for EWC"""
        self.model.eval()

        # Initialize Fisher information if first time
        if self.fisher_information is None:
            self.fisher_information = {}
            for name, param in self.model.named_parameters():
                self.fisher_information[name] = torch.zeros_like(param)

        # Calculate Fisher information
        for features, label in data:
            x = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
            y = torch.tensor([label], dtype=torch.long)

            # Forward pass
            output = self.model(x)
            loss = nn.functional.cross_entropy(output, y)

            # Backward pass to get gradients
            self.model.zero_grad()
            loss.backward()

            # Update Fisher information
            for name, param in self.model.named_parameters():
                if param.grad is not None:
                    self.fisher_information[name] += param.grad ** 2

        # Normalize Fisher information
        for name in self.fisher_information:
            self.fisher_information[name] /= len(data)

        # Store optimal parameters
        self.optimal_parameters = {
            name: param.clone().detach()
            for name, param in self.model.named_parameters()
        }

    def _save_version(self, accuracy: float, data_size: int):
        """Save current model version"""
        version = ModelVersion(
            version_id=self.current_version_id,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            accuracy=accuracy,
            training_data_size=data_size,
            method=self.method,
            model_state={name: param.clone().detach()
                        for name, param in self.model.named_parameters()},
            performance_metrics=self._get_performance_metrics()
        )

        self.versions.append(version)
        self.current_version_id = self._generate_version_id()

    def _get_performance_metrics(self) -> Dict[str, float]:
        """Get current performance metrics"""
        metrics = {}
        for task_id, accuracies in self.task_performance.items():
            if accuracies:
                metrics[f"{task_id}_latest_accuracy"] = accuracies[-1]
                metrics[f"{task_id}_avg_accuracy"] = np.mean(accuracies)
        return metrics

    def rollback_to_version(self, version_id: str) -> bool:
        """
        Rollback model to a previous version.

        Args:
            version_id: Version ID to rollback to

        Returns:
            True if rollback successful
        """
        for version in self.versions:
            if version.version_id == version_id:
                # Restore model state
                for name, param in self.model.named_parameters():
                    if name in version.model_state:
                        param.data.copy_(version.model_state[name])
                return True
        return False

    def get_forgetting_measure(self, task_id: str) -> float:
        """
        Calculate forgetting measure for a task.

        Forgetting = max accuracy - current accuracy

        Args:
            task_id: Task identifier

        Returns:
            Forgetting measure
        """
        if task_id not in self.task_performance or not self.task_performance[task_id]:
            return 0.0

        accuracies = self.task_performance[task_id]
        if len(accuracies) < 2:
            return 0.0

        max_acc = max(accuracies)
        current_acc = accuracies[-1]

        return max_acc - current_acc

    def get_average_forgetting(self) -> float:
        """Get average forgetting across all tasks"""
        forgetting_measures = [
            self.get_forgetting_measure(task_id)
            for task_id in self.task_performance.keys()
        ]
        return np.mean(forgetting_measures) if forgetting_measures else 0.0

    def export_model_state(self) -> Dict[str, Any]:
        """Export model state for persistence"""
        return {
            'model_state_dict': self.model.state_dict(),
            'replay_buffer': [
                {
                    'features': exp.features.tolist(),
                    'label': exp.label,
                    'task_id': exp.task_id,
                    'timestamp': exp.timestamp,
                    'importance': exp.importance
                }
                for exp in self.replay_buffer
            ],
            'fisher_information': {
                name: tensor.tolist()
                for name, tensor in (self.fisher_information or {}).items()
            },
            'optimal_params': {
                name: tensor.tolist()
                for name, tensor in (self.optimal_params or {}).items()
            },
            'versions': [
                {
                    'version_id': v.version_id,
                    'timestamp': v.timestamp,
                    'accuracy': v.accuracy,
                    'training_data_size': v.training_data_size,
                    'method': v.method.value,
                    'performance_metrics': v.performance_metrics
                }
                for v in self.versions
            ],
            'task_performance': self.task_performance,
            'method': self.method.value
        }

    def import_model_state(self, state: Dict[str, Any]):
        """Import model state from persistence"""
        self.model.load_state_dict(state['model_state_dict'])

        # Restore replay buffer
        self.replay_buffer.clear()
        for exp_data in state['replay_buffer']:
            experience = Experience(
                features=np.array(exp_data['features']),
                label=exp_data['label'],
                task_id=exp_data['task_id'],
                timestamp=exp_data['timestamp'],
                importance=exp_data['importance']
            )
            self.replay_buffer.append(experience)

        # Restore Fisher information
        if state['fisher_information']:
            self.fisher_information = {
                name: torch.tensor(tensor)
                for name, tensor in state['fisher_information'].items()
            }

        # Restore optimal parameters
        if state['optimal_params']:
            self.optimal_params = {
                name: torch.tensor(tensor)
                for name, tensor in state['optimal_params'].items()
            }

        # Restore task performance
        self.task_performance = state['task_performance']

        # Restore method
        self.method = ContinualLearningMethod(state['method'])


import time


# Test the continual learning system
if __name__ == "__main__":
    print("Testing Continual Learning System")

    # Create a simple model for testing
    class SimpleModel(nn.Module):
        def __init__(self, input_dim=10, hidden_dim=20, output_dim=5):
            super().__init__()
            self.fc1 = nn.Linear(input_dim, hidden_dim)
            self.fc2 = nn.Linear(hidden_dim, output_dim)

        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = self.fc2(x)
            return x

    model = SimpleModel()
    learner = ContinualLearner(
        model=model,
        method=ContinualLearningMethod.EXPERIENCE_REPLAY,
        replay_buffer_size=100
    )

    # Simulate training on multiple tasks
    for task_id in ['task1', 'task2', 'task3']:
        print(f"\nTraining on {task_id}...")

        # Generate synthetic data
        task_data = [
            (np.random.randn(10), np.random.randint(0, 5))
            for _ in range(50)
        ]

        # Train with continual learning
        metrics = learner.train_with_continual_learning(
            task_data,
            task_id,
            num_epochs=5,
            learning_rate=0.01
        )

        print(f"  Accuracy: {metrics['final_accuracy']:.4f}")
        print(f"  Loss: {metrics['final_loss']:.4f}")

    # Check forgetting
    print("\nForgetting Measures:")
    for task_id in learner.task_performance.keys():
        forgetting = learner.get_forgetting_measure(task_id)
        print(f"  {task_id}: {forgetting:.4f}")

    print(f"Average Forgetting: {learner.get_average_forgetting():.4f}")

    print("\nContinual Learning System test completed!")
