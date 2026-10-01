"""
Graph Neural Network Engine for IPL
Based on research: "Towards intelligent compiler optimization" (Kovac et al.)
and ProGraML: Graph-based Deep Learning for Program Optimization

This module implements GNN models for:
- Program embedding and representation learning
- Security pattern detection (SQL injection, XSS, command injection)
- Optimization suggestion generation
- Code classification and clustering
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from enum import Enum

try:
    from torch_geometric.nn import GCNConv, GATConv, global_mean_pool, global_max_pool
    from torch_geometric.data import Data, Batch
    PYG_AVAILABLE = True
except ImportError:
    PYG_AVAILABLE = False
    print("Warning: PyTorch Geometric not available. Using fallback implementation.")

from program_graph import ProgramGraph, NodeType, EdgeType, build_program_graph


class GNNModelType(Enum):
    """Types of GNN models"""
    GCN = "gcn"  # Graph Convolutional Network
    GAT = "gat"  # Graph Attention Network
    GCN_GAT = "gcn_gat"  # Hybrid GCN + GAT


class SecurityPattern(Enum):
    """Security patterns to detect"""
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    COMMAND_INJECTION = "command_injection"
    PATH_TRAVERSAL = "path_traversal"
    SAFE = "safe"


class GNNModel(nn.Module):
    """
    Base Graph Neural Network model for program analysis.

    Implements a GCN-based model as described in Kovac et al.
    for learning program representations and detecting patterns.
    """

    def __init__(self,
                 input_dim: int = 20,
                 hidden_dim: int = 128,
                 output_dim: int = 64,
                 num_layers: int = 3,
                 model_type: GNNModelType = GNNModelType.GCN,
                 num_heads: int = 4,
                 dropout: float = 0.5):
        """
        Initialize GNN model.

        Args:
            input_dim: Dimension of input node features
            hidden_dim: Dimension of hidden layers
            output_dim: Dimension of output embeddings
            num_layers: Number of GNN layers
            model_type: Type of GNN model (GCN, GAT, or hybrid)
            num_heads: Number of attention heads (for GAT)
            dropout: Dropout rate
        """
        super(GNNModel, self).__init__()

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.num_layers = num_layers
        self.model_type = model_type
        self.num_heads = num_heads
        self.dropout = dropout

        # Input projection
        self.input_proj = nn.Linear(input_dim, hidden_dim)

        # GNN layers
        self.convs = nn.ModuleList()
        self.batch_norms = nn.ModuleList()

        for i in range(num_layers):
            if model_type == GNNModelType.GCN:
                self.convs.append(GCNConv(hidden_dim, hidden_dim))
            elif model_type == GNNModelType.GAT:
                self.convs.append(GATConv(hidden_dim, hidden_dim // num_heads,
                                         heads=num_heads, dropout=dropout))
            elif model_type == GNNModelType.GCN_GAT:
                if i % 2 == 0:
                    self.convs.append(GCNConv(hidden_dim, hidden_dim))
                else:
                    self.convs.append(GATConv(hidden_dim, hidden_dim // num_heads,
                                             heads=num_heads, dropout=dropout))

            self.batch_norms.append(nn.BatchNorm1d(hidden_dim))

        # Output projection
        self.output_proj = nn.Linear(hidden_dim, output_dim)

        # Dropout
        self.dropout_layer = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor,
                batch: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Forward pass through GNN.

        Args:
            x: Node features [num_nodes, input_dim]
            edge_index: Edge indices [2, num_edges]
            batch: Batch vector [num_nodes] (for graph-level tasks)

        Returns:
            Node embeddings [num_nodes, output_dim] or graph embeddings [batch_size, output_dim]
        """
        # Input projection
        x = self.input_proj(x)
        x = F.relu(x)
        x = self.dropout_layer(x)

        # GNN layers
        for i, (conv, bn) in enumerate(zip(self.convs, self.batch_norms)):
            x = conv(x, edge_index)

            # Handle GAT output (concat heads)
            if self.model_type in [GNNModelType.GAT, GNNModelType.GCN_GAT]:
                if isinstance(conv, GATConv):
                    x = x.view(-1, self.hidden_dim)

            x = bn(x)
            x = F.relu(x)
            x = self.dropout_layer(x)

        # Output projection
        x = self.output_proj(x)

        # Graph-level pooling if batch provided
        if batch is not None:
            x = global_mean_pool(x, batch)

        return x


class SecurityClassifier(nn.Module):
    """
    GNN-based security classifier for detecting vulnerabilities.

    Classifies program graphs into security categories:
    - SQL injection
    - XSS
    - Command injection
    - Path traversal
    - Safe
    """

    def __init__(self,
                 input_dim: int = 20,
                 hidden_dim: int = 128,
                 num_classes: int = 5,
                 num_layers: int = 3,
                 model_type: GNNModelType = GNNModelType.GCN):
        """
        Initialize security classifier.

        Args:
            input_dim: Dimension of input node features
            hidden_dim: Dimension of hidden layers
            num_classes: Number of security classes
            num_layers: Number of GNN layers
            model_type: Type of GNN model
        """
        super(SecurityClassifier, self).__init__()

        self.gnn = GNNModel(
            input_dim=input_dim,
            hidden_dim=hidden_dim,
            output_dim=hidden_dim,
            num_layers=num_layers,
            model_type=model_type
        )

        # Classification head
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(hidden_dim // 2, num_classes)
        )

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor,
                batch: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for classification.

        Args:
            x: Node features
            edge_index: Edge indices
            batch: Batch vector

        Returns:
            Class logits [batch_size, num_classes]
        """
        # Get graph embeddings
        graph_emb = self.gnn(x, edge_index, batch)

        # Classify
        logits = self.classifier(graph_emb)

        return logits


class OptimalityPredictor(nn.Module):
    """
    GNN-based predictor for optimization effectiveness.

    Predicts which optimizations will be effective for a given program.
    Based on Cavazos et al.'s work on automatic optimization heuristics.
    """

    def __init__(self,
                 input_dim: int = 20,
                 hidden_dim: int = 128,
                 num_optimizations: int = 10,
                 num_layers: int = 3):
        """
        Initialize optimality predictor.

        Args:
            input_dim: Dimension of input node features
            hidden_dim: Dimension of hidden layers
            num_optimizations: Number of optimization options
            num_layers: Number of GNN layers
        """
        super(OptimalityPredictor, self).__init__()

        self.gnn = GNNModel(
            input_dim=input_dim,
            hidden_dim=hidden_dim,
            output_dim=hidden_dim,
            num_layers=num_layers
        )

        # Optimization prediction head
        self.optimizer_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim // 2, num_optimizations),
            nn.Sigmoid()  # Predict probability of effectiveness
        )

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor,
                batch: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for optimization prediction.

        Args:
            x: Node features
            edge_index: Edge indices
            batch: Batch vector

        Returns:
            Optimization effectiveness scores [batch_size, num_optimizations]
        """
        graph_emb = self.gnn(x, edge_index, batch)
        scores = self.optimizer_head(graph_emb)
        return scores


class GNNEngine:
    """
    Main GNN engine for IPL intelligent compiler.

    Manages GNN models, training, and inference for:
    - Security pattern detection
    - Optimization suggestion
    - Program embedding
    """

    def __init__(self,
                 device: str = 'cpu',
                 model_type: GNNModelType = GNNModelType.GCN):
        """
        Initialize GNN engine.

        Args:
            device: Device to run models on ('cpu' or 'cuda')
            model_type: Type of GNN model to use
        """
        self.device = torch.device(device)
        self.model_type = model_type

        # Models
        self.security_classifier: Optional[SecurityClassifier] = None
        self.optimality_predictor: Optional[OptimalityPredictor] = None
        self.embedding_model: Optional[GNNModel] = None

        # Training state
        self.is_trained = False
        self.training_history: List[Dict[str, float]] = []

    def initialize_security_classifier(self,
                                      input_dim: int = 20,
                                      hidden_dim: int = 128,
                                      num_classes: int = 5):
        """Initialize security classifier model"""
        self.security_classifier = SecurityClassifier(
            input_dim=input_dim,
            hidden_dim=hidden_dim,
            num_classes=num_classes,
            model_type=self.model_type
        ).to(self.device)

    def initialize_optimality_predictor(self,
                                        input_dim: int = 20,
                                        hidden_dim: int = 128,
                                        num_optimizations: int = 10):
        """Initialize optimality predictor model"""
        self.optimality_predictor = OptimalityPredictor(
            input_dim=input_dim,
            hidden_dim=hidden_dim,
            num_optimizations=num_optimizations
        ).to(self.device)

    def initialize_embedding_model(self,
                                   input_dim: int = 20,
                                   hidden_dim: int = 128,
                                   output_dim: int = 64):
        """Initialize embedding model"""
        self.embedding_model = GNNModel(
            input_dim=input_dim,
            hidden_dim=hidden_dim,
            output_dim=output_dim,
            model_type=self.model_type
        ).to(self.device)

    def program_graph_to_pyg_data(self, program_graph: ProgramGraph) -> Data:
        """
        Convert ProgramGraph to PyTorch Geometric Data object.

        Args:
            program_graph: ProgramGraph instance

        Returns:
            PyTorch Geometric Data object
        """
        # Get adjacency matrix and features
        adj_matrix, node_features, _ = program_graph.get_adjacency_matrix()

        # Convert to torch tensors
        x = torch.tensor(np.array(node_features), dtype=torch.float)
        edge_index = torch.tensor(adj_matrix.nonzero(), dtype=torch.long)

        # Create Data object
        data = Data(x=x, edge_index=edge_index)

        return data

    def train_security_classifier(self,
                                   train_data: List[Data],
                                   train_labels: List[int],
                                   num_epochs: int = 100,
                                   learning_rate: float = 0.001):
        """
        Train security classifier.

        Args:
            train_data: List of PyG Data objects
            train_labels: List of security labels
            num_epochs: Number of training epochs
            learning_rate: Learning rate
        """
        if self.security_classifier is None:
            raise ValueError("Security classifier not initialized")

        # Create DataLoader
        loader = self._create_dataloader(train_data, train_labels)

        # Optimizer and loss
        optimizer = torch.optim.Adam(self.security_classifier.parameters(),
                                     lr=learning_rate)
        criterion = nn.CrossEntropyLoss()

        # Training loop
        self.security_classifier.train()
        for epoch in range(num_epochs):
            total_loss = 0
            correct = 0
            total = 0

            for batch in loader:
                batch = batch.to(self.device)
                optimizer.zero_grad()

                # Forward pass
                logits = self.security_classifier(batch.x, batch.edge_index, batch.batch)
                loss = criterion(logits, batch.y)

                # Backward pass
                loss.backward()
                optimizer.step()

                # Statistics
                total_loss += loss.item()
                predicted = logits.argmax(dim=1)
                correct += (predicted == batch.y).sum().item()
                total += batch.y.size(0)

            # Record training history
            epoch_loss = total_loss / len(loader)
            epoch_acc = correct / total
            self.training_history.append({
                'epoch': epoch,
                'loss': epoch_loss,
                'accuracy': epoch_acc
            })

            if epoch % 10 == 0:
                print(f"Epoch {epoch}: Loss={epoch_loss:.4f}, Acc={epoch_acc:.4f}")

        self.is_trained = True

    def predict_security(self, program_graph: ProgramGraph) -> Dict[str, Any]:
        """
        Predict security classification for a program.

        Args:
            program_graph: ProgramGraph instance

        Returns:
            Dictionary with security prediction results
        """
        if self.security_classifier is None or not self.is_trained:
            return {
                'error': 'Security classifier not trained',
                'prediction': None,
                'confidence': 0.0
            }

        # Convert to PyG data
        data = self.program_graph_to_pyg_data(program_graph)
        data = data.to(self.device)

        # Predict
        self.security_classifier.eval()
        with torch.no_grad():
            data_batch = Batch.from_data_list([data])
            logits = self.security_classifier(data_batch.x, data_batch.edge_index,
                                              data_batch.batch)
            probs = F.softmax(logits, dim=1)
            predicted_class = probs.argmax(dim=1).item()
            confidence = probs[0, predicted_class].item()

        # Map to security pattern
        patterns = list(SecurityPattern)
        security_pattern = patterns[predicted_class].value if predicted_class < len(patterns) else 'unknown'

        return {
            'prediction': security_pattern,
            'confidence': confidence,
            'all_probabilities': probs[0].cpu().numpy().tolist(),
            'is_safe': security_pattern == 'safe'
        }

    def get_program_embedding(self, program_graph: ProgramGraph) -> np.ndarray:
        """
        Get embedding for a program graph.

        Args:
            program_graph: ProgramGraph instance

        Returns:
            Program embedding as numpy array
        """
        if self.embedding_model is None:
            raise ValueError("Embedding model not initialized")

        # Convert to PyG data
        data = self.program_graph_to_pyg_data(program_graph)
        data = data.to(self.device)

        # Get embedding
        self.embedding_model.eval()
        with torch.no_grad():
            data_batch = Batch.from_data_list([data])
            embedding = self.embedding_model(data_batch.x, data_batch.edge_index,
                                               data_batch.batch)

        return embedding[0].cpu().numpy()

    def _create_dataloader(self, data_list: List[Data], labels: List[int]) -> Any:
        """Create DataLoader from data and labels"""
        # Add labels to data objects
        for data, label in zip(data_list, labels):
            data.y = torch.tensor([label], dtype=torch.long)

        # Create batch
        if PYG_AVAILABLE:
            from torch_geometric.loader import DataLoader
            loader = DataLoader(data_list, batch_size=32, shuffle=True)
            return loader
        else:
            # Fallback: simple batch
            return data_list

    def save_model(self, path: str):
        """Save trained models"""
        checkpoint = {
            'security_classifier': self.security_classifier.state_dict() if self.security_classifier else None,
            'optimality_predictor': self.optimality_predictor.state_dict() if self.optimality_predictor else None,
            'embedding_model': self.embedding_model.state_dict() if self.embedding_model else None,
            'is_trained': self.is_trained,
            'training_history': self.training_history
        }
        torch.save(checkpoint, path)

    def load_model(self, path: str):
        """Load trained models"""
        checkpoint = torch.load(path, map_location=self.device)

        if self.security_classifier and checkpoint['security_classifier']:
            self.security_classifier.load_state_dict(checkpoint['security_classifier'])

        if self.optimality_predictor and checkpoint['optimality_predictor']:
            self.optimality_predictor.load_state_dict(checkpoint['optimality_predictor'])

        if self.embedding_model and checkpoint['embedding_model']:
            self.embedding_model.load_state_dict(checkpoint['embedding_model'])

        self.is_trained = checkpoint['is_trained']
        self.training_history = checkpoint['training_history']


# Test the GNN engine
if __name__ == "__main__":
    from parser import Parser
    from lexer import Lexer

    print("Testing GNN Engine")

    # Initialize engine
    engine = GNNEngine(device='cpu')
    engine.initialize_security_classifier(input_dim=20, hidden_dim=64, num_classes=5)

    # Test code
    test_code = """
    let username = set_untrusted("admin");
    let safe_username = sanitize_for_sql(username);
    db_write("users", safe_username);
    """

    # Parse and build graph
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    graph = build_program_graph(ast)

    # Convert to PyG data
    data = engine.program_graph_to_pyg_data(graph)

    print(f"Node features shape: {data.x.shape}")
    print(f"Edge index shape: {data.edge_index.shape}")
    print(f"Number of nodes: {data.num_nodes}")
    print(f"Number of edges: {data.num_edges}")

    print("\nGNN Engine initialized successfully!")
    print("Note: Training requires labeled dataset of vulnerable/safe programs.")
