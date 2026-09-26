"""
Security Model Comparison Test
Compares Enhanced Security Analyzer (GraphCodeBERT + BERT + CodeBERT) vs Previous DistilBERT
"""
import time
from enhanced_neural_security_analyzer import EnhancedNeuralSecurityAnalyzer
from real_neural_security_analyzer import RealNeuralSecurityAnalyzer
from real_neural_parser_truly_neural import RealNeuralParserTrulyNeural

class SecurityModelComparison:
    """Compare security detection capabilities"""
    
    def __init__(self):
        print("🔒 Security Model Comparison Test")
        print("Comparing Enhanced Security Models vs Previous DistilBERT")
        
        print("\n📊 Loading Previous Model (DistilBERT)...")
        self.old_analyzer = RealNeuralSecurityAnalyzer()
        
        print("\n🚀 Loading Enhanced Security Models...")
        self.new_analyzer = EnhancedNeuralSecurityAnalyzer()
        
        self.parser = RealNeuralParserTrulyNeural()
    
    def get_test_cases(self) -> List[Dict[str, str]]:
        """Get comprehensive security test cases"""
        return [
            # SQL Injection cases
            {
                'name': 'SQL Injection - OR 1=1',
                'code': 'let query = "SELECT * FROM users WHERE id = 1 OR 1=1";',
                'expected': 'malicious'
            },
            {
                'name': 'SQL Injection - UNION',
                'code': 'let query = "SELECT * FROM users WHERE id = 1 UNION SELECT password FROM admin";',
                'expected': 'malicious'
            },
            {
                'name': 'SQL Injection - DROP TABLE',
                'code': 'let query = "SELECT * FROM users WHERE id = 1; DROP TABLE users--";',
                'expected': 'malicious'
            },
            # XSS cases
            {
                'name': 'XSS - Script tag',
                'code': 'let input = "<script>alert(\'XSS\')</script>";',
                'expected': 'malicious'
            },
            {
                'name': 'XSS - Javascript protocol',
                'code': 'let url = "javascript:alert(document.cookie)";',
                'expected': 'malicious'
            },
            # Command Injection
            {
                'name': 'Command Injection - Shell command',
                'code': 'let command = "cat /etc/passwd; rm -rf /";',
                'expected': 'malicious'
            },
            {
                'name': 'Command Injection - Backticks',
                'code': 'let result = `whoami`;',
                'expected': 'malicious'
            },
            # Normal cases
            {
                'name': 'Normal - Parameterized query',
                'code': 'let query = "SELECT * FROM users WHERE id = ?";',
                'expected': 'safe'
            },
            {
                'name': 'Normal - Simple variable',
                'code': 'let user_name = "John";',
                'expected': 'safe'
            },
            {
                'name': 'Normal - Safe function call',
                'code': 'let clean = sanitize(user_input);',
                'expected': 'safe'
            }
        ]
    
    def test_analyzer(self, analyzer, test_case: Dict) -> Dict[str, Any]:
        """Test a single analyzer with a test case"""
        try:
            code = test_case['code']
            parser_result = self.parser.parse_with_neural_recovery(code)
            
            start_time = time.time()
            result = analyzer.analyze_security_with_neural(code, parser_result['ast'])
            analysis_time = (time.time() - start_time) * 1000
            
            is_malicious = result['security_score'] < 0.5
            is_correct = (is_malicious and test_case['expected'] == 'malicious') or \
                       (not is_malicious and test_case['expected'] == 'safe')
            
            return {
                'test_name': test_case['name'],
                'expected': test_case['expected'],
                'security_score': result['security_score'],
                'security_level': result['security_level'],
                'detected_as_malicious': is_malicious,
                'is_correct': is_correct,
                'analysis_time_ms': analysis_time,
                'models_used': result.get('models_used', ['unknown']),
                'vulnerabilities': len(result.get('vulnerabilities', []))
            }
        except Exception as e:
            return {
                'test_name': test_case['name'],
                'error': str(e),
                'is_correct': False
            }
    
    def run_comparison(self) -> Dict[str, Any]:
        """Run full comparison test"""
        test_cases = self.get_test_cases()
        
        print(f"\n🧪 Running {len(test_cases)} security test cases...")
        
        old_results = []
        new_results = []
        
        for test_case in test_cases:
            print(f"\n   Testing: {test_case['name']}")
            
            # Test old analyzer
            old_result = self.test_analyzer(self.old_analyzer, test_case)
            old_results.append(old_result)
            old_status = "✅" if old_result.get('is_correct') else "❌"
            print(f"   Old (DistilBERT): {old_status} Score: {old_result.get('security_score', 0):.2%}")
            
            # Test new analyzer
            new_result = self.test_analyzer(self.new_analyzer, test_case)
            new_results.append(new_result)
            new_status = "✅" if new_result.get('is_correct') else "❌"
            print(f"   New (Enhanced): {new_status} Score: {new_result.get('security_score', 0):.2%}")
        
        return {
            'old_results': old_results,
            'new_results': new_results
        }
    
    def analyze_comparison(self, comparison_results: Dict) -> Dict[str, Any]:
        """Analyze comparison results"""
        old_results = comparison_results['old_results']
        new_results = comparison_results['new_results']
        
        # Calculate metrics for old analyzer
        old_correct = sum(1 for r in old_results if r.get('is_correct', False))
        old_total = len(old_results)
        old_accuracy = old_correct / old_total if old_total > 0 else 0
        
        # Calculate metrics for new analyzer
        new_correct = sum(1 for r in new_results if r.get('is_correct', False))
        new_total = len(new_results)
        new_accuracy = new_correct / new_total if new_total > 0 else 0
        
        # Calculate improvement
        accuracy_improvement = new_accuracy - old_accuracy
        
        # Average analysis time
        old_avg_time = sum(r.get('analysis_time_ms', 0) for r in old_results) / old_total if old_total > 0 else 0
        new_avg_time = sum(r.get('analysis_time_ms', 0) for r in new_results) / new_total if new_total > 0 else 0
        
        # Malicious detection specifically
        malicious_tests = [i for i, r in enumerate(old_results) if r.get('expected') == 'malicious']
        old_malicious_correct = sum(1 for i in malicious_tests if old_results[i].get('is_correct', False))
        new_malicious_correct = sum(1 for i in malicious_tests if new_results[i].get('is_correct', False))
        
        old_malicious_rate = old_malicious_correct / len(malicious_tests) if malicious_tests else 0
        new_malicious_rate = new_malicious_correct / len(malicious_tests) if malicious_tests else 0
        
        return {
            'old_accuracy': old_accuracy,
            'new_accuracy': new_accuracy,
            'accuracy_improvement': accuracy_improvement,
            'old_avg_time_ms': old_avg_time,
            'new_avg_time_ms': new_avg_time,
            'old_malicious_detection_rate': old_malicious_rate,
            'new_malicious_detection_rate': new_malicious_rate,
            'malicious_detection_improvement': new_malicious_rate - old_malicious_rate,
            'old_correct_count': old_correct,
            'new_correct_count': new_correct,
            'total_tests': old_total
        }

def main():
    print("=" * 80)
    print("🔒 SECURITY MODEL COMPARISON TEST 🔒")
    print("Enhanced Security Models vs Previous DistilBERT")
    print("=" * 80)
    
    comparison = SecurityModelComparison()
    results = comparison.run_comparison()
    
    print("\n" + "=" * 80)
    print("📊 COMPARISON RESULTS")
    print("=" * 80)
    
    analysis = comparison.analyze_comparison(results)
    
    print(f"\n🎯 Overall Accuracy:")
    print(f"   Old (DistilBERT): {analysis['old_accuracy']:.2%} ({analysis['old_correct_count']}/{analysis['total_tests']})")
    print(f"   New (Enhanced): {analysis['new_accuracy']:.2%} ({analysis['new_correct_count']}/{analysis['total_tests']})")
    print(f"   Improvement: {analysis['accuracy_improvement']:+.2%}")
    
    print(f"\n🔍 Malicious Detection Rate:")
    print(f"   Old (DistilBERT): {analysis['old_malicious_detection_rate']:.2%}")
    print(f"   New (Enhanced): {analysis['new_malicious_detection_rate']:.2%}")
    print(f"   Improvement: {analysis['malicious_detection_improvement']:+.2%}")
    
    print(f"\n⚡ Performance:")
    print(f"   Old Avg Time: {analysis['old_avg_time_ms']:.2f}ms")
    print(f"   New Avg Time: {analysis['new_avg_time_ms']:.2f}ms")
    print(f"   Time Difference: {analysis['new_avg_time_ms'] - analysis['old_avg_time_ms']:+.2f}ms")
    
    print("\n" + "=" * 80)
    print("🎯 FINAL VERDICT")
    print("=" * 80)
    
    if analysis['accuracy_improvement'] > 0.2:
        print("🏆 SIGNIFICANT IMPROVEMENT: Enhanced security models are much better!")
        print(f"   Accuracy improved by {analysis['accuracy_improvement']:.2%}")
    elif analysis['accuracy_improvement'] > 0:
        print("✅ IMPROVEMENT: Enhanced security models show better performance")
        print(f"   Accuracy improved by {analysis['accuracy_improvement']:.2%}")
    elif analysis['accuracy_improvement'] == 0:
        print("⚖️  EQUAL: Both models perform similarly")
    else:
        print("❌ DECLINE: Enhanced models performed worse (unexpected)")
        print(f"   Accuracy changed by {analysis['accuracy_improvement']:.2%}")

if __name__ == "__main__":
    main()