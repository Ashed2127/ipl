"""
IPL Brute Force Fast Test - Core Neural Components Only
Tests 6/7 neural components (excludes slow LLM)
No rate limiters - Maximum performance test
"""
import time
import threading
import multiprocessing
from typing import List, Dict, Any
import psutil
from real_neural_lexer_v2 import RealNeuralLexerV2
from real_neural_parser_truly_neural import RealNeuralParserTrulyNeural
from real_neural_semantic_analyzer import RealNeuralSemanticAnalyzer
from real_neural_type_system import RealNeuralTypeSystem
from real_neural_security_analyzer import RealNeuralSecurityAnalyzer
from real_neural_optimizer import RealNeuralOptimizer

class IPLFastController:
    """Fast IPL controller testing core neural components"""
    
    def __init__(self):
        print("🔥 IPL Fast Controller - Core Neural Components Only")
        print("Loading neural components...")
        self.lexer = RealNeuralLexerV2()
        self.parser = RealNeuralParserTrulyNeural()
        self.semantic_analyzer = RealNeuralSemanticAnalyzer()
        self.type_system = RealNeuralTypeSystem()
        self.security_analyzer = RealNeuralSecurityAnalyzer()
        self.optimizer = RealNeuralOptimizer()
        print("✅ All 6 core neural components loaded")
        
        self.results = []
        self.errors = []
        self.start_time = time.time()
        
    def generate_test_code(self, complexity: str = "medium") -> str:
        """Generate test code of varying complexity"""
        if complexity == "simple":
            return "let x = 25; let y = 30; let result = x + y;"
        elif complexity == "medium":
            return """let user_age = 25; let user_name = "John"; let price = 19.99; let total = user_age * price; let is_valid = true; let clean_input = sanitize(user_name);"""
        elif complexity == "complex":
            return """let user_data = parse_input(raw_data); let user_age = extract_age(user_data); let user_name = extract_name(user_data); let user_balance = extract_balance(user_data); let price = calculate_price(user_data); let tax = calculate_tax(price); let total = price + tax; let is_valid = validate_user(user_data); let clean_input = sanitize(user_name); let encrypted = encrypt(clean_input); for i in 0..100 { let result = calculate_complex(i * 2, user_balance); }"""
        else:  # extreme
            return """let system_state = initialize_system(); let user_context = build_context(raw_input); let neural_embeddings = generate_embeddings(user_context); let security_analysis = analyze_security(user_context); let type_inference = infer_types(neural_embeddings); let optimization_strategy = select_optimization(security_analysis); for i in 0..1000 { let neural_step = process_neural_step(i, neural_embeddings); let optimization_step = apply_optimization(neural_step, optimization_strategy); let security_step = validate_security(optimization_step, security_analysis); let type_step = validate_types(security_step, type_inference); } while system_state.active { let monitoring = monitor_system(system_state); let adjustment = adjust_parameters(monitoring); let recompilation = recompile_optimized(adjustment); }"""

    def run_fast_compilation(self, test_id: int, complexity: str = "medium") -> Dict[str, Any]:
        """Run fast compilation without LLM"""
        try:
            code = self.generate_test_code(complexity)
            start_time = time.time()
            
            # Step 1: Neural Lexical Analysis
            lexer_result = self.lexer.tokenize_with_neural(code)
            lexer_time = time.time() - start_time
            
            # Step 2: Neural Parsing
            parser_start = time.time()
            parser_result = self.parser.parse_with_neural_recovery(code)
            parser_time = time.time() - parser_start
            
            # Step 3: Neural Semantic Analysis
            semantic_start = time.time()
            semantic_result = self.semantic_analyzer.analyze_semantics_with_neural(code, parser_result['ast'])
            semantic_time = time.time() - semantic_start
            
            # Step 4: Neural Type System
            type_start = time.time()
            type_result = self.type_system.analyze_types_with_neural(code, parser_result['ast'])
            type_time = time.time() - type_start
            
            # Step 5: Neural Security Analysis
            security_start = time.time()
            security_result = self.security_analyzer.analyze_security_with_neural(code, parser_result['ast'])
            security_time = time.time() - security_start
            
            # Step 6: Neural Optimization
            optimizer_start = time.time()
            optimizer_result = self.optimizer.optimize_with_neural(code, parser_result['ast'])
            optimizer_time = time.time() - optimizer_start
            
            total_time = time.time() - start_time
            
            return {
                'test_id': test_id,
                'complexity': complexity,
                'success': True,
                'total_time_ms': total_time * 1000,
                'lexer_time_ms': lexer_time * 1000,
                'parser_time_ms': parser_time * 1000,
                'semantic_time_ms': semantic_time * 1000,
                'type_time_ms': type_time * 1000,
                'security_time_ms': security_time * 1000,
                'optimizer_time_ms': optimizer_time * 1000,
                'lexer_confidence': lexer_result['average_confidence'],
                'parser_neural': parser_result['syntax_analysis']['uses_neural_networks'],
                'semantic_method': semantic_result['method'],
                'type_method': type_result['method'],
                'security_score': security_result['security_score'],
                'optimizer_confidence': optimizer_result['optimization_confidence']
            }
        except Exception as e:
            return {
                'test_id': test_id,
                'complexity': complexity,
                'success': False,
                'error': str(e),
                'total_time_ms': 0
            }

    def run_stress_test(self, num_tests: int):
        """Run stress test with specified number of tests"""
        print(f"🔥 Starting stress test: {num_tests} compilations")
        print(f"🚀 NO RATE LIMITS - Maximum IPL Performance")
        
        for i in range(num_tests):
            complexity = ['simple', 'medium', 'complex', 'extreme'][i % 4]
            result = self.run_fast_compilation(i, complexity)
            self.results.append(result)
            
            if not result.get('success'):
                self.errors.append(result)
            
            # Progress update
            if (i + 1) % 10 == 0:
                elapsed = time.time() - self.start_time
                rate = (i + 1) / elapsed
                print(f"Progress: {i + 1}/{num_tests} | {rate:.2f} tests/sec | {elapsed:.1f}s elapsed")
        
        print(f"✅ Stress test completed: {num_tests} compilations")

    def run_parallel_stress_test(self, num_threads: int, tests_per_thread: int):
        """Run parallel stress test"""
        print(f"🚀 Starting parallel test: {num_threads} threads, {tests_per_thread} tests each")
        print(f"🔥 NO RATE LIMITS - Maximum Parallel Performance")
        
        threads = []
        
        def worker(thread_id):
            for i in range(tests_per_thread):
                test_id = thread_id * tests_per_thread + i
                complexity = ['simple', 'medium', 'complex', 'extreme'][i % 4]
                result = self.run_fast_compilation(test_id, complexity)
                self.results.append(result)
                
                if not result.get('success'):
                    self.errors.append(result)
        
        for thread_id in range(num_threads):
            thread = threading.Thread(target=worker, args=(thread_id,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        print(f"✅ Parallel test completed: {num_threads * tests_per_thread} total compilations")

    def analyze_ipl_level(self) -> Dict[str, Any]:
        """Analyze IPL level based on test results"""
        if not self.results:
            return {'error': 'No results to analyze'}
        
        successful = [r for r in self.results if r.get('success', False)]
        failed = [r for r in self.results if not r.get('success', False)]
        
        avg_time = sum(r['total_time_ms'] for r in successful) / len(successful) if successful else 0
        avg_lexer_confidence = sum(r.get('lexer_confidence', 0) for r in successful) / len(successful) if successful else 0
        avg_security_score = sum(r.get('security_score', 0) for r in successful) / len(successful) if successful else 0
        avg_optimizer_confidence = sum(r.get('optimizer_confidence', 0) for r in successful) / len(successful) if successful else 0
        
        # Count neural features
        neural_parser_count = sum(1 for r in successful if r.get('parser_neural', False))
        
        # Calculate component performance
        avg_lexer_time = sum(r.get('lexer_time_ms', 0) for r in successful) / len(successful) if successful else 0
        avg_parser_time = sum(r.get('parser_time_ms', 0) for r in successful) / len(successful) if successful else 0
        avg_semantic_time = sum(r.get('semantic_time_ms', 0) for r in successful) / len(successful) if successful else 0
        avg_type_time = sum(r.get('type_time_ms', 0) for r in successful) / len(successful) if successful else 0
        avg_security_time = sum(r.get('security_time_ms', 0) for r in successful) / len(successful) if successful else 0
        avg_optimizer_time = sum(r.get('optimizer_time_ms', 0) for r in successful) / len(successful) if successful else 0
        
        # Calculate IPL level
        success_rate = len(successful) / len(self.results) * 100 if self.results else 0
        neural_parser_rate = neural_parser_count / len(successful) * 100 if successful else 0
        
        # IPL Score calculation (weighted)
        ipl_score = (
            success_rate * 0.25 +
            neural_parser_rate * 0.25 +
            avg_lexer_confidence * 100 * 0.15 +
            avg_security_score * 100 * 0.15 +
            avg_optimizer_confidence * 100 * 0.20
        )
        
        if ipl_score >= 90:
            ipl_level = "GOD_TIER"
        elif ipl_score >= 80:
            ipl_level = "EXPERT"
        elif ipl_score >= 70:
            ipl_level = "ADVANCED"
        elif ipl_score >= 60:
            ipl_level = "INTERMEDIATE"
        elif ipl_score >= 50:
            ipl_level = "BASIC"
        else:
            ipl_level = "NOVICE"
        
        return {
            'total_tests': len(self.results),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': success_rate,
            'avg_total_time_ms': avg_time,
            'tests_per_second': len(self.results) / (time.time() - self.start_time) if time.time() > self.start_time else 0,
            'avg_lexer_confidence': avg_lexer_confidence,
            'neural_parser_rate': neural_parser_rate,
            'avg_security_score': avg_security_score,
            'avg_optimizer_confidence': avg_optimizer_confidence,
            'component_times': {
                'lexer_ms': avg_lexer_time,
                'parser_ms': avg_parser_time,
                'semantic_ms': avg_semantic_time,
                'type_ms': avg_type_time,
                'security_ms': avg_security_time,
                'optimizer_ms': avg_optimizer_time
            },
            'ipl_score': ipl_score,
            'ipl_level': ipl_level,
            'errors': len(self.errors),
            'test_duration_seconds': time.time() - self.start_time
        }

def main():
    print("=" * 80)
    print("🔥 IPL BRUTE FORCE FAST TEST 🔥")
    print("CORE NEURAL COMPONENTS ONLY - NO RATE LIMITS")
    print("=" * 80)
    
    # System info
    print(f"\n💻 System Resources:")
    resources = psutil.virtual_memory()
    print(f"   Total Memory: {resources.total / (1024**3):.2f} GB")
    print(f"   Available Memory: {resources.available / (1024**3):.2f} GB")
    print(f"   CPU Cores: {multiprocessing.cpu_count()}")
    
    # Initialize controller
    controller = IPLFastController()
    
    # Run stress test
    print(f"\n🚀 Running Stress Test: 100 compilations")
    controller.run_stress_test(100)
    
    # Analyze results
    print("\n" + "=" * 80)
    print("📊 IPL LEVEL ANALYSIS")
    print("=" * 80)
    
    analysis = controller.analyze_ipl_level()
    
    print(f"\n🎯 IPL Level: {analysis['ipl_level']}")
    print(f"📈 IPL Score: {analysis['ipl_score']:.2f}/100")
    print(f"\n📊 Test Results:")
    print(f"   Total Tests: {analysis['total_tests']}")
    print(f"   Successful: {analysis['successful']}")
    print(f"   Failed: {analysis['failed']}")
    print(f"   Success Rate: {analysis['success_rate']:.2f}%")
    print(f"   Avg Total Time: {analysis['avg_total_time_ms']:.2f}ms")
    print(f"   Tests/Second: {analysis['tests_per_second']:.2f}")
    
    print(f"\n🧠 Neural Capabilities:")
    print(f"   Avg Lexer Confidence: {analysis['avg_lexer_confidence']:.2%}")
    print(f"   Neural Parser Rate: {analysis['neural_parser_rate']:.2f}%")
    
    print(f"\n🔒 Security & Optimization:")
    print(f"   Avg Security Score: {analysis['avg_security_score']:.2%}")
    print(f"   Avg Optimization Confidence: {analysis['avg_optimizer_confidence']:.2%}")
    
    print(f"\n⚡ Component Performance (avg times):")
    times = analysis['component_times']
    print(f"   Lexer: {times['lexer_ms']:.2f}ms")
    print(f"   Parser: {times['parser_ms']:.2f}ms")
    print(f"   Semantic: {times['semantic_ms']:.2f}ms")
    print(f"   Type System: {times['type_ms']:.2f}ms")
    print(f"   Security: {times['security_ms']:.2f}ms")
    print(f"   Optimizer: {times['optimizer_ms']:.2f}ms")
    
    print(f"\n💻 System Resources After Test:")
    final_resources = {
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'memory_available_gb': psutil.virtual_memory().available / (1024**3)
    }
    print(f"   CPU Usage: {final_resources['cpu_percent']:.1f}%")
    print(f"   Memory Usage: {final_resources['memory_percent']:.1f}%")
    print(f"   Memory Available: {final_resources['memory_available_gb']:.2f} GB")
    
    print(f"\n⏱️  Test Duration: {analysis['test_duration_seconds']:.2f} seconds")
    print(f"❌ Errors: {analysis['errors']}")
    
    print("\n" + "=" * 80)
    print(f"🎉 IPL LEVEL: {analysis['ipl_level']} (Score: {analysis['ipl_score']:.2f}/100)")
    print("=" * 80)
    
    # Final verdict
    if analysis['ipl_level'] == "GOD_TIER":
        print("🏆 IPL has achieved GOD TIER status!")
    elif analysis['ipl_level'] == "EXPERT":
        print("🥈 IPL has achieved EXPERT level!")
    elif analysis['ipl_level'] == "ADVANCED":
        print("🥉 IPL has achieved ADVANCED level!")
    else:
        print(f"📈 IPL is at {analysis['ipl_level']} level - room for improvement")

if __name__ == "__main__":
    main()