"""
Verify CodeBERT-only security changes (no rule-based fallback).
This test verifies the code changes without requiring torch to be installed.
"""
import re

def verify_runtime_changes():
    """Verify runtime.py uses CodeBERT instead of SecurityEngine."""
    print("=" * 70)
    print("Verifying runtime.py changes")
    print("=" * 70)
    
    with open('runtime.py', 'r') as f:
        content = f.read()
    
    # Check that SecurityEngine is not imported
    if 'from security_engine import SecurityEngine' in content:
        print("❌ FAIL: SecurityEngine still imported in runtime.py")
        return False
    else:
        print("✅ PASS: SecurityEngine not imported in runtime.py")
    
    # Check that CodeBERT firewall is imported
    if 'from codebert_firewall import IntelligentFirewall as CodeBERTFirewall' in content:
        print("✅ PASS: CodeBERT firewall imported in runtime.py")
    else:
        print("❌ FAIL: CodeBERT firewall not imported in runtime.py")
        return False
    
    # Check that self.security_engine is not used
    if 'self.security_engine' in content:
        print("❌ FAIL: self.security_engine still used in runtime.py")
        return False
    else:
        print("✅ PASS: self.security_engine not used in runtime.py")
    
    # Check that self.codebert_firewall is used
    if 'self.codebert_firewall' in content:
        print("✅ PASS: self.codebert_firewall used in runtime.py")
    else:
        print("❌ FAIL: self.codebert_firewall not used in runtime.py")
        return False
    
    # Check that sanitization functions use CodeBERT
    codebert_checks = content.count('self.codebert_firewall.check_code')
    if codebert_checks >= 5:  # Should have at least 5 sanitization functions
        print(f"✅ PASS: CodeBERT check_code called {codebert_checks} times in sanitization functions")
    else:
        print(f"❌ FAIL: CodeBERT check_code only called {codebert_checks} times (expected >= 5)")
        return False
    
    print("\n" + "=" * 70)
    print("runtime.py verification PASSED")
    print("=" * 70)
    return True

def verify_bytecode_changes():
    """Verify bytecode.py uses CodeBERT instead of SecurityEngine."""
    print("\n" + "=" * 70)
    print("Verifying bytecode.py changes")
    print("=" * 70)
    
    with open('bytecode.py', 'r') as f:
        content = f.read()
    
    # Check that SecurityEngine is not imported in sanitization functions
    if 'from security_engine import SecurityEngine' in content:
        print("❌ FAIL: SecurityEngine still imported in bytecode.py")
        return False
    else:
        print("✅ PASS: SecurityEngine not imported in bytecode.py")
    
    # Check that CodeBERT firewall is initialized
    if 'self.codebert_firewall = CodeBERTFirewall()' in content:
        print("✅ PASS: CodeBERT firewall initialized in bytecode.py")
    else:
        print("❌ FAIL: CodeBERT firewall not initialized in bytecode.py")
        return False
    
    # Check that sanitization opcodes use CodeBERT
    codebert_checks = content.count('self.codebert_firewall.check_code')
    if codebert_checks >= 5:  # Should have at least 5 sanitization opcodes
        print(f"✅ PASS: CodeBERT check_code called {codebert_checks} times in bytecode opcodes")
    else:
        print(f"❌ FAIL: CodeBERT check_code only called {codebert_checks} times (expected >= 5)")
        return False
    
    # Check that rule-based sanitization is removed
    if 'SecurityEngine.sanitize_for_sql' in content:
        print("❌ FAIL: SecurityEngine.sanitize_for_sql still used in bytecode.py")
        return False
    else:
        print("✅ PASS: SecurityEngine.sanitize_for_sql not used in bytecode.py")
    
    print("\n" + "=" * 70)
    print("bytecode.py verification PASSED")
    print("=" * 70)
    return True

def verify_compiler_integration():
    """Verify compiler.py still uses CodeBERT."""
    print("\n" + "=" * 70)
    print("Verifying compiler.py CodeBERT integration")
    print("=" * 70)
    
    with open('compiler.py', 'r') as f:
        content = f.read()
    
    # Check that IntelligentFirewall uses CodeBERT
    if 'from codebert_firewall import IntelligentFirewall as CodeBERTFirewall' in content:
        print("✅ PASS: CodeBERT firewall imported in compiler.py")
    else:
        print("❌ FAIL: CodeBERT firewall not imported in compiler.py")
        return False
    
    # Check that firewall uses CodeBERT
    if 'self.codebert_firewall = CodeBERTFirewall(model_path)' in content:
        print("✅ PASS: IntelligentFirewall uses CodeBERT in compiler.py")
    else:
        print("❌ FAIL: IntelligentFirewall does not use CodeBERT in compiler.py")
        return False
    
    # Check that verify_ast_node uses CodeBERT
    if 'self.codebert_firewall.verify_ast_node' in content:
        print("✅ PASS: verify_ast_node uses CodeBERT in compiler.py")
    else:
        print("❌ FAIL: verify_ast_node does not use CodeBERT in compiler.py")
        return False
    
    print("\n" + "=" * 70)
    print("compiler.py verification PASSED")
    print("=" * 70)
    return True

def main():
    """Run all verification tests."""
    print("\n" + "=" * 70)
    print("CODEBERT-ONLY SECURITY VERIFICATION")
    print("Verifying that all security decisions are made by CodeBERT")
    print("(no rule-based fallback)")
    print("=" * 70 + "\n")
    
    results = []
    results.append(("runtime.py", verify_runtime_changes()))
    results.append(("bytecode.py", verify_bytecode_changes()))
    results.append(("compiler.py", verify_compiler_integration()))
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    all_passed = True
    for file_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{file_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 70)
    if all_passed:
        print("ALL VERIFICATIONS PASSED")
        print("Security pipeline is now CodeBERT-only (no rule-based fallback)")
    else:
        print("SOME VERIFICATIONS FAILED")
        print("Please review the failures above")
    print("=" * 70)
    
    return all_passed

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
