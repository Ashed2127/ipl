"""
IPL SQL Injection Neural Detection Test
Tests if IPL's neural security analyzer can inherently detect SQL injection
using only its ML capabilities (DistilBERT) - no external detection systems
"""
import time
from typing import List, Dict, Any
from real_neural_security_analyzer import RealNeuralSecurityAnalyzer
from real_neural_parser_truly_neural import RealNeuralParserTrulyNeural

class IPLSQLInjectionNeuralTest:
    """Test IPL's neural ML capabilities for SQL injection detection"""
    
    def __init__(self):
        print("🔥 IPL SQL Injection Neural Detection Test")
        print("Testing pure neural ML capabilities - no external detection systems")
        self.security_analyzer = RealNeuralSecurityAnalyzer()
        self.parser = RealNeuralParserTrulyNeural()
        
    def generate_sql_injection_patterns(self) -> List[Dict[str, str]]:
        """Generate various SQL injection attack patterns"""
        print("🔨 Generating SQL injection attack patterns...")
        
        patterns = [
            # Classic SQL injection
            {
                'name': 'Classic OR 1=1',
                'code': 'let query = "SELECT * FROM users WHERE id = 1 OR 1=1";',
                'type': 'sql_injection',
                'severity': 'HIGH'
            },
            {
                'name': 'UNION-based',
                'code': 'let query = "SELECT * FROM users WHERE id = 1 UNION SELECT password FROM admin";',
                'type': 'sql_injection',
                'severity': 'HIGH'
            },
            {
                'name': 'Comment-based',
                'code': 'let query = "SELECT * FROM users WHERE id = 1 -- comment";',
                'type': 'sql_injection',
                'severity': 'MEDIUM'
            },
            {
                'name': 'Time-based blind',
                'code': 'let query = "SELECT * FROM users WHERE id = 1; WAITFOR DELAY \'0:0:5\'--";',
                'type': 'sql_injection',
                'severity': 'HIGH'
            },
            {
                'name': 'Error-based',
                'code': 'let query = "SELECT * FROM users WHERE id = 1 AND 1=CONVERT(int, (SELECT TOP 1 name FROM sysobjects))";',
                'type': 'sql_injection',
                'severity': 'HIGH'
            },
            {
                'name': 'Stacked queries',
                'code': 'let query = "SELECT * FROM users WHERE id = 1; DROP TABLE users--";',
                'type': 'sql_injection',
                'severity': 'CRITICAL'
            },
            {
                'name': 'Second-order injection',
                'code': 'let input = "admin\'; DROP TABLE users--"; let query = "SELECT * FROM users WHERE name = \'" + input + "\'";',
                'type': 'sql_injection',
                'severity': 'HIGH'
            },
            {
                'name': 'Cookie-based injection',
                'code': 'let cookie = "SELECT * FROM users WHERE id = " + document.cookie;',
                'type': 'sql_injection',
                'severity': 'HIGH'
            },
            # Advanced patterns
            {
                'name': 'Encoded injection',
                'code': 'let query = "SELECT * FROM users WHERE id = 1%20OR%201=1";',
                'type': 'sql_injection',
                'severity': 'MEDIUM'
            },
            {
                'name': 'Hex-encoded',
                'code': 'let query = "SELECT * FROM users WHERE id = 0x" + malicious_hex;',
                'type': 'sql_injection',
                'severity': 'MEDIUM'
            },
            {
                'name': 'Conditional injection',
                'code': 'let query = "SELECT * FROM users WHERE id = 1 AND (SELECT SUBSTRING(password,1,1) FROM admin) = \'a\'";',
                'type': 'sql_injection',
                'severity': 'HIGH'
            },
            {
                'name': 'Boolean-based blind',
                'code': 'let query = "SELECT * FROM users WHERE id = 1 AND 1=1";',
                'type': 'sql_injection',
                'severity': 'MEDIUM'
            },
            # Bypass techniques
            {
                'name': 'Case variation',
                'code': 'let query = "SeLeCt * FrOm uSeRs WhErE iD = 1 oR 1=1";',
                'type': 'sql_injection',
                'severity': 'MEDIUM'
            },
            {
                'name': 'Whitespace bypass',
                'code': 'let query = "SELECT/**//* FROM/**/users/**/WHERE/**/id=1/**/OR/**/1=1";',
                'type': 'sql_injection',
                'severity': 'MEDIUM'
            },
            {
                'name': 'Function obfuscation',
                'code': 'let query = "SELECT * FROM users WHERE id = CHAR(83)+CHAR(81)+CHAR(76)";',
                'type': 'sql_injection',
                'severity': 'MEDIUM'
            }
        ]
        
        print(f"✅ Generated {len(patterns)} SQL injection patterns")
        return patterns
    
    def generate_normal_sql_code(self) -> List[Dict[str, str]]:
        """Generate normal SQL code for comparison"""
        print("📝 Generating normal SQL code patterns...")
        
        patterns = [
            {
                'name': 'Simple SELECT',
                'code': 'let query = "SELECT * FROM users WHERE id = 1";',
                'type': 'normal',
                'severity': 'NONE'
            },
            {
                'name': 'Parameterized query',
                'code': 'let query = "SELECT * FROM users WHERE id = ?"; let params = [user_id];',
                'type': 'normal',
                'severity': 'NONE'
            },
            {
                'name': 'JOIN query',
                'code': 'let query = "SELECT u.name, o.order_id FROM users u JOIN orders o ON u.id = o.user_id";',
                'type': 'normal',
                'severity': 'NONE'
            },
            {
                'name': 'INSERT statement',
                'code': 'let query = "INSERT INTO users (name, email) VALUES (?, ?)";',
                'type': 'normal',
                'severity': 'NONE'
            },
            {
                'name': 'UPDATE statement',
                'code': 'let query = "UPDATE users SET last_login = NOW() WHERE id = ?";',
                'type': 'normal',
                'severity': 'NONE'
            },
            {
                'name': 'DELETE statement',
                'code': 'let query = "DELETE FROM sessions WHERE expires < NOW()";',
                'type': 'normal',
                'severity': 'NONE'
            },
            {
                'name': 'Aggregation query',
                'code': 'let query = "SELECT COUNT(*) as total, AVG(price) as avg_price FROM products";',
                'type': 'normal',
                'severity': 'NONE'
            },
            {
                'name': 'Subquery',
                'code': 'let query = "SELECT * FROM users WHERE id IN (SELECT user_id FROM orders)";',
                'type': 'normal',
                'severity': 'NONE'
            },
            {
                'name': 'Stored procedure call',
                'code': 'let query = "CALL get_user_data(?)";',
                'type': 'normal',
                'severity': 'NONE'
            },
            {
                'name': 'Transaction block',
                'code': 'let query = "BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; COMMIT;";',
                'type': 'normal',
                'severity': 'NONE'
            }
        ]
        
        print(f"✅ Generated {len(patterns)} normal SQL patterns")
        return patterns
    
    def analyze_code_with_neural_security(self, pattern: Dict[str, str]) -> Dict[str, Any]:
        """Analyze code pattern using only neural security (no external systems)"""
        try:
            code = pattern['code']
            
            # Parse the code
            parser_result = self.parser.parse_with_neural_recovery(code)
            
            # Analyze with neural security ONLY (DistilBERT-based)
            security_result = self.security_analyzer.analyze_security_with_neural(code, parser_result['ast'])
            
            # Determine if neural ML detected the threat
            is_threat_detected = security_result['security_score'] < 0.5
            security_level = security_result['security_level']
            
            # Check if SQL injection was specifically detected
            vulnerabilities = security_result.get('vulnerabilities', [])
            sql_injection_detected = any('sql' in str(v).lower() for v in vulnerabilities)
            
            return {
                'pattern_name': pattern['name'],
                'pattern_type': pattern['type'],
                'expected_severity': pattern['severity'],
                'security_score': security_result['security_score'],
                'security_level': security_level,
                'is_threat_detected': is_threat_detected,
                'sql_injection_detected': sql_injection_detected,
                'vulnerabilities': vulnerabilities,
                'neural_method': security_result['method'],
                'correct_detection': (pattern['type'] == 'sql_injection' and is_threat_detected) or
                                   (pattern['type'] == 'normal' and not is_threat_detected)
            }
        except Exception as e:
            return {
                'pattern_name': pattern['name'],
                'error': str(e),
                'correct_detection': False
            }
    
    def run_neural_detection_test(self) -> Dict[str, Any]:
        """Run comprehensive neural detection test"""
        print(f"\n🧠 Running Neural ML Detection Test (No External Systems)")
        print(f"🎯 Testing IPL's DistilBERT-based security analyzer")
        
        # Test SQL injection patterns
        sql_patterns = self.generate_sql_injection_patterns()
        sql_results = []
        
        print(f"\n🔍 Testing {len(sql_patterns)} SQL injection patterns...")
        for pattern in sql_patterns:
            result = self.analyze_code_with_neural_security(pattern)
            sql_results.append(result)
            detected = "✅ DETECTED" if result['is_threat_detected'] else "❌ MISSED"
            print(f"   {pattern['name']}: {detected} (Score: {result.get('security_score', 0):.2%})")
        
        # Test normal SQL patterns
        normal_patterns = self.generate_normal_sql_code()
        normal_results = []
        
        print(f"\n🔍 Testing {len(normal_patterns)} normal SQL patterns...")
        for pattern in normal_patterns:
            result = self.analyze_code_with_neural_security(pattern)
            normal_results.append(result)
            blocked = "❌ FALSE POSITIVE" if result['is_threat_detected'] else "✅ CORRECTLY ALLOWED"
            print(f"   {pattern['name']}: {blocked} (Score: {result.get('security_score', 0):.2%})")
        
        return {
            'sql_results': sql_results,
            'normal_results': normal_results
        }
    
    def analyze_neural_detection_performance(self, test_results: Dict) -> Dict[str, Any]:
        """Analyze neural ML detection performance"""
        sql_results = test_results['sql_results']
        normal_results = test_results['normal_results']
        
        # SQL injection detection metrics
        true_positives = sum(1 for r in sql_results if r.get('is_threat_detected', False))
        false_negatives = len(sql_results) - true_positives
        
        # Normal traffic metrics
        true_negatives = sum(1 for r in normal_results if not r.get('is_threat_detected', False))
        false_positives = len(normal_results) - true_negatives
        
        # Calculate metrics
        sql_detection_rate = true_positives / len(sql_results) if sql_results else 0
        false_positive_rate = false_positives / len(normal_results) if normal_results else 0
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        
        # F1 score
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Overall accuracy
        total_correct = true_positives + true_negatives
        total_tests = len(sql_results) + len(normal_results)
        accuracy = total_correct / total_tests if total_tests > 0 else 0
        
        # Neural method verification
        neural_methods = [r.get('neural_method') for r in sql_results + normal_results if r.get('neural_method')]
        uses_real_neural = any('neural' in str(method).lower() for method in neural_methods)
        
        return {
            'sql_detection_rate': sql_detection_rate,
            'false_positive_rate': false_positive_rate,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'accuracy': accuracy,
            'true_positives': true_positives,
            'false_negatives': false_negatives,
            'true_negatives': true_negatives,
            'false_positives': false_positives,
            'uses_real_neural': uses_real_neural,
            'neural_methods': neural_methods
        }

def main():
    print("=" * 80)
    print("🔥 IPL SQL INJECTION NEURAL DETECTION TEST 🔥")
    print("Testing pure neural ML capabilities - NO external detection systems")
    print("Only DistilBERT-based neural security analyzer")
    print("=" * 80)
    
    tester = IPLSQLInjectionNeuralTest()
    
    # Run neural detection test
    test_results = tester.run_neural_detection_test()
    
    # Analyze performance
    print("\n" + "=" * 80)
    print("📊 NEURAL ML DETECTION PERFORMANCE ANALYSIS")
    print("=" * 80)
    
    performance = tester.analyze_neural_detection_performance(test_results)
    
    print(f"\n🧠 Neural ML Verification:")
    print(f"   Uses Real Neural Networks: {performance['uses_real_neural']}")
    print(f"   Neural Methods: {set(performance['neural_methods'])}")
    
    print(f"\n🎯 SQL Injection Detection:")
    print(f"   Detection Rate: {performance['sql_detection_rate']:.2%}")
    print(f"   True Positives (correctly detected): {performance['true_positives']}")
    print(f"   False Negatives (missed attacks): {performance['false_negatives']}")
    
    print(f"\n📈 Detection Metrics:")
    print(f"   Precision: {performance['precision']:.2%}")
    print(f"   Recall: {performance['recall']:.2%}")
    print(f"   F1 Score: {performance['f1_score']:.2%}")
    print(f"   Overall Accuracy: {performance['accuracy']:.2%}")
    
    print(f"\n⚠️  False Positive Analysis:")
    print(f"   False Positive Rate: {performance['false_positive_rate']:.2%}")
    print(f"   True Negatives (correctly allowed): {performance['true_negatives']}")
    print(f"   False Positives (incorrectly blocked): {performance['false_positives']}")
    
    # Detailed breakdown of missed attacks
    missed_attacks = [r for r in test_results['sql_results'] if not r.get('is_threat_detected', False)]
    if missed_attacks:
        print(f"\n❌ Missed SQL Injection Patterns ({len(missed_attacks)}):")
        for attack in missed_attacks:
            print(f"   - {attack['pattern_name']}: Score {attack.get('security_score', 0):.2%}")
    
    # Detailed breakdown of false positives
    false_positives = [r for r in test_results['normal_results'] if r.get('is_threat_detected', False)]
    if false_positives:
        print(f"\n⚠️  False Positives - Normal Code Blocked ({len(false_positives)}):")
        for fp in false_positives:
            print(f"   - {fp['pattern_name']}: Score {fp.get('security_score', 0):.2%}")
    
    # Final verdict
    print("\n" + "=" * 80)
    print("🎯 FINAL VERDICT: IPL NEURAL ML SQL INJECTION DETECTION")
    print("=" * 80)
    
    if performance['sql_detection_rate'] > 0.8 and performance['false_positive_rate'] < 0.1:
        print("🏆 EXCELLENT: IPL's neural ML can effectively detect SQL injection!")
        print(f"   - Detection Rate: {performance['sql_detection_rate']:.2%}")
        print(f"   - False Positive Rate: {performance['false_positive_rate']:.2%}")
    elif performance['sql_detection_rate'] > 0.5:
        print("🥈 MODERATE: IPL's neural ML has some SQL injection detection capability")
        print(f"   - Detection Rate: {performance['sql_detection_rate']:.2%}")
        print(f"   - False Positive Rate: {performance['false_positive_rate']:.2%}")
    elif performance['sql_detection_rate'] > 0.2:
        print("🥉 WEAK: IPL's neural ML has limited SQL injection detection")
        print(f"   - Detection Rate: {performance['sql_detection_rate']:.2%}")
        print(f"   - False Positive Rate: {performance['false_positive_rate']:.2%}")
    else:
        print("❌ POOR: IPL's neural ML cannot effectively detect SQL injection")
        print(f"   - Detection Rate: {performance['sql_detection_rate']:.2%}")
        print(f"   - False Positive Rate: {performance['false_positive_rate']:.2%}")
    
    if performance['uses_real_neural']:
        print("✅ Confirmed: Testing used real neural networks (DistilBERT)")
    else:
        print("❌ Warning: May not be using real neural networks")

if __name__ == "__main__":
    main()