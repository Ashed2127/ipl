"""
IPL Brute Force Attack Detection Test
Tests if IPL's neural security analyzer can detect and handle 1000 repetitive malicious requests
Measures IPL's ability to identify brute force patterns and control attacks
"""
import time
import random
from typing import List, Dict, Any
from real_neural_security_analyzer import RealNeuralSecurityAnalyzer
from real_neural_parser_truly_neural import RealNeuralParserTrulyNeural

class IPLBruteForceAttackDetector:
    """Test IPL's ability to detect and control brute force attacks"""
    
    def __init__(self):
        print("🔥 IPL Brute Force Attack Detection Test")
        print("Testing neural security analyzer against 1000 repetitive requests")
        self.security_analyzer = RealNeuralSecurityAnalyzer()
        self.parser = RealNeuralParserTrulyNeural()
        
        # Track request patterns for detection
        self.request_history = []
        self.attack_detected = False
        self.attack_detection_count = 0
        self.blocked_requests = 0
        
    def generate_brute_force_requests(self, num_requests: int = 1000) -> List[str]:
        """Generate repetitive requests simulating brute force attack"""
        print(f"🔨 Generating {num_requests} repetitive brute force requests...")
        
        requests = []
        
        # Pattern 1: Repetitive login attempts (30%)
        for i in range(int(num_requests * 0.3)):
            requests.append(f'let login_attempt = attempt_login("admin", "password{i}");')
        
        # Pattern 2: Repetitive SQL injection attempts (25%)
        for i in range(int(num_requests * 0.25)):
            requests.append(f'let query = "SELECT * FROM users WHERE id = {i} OR 1=1";')
        
        # Pattern 3: Repetitive XSS attempts (20%)
        for i in range(int(num_requests * 0.20)):
            requests.append(f'let input = "<script>alert(\'XSS{i}\')</script>";')
        
        # Pattern 4: Repetitive command injection (15%)
        for i in range(int(num_requests * 0.15)):
            requests.append(f'let command = "cat /etc/passwd; rm -rf /";')
        
        # Pattern 5: Repetitive sensitive data access (10%)
        for i in range(int(num_requests * 0.10)):
            requests.append(f'let api_key = "sk-{i}{"a" * 40}";')
        
        # Shuffle to make it more realistic
        random.shuffle(requests)
        
        print(f"✅ Generated {len(requests)} malicious requests")
        return requests
    
    def generate_normal_requests(self, num_requests: int = 100) -> List[str]:
        """Generate normal requests for comparison"""
        print(f"📝 Generating {num_requests} normal requests...")
        
        requests = []
        normal_patterns = [
            'let x = 25;',
            'let name = "John";',
            'let result = calculate(x, y);',
            'let total = price + tax;',
            'let valid = check_status(status);',
            'let clean = sanitize(input);',
            'let encrypted = encrypt(data);'
        ]
        
        for i in range(num_requests):
            requests.append(random.choice(normal_patterns))
        
        print(f"✅ Generated {len(requests)} normal requests")
        return requests
    
    def analyze_request_for_attack(self, request: str, request_number: int) -> Dict[str, Any]:
        """Analyze single request for attack patterns using neural security"""
        try:
            # Parse the request
            parser_result = self.parser.parse_with_neural_recovery(request)
            
            # Analyze with neural security
            security_result = self.security_analyzer.analyze_security_with_neural(request, parser_result['ast'])
            
            # Check for brute force patterns
            is_repetitive = self._check_repetitive_pattern(request, request_number)
            is_malicious = security_result['security_score'] < 0.5
            
            # Determine if this should be blocked
            should_block = is_malicious or is_repetitive
            
            if should_block:
                self.blocked_requests += 1
            
            # Track for pattern detection
            self.request_history.append({
                'request_number': request_number,
                'request': request[:50],  # Truncated for storage
                'security_score': security_result['security_score'],
                'is_malicious': is_malicious,
                'is_repetitive': is_repetitive,
                'should_block': should_block,
                'vulnerabilities': security_result.get('vulnerabilities', [])
            })
            
            return {
                'request_number': request_number,
                'security_score': security_result['security_score'],
                'security_level': security_result['security_level'],
                'is_malicious': is_malicious,
                'is_repetitive': is_repetitive,
                'should_block': should_block,
                'vulnerabilities': security_result.get('vulnerabilities', []),
                'neural_analysis': security_result['method']
            }
        except Exception as e:
            return {
                'request_number': request_number,
                'error': str(e),
                'should_block': True  # Block on error
            }
    
    def _check_repetitive_pattern(self, request: str, request_number: int) -> bool:
        """Check if request shows repetitive pattern (brute force indicator)"""
        if len(self.request_history) < 10:
            return False
        
        # Check last 10 requests for similarity
        recent_requests = self.request_history[-10:]
        
        # Simple similarity check - if 7+ of last 10 are similar
        similar_count = 0
        for hist in recent_requests:
            # Check if requests have similar structure
            if self._requests_similar(request, hist['request']):
                similar_count += 1
        
        return similar_count >= 7
    
    def _requests_similar(self, req1: str, req2: str) -> bool:
        """Simple similarity check between requests"""
        # Remove numbers and check structure
        import re
        pattern1 = re.sub(r'\d+', 'X', req1)
        pattern2 = re.sub(r'\d+', 'X', req2)
        return pattern1 == pattern2
    
    def detect_brute_force_attack(self) -> Dict[str, Any]:
        """Analyze request history to detect brute force attack"""
        if len(self.request_history) < 50:
            return {'attack_detected': False, 'reason': 'Insufficient data'}
        
        # Calculate attack indicators
        malicious_count = sum(1 for r in self.request_history if r['is_malicious'])
        repetitive_count = sum(1 for r in self.request_history if r['is_repetitive'])
        low_security_count = sum(1 for r in self.request_history if r['security_score'] < 0.3)
        
        total_requests = len(self.request_history)
        
        # Attack detection thresholds
        malicious_rate = malicious_count / total_requests
        repetitive_rate = repetitive_count / total_requests
        low_security_rate = low_security_count / total_requests
        
        # Determine if attack is detected
        attack_detected = (
            malicious_rate > 0.7 or  # 70%+ malicious
            repetitive_rate > 0.6 or  # 60%+ repetitive
            low_security_rate > 0.5   # 50%+ very low security
        )
        
        if attack_detected:
            self.attack_detected = True
            self.attack_detection_count += 1
        
        return {
            'attack_detected': attack_detected,
            'malicious_rate': malicious_rate,
            'repetitive_rate': repetitive_rate,
            'low_security_rate': low_security_rate,
            'total_analyzed': total_requests,
            'malicious_count': malicious_count,
            'repetitive_count': repetitive_count,
            'blocked_count': self.blocked_requests
        }
    
    def run_brute_force_attack_simulation(self, num_requests: int = 1000):
        """Run full brute force attack simulation"""
        print(f"\n🔨 Starting Brute Force Attack Simulation: {num_requests} requests")
        print(f"🎯 Testing IPL's neural security detection capabilities")
        
        # Generate malicious requests
        malicious_requests = self.generate_brute_force_requests(num_requests)
        
        print(f"\n🚀 Processing {len(malicious_requests)} requests through IPL neural security...")
        
        results = []
        start_time = time.time()
        
        for i, request in enumerate(malicious_requests):
            result = self.analyze_request_for_attack(request, i)
            results.append(result)
            
            # Check for attack detection periodically
            if (i + 1) % 100 == 0:
                attack_status = self.detect_brute_force_attack()
                print(f"Progress: {i + 1}/{num_requests} | Attack Detected: {attack_status['attack_detected']} | Blocked: {self.blocked_requests}")
                
                if attack_status['attack_detected'] and not self.attack_detected:
                    print(f"🚨 BRUTE FORCE ATTACK DETECTED at request {i + 1}!")
                    self.attack_detected = True
        
        total_time = time.time() - start_time
        
        # Final attack detection
        final_attack_status = self.detect_brute_force_attack()
        
        print(f"\n✅ Attack simulation completed in {total_time:.2f} seconds")
        
        return {
            'results': results,
            'attack_status': final_attack_status,
            'total_time': total_time,
            'blocked_requests': self.blocked_requests,
            'attack_detected': self.attack_detected
        }
    
    def run_normal_traffic_simulation(self, num_requests: int = 100):
        """Run normal traffic simulation for comparison"""
        print(f"\n📝 Starting Normal Traffic Simulation: {num_requests} requests")
        
        # Generate normal requests
        normal_requests = self.generate_normal_requests(num_requests)
        
        print(f"\n🚀 Processing {len(normal_requests)} normal requests through IPL neural security...")
        
        results = []
        blocked_count = 0
        
        for i, request in enumerate(normal_requests):
            result = self.analyze_request_for_attack(request, i)
            results.append(result)
            
            if result['should_block']:
                blocked_count += 1
            
            if (i + 1) % 25 == 0:
                print(f"Progress: {i + 1}/{num_requests} | Blocked: {blocked_count}")
        
        print(f"\n✅ Normal traffic simulation completed")
        
        return {
            'results': results,
            'blocked_count': blocked_count,
            'total_requests': num_requests
        }
    
    def analyze_detection_performance(self, attack_results: Dict, normal_results: Dict) -> Dict[str, Any]:
        """Analyze IPL's attack detection performance"""
        attack_reqs = attack_results['results']
        normal_reqs = normal_results['results']
        
        # Attack detection metrics
        true_positives = sum(1 for r in attack_reqs if r.get('should_block', False))
        false_negatives = len(attack_reqs) - true_positives
        
        # Normal traffic metrics
        true_negatives = sum(1 for r in normal_reqs if not r.get('should_block', False))
        false_positives = len(normal_reqs) - true_negatives
        
        # Calculate metrics
        attack_detection_rate = true_positives / len(attack_reqs) if attack_reqs else 0
        false_positive_rate = false_positives / len(normal_reqs) if normal_reqs else 0
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        
        # F1 score
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'attack_detection_rate': attack_detection_rate,
            'false_positive_rate': false_positive_rate,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'true_positives': true_positives,
            'false_negatives': false_negatives,
            'true_negatives': true_negatives,
            'false_positives': false_positives,
            'attack_detected_by_ipl': attack_results['attack_detected'],
            'blocked_attack_requests': attack_results['blocked_requests'],
            'blocked_normal_requests': normal_results['blocked_count']
        }

def main():
    print("=" * 80)
    print("🔥 IPL BRUTE FORCE ATTACK DETECTION TEST 🔥")
    print("Testing if IPL can detect and control 1000 repetitive malicious requests")
    print("=" * 80)
    
    detector = IPLBruteForceAttackDetector()
    
    # Test 1: Brute Force Attack Simulation
    print("\n" + "=" * 80)
    print("TEST 1: BRUTE FORCE ATTACK SIMULATION (1000 requests)")
    print("=" * 80)
    
    attack_results = detector.run_brute_force_attack_simulation(1000)
    
    # Test 2: Normal Traffic Simulation (for comparison)
    print("\n" + "=" * 80)
    print("TEST 2: NORMAL TRAFFIC SIMULATION (100 requests)")
    print("=" * 80)
    
    # Reset history for normal test
    detector.request_history = []
    detector.blocked_requests = 0
    
    normal_results = detector.run_normal_traffic_simulation(100)
    
    # Analyze performance
    print("\n" + "=" * 80)
    print("📊 IPL ATTACK DETECTION PERFORMANCE ANALYSIS")
    print("=" * 80)
    
    performance = detector.analyze_detection_performance(attack_results, normal_results)
    
    print(f"\n🎯 Attack Detection Capabilities:")
    print(f"   Attack Detection Rate: {performance['attack_detection_rate']:.2%}")
    print(f"   IPL Detected Attack: {performance['attack_detected_by_ipl']}")
    print(f"   Blocked Attack Requests: {performance['blocked_attack_requests']}/1000")
    
    print(f"\n📈 Detection Metrics:")
    print(f"   Precision: {performance['precision']:.2%}")
    print(f"   Recall: {performance['recall']:.2%}")
    print(f"   F1 Score: {performance['f1_score']:.2%}")
    
    print(f"\n⚠️  False Positive Analysis:")
    print(f"   False Positive Rate: {performance['false_positive_rate']:.2%}")
    print(f"   Blocked Normal Requests: {performance['blocked_normal_requests']}/100")
    
    print(f"\n🔍 Detailed Breakdown:")
    print(f"   True Positives (correctly blocked attacks): {performance['true_positives']}")
    print(f"   False Negatives (missed attacks): {performance['false_negatives']}")
    print(f"   True Negatives (correctly allowed normal): {performance['true_negatives']}")
    print(f"   False Positives (incorrectly blocked normal): {performance['false_positives']}")
    
    # Final verdict
    print("\n" + "=" * 80)
    print("🎯 FINAL VERDICT: IPL BRUTE FORCE DETECTION CAPABILITY")
    print("=" * 80)
    
    if performance['attack_detection_rate'] > 0.8 and performance['false_positive_rate'] < 0.2:
        print("🏆 EXCELLENT: IPL can effectively detect and control brute force attacks!")
        print(f"   - Detection Rate: {performance['attack_detection_rate']:.2%}")
        print(f"   - False Positive Rate: {performance['false_positive_rate']:.2%}")
    elif performance['attack_detection_rate'] > 0.6:
        print("🥈 GOOD: IPL can detect most brute force attacks with some room for improvement")
        print(f"   - Detection Rate: {performance['attack_detection_rate']:.2%}")
        print(f"   - False Positive Rate: {performance['false_positive_rate']:.2%}")
    elif performance['attack_detection_rate'] > 0.4:
        print("🥉 MODERATE: IPL has limited brute force detection capabilities")
        print(f"   - Detection Rate: {performance['attack_detection_rate']:.2%}")
        print(f"   - False Positive Rate: {performance['false_positive_rate']:.2%}")
    else:
        print("⚠️  POOR: IPL has weak brute force detection capabilities")
        print(f"   - Detection Rate: {performance['attack_detection_rate']:.2%}")
        print(f"   - False Positive Rate: {performance['false_positive_rate']:.2%}")
    
    if performance['attack_detected_by_ipl']:
        print("✅ IPL successfully identified the brute force attack pattern")
    else:
        print("❌ IPL failed to identify the brute force attack pattern")

if __name__ == "__main__":
    main()