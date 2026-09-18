#!/usr/bin/env python3
"""
Brute Force Attack Test Script
Tests the IPL AI authorization system's ability to detect and block brute force attacks
WITHOUT using rate limiting - purely AI-based detection
"""

import requests
import time
import json
from datetime import datetime
from typing import List, Dict

class BruteForceAttacker:
    """Simulates brute force attacks against the test server"""
    
    def __init__(self, server_url: str = "http://localhost:5000"):
        self.server_url = server_url
        self.results = []
    
    def single_login_attempt(self, username: str, password: str) -> Dict:
        """Single login attempt"""
        try:
            response = requests.post(
                f"{self.server_url}/login",
                json={"username": username, "password": password},
                timeout=5
            )
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "username": username,
                "password": password,
                "status_code": response.status_code,
                "success": response.json().get("success", False),
                "blocked": response.json().get("blocked", False),
                "block_reason": response.json().get("block_reason", ""),
                "ai_decision": response.json().get("ai_decision"),
                "ai_reason": response.json().get("ai_reason"),
                "ai_confidence": response.json().get("ai_confidence"),
                "pattern_analysis": response.json().get("pattern_analysis", {})
            }
            
            return result
            
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "username": username,
                "password": password,
                "error": str(e),
                "success": False,
                "blocked": False
            }
    
    def credential_stuffing_attack(self, username: str, passwords: List[str], delay: float = 0.1) -> List[Dict]:
        """Credential stuffing attack - try many passwords for one user"""
        print(f"\n🔨 CREDENTIAL STUFFING ATTACK on {username}")
        print(f"   Testing {len(passwords)} passwords with {delay}s delay")
        print("="*70)
        
        results = []
        for i, password in enumerate(passwords, 1):
            print(f"[{i}/{len(passwords)}] Attempt: {username}:{password}")
            
            result = self.single_login_attempt(username, password)
            results.append(result)
            
            # Print result
            if result.get("blocked"):
                print(f"   ❌ BLOCKED by AI: {result.get('block_reason')}")
                print(f"   AI Reason: {result.get('ai_reason')}")
                print(f"   AI Confidence: {result.get('ai_confidence')}")
            elif result.get("success"):
                print(f"   ✅ SUCCESS: Authentication worked!")
            else:
                print(f"   ❌ FAILED: Invalid credentials")
            
            # Delay between attempts
            if delay > 0 and i < len(passwords):
                time.sleep(delay)
        
        return results
    
    def password_spray_attack(self, usernames: List[str], password: str, delay: float = 0.1) -> List[Dict]:
        """Password spray attack - try one password against many users"""
        print(f"\n🔨 PASSWORD SPRAY ATTACK with password: {password}")
        print(f"   Testing {len(usernames)} users with {delay}s delay")
        print("="*70)
        
        results = []
        for i, username in enumerate(usernames, 1):
            print(f"[{i}/{len(usernames)}] Attempt: {username}:{password}")
            
            result = self.single_login_attempt(username, password)
            results.append(result)
            
            # Print result
            if result.get("blocked"):
                print(f"   ❌ BLOCKED by AI: {result.get('block_reason')}")
                print(f"   AI Reason: {result.get('ai_reason')}")
                print(f"   AI Confidence: {result.get('ai_confidence')}")
            elif result.get("success"):
                print(f"   ✅ SUCCESS: Authentication worked!")
            else:
                print(f"   ❌ FAILED: Invalid credentials")
            
            # Delay between attempts
            if delay > 0 and i < len(usernames):
                time.sleep(delay)
        
        return results
    
    def rapid_fire_attack(self, username: str, password: str, count: int = 20) -> List[Dict]:
        """Rapid fire attack - many attempts with minimal delay"""
        print(f"\n🔨 RAPID FIRE ATTACK on {username}")
        print(f"   Sending {count} rapid attempts with minimal delay")
        print("="*70)
        
        results = []
        for i in range(1, count + 1):
            print(f"[{i}/{count}] Rapid attempt...")
            
            result = self.single_login_attempt(username, password)
            results.append(result)
            
            # Print result
            if result.get("blocked"):
                print(f"   ❌ BLOCKED by AI: {result.get('block_reason')}")
                print(f"   AI Reason: {result.get('ai_reason')}")
                print(f"   AI Confidence: {result.get('ai_confidence')}")
                # If blocked, maybe stop the attack
                if result.get("ai_confidence", 0) > 0.8:
                    print(f"   🛑 Stopping attack due to high-confidence AI block")
                    break
            elif result.get("success"):
                print(f"   ✅ SUCCESS: Authentication worked!")
            else:
                print(f"   ❌ FAILED: Invalid credentials")
            
            # Minimal delay for rapid fire
            time.sleep(0.05)  # 50ms delay
        
        return results
    
    def analyze_results(self, results: List[Dict]) -> Dict:
        """Analyze attack results"""
        total_attempts = len(results)
        blocked_attempts = sum(1 for r in results if r.get("blocked"))
        successful_attempts = sum(1 for r in results if r.get("success"))
        failed_attempts = total_attempts - blocked_attempts - successful_attempts
        
        # AI decision analysis
        ai_blocks = [r for r in results if r.get("blocked") and r.get("ai_decision") == False]
        ai_confidences = [r.get("ai_confidence", 0) for r in ai_blocks]
        
        analysis = {
            "total_attempts": total_attempts,
            "blocked_by_ai": blocked_attempts,
            "successful_logins": successful_attempts,
            "failed_attempts": failed_attempts,
            "ai_block_rate": blocked_attempts / total_attempts if total_attempts > 0 else 0,
            "success_rate": successful_attempts / total_attempts if total_attempts > 0 else 0,
            "ai_avg_confidence": sum(ai_confidences) / len(ai_confidences) if ai_confidences else 0,
            "ai_blocks": ai_blocks
        }
        
        return analysis

def reset_server(server_url: str):
    """Reset server test data"""
    try:
        response = requests.post(f"{server_url}/reset")
        print(f"✅ Server reset: {response.json()}")
    except Exception as e:
        print(f"❌ Failed to reset server: {e}")

def get_server_stats(server_url: str) -> Dict:
    """Get server statistics"""
    try:
        response = requests.get(f"{server_url}/stats")
        return response.json()
    except Exception as e:
        print(f"❌ Failed to get server stats: {e}")
        return {}

def print_honest_summary(analysis: Dict, attack_type: str):
    """Print honest assessment of AI effectiveness"""
    print(f"\n{'='*70}")
    print(f"📊 HONEST AI EFFECTIVENESS ASSESSMENT: {attack_type}")
    print(f"{'='*70}")
    
    print(f"Total Attempts: {analysis['total_attempts']}")
    print(f"Blocked by AI: {analysis['blocked_by_ai']} ({analysis['ai_block_rate']:.1%})")
    print(f"Successful Logins: {analysis['successful_logins']} ({analysis['success_rate']:.1%})")
    print(f"Failed (Not Blocked): {analysis['failed_attempts']}")
    print(f"AI Average Confidence: {analysis['ai_avg_confidence']:.2f}")
    
    print(f"\n🧠 AI ASSESSMENT:")
    if analysis['ai_block_rate'] >= 0.8:
        print("✅ STRONG: AI effectively blocked most brute force attempts")
    elif analysis['ai_block_rate'] >= 0.5:
        print("⚠️  MODERATE: AI blocked some attempts but needs improvement")
    else:
        print("❌ WEAK: AI failed to effectively block brute force attacks")
    
    print(f"\n⚠️  HONEST NOTES:")
    print("- This tests AI-based detection WITHOUT rate limiting")
    print("- AI relies on pattern recognition and context analysis")
    print("- Effectiveness depends on AI training and pattern definitions")
    print("- Real production should combine AI with rate limiting")
    
    print(f"{'='*70}")

def main():
    """Main test execution"""
    server_url = "http://localhost:5000"
    
    print("="*70)
    print("🔨 BRUTE FORCE ATTACK TESTER")
    print("="*70)
    print("Testing IPL AI authorization WITHOUT rate limiting")
    print("="*70)
    
    # Check server health
    try:
        response = requests.get(f"{server_url}/health", timeout=2)
        print(f"✅ Server is healthy: {response.json()}")
    except Exception as e:
        print(f"❌ Server is not accessible: {e}")
        print("Please start the test server first: python3 test_server.py")
        return
    
    # Reset server
    reset_server(server_url)
    
    attacker = BruteForceAttacker(server_url)
    
    # Test 1: Credential Stuffing Attack
    print("\n" + "="*70)
    print("TEST 1: CREDENTIAL STUFFING ATTACK")
    print("="*70)
    
    common_passwords = [
        "wrongpassword1", "wrongpassword2", "wrongpassword3", "wrongpassword4", "wrongpassword5",
        "wrongpassword6", "wrongpassword7", "wrongpassword8", "wrongpassword9", "wrongpassword10"
    ]
    
    results1 = attacker.credential_stuffing_attack("admin", common_passwords, delay=0.2)
    analysis1 = attacker.analyze_results(results1)
    print_honest_summary(analysis1, "CREDENTIAL STUFFING")
    
    # Reset for next test
    reset_server(server_url)
    time.sleep(1)
    
    # Test 2: Password Spray Attack
    print("\n" + "="*70)
    print("TEST 2: PASSWORD SPRAY ATTACK")
    print("="*70)
    
    common_usernames = ["admin", "user", "guest", "moderator", "test"]
    
    results2 = attacker.password_spray_attack(common_usernames, "wrongpassword123", delay=0.2)
    analysis2 = attacker.analyze_results(results2)
    print_honest_summary(analysis2, "PASSWORD SPRAY")
    
    # Reset for next test
    reset_server(server_url)
    time.sleep(1)
    
    # Test 3: Rapid Fire Attack
    print("\n" + "="*70)
    print("TEST 3: RAPID FIRE ATTACK")
    print("="*70)
    
    results3 = attacker.rapid_fire_attack("admin", "wrongpassword", count=15)
    analysis3 = attacker.analyze_results(results3)
    print_honest_summary(analysis3, "RAPID FIRE")
    
    # Final server stats
    print("\n" + "="*70)
    print("📈 FINAL SERVER STATISTICS")
    print("="*70)
    final_stats = get_server_stats(server_url)
    print(json.dumps(final_stats, indent=2))
    
    # Overall assessment
    print("\n" + "="*70)
    print("🎯 OVERALL HONEST ASSESSMENT")
    print("="*70)
    
    total_ai_blocks = analysis1['blocked_by_ai'] + analysis2['blocked_by_ai'] + analysis3['blocked_by_ai']
    total_attempts = analysis1['total_attempts'] + analysis2['total_attempts'] + analysis3['total_attempts']
    overall_ai_rate = total_ai_blocks / total_attempts if total_attempts > 0 else 0
    
    print(f"Total Attempts Across All Tests: {total_attempts}")
    print(f"Total AI Blocks: {total_ai_blocks}")
    print(f"Overall AI Block Rate: {overall_ai_rate:.1%}")
    
    print(f"\n🧠 FINAL AI ASSESSMENT:")
    if overall_ai_rate >= 0.7:
        print("✅ AI authorization shows strong brute force detection capability")
    elif overall_ai_rate >= 0.4:
        print("⚠️  AI authorization shows moderate capability - needs enhancement")
    else:
        print("❌ AI authorization shows weak brute force detection - not production ready")
    
    print(f"\n⚠️  PRODUCTION RECOMMENDATION:")
    print("- AI-based detection alone is not sufficient for production")
    print("- Should be combined with traditional rate limiting")
    print("- Multi-layered security approach is recommended")
    print("- Monitor and tune AI confidence thresholds")

if __name__ == "__main__":
    main()