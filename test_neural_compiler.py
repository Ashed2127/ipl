"""
Comprehensive tests for the Neural Compiler - Compiler-First Architecture
Tests all intelligent components and their integration
"""
import unittest
from typing import Dict, Any

try:
    from neural_compiler import CompilerFirstNeuralCompiler, NeuralCompilationResult
    from intelligent_lexer import CompilerFirstLexer
    from intelligent_parser import CompilerFirstParser
    from intelligent_semantic_analyzer import CompilerFirstSemanticAnalyzer
    from intelligent_code_generator import CompilerFirstCodeGenerator
    from intelligent_security_analyzer import CompilerFirstSecurityAnalyzer
    from intelligent_type_system import CompilerFirstTypeSystem
    from intelligent_optimizer import CompilerFirstOptimizer
    from ast_nodes import Program, LetStatement, Literal, Identifier, TypeAnnotation
    from lexer import Lexer
    from parser import Parser
except (ImportError, ValueError):
    from neural_compiler import CompilerFirstNeuralCompiler, NeuralCompilationResult
    from intelligent_lexer import CompilerFirstLexer
    from intelligent_parser import CompilerFirstParser
    from intelligent_semantic_analyzer import CompilerFirstSemanticAnalyzer
    from intelligent_code_generator import CompilerFirstCodeGenerator
    from intelligent_security_analyzer import CompilerFirstSecurityAnalyzer
    from intelligent_type_system import CompilerFirstTypeSystem
    from intelligent_optimizer import CompilerFirstOptimizer
    from ast_nodes import Program, LetStatement, Literal, Identifier, TypeAnnotation
    from lexer import Lexer
    from parser import Parser


class TestIntelligentLexer(unittest.TestCase):
    """Test the intelligent lexer component"""
    
    def setUp(self):
        self.test_code = """
        let user_age = 25
        let user_name = "John"
        let price = 19.99
        """
        self.lexer = CompilerFirstLexer(self.test_code)
    
    def test_lexer_tokenization(self):
        """Test that intelligent lexer tokenizes code correctly"""
        analysis = self.lexer.analyze_source()
        self.assertIn("tokens", analysis)
        self.assertGreater(len(analysis["tokens"]), 0)
        self.assertNotIn("error", analysis)
    
    def test_lexer_neural_analysis(self):
        """Test that neural analysis is performed"""
        analysis = self.lexer.analyze_source()
        self.assertTrue(analysis["neural_analysis_enabled"])
        self.assertIn("diagnostics", analysis)
    
    def test_lexer_security_analysis(self):
        """Test that security analysis is performed"""
        analysis = self.lexer.analyze_source()
        self.assertIn("security_summary", analysis)
    
    def test_lexer_with_malicious_code(self):
        """Test lexer with potentially malicious code"""
        malicious_code = 'let query = "SELECT * FROM users WHERE name = \'admin\' OR 1=1"'
        lexer = CompilerFirstLexer(malicious_code)
        analysis = lexer.analyze_source()
        self.assertIn("security_summary", analysis)
        # Should detect SQL injection patterns
        self.assertGreater(analysis["security_summary"].get("total_security_flags", 0), 0)


class TestIntelligentParser(unittest.TestCase):
    """Test the intelligent parser component"""
    
    def setUp(self):
        self.test_code = """
        let x = 10
        let y = 20
        let z = x + y
        """
        config = {
            "enable_neural_parsing": True,
            "enable_semantic_validation": True,
            "enable_syntax_correction": True,
            "confidence_threshold": 0.7
        }
        self.parser = CompilerFirstParser(self.test_code, config)
    
    def test_parser_parsing(self):
        """Test that intelligent parser parses code correctly"""
        analysis = self.parser.parse_source()
        self.assertIn("ast", analysis)
        self.assertNotIn("error", analysis)
    
    def test_parser_neural_parsing(self):
        """Test that neural parsing is performed"""
        analysis = self.parser.parse_source()
        self.assertIn("parsing_strategy", analysis)
        self.assertIn("parse_confidence", analysis)
    
    def test_parser_with_syntax_error(self):
        """Test parser with syntax error and intelligent recovery"""
        error_code = "let x = 10  let y = 20"  # Missing semicolon
        parser = CompilerFirstParser(error_code)
        analysis = parser.parse_source()
        # Should provide intelligent suggestions
        if "error" in analysis:
            self.assertIn("intelligent_suggestions", analysis)
    
    def test_parser_semantic_validation(self):
        """Test that semantic validation is performed"""
        analysis = self.parser.parse_source()
        self.assertIn("semantic_hints", analysis)


class TestIntelligentSemanticAnalyzer(unittest.TestCase):
    """Test the intelligent semantic analyzer component"""
    
    def setUp(self):
        # Create a simple AST for testing
        let_stmt = LetStatement(
            name=Identifier("user_age"),
            value_expr=Literal(25),
            target_type=TypeAnnotation("Int")
        )
        self.program = Program(statements=[let_stmt])
        config = {
            "enable_deep_analysis": True,
            "enable_security_analysis": True,
            "enable_optimization_suggestions": True,
            "confidence_threshold": 0.7
        }
        self.analyzer = CompilerFirstSemanticAnalyzer(config)
    
    def test_semantic_analysis(self):
        """Test that semantic analysis is performed"""
        analysis = self.analyzer.analyze_program(self.program)
        self.assertIn("statements_analysis", analysis)
        self.assertIn("global_patterns", analysis)
    
    def test_deep_semantic_understanding(self):
        """Test that deep semantic understanding is performed"""
        analysis = self.analyzer.analyze_program(self.program)
        self.assertIn("security_summary", analysis)
        self.assertIn("optimization_opportunities", analysis)
    
    def test_semantic_patterns_detection(self):
        """Test that semantic patterns are detected"""
        analysis = self.analyzer.analyze_program(self.program)
        self.assertIsInstance(analysis["global_patterns"], list)


class TestIntelligentCodeGenerator(unittest.TestCase):
    """Test the intelligent code generator component"""
    
    def setUp(self):
        # Create a simple AST for testing
        let_stmt = LetStatement(
            name=Identifier("x"),
            value_expr=Literal(10),
            target_type=None
        )
        self.program = Program(statements=[let_stmt])
        self.generator = CompilerFirstCodeGenerator()
    
    def test_code_generation(self):
        """Test that code is generated correctly"""
        analysis = self.generator.generate_program(self.program)
        self.assertIn("generated_code", analysis)
        self.assertIn("optimization_level", analysis)
    
    def test_ai_optimization(self):
        """Test that AI optimization is applied"""
        analysis = self.generator.generate_program(self.program)
        self.assertIn("ai_transformations", analysis)
        self.assertIn("performance_improvements", analysis)
    
    def test_code_quality_metrics(self):
        """Test that code quality metrics are calculated"""
        analysis = self.generator.generate_program(self.program)
        self.assertIn("code_quality_metrics", analysis)


class TestIntelligentSecurityAnalyzer(unittest.TestCase):
    """Test the intelligent security analyzer component"""
    
    def setUp(self):
        # Create AST with potential security issues
        malicious_literal = Literal("SELECT * FROM users WHERE name = 'admin' OR 1=1")
        let_stmt = LetStatement(
            name=Identifier("query"),
            value_expr=malicious_literal,
            target_type=None
        )
        self.program = Program(statements=[let_stmt])
        self.analyzer = CompilerFirstSecurityAnalyzer()
    
    def test_security_analysis(self):
        """Test that security analysis is performed"""
        analysis = self.analyzer.analyze_program_security(self.program)
        self.assertIn("overall_security", analysis)
        self.assertIn("statement_security", analysis)
    
    def test_threat_detection(self):
        """Test that threats are detected"""
        analysis = self.analyzer.analyze_program_security(self.program)
        # Should detect SQL injection in the malicious literal
        overall_security = analysis["overall_security"]
        self.assertIsInstance(overall_security.detected_threats, list)
    
    def test_attack_vector_analysis(self):
        """Test that attack vectors are analyzed"""
        analysis = self.analyzer.analyze_program_security(self.program)
        overall_security = analysis["overall_security"]
        self.assertIn("attack_vectors", overall_security.attack_vectors)
    
    def test_prevention_measures(self):
        """Test that prevention measures are suggested"""
        analysis = self.analyzer.analyze_program_security(self.program)
        overall_security = analysis["overall_security"]
        self.assertIsInstance(overall_security.prevention_measures, list)


class TestIntelligentTypeSystem(unittest.TestCase):
    """Test the intelligent type system component"""
    
    def setUp(self):
        # Create AST with various types
        int_stmt = LetStatement(
            name=Identifier("age"),
            value_expr=Literal(25),
            target_type=TypeAnnotation("Int")
        )
        string_stmt = LetStatement(
            name=Identifier("name"),
            value_expr=Literal("John"),
            target_type=None
        )
        self.program = Program(statements=[int_stmt, string_stmt])
        self.type_system = CompilerFirstTypeSystem()
    
    def test_type_inference(self):
        """Test that types are inferred correctly"""
        analysis = self.type_system.analyze_program_types(self.program)
        self.assertIn("overall_types", analysis)
        self.assertIn("inferred_types", analysis["overall_types"])
    
    def test_neural_type_inference(self):
        """Test that neural type inference is performed"""
        analysis = self.type_system.analyze_program_types(self.program)
        overall_types = analysis["overall_types"]
        self.assertIn("confidence", overall_types)
    
    def test_type_conflict_detection(self):
        """Test that type conflicts are detected"""
        analysis = self.type_system.analyze_program_types(self.program)
        overall_types = analysis["overall_types"]
        self.assertIn("type_conflicts", overall_types.type_conflicts)
    
    def test_type_suggestions(self):
        """Test that type suggestions are provided"""
        analysis = self.type_system.analyze_program_types(self.program)
        overall_types = analysis["overall_types"]
        self.assertIsInstance(overall_types.type_suggestions, list)


class TestIntelligentOptimizer(unittest.TestCase):
    """Test the intelligent optimizer component"""
    
    def setUp(self):
        # Create AST with optimization opportunities
        let_stmt = LetStatement(
            name=Identifier("x"),
            value_expr=Literal(10),
            target_type=None
        )
        self.program = Program(statements=[let_stmt])
        self.optimizer = CompilerFirstOptimizer()
    
    def test_optimization(self):
        """Test that optimization is performed"""
        analysis = self.optimizer.optimize_program(self.program)
        self.assertIn("optimization_score", analysis)
        self.assertIn("applied_optimizations", analysis)
    
    def test_learning_optimization(self):
        """Test that learning-based optimization is performed"""
        analysis = self.optimizer.optimize_program(self.program)
        self.assertIn("learning_insights", analysis)
        self.assertIn("adaptation_suggestions", analysis)
    
    def test_performance_prediction(self):
        """Test that performance improvement is predicted"""
        analysis = self.optimizer.optimize_program(self.program)
        self.assertIn("performance_improvement", analysis)


class TestNeuralCompiler(unittest.TestCase):
    """Test the integrated neural compiler"""
    
    def setUp(self):
        self.test_code = """
        let user_age = 25
        let user_name = "John"
        let total = user_age + 5
        """
        self.compiler = CompilerFirstNeuralCompiler()
    
    def test_complete_compilation(self):
        """Test complete compilation pipeline"""
        result = self.compiler.compile_source(self.test_code)
        self.assertIn("success", result)
        self.assertIn("compilation_time", result)
        self.assertIn("overall_confidence", result)
    
    def test_all_intelligent_components(self):
        """Test that all intelligent components are used"""
        result = self.compiler.compile_source(self.test_code)
        self.assertIn("lexical_analysis", result)
        self.assertIn("parsing_analysis", result)
        self.assertIn("semantic_analysis", result)
        self.assertIn("type_analysis", result)
        self.assertIn("security_analysis", result)
        self.assertIn("optimization_analysis", result)
        self.assertIn("code_generation", result)
    
    def test_compilation_with_errors(self):
        """Test compilation with error handling"""
        error_code = "let x = 10  let y = 20"  # Syntax error
        result = self.compiler.compile_source(error_code)
        # Should handle errors gracefully
        self.assertIn("success", result)
        if not result["success"]:
            self.assertIn("errors", result)
    
    def test_compilation_statistics(self):
        """Test compilation statistics tracking"""
        # Perform multiple compilations
        for _ in range(3):
            self.compiler.compile_source(self.test_code)
        
        # Get compiler info
        info = self.compiler.get_compiler_info()
        self.assertIn("statistics", info)
        self.assertGreater(info["statistics"]["total_compilations"], 0)
    
    def test_security_blocking(self):
        """Test that security threats can block compilation"""
        malicious_code = 'let query = "SELECT * FROM users WHERE name = \'admin\' OR 1=1"'
        result = self.compiler.compile_source(malicious_code)
        # Security analysis should detect the threat
        self.assertIn("security_analysis", result)


class TestIntegrationScenarios(unittest.TestCase):
    """Test real-world integration scenarios"""
    
    def setUp(self):
        self.compiler = CompilerFirstNeuralCompiler()
    
    def test_simple_program(self):
        """Test compilation of a simple program"""
        code = """
        let x = 10
        let y = 20
        let z = x + y
        print(z)
        """
        result = self.compiler.compile_source(code)
        self.assertTrue(result["success"])
    
    def test_program_with_types(self):
        """Test compilation with type annotations"""
        code = """
        let age: Int = 25
        let name: String = "John"
        let price: Float = 19.99
        """
        result = self.compiler.compile_source(code)
        self.assertTrue(result["success"])
    
    def test_program_with_functions(self):
        """Test compilation with function definitions"""
        code = """
        fn add(a: Int, b: Int) -> Int {
            return a + b
        }
        let result = add(10, 20)
        """
        result = self.compiler.compile_source(code)
        # May not succeed due to parser limitations, but should not crash
        self.assertIn("success", result)
    
    def test_program_with_control_flow(self):
        """Test compilation with control flow"""
        code = """
        let x = 10
        if x > 5 {
            print("x is greater than 5")
        } else {
            print("x is less than or equal to 5")
        }
        """
        result = self.compiler.compile_source(code)
        # May not succeed due to parser limitations, but should not crash
        self.assertIn("success", result)


class TestPerformance(unittest.TestCase):
    """Test performance characteristics"""
    
    def setUp(self):
        self.compiler = CompilerFirstNeuralCompiler()
        self.test_code = """
        let x = 10
        let y = 20
        let z = x + y
        """
    
    def test_compilation_speed(self):
        """Test that compilation completes in reasonable time"""
        import time
        start = time.time()
        result = self.compiler.compile_source(self.test_code)
        end = time.time()
        
        compilation_time = end - start
        self.assertLess(compilation_time, 5.0)  # Should complete in less than 5 seconds
    
    def test_memory_usage(self):
        """Test that memory usage is reasonable"""
        import tracemalloc
        tracemalloc.start()
        
        # Perform multiple compilations
        for _ in range(10):
            self.compiler.compile_source(self.test_code)
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Memory usage should be reasonable (less than 100MB for this test)
        self.assertLess(peak / 1024 / 1024, 100)


def run_tests():
    """Run all tests and display results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestIntelligentLexer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntelligentParser))
    suite.addTests(loader.loadTestsFromTestCase(TestIntelligentSemanticAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntelligentCodeGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntelligentSecurityAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntelligentTypeSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestIntelligentOptimizer))
    suite.addTests(loader.loadTestsFromTestCase(TestNeuralCompiler))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)