#!/usr/bin/env python3
"""
AI-Driven Brute Force Attack Test Script
Tests IPL's hierarchical AI engine with Qwen2.5-Coder:0.5b for brute force detection
Compares AI-driven decisions vs hardcoded pattern matching
"""

import requests
import time
import json
from datetime import datetime
from typing import List, Dict

class AIBruteForceAttacker:
    """Tests AI-driven brute force detection"""
    
    def __init__(self, server_url: str = "http://localhost:5000"):
        self.server_url = server_url
        self.results = []
    
    def single_login_attempt(self, username: str, password: str) -> Dict:
        """Single login attempt with AI analysis"""
        try:
            response = requests.post(
                f"{self.server_url}/login",
                json={"username": username, "password": password},
                timeout=30  # Longer timeout for AI processing
            )
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "username": username,
                "password": password,
                "status_code": response.status_code,
                "success": response.json().get("success", False),
                "blocked": response.json().get("blocked", False),
                "block_reason": response.json().get("block_reason", ""),
                "ai_analysis": response.json().get("ai_analysis", {}),
                "ai_driven": response.json().get("ai_analysis", {}).get("ai_driven", False)
            }
            
            return result
            
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "username": username,
                "password": password,
                "error": str(e),
                "success": False,
                "blocked": False,
                "ai_driven": False
            }
    
    def credential_stuffing_attack(self, username: str, passwords: List[str], delay: float = 0.5) -> List[Dict]:
        """Credential stuffing attack - try many passwords for one user"""
        print(f"\n🔨 AI CREDENTIAL STUFFING ATTACK on {username}")
        print(f"   Testing {len(passwords)} passwords with {delay}s delay")
        print(f"   AI Model: Qwen2.5-Coder:0.5b making decisions")
        print("="*70)
        
        results = []
        for i, password in enumerate(passwords, 1):
            print(f"[{i}/{len(passwords)}] Attempt: {username}:{password}")
            
            result = self.single_login_attempt(username, password)
            results.append(result)
            
            # Print AI analysis
            ai_analysis = result.get("ai_analysis", {})
            if ai_analysis:
                decision = ai_analysis.get("decision", {})
                print(f"   🧠 AI Decision: {decision.get('recommendation', 'unknown')} (confidence: {ai_analysis.get('confidence', 0):.2f})")
                print(f"   Attack Type: {decision.get('attack_type', 'unknown')}")
                print(f"   Reason: {decision.get('reason', 'unknown')}")
                if ai_analysis.get('ai_driven'):
                    print(f"   AI Tier: {ai_analysis.get('tier_used', 'unknown')}")
                    print(f"   Execution Time: {ai_analysis.get('execution_time_ms', 0):.2f}ms")
            
            # Print result
            if result.get("blocked"):
                print(f"   ❌ BLOCKED by AI: {result.get('block_reason')}")
            elif result.get("success"):
                print(f"   ✅ SUCCESS: Authentication worked!")
            else:
                print(f"   ❌ FAILED: Invalid credentials")
            
            # Delay between attempts (longer for AI processing)
            if delay > 0 and i < len(passwords):
                time.sleep(delay)
        
        return results
    
    def password_spray_attack(self, usernames: List[str], password: str, delay: float = 0.5) -> List[Dict]:
        """Password spray attack - try one password against many users"""
        print(f"\n🔨 AI PASSWORD SPRAY ATTACK with password: {password}")
        print(f"   Testing {len(usernames)} users with {delay}s delay")
        print(f"   AI Model: Qwen2.5-Coder:0.5b making decisions")
        print("="*70)
        
        results = []
        for i, username in enumerate(usernames, 1):
            print(f"[{i}/{len(usernames)}] Attempt: {username}:{password}")
            
            result = self.single_login_attempt(username, password)
            results.append(result)
            
            # Print AI analysis
            ai_analysis = result.get("ai_analysis", {})
            if ai_analysis:
                decision = ai_analysis.get("decision", {})
                print(f"   🧠 AI Decision: {decision.get('recommendation', 'unknown')} (confidence: {ai_analysis.get('confidence', 0):.2f})")
                print(f"   Attack Type: {decision.get('attack_type', 'unknown')}")
                print(f"   Reason: {decision.get('reason', 'unknown')}")
            
            # Print result
            if result.get("blocked"):
                print(f"   ❌ BLOCKED by AI: {result.get('block_reason')}")
            elif result.get("success"):
                print(f"   ✅ SUCCESS: Authentication worked!")
            else:
                print(f"   ❌ FAILED: Invalid credentials")
            
            # Delay between attempts
            if delay > 0 and i < len(usernames):
                time.sleep(delay)
        
        return results
    
    def rapid_fire_attack(self, username: str, password: str, count: int = 10) -> List[Dict]:
        """Rapid fire attack - many attempts with minimal delay"""
        print(f"\n🔨 AI RAPID FIRE ATTACK on {username}")
        print(f"   Sending {count} rapid attempts with minimal delay")
        print(f"   AI Model: Qwen2.5-Coder:0.5b making decisions")
        print("="*70)
        
        results = []
        for i in range(1, count + 1):
            print(f"[{i}/{count}] Rapid attempt...")
            
            result = self.single_login_attempt(username, password)
            results.append(result)
            
            # Print AI analysis
            ai_analysis = result.get("ai_analysis", {})
            if ai_analysis:
                decision = ai_analysis.get("decision", {})
                print(f"   🧠 AI Decision: {decision.get('recommendation', 'unknown')} (confidence: {ai_analysis.get('confidence', 0):.2f})")
                print(f"   Attack Type: {decision.get('attack_type', 'unknown')}")
            
            # Print result
            if result.get("blocked"):
                print(f"   ❌ BLOCKED by AI: {result.get('block_reason')}")
                # If blocked with high confidence, maybe stop
                if ai_analysis.get('confidence', 0) > 0.8:
                    print(f"   🛑 Stopping attack due to high-confidence AI block")
                    break
            elif result.get("success"):
                print(f"   ✅ SUCCESS: Authentication worked!")
            else:
                print(f"   ❌ FAILED: Invalid credentials")
            
            # Minimal delay for rapid fire (but AI needs time)
            time.sleep(0.3)  # 300ms for AI processing
        
        return results
    
    def analyze_results(self, results: List[Dict]) -> Dict:
        """Analyze AI-driven attack results"""
        total_attempts = len(results)
        blocked_attempts = sum(1 for r in results if r.get("blocked"))
        successful_attempts = sum(1 for r in results if r.get("success"))
        failed_attempts = total_attempts - blocked_attempts - successful_attempts
        
        # AI decision analysis
        ai_driven_attempts = sum(1 for r in results if r.get("ai_driven"))
        ai_blocks = [r for r in results if r.get("blocked") and r.get("ai_driven")]
        ai_confidences = [r.get("ai_analysis", {}).get("confidence", 0) for r in ai_blocks]
        
        # Attack type detection
        attack_types = {}
        for r in results:
            ai_analysis = r.get("ai_analysis", {})
            decision = ai_analysis.get("decision", {})
            attack_type = decision.get("attack_type", "none")
            attack_types[attack_type] = attack_types.get(attack_type, 0) + 1
        
        analysis = {
            "total_attempts": total_attempts,
            "blocked_by_ai": blocked_attempts,
            "successful_logins": successful_attempts,
            "failed_attempts": failed_attempts,
            "ai_driven_attempts": ai_driven_attempts,
            "ai_block_rate": blocked_attempts / total_attempts if total_attempts > 0 else 0,
            "success_rate": successful_attempts / total_attempts if total_attempts > 0 else 0,
            "ai_avg_confidence": sum(ai_confidences) / len(ai_confidences) if ai_confidences else 0,
            "attack_types_detected": attack_types,
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

def print_ai_summary(analysis: Dict, attack_type: str):
    """Print AI effectiveness assessment"""
    print(f"\n{'='*70}")
    print(f"📊 AI-DRIVEN EFFECTIVENESS ASSESSMENT: {attack_type}")
    print(f"{'='*70}")
    
    print(f"Total Attempts: {analysis['total_attempts']}")
    print(f"AI-Driven Attempts: {analysis['ai_driven_attempts']} ({analysis['ai_driven_attempts']/analysis['total_attempts']*100 if analysis['total_attempts'] > 0 else 0:.1f}%)")
    print(f"Blocked by AI: {analysis['blocked_by_ai']} ({analysis['ai_block_rate']:.1%})")
    print(f"Successful Logins: {analysis['successful_logins']} ({analysis['success_rate']:.1%})")
    print(f"Failed (Not Blocked): {analysis['failed_attempts']}")
    print(f"AI Average Confidence: {analysis['ai_avg_confidence']:.2f}")
    print(f"Attack Types Detected: {analysis['attack_types_detected']}")
    
    print(f"\n🧠 AI ASSESSMENT:")
    if analysis['ai_block_rate'] >= 0.8:
        print("✅ STRONG: AI effectively blocked most brute force attempts")
    elif analysis['ai_block_rate'] >= 0.5:
        print("⚠️  MODERATE: AI blocked some attempts but needs improvement")
    else:
        print("❌ WEAK: AI failed to effectively block brute force attacks")
    
    print(f"\n⚠️  AI-SPECIFIC NOTES:")
    print(f"- AI Model: Qwen2.5-Coder:0.5b")
    print(f"- AI-Driven Rate: {analysis['ai_driven_attempts']/analysis['total_attempts']*100 if analysis['total_attempts'] > 0 else 0:.1f}%")
    print(f"- Attack Type Recognition: {analysis['attack_types_detected']}")
    print(f"- Decision Confidence: {analysis['ai_avg_confidence']:.2f}")
    
    print(f"{'='*70}")

def main():
    """Main test execution"""
    server_url = "http://localhost:5000"
    
    print("="*70)
    print("🧠 AI-DRIVEN BRUTE FORCE ATTACK TESTER")
    print("="*70)
    print("Testing IPL's Hierarchical AI Engine with Qwen2.5-Coder:0.5b")
    print("Minimal hardcoded rules - AI makes the decisions")
    print("="*70)
    
    # Check server health
    try:
        response = requests.get(f"{server_url}/health", timeout=2)
        health_data = response.json()
        print(f"✅ Server is healthy: {health_data}")
        print(f"   AI Engine: {health_data.get('ai_engine', 'unknown')}")
        print(f"   AI Model: {health_data.get('ai_model', 'unknown')}")
    except Exception as e:
        print(f"❌ Server is not accessible: {e}")
        print("Please start the AI test server first: python3 test_server_ai.py")
        return
    
    # Reset server
    reset_server(server_url)
    
    attacker = AIBruteForceAttacker(server_url)
    
    # Test 1: AI Credential Stuffing Attack
    print("\n" + "="*70)
    print("TEST 1: AI CREDENTIAL STUFFING ATTACK")
    print("="*70)
    
    wrong_passwords = [
        "wrongpassword1", "wrongpassword2", "wrongpassword3", "wrongpassword4", "wrongpassword5",
        "wrongpassword6", "wrongpassword7", "wrongpassword8", "wrongpassword9", "wrongpassword10"
    ]
    
    results1 = attacker.credential_stuffing_attack("admin", wrong_passwords, delay=0.8)
    analysis1 = attacker.analyze_results(results1)
    print_ai_summary(analysis1, "AI CREDENTIAL STUFFING")
    
    # Reset for next test
    reset_server(server_url)
    time.sleep(2)
    
    # Test 2: AI Password Spray Attack
    print("\n" + "="*70)
    print("TEST 2: AI PASSWORD SPRAY ATTACK")
    print("="*70)
    
    common_usernames = ["admin", "user", "guest", "moderator", "test"]
    
    results2 = attacker.password_spray_attack(common_usernames, "wrongpassword123", delay=0.8)
    analysis2 = attacker.analyze_results(results2)
    print_ai_summary(analysis2, "AI PASSWORD SPRAY")
    
    # Reset for next test
    reset_server(server_url)
    time.sleep(2)
    
    # Test 3: AI Rapid Fire Attack
    print("\n" + "="*70)
    print("TEST 3: AI RAPID FIRE ATTACK")
    print("="*70)
    
    results3 = attacker.rapid_fire_attack("admin", "wrongpassword", count=8)
    analysis3 = attacker.analyze_results(results3)
    print_ai_summary(analysis3, "AI RAPID FIRE")
    
    # Final server stats
    print("\n" + "="*70)
    print("📈 FINAL SERVER STATISTICS")
    print("="*70)
    final_stats = get_server_stats(server_url)
    print(json.dumps(final_stats, indent=2))
    
    # Overall assessment
    print("\n" + "="*70)
    print("🎯 OVERALL AI ASSESSMENT")
    print("="*70)
    
    total_ai_blocks = analysis1['blocked_by_ai'] + analysis2['blocked_by_ai'] + analysis3['blocked_by_ai']
    total_attempts = analysis1['total_attempts'] + analysis2['total_attempts'] + analysis3['total_attempts']
    overall_ai_rate = total_ai_blocks / total_attempts if total_attempts > 0 else 0
    
    total_ai_driven = analysis1['ai_driven_attempts'] + analysis2['ai_driven_attempts'] + analysis3['ai_driven_attempts']
    ai_driven_rate = total_ai_driven / total_attempts if total_attempts > 0 else 0
    
    print(f"Total Attempts Across All Tests: {total_attempts}")
    print(f"AI-Driven Decisions: {total_ai_driven} ({ai_driven_rate:.1%})")
    print(f"Total AI Blocks: {total_ai_blocks}")
    print(f"Overall AI Block Rate: {overall_ai_rate:.1%}")
    
    print(f"\n🧠 FINAL AI ASSESSMENT:")
    if overall_ai_rate >= 0.7:
        print("✅ AI authorization shows strong brute force detection capability")
    elif overall_ai_rate >= 0.4:
        print("⚠️  AI authorization shows moderate capability - needs enhancement")
    else:
        print("❌ AI authorization shows weak brute force detection - needs improvement")
    
    print(f"\n⚠️  AI vs HARDCODED COMPARISON:")
    print(f"- AI Block Rate: {overall_ai_rate:.1%}")
    print(f"- AI-Driven Rate: {ai_driven_rate:.1%}")
    print(f"- Hardcoded Block Rate (from previous test): 61.1%")
    print(f"- Difference: {(overall_ai_rate - 0.611)*100:+.1f}%")
    
    print(f"\n⚠️  PRODUCTION RECOMMENDATION:")
    if ai_driven_rate > 0.8:
        print("- AI-driven detection shows promise for production use")
        print("- Consider combining AI with traditional rate limiting")
        print("- Monitor AI confidence levels and decision patterns")
    else:
        print("- AI-driven detection needs more tuning before production")
        print("- Hybrid approach (AI + hardcoded rules) may be optimal")
        print("- Consider AI model training specific to security patterns")

if __name__ == "__main__":
    main()