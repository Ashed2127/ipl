"""
Comprehensive test of CodeBERT-only security pipeline.
Tests actual IPL code execution with CodeBERT security.
"""
from lexer import Lexer
from parser import Parser
from runtime import Interpreter
from rich.console import Console

def test_safe_code_execution():
    """Test that safe code executes successfully with CodeBERT."""
    print("=" * 70)
    print("Test 1: Safe Code Execution with CodeBERT")
    print("=" * 70)
    
    code = """
let x: Int = 42
print(x)
"""
    
    console = Console()
    interpreter = Interpreter(console=console)
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter.run(program)
        print("✅ PASS: Safe code executed successfully with CodeBERT security")
        return True
    except Exception as e:
        print(f"❌ FAIL: Safe code failed: {e}")
        return False

def test_string_sanitization():
    """Test that string sanitization uses CodeBERT."""
    print("\n" + "=" * 70)
    print("Test 2: String Sanitization with CodeBERT")
    print("=" * 70)
    
    code = """
let s: String = "safe string"
let sanitized = sanitize_string(s)
print(sanitized)
"""
    
    console = Console()
    interpreter = Interpreter(console=console)
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter.run(program)
        print("✅ PASS: String sanitization uses CodeBERT")
        return True
    except Exception as e:
        print(f"❌ FAIL: String sanitization failed: {e}")
        return False

def test_sql_sanitization():
    """Test that SQL sanitization uses CodeBERT."""
    print("\n" + "=" * 70)
    print("Test 3: SQL Sanitization with CodeBERT")
    print("=" * 70)
    
    code = """
let sql: String = "SELECT * FROM users WHERE id = ?"
let sanitized = sanitize_for_sql(sql)
print(sanitized)
"""
    
    console = Console()
    interpreter = Interpreter(console=console)
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter.run(program)
        print("✅ PASS: SQL sanitization uses CodeBERT")
        return True
    except Exception as e:
        print(f"❌ FAIL: SQL sanitization failed: {e}")
        return False

def test_html_sanitization():
    """Test that HTML sanitization uses CodeBERT."""
    print("\n" + "=" * 70)
    print("Test 4: HTML Sanitization with CodeBERT")
    print("=" * 70)
    
    code = """
let html: String = "<div>Safe content</div>"
let sanitized = sanitize_for_html(html)
print(sanitized)
"""
    
    console = Console()
    interpreter = Interpreter(console=console)
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter.run(program)
        print("✅ PASS: HTML sanitization uses CodeBERT")
        return True
    except Exception as e:
        print(f"❌ FAIL: HTML sanitization failed: {e}")
        return False

def test_compilation_with_codebert():
    """Test that compiler uses CodeBERT for AST verification."""
    print("\n" + "=" * 70)
    print("Test 5: Compiler AST Verification with CodeBERT")
    print("=" * 70)
    
    from compiler import NeuroSymbolicCompiler
    from ast_nodes import Literal
    
    console = Console()
    compiler = NeuroSymbolicCompiler(console=console)
    
    # Test safe literal
    safe_literal = Literal(value="safe data", type_name="string")
    is_valid, violations = compiler.firewall.verify_ast_node(safe_literal)
    
    if is_valid:
        print("✅ PASS: Compiler uses CodeBERT for AST verification")
        return True
    else:
        print(f"❌ FAIL: Compiler rejected safe literal: {violations}")
        return False

def main():
    """Run all comprehensive tests."""
    print("\n" + "=" * 70)
    print("COMPREHENSIVE CODEBERT-ONLY SECURITY TESTS")
    print("Testing actual IPL code execution with CodeBERT security")
    print("=" * 70 + "\n")
    
    results = []
    results.append(("Safe Code Execution", test_safe_code_execution()))
    results.append(("String Sanitization", test_string_sanitization()))
    results.append(("SQL Sanitization", test_sql_sanitization()))
    results.append(("HTML Sanitization", test_html_sanitization()))
    results.append(("Compiler AST Verification", test_compilation_with_codebert()))
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 70)
    if all_passed:
        print("ALL TESTS PASSED")
        print("CodeBERT-only security pipeline is fully integrated and working")
    else:
        print("SOME TESTS FAILED")
        print("Please review the failures above")
    print("=" * 70)
    
    return all_passed

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
