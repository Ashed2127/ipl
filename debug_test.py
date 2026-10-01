from lexer import Lexer
from parser import Parser
from program_graph import build_program_graph
from intelligent_security_analyzer import IntelligentSecurityAnalyzer, SecurityDecision
from statistics_collector import StatisticsCollector

# Test vulnerable code
vulnerable_code = """
let malicious = set_untrusted("'; DROP TABLE users; --");
db_write("users", malicious);
"""

print("Testing vulnerable code:")
print(vulnerable_code)

lexer = Lexer(vulnerable_code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

print("\nParsing successful")

graph = build_program_graph(ast)
stats = graph.get_statistics()

print("\nGraph statistics:")
print(f"  Nodes: {stats['num_nodes']}")
print(f"  Edges: {stats['num_edges']}")
print(f"  Node types: {stats['node_types']}")

print("\nNode details:")
for node_id in graph.graph.nodes():
    node_data = graph.graph.nodes[node_id]
    print(f"  Node {node_id}: {node_data.get('node_type')} - {node_data.get('ast_type')}")

stats_collector = StatisticsCollector(":memory:")
analyzer = IntelligentSecurityAnalyzer(
    gnn_engine=None,
    statistics_collector=stats_collector,
    enable_gnn=False,
    enable_static=True,
    confidence_threshold=0.7
)

result = analyzer.analyze_code(ast, vulnerable_code, "vulnerable_hash")

print(f"\nSecurity decision: {result.decision}")
print(f"Threat type: {result.threat_type}")
print(f"Severity: {result.severity}")
print(f"Reasoning: {result.reasoning}")
print(f"Static violations: {result.static_violations}")
