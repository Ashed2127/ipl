"""
Advanced Security Training - OWASP Top 10 2025 + Emerging Threats
Train IPL with top typical exploits and new security issues
"""
import time
import json
import random
from autonomous_decision_engine import (
    AutonomousDecisionEngine,
    Decision,
    DecisionType,
    DecisionOutcome
)


def generate_ssrf_scenarios(n=30):
    """Server-Side Request Forgery attack scenarios"""
    payloads = [
        "http://localhost",
        "http://127.0.0.1",
        "http://169.254.169.254/latest/meta-data/",  # AWS metadata
        "http://localhost:5000/admin",
        "http://127.0.0.1:22",
        "file:///etc/passwd",
        "http://localhost:8080/internal",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "http://localhost:3306",
        "http://[::1]",  # IPv6 localhost
    ]
    
    scenarios = []
    for i in range(n):
        payload = random.choice(payloads)
        scenarios.append({
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': random.randint(2, 5),
            'num_nodes': random.randint(8, 15),
            'num_edges': random.randint(12, 20),
            'avg_degree': random.uniform(2.5, 3.5),
            'execution_count': random.randint(20, 60),
            'avg_execution_time_ms': random.uniform(5.0, 15.0),
            'network_request_count': 1,
            'external_request': True,
            'internal_network_access': True,
            'ssrf_score': random.uniform(0.8, 1.0),
            'attack_type': 'ssrf',
            'expected_safe': False
        })
    return scenarios


def generate_broken_access_control_scenarios(n=40):
    """Broken Access Control - OWASP A01:2025"""
    scenarios = []
    
    # IDOR (Insecure Direct Object Reference)
    for i in range(n // 2):
        scenarios.append({
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': random.randint(1, 3),
            'num_nodes': random.randint(10, 20),
            'num_edges': random.randint(15, 25),
            'avg_degree': random.uniform(2.5, 3.0),
            'execution_count': random.randint(30, 80),
            'avg_execution_time_ms': random.uniform(8.0, 20.0),
            'access_control_check': False,
            'authorization_bypass': True,
            'horizontal_privilege_escalation': True,
            'access_control_score': random.uniform(0.8, 1.0),
            'attack_type': 'broken_access_control',
            'expected_safe': False
        })
    
    # Missing authorization
    for i in range(n // 2):
        scenarios.append({
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': random.randint(1, 4),
            'num_nodes': random.randint(8, 18),
            'num_edges': random.randint(12, 22),
            'avg_degree': random.uniform(2.5, 3.2),
            'execution_count': random.randint(25, 70),
            'avg_execution_time_ms': random.uniform(7.0, 18.0),
            'access_control_check': False,
            'vertical_privilege_escalation': True,
            'admin_endpoint_exposed': True,
            'access_control_score': random.uniform(0.85, 1.0),
            'attack_type': 'broken_access_control',
            'expected_safe': False
        })
    
    return scenarios


def generate_security_misconfiguration_scenarios(n=30):
    """Security Misconfiguration - OWASP A02:2025"""
    scenarios = []
    
    misconfig_types = [
        'default_credentials',
        'debug_mode_enabled',
        'verbose_errors',
        'unnecessary_services',
        'open_ports',
        'default_keys',
    ]
    
    for i in range(n):
        mtype = random.choice(misconfig_types)
        scenarios.append({
            'has_untrusted_data': False,
            'has_sanitization': False,
            'taint_propagation_steps': 0,
            'num_nodes': random.randint(5, 15),
            'num_edges': random.randint(8, 18),
            'avg_degree': random.uniform(2.0, 3.0),
            'execution_count': random.randint(10, 50),
            'avg_execution_time_ms': random.uniform(3.0, 12.0),
            'default_configuration': True,
            'misconfiguration_type': mtype,
            'security_headers_missing': True,
            'misconfiguration_score': random.uniform(0.7, 0.95),
            'attack_type': 'security_misconfiguration',
            'expected_safe': False
        })
    return scenarios


def generate_cryptographic_failure_scenarios(n=30):
    """Cryptographic Failures - OWASP A04:2025"""
    scenarios = []
    
    crypto_failures = [
        'weak_hash',
        'no_encryption',
        'hardcoded_keys',
        'deprecated_crypto',
        'no_https',
        'weak_random',
    ]
    
    for i in range(n):
        cfail = random.choice(crypto_failures)
        scenarios.append({
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': random.randint(1, 3),
            'num_nodes': random.randint(8, 16),
            'num_edges': random.randint(12, 20),
            'avg_degree': random.uniform(2.5, 3.2),
            'execution_count': random.randint(20, 60),
            'avg_execution_time_ms': random.uniform(6.0, 15.0),
            'encryption_used': False,
            'crypto_algorithm_weak': True,
            'keys_hardcoded': True,
            'crypto_failure_score': random.uniform(0.8, 1.0),
            'attack_type': 'cryptographic_failure',
            'expected_safe': False
        })
    return scenarios


def generate_authentication_failure_scenarios(n=30):
    """Authentication Failures - OWASP A07:2025"""
    scenarios = []
    
    auth_failures = [
        'weak_password_policy',
        'no_rate_limiting',
        'session_fixation',
        'credential_stuffing',
        'missing_mfa',
        'password_reuse',
    ]
    
    for i in range(n):
        afail = random.choice(auth_failures)
        scenarios.append({
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': random.randint(1, 4),
            'num_nodes': random.randint(10, 18),
            'num_edges': random.randint(15, 22),
            'avg_degree': random.uniform(2.8, 3.5),
            'execution_count': random.randint(30, 70),
            'avg_execution_time_ms': random.uniform(8.0, 18.0),
            'authentication_weak': True,
            'session_management_poor': True,
            'password_policy_weak': True,
            'auth_failure_score': random.uniform(0.75, 0.95),
            'attack_type': 'authentication_failure',
            'expected_safe': False
        })
    return scenarios


def generate_supply_chain_attack_scenarios(n=25):
    """Software Supply Chain Failures - OWASP A03:2025"""
    scenarios = []
    
    supply_chain_types = [
        'malicious_dependency',
        'compromised_build',
        'typosquatting',
        'dependency_confusion',
        'token_theft',
        'malicious_npm_package',
    ]
    
    for i in range(n):
        sctype = random.choice(supply_chain_types)
        scenarios.append({
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': random.randint(2, 5),
            'num_nodes': random.randint(12, 20),
            'num_edges': random.randint(18, 28),
            'avg_degree': random.uniform(3.0, 3.8),
            'execution_count': random.randint(40, 80),
            'avg_execution_time_ms': random.uniform(10.0, 20.0),
            'external_dependency': True,
            'dependency_unverified': True,
            'supply_chain_compromised': True,
            'supply_chain_score': random.uniform(0.85, 1.0),
            'attack_type': 'supply_chain_attack',
            'expected_safe': False
        })
    return scenarios


def generate_zero_day_scenarios(n=20):
    """Zero-day vulnerabilities"""
    scenarios = []
    
    zero_day_types = [
        'use_after_free',
        'buffer_overflow',
        'race_condition',
        'type_confusion',
        'memory_corruption',
    ]
    
    for i in range(n):
        zdtype = random.choice(zero_day_types)
        scenarios.append({
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': random.randint(1, 4),
            'num_nodes': random.randint(15, 25),
            'num_edges': random.randint(20, 35),
            'avg_degree': random.uniform(3.2, 4.0),
            'execution_count': random.randint(50, 100),
            'avg_execution_time_ms': random.uniform(12.0, 25.0),
            'memory_unsafe': True,
            'unknown_vulnerability': True,
            'exploit_in_wild': True,
            'zero_day_score': random.uniform(0.9, 1.0),
            'attack_type': 'zero_day',
            'expected_safe': False
        })
    return scenarios


def generate_safe_advanced_scenarios(n=50):
    """Safe code scenarios for advanced patterns"""
    scenarios = []
    
    safe_patterns = [
        'proper_access_control',
        'secure_configuration',
        'strong_encryption',
        'multi_factor_auth',
        'verified_dependencies',
        'secure_coding_practices',
    ]
    
    for i in range(n):
        pattern = random.choice(safe_patterns)
        scenarios.append({
            'has_untrusted_data': False,
            'has_sanitization': True,
            'taint_propagation_steps': 0,
            'num_nodes': random.randint(10, 20),
            'num_edges': random.randint(15, 25),
            'avg_degree': random.uniform(2.8, 3.5),
            'execution_count': random.randint(30, 80),
            'avg_execution_time_ms': random.uniform(8.0, 18.0),
            'access_control_check': True,
            'security_headers_present': True,
            'encryption_used': True,
            'dependency_verified': True,
            'safe_score': random.uniform(0.8, 1.0),
            'attack_type': 'safe',
            'expected_safe': True
        })
    return scenarios


def train_advanced_security():
    """Train IPL with OWASP Top 10 2025 + Emerging Threats"""
    print("=" * 70)
    print("ADVANCED SECURITY TRAINING - OWASP Top 10 2025 + Emerging Threats")
    print("=" * 70)
    
    start_time = time.time()
    
    # Generate all advanced scenarios
    print("\n[1/4] Generating advanced security scenarios...")
    gen_start = time.time()
    
    all_scenarios = []
    
    # OWASP Top 10 2025
    all_scenarios.extend(generate_broken_access_control_scenarios(40))
    print(f"  ✓ Broken Access Control (A01): 40 scenarios")
    
    all_scenarios.extend(generate_security_misconfiguration_scenarios(30))
    print(f"  ✓ Security Misconfiguration (A02): 30 scenarios")
    
    all_scenarios.extend(generate_supply_chain_attack_scenarios(25))
    print(f"  ✓ Supply Chain Failures (A03): 25 scenarios")
    
    all_scenarios.extend(generate_cryptographic_failure_scenarios(30))
    print(f"  ✓ Cryptographic Failures (A04): 30 scenarios")
    
    all_scenarios.extend(generate_authentication_failure_scenarios(30))
    print(f"  ✓ Authentication Failures (A07): 30 scenarios")
    
    # Emerging threats
    all_scenarios.extend(generate_ssrf_scenarios(30))
    print(f"  ✓ SSRF (Emerging): 30 scenarios")
    
    all_scenarios.extend(generate_zero_day_scenarios(20))
    print(f"  ✓ Zero-day (Emerging): 20 scenarios")
    
    # Safe scenarios
    all_scenarios.extend(generate_safe_advanced_scenarios(50))
    print(f"  ✓ Safe Advanced Patterns: 50 scenarios")
    
    print(f"  Total: {len(all_scenarios)} advanced scenarios")
    print(f"  Generation time: {time.time() - gen_start:.2f}s")
    
    # Initialize engine
    print("\n[2/4] Initializing Autonomous Decision Engine...")
    engine = AutonomousDecisionEngine(use_intelligent_components=True)
    
    # Train with advanced scenarios
    print("\n[3/4] Training with advanced security scenarios...")
    train_start = time.time()
    
    total_decisions = 0
    correct_decisions = 0
    
    for i, scenario in enumerate(all_scenarios):
        # Extract context (add 64 features)
        context = {
            'has_untrusted_data': scenario['has_untrusted_data'],
            'has_sanitization': scenario['has_sanitization'],
            'taint_propagation_steps': scenario['taint_propagation_steps'],
            'num_nodes': scenario['num_nodes'],
            'num_edges': scenario['num_edges'],
            'avg_degree': scenario['avg_degree'],
            'execution_count': scenario['execution_count'],
            'avg_execution_time_ms': scenario['avg_execution_time_ms'],
            # Advanced features
            'network_request_count': scenario.get('network_request_count', 0),
            'external_request': scenario.get('external_request', False),
            'internal_network_access': scenario.get('internal_network_access', False),
            'access_control_check': scenario.get('access_control_check', True),
            'authorization_bypass': scenario.get('authorization_bypass', False),
            'encryption_used': scenario.get('encryption_used', True),
            'external_dependency': scenario.get('external_dependency', False),
            'dependency_verified': scenario.get('dependency_verified', True),
            'memory_unsafe': scenario.get('memory_unsafe', False),
            # Attack scores
            'ssrf_score': scenario.get('ssrf_score', 0.0),
            'access_control_score': scenario.get('access_control_score', 0.0),
            'misconfiguration_score': scenario.get('misconfiguration_score', 0.0),
            'crypto_failure_score': scenario.get('crypto_failure_score', 0.0),
            'auth_failure_score': scenario.get('auth_failure_score', 0.0),
            'supply_chain_score': scenario.get('supply_chain_score', 0.0),
            'zero_day_score': scenario.get('zero_day_score', 0.0),
            'safe_score': scenario.get('safe_score', 0.0),
        }
        
        # Make decision
        judgment = engine.judge_safety(context)
        
        # Record outcome
        decision = Decision(
            decision_id=f"adv_dec_{total_decisions}",
            decision_type=DecisionType.SECURITY,
            context=context,
            action=judgment.is_safe,
            confidence=judgment.confidence,
            timestamp=time.time()
        )
        
        # Determine if correct
        is_correct = (judgment.is_safe == scenario['expected_safe'])
        if is_correct:
            correct_decisions += 1
        
        outcome = DecisionOutcome.GOOD if is_correct else DecisionOutcome.BAD
        reward = 1.0 if is_correct else -1.0
        
        engine.record_outcome(decision, outcome, reward=reward)
        total_decisions += 1
        
        if (i + 1) % 50 == 0:
            print(f"  ✓ Processed {i+1}/{len(all_scenarios)} scenarios")
    
    train_time = time.time() - train_start
    print(f"  Training time: {train_time:.2f}s")
    
    # Get statistics
    stats = engine.get_statistics()
    
    # Save structured data
    print("\n[4/4] Saving advanced training data...")
    save_start = time.time()
    
    structured_data = []
    for i, scenario in enumerate(all_scenarios):
        structured_data.append({
            'id': f"adv_sample_{i}",
            'attack_type': scenario['attack_type'],
            'features': {
                'has_untrusted_data': scenario['has_untrusted_data'],
                'has_sanitization': scenario['has_sanitization'],
                'taint_propagation_steps': scenario['taint_propagation_steps'],
                'num_nodes': scenario['num_nodes'],
                'num_edges': scenario['num_edges'],
                'avg_degree': scenario['avg_degree'],
                'execution_count': scenario['execution_count'],
                'avg_execution_time_ms': scenario['avg_execution_time_ms'],
                'network_request_count': scenario.get('network_request_count', 0),
                'external_request': scenario.get('external_request', False),
                'internal_network_access': scenario.get('internal_network_access', False),
                'access_control_check': scenario.get('access_control_check', True),
                'authorization_bypass': scenario.get('authorization_bypass', False),
                'encryption_used': scenario.get('encryption_used', True),
                'external_dependency': scenario.get('external_dependency', False),
                'dependency_verified': scenario.get('dependency_verified', True),
                'memory_unsafe': scenario.get('memory_unsafe', False),
                'ssrf_score': scenario.get('ssrf_score', 0.0),
                'access_control_score': scenario.get('access_control_score', 0.0),
                'misconfiguration_score': scenario.get('misconfiguration_score', 0.0),
                'crypto_failure_score': scenario.get('crypto_failure_score', 0.0),
                'auth_failure_score': scenario.get('auth_failure_score', 0.0),
                'supply_chain_score': scenario.get('supply_chain_score', 0.0),
                'zero_day_score': scenario.get('zero_day_score', 0.0),
                'safe_score': scenario.get('safe_score', 0.0),
            },
            'label': 1 if not scenario['expected_safe'] else 0,
            'expected_safe': scenario['expected_safe']
        })
    
    with open('.ipl_data/advanced_training_data.json', 'w') as f:
        json.dump(structured_data, f, indent=2)
    
    print(f"  ✓ Saved {len(structured_data)} samples to .ipl_data/advanced_training_data.json")
    print(f"  Save time: {time.time() - save_start:.2f}s")
    
    # Summary
    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print("ADVANCED SECURITY TRAINING COMPLETE")
    print("=" * 70)
    print(f"Total scenarios: {len(all_scenarios)}")
    print("Attack Types Covered:")
    print("  OWASP A01: Broken Access Control (40)")
    print("  OWASP A02: Security Misconfiguration (30)")
    print("  OWASP A03: Supply Chain Failures (25)")
    print("  OWASP A04: Cryptographic Failures (30)")
    print("  OWASP A07: Authentication Failures (30)")
    print("  Emerging: SSRF (30)")
    print("  Emerging: Zero-day (20)")
    print("  Safe: Advanced Patterns (50)")
    print(f"Total decisions: {stats['total_decisions']}")
    print(f"Success rate: {stats['success_rate']:.2%}")
    print(f"Training samples: {stats['training_samples_collected']}")
    print(f"Total time: {total_time:.2f}s ({total_time/60:.2f} minutes)")
    print("=" * 70)
    
    return engine


if __name__ == "__main__":
    train_advanced_security()
