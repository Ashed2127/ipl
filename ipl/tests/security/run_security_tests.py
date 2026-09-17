#!/usr/bin/env python3
"""
IPL Security Test Runner
Run all security tests to validate compiler-level AI intelligence
"""

import sys
import os
import subprocess

def run_test(test_file, description, project_root):
    """Run a single security test"""
    print(f"\n{'='*70}")
    print(f"Running: {description}")
    print(f"{'='*70}")
    
    try:
        # Run from project root directory
        result = subprocess.run(
            [sys.executable, test_file],
            cwd=project_root,
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    """Run all security tests"""
    print("\n" + "="*70)
    print("IPL Compiler-Level AI Security Test Suite")
    print("Testing intelligence for every architecture change")
    print("="*70)
    
    # Get project root (go up 4 levels from ipl/tests/security to project root)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    # Test files (relative to project root)
    tests = [
        (
            "ipl/tests/security/test_compiler_ai_security.py",
            "Basic Security Attack Tests"
        ),
        (
            "ipl/tests/security/test_user_authentication.py",
            "User Authentication Security Tests"
        ),
        (
            "ipl/tests/security/test_advanced_security_attacks.py",
            "Advanced Security Attack Tests"
        )
    ]
    
    results = []
    for test_file, description in tests:
        # Check if file exists relative to project root
        full_path = os.path.join(project_root, test_file)
        if os.path.exists(full_path):
            result = run_test(test_file, description, project_root)
            results.append((description, result))
        else:
            print(f"⚠️  Test file not found: {full_path}")
            results.append((description, False))
    
    # Print summary
    print("\n" + "="*70)
    print("SECURITY TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for description, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {description}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All security tests passed! IPL compiler-level AI is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())