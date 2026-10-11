#!/usr/bin/env python3
"""
Test script for multi-class CodeBERT security model
Tests the model's ability to classify specific vulnerability types
"""
from codebert_firewall import MultiClassIntelligentFirewall, IntelligentFirewall
import sys

def test_multiclass_firewall():
    """Test the multi-class CodeBERT firewall with various vulnerability types"""
    print("=" * 70)
    print("Testing Multi-class CodeBERT Intelligent Firewall")
    print("=" * 70)
    
    # Initialize firewall (will use pretrained if no model path provided)
    model_path = ".ipl_data/codebert_multiclass_model.pt"
    try:
        firewall = MultiClassIntelligentFirewall(model_path=model_path)
        print(f"Using fine-tuned multi-class model from: {model_path}")
    except Exception as e:
        print(f"Could not load fine-tuned model: {e}")
        print("Falling back to pretrained model (not fine-tuned)")
        firewall = MultiClassIntelligentFirewall()
    
    # Test cases covering different vulnerability types
    test_cases = [
        # SQL Injection (should be class 0)
        ("SELECT * FROM users WHERE id = '" + "' OR '1'='1", "SQL Injection - Basic", 0),
        ("admin' OR '1'='1", "SQL Injection - Tautology", 0),
        ("' UNION SELECT password FROM users--", "SQL Injection - Union-based", 0),
        
        # XSS (should be class 1)
        ("<script>alert('XSS')</script>", "XSS - Script tag", 1),
        ("<img src=x onerror=alert('XSS')>", "XSS - Image onerror", 1),
        ("javascript:alert('XSS')", "XSS - JavaScript protocol", 1),
        
        # Command Injection (should be class 2)
        ("; cat /etc/passwd", "Command Injection - Semicolon", 2),
        ("| ls -la", "Command Injection - Pipe", 2),
        ("&& whoami", "Command Injection - AND", 2),
        
        # Path Traversal (should be class 3)
        ("../../../etc/passwd", "Path Traversal - Unix", 3),
        ("..\\..\\..\\windows\\system32", "Path Traversal - Windows", 3),
        ("/etc/passwd", "Path Traversal - Direct", 3),
        
        # Dangerous Functions (should be class 4)
        ("eval(malicious_code)", "Dangerous Function - eval", 4),
        ("exec(user_input)", "Dangerous Function - exec", 4),
        ("system(user_command)", "Dangerous Function - system", 4),
        
        # Other Vulnerabilities (should be class 5)
        ("DROP TABLE users", "Other - SQL Destructive", 5),
        ("onerror=alert(1)", "Other - Event handler", 5),
        
        # Safe Code (should be class 6)
        ("SELECT * FROM users WHERE id = ?", "Safe - Parameterized Query", 6),
        ("<div>Safe content</div>", "Safe - HTML", 6),
        ("def calculate(x, y): return x + y", "Safe - Python", 6),
        ("Hello World", "Safe - String", 6),
    ]
    
    correct = 0
    total = len(test_cases)
    
    for code, description, expected_class in test_cases:
        vuln_type, confidence, reasoning = firewall.check_code(code)
        expected_type = firewall.VULN_TYPES[expected_class]
        
        is_correct = vuln_type == expected_type
        if is_correct:
            correct += 1
            status = "✅ CORRECT"
        else:
            status = f"❌ WRONG (expected: {expected_type})"
        
        print(f"\n{description}:")
        print(f"  Code: {code[:60]}...")
        print(f"  Predicted: {vuln_type}")
        print(f"  Expected: {expected_type}")
        print(f"  Status: {status}")
        print(f"  Confidence: {confidence:.2f}")
        print(f"  Reasoning: {reasoning}")
    
    accuracy = (correct / total) * 100
    print("\n" + "=" * 70)
    print(f"Test Complete: {correct}/{total} correct ({accuracy:.1f}% accuracy)")
    print("=" * 70)
    
    return accuracy

def test_binary_vs_multiclass():
    """Compare binary and multi-class firewalls"""
    print("\n" + "=" * 70)
    print("Comparing Binary vs Multi-class Firewalls")
    print("=" * 70)
    
    # Binary firewall
    print("\n--- Binary Firewall (Safe/Unsafe) ---")
    binary_fw = IntelligentFirewall()
    
    # Multi-class firewall
    print("\n--- Multi-class Firewall (Specific Types) ---")
    multiclass_fw = MultiClassIntelligentFirewall()
    
    test_code = "SELECT * FROM users WHERE id = '" + "' OR '1'='1"
    
    print(f"\nTest code: {test_code}")
    
    # Binary prediction
    is_safe, confidence, reasoning = binary_fw.check_code(test_code)
    print(f"\nBinary Prediction:")
    print(f"  Safe: {is_safe}")
    print(f"  Confidence: {confidence:.2f}")
    print(f"  Reasoning: {reasoning}")
    
    # Multi-class prediction
    vuln_type, confidence, reasoning = multiclass_fw.check_code(test_code)
    print(f"\nMulti-class Prediction:")
    print(f"  Type: {vuln_type}")
    print(f"  Confidence: {confidence:.2f}")
    print(f"  Reasoning: {reasoning}")

if __name__ == "__main__":
    print("Testing Multi-class CodeBERT Security Model\n")
    
    # Test multi-class firewall
    accuracy = test_multiclass_firewall()
    
    # Compare with binary
    test_binary_vs_multiclass()
    
    print("\n\n✅ All tests complete!")
