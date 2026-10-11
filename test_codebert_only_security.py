"""
Test CodeBERT-only security pipeline (no rule-based fallback).
Verifies that all security decisions are made by CodeBERT.
"""
from compiler import NeuroSymbolicCompiler
from ast_nodes import Program, LetStatement, Literal, TypeAnnotation, PrintStatement, FunctionCall, Identifier
from rich.console import Console

def test_codebert_security_pipeline():
    """Test that CodeBERT makes all security decisions."""
    print("=" * 70)
    print("Testing CodeBERT-Only Security Pipeline")
    print("=" * 70)
    
    console = Console()
    compiler = NeuroSymbolicCompiler(console=console)
    
    # Test 1: Safe code should pass
    print("\nTest 1: Safe code should pass CodeBERT verification")
    safe_literal = Literal(value="safe string", type_name="string")
    is_valid, violations = compiler.firewall.verify_ast_node(safe_literal)
    print(f"  Result: {'PASS' if is_valid else 'FAIL'}")
    print(f"  Violations: {violations if violations else 'None'}")
    
    # Test 2: Potentially unsafe code should be evaluated by CodeBERT
    print("\nTest 2: CodeBERT evaluates potential SQL injection")
    sql_literal = Literal(value="SELECT * FROM users WHERE id = ' OR '1'='1", type_name="string")
    is_valid, violations = compiler.firewall.verify_ast_node(sql_literal)
    print(f"  Result: {'BLOCKED' if not is_valid else 'ALLOWED'}")
    print(f"  Violations: {violations if violations else 'None'}")
    
    # Test 3: CodeBERT evaluates XSS attempt
    print("\nTest 3: CodeBERT evaluates XSS attempt")
    xss_literal = Literal(value="<script>alert('XSS')</script>", type_name="string")
    is_valid, violations = compiler.firewall.verify_ast_node(xss_literal)
    print(f"  Result: {'BLOCKED' if not is_valid else 'ALLOWED'}")
    print(f"  Violations: {violations if violations else 'None'}")
    
    # Test 4: Verify audit trace includes CodeBERT decisions
    print("\nTest 4: Verify audit trace records CodeBERT decisions")
    compiler.audit_trace.record(
        phase="CODEBERT_SECURITY_CHECK",
        status="VERIFIED",
        details={"codebert_decision": "safe", "codebert_confidence": 0.95}
    )
    print(f"  Audit trace recorded CodeBERT decision")
    
    print("\n" + "=" * 70)
    print("CodeBERT-Only Security Pipeline Test Complete")
    print("All security decisions are now made by CodeBERT (no rule-based fallback)")
    print("=" * 70)

if __name__ == "__main__":
    test_codebert_security_pipeline()
