#!/usr/bin/env python3
"""
IPL Security Test Runner
Run all security tests to validate compiler-level AI intelligence
"""

import sys
import os
import subprocess

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def run_test(test_file, description):
    """Run a single security test"""
    print(f"\n{'='*70}")
    print(f"Running: {description}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
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
    
    # Test files
    test_dir = os.path.dirname(os.path.abspath(__file__))
    tests = [
        (
            os.path.join(test_dir, "test_compiler_ai_security.py"),
            "Basic Security Attack Tests"
        ),
        (
            os.path.join(test_dir, "test_user_authentication.py"),
            "User Authentication Security Tests"
        )
    ]
    
    results = []
    for test_file, description in tests:
        if os.path.exists(test_file):
            result = run_test(test_file, description)
            results.append((description, result))
        else:
            print(f"⚠️  Test file not found: {test_file}")
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