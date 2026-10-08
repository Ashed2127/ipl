"""
Test CodeBERT integration in IPL compiler
"""
import sys
sys.path.insert(0, '.')

from compiler import NeuroSymbolicCompiler
from ast_nodes import IntentExpr, TypeAnnotation

def test_codebert_compiler():
    """Test compiler with CodeBERT firewall"""
    print("=" * 70)
    print("Testing CodeBERT Integration in IPL Compiler")
    print("=" * 70)
    
    # Initialize compiler (should load CodeBERT)
    print("\nInitializing compiler...")
    compiler = NeuroSymbolicCompiler()
    
    # Test with a simple intent
    print("\nTest 1: Simple integer value")
    intent = IntentExpr(
        intent_prompt="user age is 25",
        target_type=TypeAnnotation(name="Int")
    )
    
    try:
        result_ast, taint_tag = compiler.compile_intent_node(intent)
        print(f"✅ Compilation successful")
        print(f"   Result: {result_ast}")
        print(f"   Taint: {taint_tag.level}")
    except Exception as e:
        print(f"❌ Compilation failed: {e}")
    
    # Test with potential SQL injection
    print("\nTest 2: SQL-like pattern")
    intent2 = IntentExpr(
        intent_prompt="SELECT * FROM users WHERE id = user_input",
        target_type=None
    )
    
    try:
        result_ast, taint_tag = compiler.compile_intent_node(intent2)
        print(f"✅ Compilation successful")
        print(f"   Result: {result_ast}")
        print(f"   Taint: {taint_tag.level}")
    except Exception as e:
        print(f"❌ Compilation failed: {e}")
    
    print("\n" + "=" * 70)
    print("Test Complete")
    print("=" * 70)

if __name__ == "__main__":
    test_codebert_compiler()
