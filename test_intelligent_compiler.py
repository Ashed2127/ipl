"""
Test Suite for Intelligent Compiler
Based on research: "Towards intelligent compiler optimization" (Kovac et al.)
and "Intelligent Compilers" (Cavazos et al.)

This test suite validates:
- Program graph construction
- GNN-based security analysis
- Dynamic optimization
- ML-based heuristic generation
- Continual learning
- Integration with existing IPL pipeline
"""

import unittest
import time
from typing import List, Dict, Any

from lexer import Lexer
from parser import Parser
from program_graph import ProgramGraph, build_program_graph
from gnn_engine import GNNEngine, GNNModelType, SecurityPattern
from statistics_collector import StatisticsCollector, CompilationStatistic
from dynamic_optimizer import DynamicOptimizer, OptimizationLevel
from ml_heuristic_generator import MLHeuristicGenerator, MLModelType
from intelligent_security_analyzer import IntelligentSecurityAnalyzer, SecurityDecision
from continual_learning import ContinualLearner, ContinualLearningMethod


class TestProgramGraph(unittest.TestCase):
    """Test program graph construction"""

    def test_safe_code_graph(self):
        """Test graph construction for safe code"""
        code = """
        let username = set_untrusted("admin");
        let safe_username = sanitize_for_sql(username);
        db_write("users", safe_username);
        """

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        graph = build_program_graph(ast)
        stats = graph.get_statistics()

        self.assertGreater(stats['num_nodes'], 0)
        self.assertGreater(stats['num_edges'], 0)
        self.assertIn('sanitizer', stats['node_types'])
        self.assertIn('sink', stats['node_types'])

    def test_vulnerable_code_graph(self):
        """Test graph construction for vulnerable code"""
        code = """
        let malicious = set_untrusted("'; DROP TABLE users; --");
        db_write("users", malicious);
        """

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        graph = build_program_graph(ast)
        stats = graph.get_statistics()

        self.assertGreater(stats['num_nodes'], 0)
        self.assertIn('source', stats['node_types'])
        self.assertIn('sink', stats['node_types'])

    def test_data_flow_path(self):
        """Test data flow path detection"""
        code = """
        let input = set_untrusted("test");
        let clean = sanitize_for_sql(input);
        db_write("users", clean);
        """

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        graph = build_program_graph(ast)

        # Find source and sink nodes
        source_id = None
        sink_id = None

        for node_id in graph.graph.nodes():
            node_type = graph.graph.nodes[node_id].get('node_type')
            if node_type == 'source' and source_id is None:
                source_id = node_id
            elif node_type == 'sink' and sink_id is None:
                sink_id = node_id

        if source_id and sink_id:
            path = graph.get_data_flow_path(source_id, sink_id)
            self.assertIsInstance(path, list)


class TestGNNEngine(unittest.TestCase):
    """Test GNN engine functionality"""

    def setUp(self):
        """Set up GNN engine"""
        self.engine = GNNEngine(device='cpu')
        self.engine.initialize_security_classifier(
            input_dim=20,
            hidden_dim=64,
            num_classes=5
        )

    def test_program_graph_conversion(self):
        """Test conversion of program graph to PyG data"""
        code = "let x = 5;"

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        graph = build_program_graph(ast)
        data = self.engine.program_graph_to_pyg_data(graph)

        self.assertIsNotNone(data)
        self.assertGreater(data.num_nodes, 0)

    def test_embedding_generation(self):
        """Test program embedding generation"""
        # Skip this test if PyTorch Geometric is not available
        import gnn_engine
        if not gnn_engine.PYG_AVAILABLE:
            self.skipTest("PyTorch Geometric not available")

        self.engine.initialize_embedding_model(input_dim=20, hidden_dim=64, output_dim=32)

        code = "let x = 5;"

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        graph = build_program_graph(ast)
        embedding = self.engine.get_program_embedding(graph)

        self.assertEqual(len(embedding), 32)


class TestStatisticsCollector(unittest.TestCase):
    """Test statistics collection"""

    def setUp(self):
        """Set up statistics collector"""
        self.collector = StatisticsCollector(":memory:")

    def test_compilation_statistics(self):
        """Test recording compilation statistics"""
        stat = CompilationStatistic(
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            program_hash="test_hash",
            compilation_time_ms=5.2,
            num_nodes=10,
            num_edges=15,
            security_violations=0,
            static_safe_sites=3,
            dynamic_sites=1,
            taint_propagation_steps=5,
            optimization_flags=["optimize"],
            success=True
        )

        self.collector.record_compilation(stat)

        stats = self.collector.get_compilation_statistics()
        self.assertEqual(len(stats), 1)

    def test_aggregated_statistics(self):
        """Test aggregated statistics"""
        stat = CompilationStatistic(
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            program_hash="test_hash",
            compilation_time_ms=5.2,
            num_nodes=10,
            num_edges=15,
            security_violations=0,
            static_safe_sites=3,
            dynamic_sites=1,
            taint_propagation_steps=5,
            optimization_flags=["optimize"],
            success=True
        )

        self.collector.record_compilation(stat)

        agg = self.collector.get_aggregated_statistics()
        self.assertIn('compilation', agg)
        self.assertIn('execution', agg)


class TestDynamicOptimizer(unittest.TestCase):
    """Test dynamic optimization"""

    def setUp(self):
        """Set up dynamic optimizer"""
        self.optimizer = DynamicOptimizer(
            hot_path_threshold=5,
            time_threshold_ms=0.5,
            enable_jit=True
        )

    def test_profiling(self):
        """Test execution profiling"""
        for i in range(10):
            self.optimizer.record_execution(
                node_id=1,
                function_name="test_func",
                execution_time_ms=2.0,
                success=True
            )

        stats = self.optimizer.get_profiling_statistics()
        self.assertEqual(stats['total_executions'], 10)

    def test_hot_path_detection(self):
        """Test hot path detection"""
        for i in range(20):
            self.optimizer.record_execution(
                node_id=1,
                function_name="hot_func",
                execution_time_ms=2.0,
                success=True
            )

        hot_paths = self.optimizer.get_hot_paths(limit=5)
        self.assertGreater(len(hot_paths), 0)


class TestMLHeuristicGenerator(unittest.TestCase):
    """Test ML-based heuristic generation"""

    def setUp(self):
        """Set up ML heuristic generator"""
        self.generator = MLHeuristicGenerator()

    def test_feature_extraction(self):
        """Test feature extraction from program graph"""
        code = "let x = 5;"

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        graph = build_program_graph(ast)
        features = self.generator.extract_features(graph, {})

        self.assertIsInstance(features, dict)
        self.assertIn('num_nodes', features)

    def test_heuristic_learning(self):
        """Test heuristic learning"""
        import numpy as np

        # Generate synthetic training data
        training_data = []
        labels = []

        for i in range(50):
            features = {
                'num_nodes': np.random.randint(5, 50),
                'num_edges': np.random.randint(5, 100),
                'node_count_sink': np.random.randint(0, 5),
                'node_count_source': np.random.randint(0, 5),
            }
            label = 1 if features['node_count_source'] > 0 else 0

            training_data.append(features)
            labels.append(label)

        heuristic = self.generator.learn_security_check_heuristic(
            training_data,
            labels,
            MLModelType.RANDOM_FOREST
        )

        self.assertIsNotNone(heuristic)
        self.assertGreater(heuristic.accuracy, 0)


class TestIntelligentSecurityAnalyzer(unittest.TestCase):
    """Test intelligent security analyzer"""

    def setUp(self):
        """Set up intelligent security analyzer"""
        self.stats_collector = StatisticsCollector(":memory:")
        self.analyzer = IntelligentSecurityAnalyzer(
            gnn_engine=None,  # Disable GNN for testing
            statistics_collector=self.stats_collector,
            enable_gnn=False,
            enable_static=True,
            confidence_threshold=0.7
        )

    def test_safe_code_analysis(self):
        """Test analysis of safe code"""
        code = """
        let username = set_untrusted("admin");
        let safe_username = sanitize_for_sql(username);
        db_write("users", safe_username);
        """

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        result = self.analyzer.analyze_code(ast, code, "safe_hash")

        self.assertEqual(result.decision, SecurityDecision.EXECUTE)

    def test_vulnerable_code_analysis(self):
        """Test analysis of vulnerable code"""
        code = """
        let malicious = set_untrusted("'; DROP TABLE users; --");
        db_write("users", malicious);
        """

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        result = self.analyzer.analyze_code(ast, code, "vulnerable_hash")

        self.assertEqual(result.decision, SecurityDecision.BLOCK)
        self.assertIsNotNone(result.threat_type)


class TestContinualLearning(unittest.TestCase):
    """Test continual learning system"""

    def setUp(self):
        """Set up continual learner"""
        import torch
        import torch.nn as nn

        class SimpleModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.fc1 = nn.Linear(10, 20)
                self.fc2 = nn.Linear(20, 5)

            def forward(self, x):
                x = torch.relu(self.fc1(x))
                x = self.fc2(x)
                return x

        self.model = SimpleModel()
        self.learner = ContinualLearner(
            model=self.model,
            method=ContinualLearningMethod.EXPERIENCE_REPLAY,
            replay_buffer_size=50
        )

    def test_continual_training(self):
        """Test continual training on multiple tasks"""
        import numpy as np

        for task_id in ['task1', 'task2']:
            task_data = [
                (np.random.randn(10), np.random.randint(0, 5))
                for _ in range(20)
            ]

            metrics = self.learner.train_with_continual_learning(
                task_data,
                task_id,
                num_epochs=3,
                learning_rate=0.01
            )

            self.assertIn('final_accuracy', metrics)

    def test_forgetting_measure(self):
        """Test forgetting measure calculation"""
        import numpy as np

        # Train on first task
        task1_data = [
            (np.random.randn(10), np.random.randint(0, 5))
            for _ in range(20)
        ]

        self.learner.train_with_continual_learning(
            task1_data,
            'task1',
            num_epochs=3,
            learning_rate=0.01
        )

        # Train on second task
        task2_data = [
            (np.random.randn(10), np.random.randint(0, 5))
            for _ in range(20)
        ]

        self.learner.train_with_continual_learning(
            task2_data,
            'task2',
            num_epochs=3,
            learning_rate=0.01
        )

        # Check forgetting
        forgetting = self.learner.get_forgetting_measure('task1')
        self.assertIsInstance(forgetting, float)


class TestIntegration(unittest.TestCase):
    """Integration tests for intelligent compiler"""

    def test_full_pipeline(self):
        """Test full intelligent compiler pipeline"""
        # Initialize components
        stats_collector = StatisticsCollector(":memory:")
        analyzer = IntelligentSecurityAnalyzer(
            gnn_engine=None,
            statistics_collector=stats_collector,
            enable_gnn=False,
            enable_static=True
        )

        # Test code
        code = """
        let username = set_untrusted("admin");
        let safe_username = sanitize_for_sql(username);
        db_write("users", safe_username);
        """

        # Parse
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Build graph
        graph = build_program_graph(ast)

        # Analyze
        result = analyzer.analyze_code(ast, code, "test_hash")

        # Verify
        self.assertEqual(result.decision, SecurityDecision.EXECUTE)
        self.assertGreater(result.analysis_time_ms, 0)

    def test_adversarial_attack_detection(self):
        """Test detection of adversarial attacks"""
        stats_collector = StatisticsCollector(":memory:")
        analyzer = IntelligentSecurityAnalyzer(
            gnn_engine=None,
            statistics_collector=stats_collector,
            enable_gnn=False,
            enable_static=True
        )

        # SQL injection
        sql_injection = """
        let malicious = set_untrusted("'; DROP TABLE users; --");
        db_write("users", malicious);
        """

        lexer = Lexer(sql_injection)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        result = analyzer.analyze_code(ast, sql_injection, "sql_injection_hash")

        self.assertEqual(result.decision, SecurityDecision.BLOCK)
        self.assertIsNotNone(result.threat_type)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestProgramGraph))
    suite.addTests(loader.loadTestsFromTestCase(TestGNNEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestStatisticsCollector))
    suite.addTests(loader.loadTestsFromTestCase(TestDynamicOptimizer))
    suite.addTests(loader.loadTestsFromTestCase(TestMLHeuristicGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntelligentSecurityAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestContinualLearning))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    print("=" * 80)
    print("Intelligent Compiler Test Suite")
    print("Based on Kovac et al. and Cavazos et al. research")
    print("=" * 80)
    print()

    result = run_tests()

    print()
    print("=" * 80)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print(f"❌ {len(result.failures)} failures, {len(result.errors)} errors")
    print("=" * 80)
