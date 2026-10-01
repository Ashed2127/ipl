"""
Program Graph Representation for IPL
Based on research: "Towards intelligent compiler optimization" (Kovac et al.)
and "Intelligent Compilers" (Cavazos)

This module converts IPL AST into a graph representation suitable for
Graph Neural Network (GNN) analysis. The graph captures:
- Program structure (control flow, data flow)
- Node features (operation types, taint levels, semantic types)
- Edge features (dependency types, control flow edges)
"""

import networkx as nx
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import hashlib
from ast_nodes import (
    ASTNode, Expr, Literal, Identifier, BinaryOp, UnaryOp, ListLiteral, DictLiteral,
    MemberAccess, IndexAccess, FunctionCall, Block, Program as ProgramNode, IfStatement, ForStatement, WhileStatement,
    BreakStatement, ContinueStatement, FunctionDef, ReturnStatement, LetStatement,
    AssignStatement, PrintStatement, SanitizationNode, IntentExpr, TypeAnnotation, ImportStatement,
    SanitizationNode as SanitizationNodeExpr
)


class NodeType(Enum):
    """Types of nodes in the program graph"""
    INSTRUCTION = "instruction"  # Function calls, operations
    VARIABLE = "variable"  # Variable declarations and references
    CONSTANT = "constant"  # Literal values
    OPERATION = "operation"  # Binary/unary operations
    CONTROL_FLOW = "control_flow"  # If, for, while, function definitions
    SINK = "sink"  # Security-sensitive operations (db_write, etc.)
    SOURCE = "source"  # Untrusted data sources
    SANITIZER = "sanitizer"  # Sanitization operations


class EdgeType(Enum):
    """Types of edges in the program graph"""
    DATA_FLOW = "data_flow"  # Data dependencies
    CONTROL_FLOW = "control_flow"  # Control flow dependencies
    DEFINITION_USE = "definition_use"  # Variable definition to use
    CALL = "call"  # Function call edges
    PARAMETER = "parameter"  # Function parameter edges
    TAINT_PROPAGATION = "taint_propagation"  # Taint flow edges


class ProgramGraph:
    """
    Program graph representation for GNN-based analysis.

    Converts IPL AST into a heterogenous graph with rich node and edge features.
    Follows the approach from Kovac et al. for GNN-based compiler optimization.
    """

    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.node_counter = 0
        self.ast_to_graph_map: Dict[int, int] = {}  # AST node id -> graph node id
        self.variable_definitions: Dict[str, int] = {}  # Variable name -> definition node id
        self.taint_levels: Dict[int, str] = {}  # Node id -> taint level
        self.semantic_types: Dict[int, str] = {}  # Node id -> semantic type

    def _create_node_id(self) -> int:
        """Create a unique node ID"""
        node_id = self.node_counter
        self.node_counter += 1
        return node_id

    def _add_node(self, node_type: NodeType, features: Dict[str, Any]) -> int:
        """Add a node to the graph with features"""
        node_id = self._create_node_id()
        self.graph.add_node(node_id, node_type=node_type.value, **features)
        return node_id

    def _add_edge(self, source: int, target: int, edge_type: EdgeType, features: Dict[str, Any] = None):
        """Add an edge to the graph with features"""
        if features is None:
            features = {}
        self.graph.add_edge(source, target, edge_type=edge_type.value, **features)

    def convert_ast_to_graph(self, ast_node: ASTNode) -> nx.MultiDiGraph:
        """
        Convert IPL AST to program graph.

        Args:
            ast_node: Root AST node

        Returns:
            NetworkX MultiDiGraph representing the program
        """
        # Handle Program node specially - process its statements directly
        if isinstance(ast_node, ProgramNode):
            for stmt in ast_node.statements:
                self._process_node(stmt, parent_id=None)
        else:
            self._process_node(ast_node, parent_id=None)
        return self.graph

    def _process_node(self, node: ASTNode, parent_id: Optional[int] = None) -> int:
        """
        Recursively process AST node and add to graph.

        Returns:
            Graph node ID for this AST node
        """
        node_id = self._create_node_id()
        self.ast_to_graph_map[id(node)] = node_id

        # Extract features based on node type
        features = self._extract_node_features(node)

        # Determine node type
        node_type = self._determine_node_type(node)
        features['node_type'] = node_type.value

        # Add node to graph
        self.graph.add_node(node_id, **features)

        # Add edge from parent if exists
        if parent_id is not None:
            self._add_edge(parent_id, node_id, EdgeType.CONTROL_FLOW)

        # Process children based on node type
        child_ids = self._process_children(node, node_id)

        # Add data flow edges based on node type
        self._add_data_flow_edges(node, node_id, child_ids)

        return node_id

    def _extract_node_features(self, node: ASTNode) -> Dict[str, Any]:
        """Extract features from AST node"""
        features = {
            'ast_type': node.__class__.__name__,
            'has_taint': False,
            'taint_level': 'TRUSTED',
            'semantic_type': None,
            'value': None,
            'line': getattr(node, 'line', 0),
        }

        # Extract taint information if available
        if hasattr(node, 'taint_tag') and node.taint_tag:
            features['has_taint'] = True
            features['taint_level'] = node.taint_tag.level.value
            if node.taint_tag.sink_kind:
                features['sink_kind'] = node.taint_tag.sink_kind.value

        # Extract semantic type if available
        if hasattr(node, 'semantic_type') and node.semantic_type:
            features['semantic_type'] = node.semantic_type

        # Extract value for literals
        if isinstance(node, Literal):
            features['value'] = str(node.value)

        # Extract variable name
        if isinstance(node, Identifier):
            features['variable_name'] = node.name

        # Extract function name
        if isinstance(node, FunctionCall):
            # Handle both callee and function_name attributes
            if hasattr(node, 'callee'):
                features['function_name'] = node.callee.name if hasattr(node.callee, 'name') else str(node.callee)
            elif hasattr(node, 'function_name'):
                features['function_name'] = node.function_name

        return features

    def _determine_node_type(self, node: ASTNode) -> NodeType:
        """Determine the graph node type based on AST node"""
        if isinstance(node, Literal):
            return NodeType.CONSTANT
        elif isinstance(node, Identifier):
            return NodeType.VARIABLE
        elif isinstance(node, BinaryOp) or isinstance(node, UnaryOp):
            return NodeType.OPERATION
        elif isinstance(node, FunctionCall):
            # Get function name
            func_name = None
            if hasattr(node, 'callee'):
                func_name = node.callee.name if hasattr(node.callee, 'name') else str(node.callee)
            elif hasattr(node, 'function_name'):
                func_name = node.function_name

            # Check if it's a security sink
            if func_name in ['db_write', 'file_write', 'html_render', 'shell_exec']:
                return NodeType.SINK
            # Check if it's a sanitizer
            elif func_name in ['sanitize_for_sql', 'sanitize_for_html',
                              'sanitize_for_shell', 'sanitize_for_file',
                              'sanitize_string']:
                return NodeType.SANITIZER
            # Check if it's a source
            elif func_name in ['set_untrusted', 'user_input']:
                return NodeType.SOURCE
            else:
                return NodeType.INSTRUCTION
        elif isinstance(node, (IfStatement, ForStatement, WhileStatement, FunctionDef)):
            return NodeType.CONTROL_FLOW
        else:
            return NodeType.INSTRUCTION

    def _process_children(self, node: ASTNode, parent_id: int) -> List[int]:
        """Process children of AST node and return their graph IDs"""
        child_ids = []

        if isinstance(node, BinaryOp):
            left_id = self._process_node(node.left, parent_id)
            right_id = self._process_node(node.right, parent_id)
            child_ids.extend([left_id, right_id])

        elif isinstance(node, UnaryOp):
            operand_id = self._process_node(node.operand, parent_id)
            child_ids.append(operand_id)

        elif isinstance(node, FunctionCall):
            # Handle both args and arguments attributes
            args = node.args if hasattr(node, 'args') else (node.arguments if hasattr(node, 'arguments') else [])
            for arg in args:
                arg_id = self._process_node(arg, parent_id)
                child_ids.append(arg_id)
                self._add_edge(parent_id, arg_id, EdgeType.PARAMETER)

        elif isinstance(node, AssignStatement):
            value_id = self._process_node(node.value, parent_id)
            child_ids.append(value_id)

            # Track variable definition
            if isinstance(node.target, Identifier):
                self.variable_definitions[node.target.name] = parent_id

        elif isinstance(node, LetStatement):
            value_id = self._process_node(node.value_expr, parent_id)
            child_ids.append(value_id)

            # Track variable definition
            self.variable_definitions[node.name] = parent_id

        elif isinstance(node, IfStatement):
            condition_id = self._process_node(node.condition, parent_id)
            child_ids.append(condition_id)

            if node.then_branch:
                then_id = self._process_node(node.then_branch, parent_id)
                child_ids.append(then_id)

            if node.else_branch:
                else_id = self._process_node(node.else_branch, parent_id)
                child_ids.append(else_id)

        elif isinstance(node, ForStatement):
            # Process init, condition, increment, body
            if node.init:
                init_id = self._process_node(node.init, parent_id)
                child_ids.append(init_id)
            if node.condition:
                cond_id = self._process_node(node.condition, parent_id)
                child_ids.append(cond_id)
            if node.increment:
                inc_id = self._process_node(node.increment, parent_id)
                child_ids.append(inc_id)
            if node.body:
                body_id = self._process_node(node.body, parent_id)
                child_ids.append(body_id)

        elif isinstance(node, WhileStatement):
            cond_id = self._process_node(node.condition, parent_id)
            child_ids.append(cond_id)
            if node.body:
                body_id = self._process_node(node.body, parent_id)
                child_ids.append(body_id)

        elif isinstance(node, FunctionDef):
            for param in node.parameters:
                param_id = self._process_node(param, parent_id)
                child_ids.append(param_id)
            if node.body:
                body_id = self._process_node(node.body, parent_id)
                child_ids.append(body_id)

        elif isinstance(node, Block):
            for stmt in node.statements:
                stmt_id = self._process_node(stmt, parent_id)
                child_ids.append(stmt_id)

        elif isinstance(node, ProgramNode):
            for stmt in node.statements:
                stmt_id = self._process_node(stmt, parent_id)
                child_ids.append(stmt_id)

        return child_ids

    def _add_data_flow_edges(self, node: ASTNode, node_id: int, child_ids: List[int]):
        """Add data flow edges based on node semantics"""
        # Variable reference to definition
        if isinstance(node, Identifier):
            if node.name in self.variable_definitions:
                def_id = self.variable_definitions[node.name]
                self._add_edge(def_id, node_id, EdgeType.DEFINITION_USE)

        # Function call edges
        if isinstance(node, FunctionCall):
            for child_id in child_ids:
                self._add_edge(child_id, node_id, EdgeType.DATA_FLOW)

        # Assignment data flow
        if isinstance(node, AssignStatement):
            if len(child_ids) > 0:
                self._add_edge(child_ids[0], node_id, EdgeType.DATA_FLOW)

        # Binary/Unary operation data flow
        if isinstance(node, (BinaryOp, UnaryOp)):
            for child_id in child_ids:
                self._add_edge(child_id, node_id, EdgeType.DATA_FLOW)

    def get_node_features(self, node_id: int) -> Dict[str, Any]:
        """Get features for a specific node"""
        return dict(self.graph.nodes[node_id])

    def get_adjacency_matrix(self) -> Tuple:
        """
        Get adjacency matrix representation for GNN.

        Returns:
            Tuple of (adjacency_matrix, node_features, edge_features)
        """
        adj_matrix = nx.to_scipy_sparse_array(self.graph)
        node_features = []
        edge_features = {}

        for node_id in self.graph.nodes():
            features = self.get_node_features(node_id)
            node_features.append(self._encode_features(features))

        return adj_matrix, node_features, edge_features

    def _encode_features(self, features: Dict[str, Any]) -> List[float]:
        """
        Encode node features into fixed-length vector.

        This is a simple encoding - in production, use proper embedding.
        """
        # Simple hash-based encoding for categorical features
        encoded = []

        # Node type encoding (one-hot)
        node_types = [nt.value for nt in NodeType]
        node_type_vec = [1.0 if features.get('node_type') == nt else 0.0 for nt in node_types]
        encoded.extend(node_type_vec)

        # Taint level encoding
        taint_levels = ['UNTRUSTED', 'SANITIZED', 'TRUSTED']
        taint_vec = [1.0 if features.get('taint_level') == tl else 0.0 for tl in taint_levels]
        encoded.extend(taint_vec)

        # Has taint flag
        encoded.append(1.0 if features.get('has_taint', False) else 0.0)

        # Semantic type encoding (simple hash)
        semantic_type = features.get('semantic_type', 'None')
        encoded.append(float(hash(semantic_type) % 100) / 100.0)

        # Line number (normalized)
        line = features.get('line', 0)
        encoded.append(float(line) / 1000.0)

        return encoded

    def get_subgraph(self, node_id: int, radius: int = 2) -> nx.MultiDiGraph:
        """
        Extract subgraph around a node for local analysis.

        Args:
            node_id: Center node
            radius: Number of hops to include

        Returns:
            Subgraph as NetworkX MultiDiGraph
        """
        # Get nodes within radius
        nodes = {node_id}
        current_frontier = {node_id}

        for _ in range(radius):
            next_frontier = set()
            for n in current_frontier:
                # Add predecessors and successors
                next_frontier.update(self.graph.predecessors(n))
                next_frontier.update(self.graph.successors(n))
            nodes.update(next_frontier)
            current_frontier = next_frontier

        # Extract subgraph
        subgraph = self.graph.subgraph(nodes).copy()
        return subgraph

    def get_data_flow_path(self, source_id: int, sink_id: int) -> List[int]:
        """
        Find data flow path from source to sink.

        Args:
            source_id: Source node ID
            sink_id: Sink node ID

        Returns:
            List of node IDs representing the path
        """
        try:
            # Find shortest path using data flow edges
            path = nx.shortest_path(
                self.graph,
                source=source_id,
                target=sink_id,
                weight=None
            )
            return path
        except nx.NetworkXNoPath:
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics for analysis"""
        return {
            'num_nodes': self.graph.number_of_nodes(),
            'num_edges': self.graph.number_of_edges(),
            'num_variables': len(self.variable_definitions),
            'node_types': self._count_node_types(),
            'edge_types': self._count_edge_types(),
            'avg_degree': sum(dict(self.graph.degree()).values()) / max(1, self.graph.number_of_nodes()),
        }

    def _count_node_types(self) -> Dict[str, int]:
        """Count nodes by type"""
        counts = {}
        for node_id in self.graph.nodes():
            node_type = self.graph.nodes[node_id].get('node_type', 'unknown')
            counts[node_type] = counts.get(node_type, 0) + 1
        return counts

    def _count_edge_types(self) -> Dict[str, int]:
        """Count edges by type"""
        counts = {}
        for u, v, key in self.graph.edges(keys=True):
            edge_type = self.graph.edges[u, v, key].get('edge_type', 'unknown')
            counts[edge_type] = counts.get(edge_type, 0) + 1
        return counts

    def visualize(self, output_path: Optional[str] = None):
        """
        Visualize the program graph.

        Args:
            output_path: Path to save visualization (optional)
        """
        try:
            import matplotlib.pyplot as plt

            pos = nx.spring_layout(self.graph)

            # Color nodes by type
            node_colors = []
            for node_id in self.graph.nodes():
                node_type = self.graph.nodes[node_id].get('node_type', 'instruction')
                if node_type == 'sink':
                    node_colors.append('red')
                elif node_type == 'source':
                    node_colors.append('orange')
                elif node_type == 'sanitizer':
                    node_colors.append('green')
                elif node_type == 'variable':
                    node_colors.append('blue')
                elif node_type == 'constant':
                    node_colors.append('gray')
                else:
                    node_colors.append('lightblue')

            # Draw graph
            plt.figure(figsize=(12, 8))
            nx.draw(self.graph, pos, node_color=node_colors,
                    with_labels=True, node_size=500,
                    font_size=8, font_weight='bold')
            plt.title("IPL Program Graph")

            if output_path:
                plt.savefig(output_path)
            else:
                plt.show()

        except ImportError:
            print("Matplotlib not available for visualization")


def build_program_graph(ast_root: ASTNode) -> ProgramGraph:
    """
    Convenience function to build program graph from AST.

    Args:
        ast_root: Root AST node

    Returns:
        ProgramGraph instance
    """
    graph_builder = ProgramGraph()
    graph_builder.convert_ast_to_graph(ast_root)
    return graph_builder


# Test the program graph construction
if __name__ == "__main__":
    from parser import Parser
    from lexer import Lexer

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

    # Build program graph
    graph = build_program_graph(ast)

    # Print statistics
    print("Program Graph Statistics:")
    print(graph.get_statistics())

    # Print node types
    print("\nNode Types:")
    for node_id in graph.graph.nodes():
        features = graph.get_node_features(node_id)
        print(f"  Node {node_id}: {features.get('node_type')} - {features.get('ast_type')}")
