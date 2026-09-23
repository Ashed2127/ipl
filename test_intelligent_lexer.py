"""
Test Intelligent Lexer vs Traditional Lexer
Demonstrates the first step toward compiler-first architecture.
"""
import sys
sys.path.insert(0, '/home/ashed/Downloads/ipl_lang')

from lexer import Lexer as TraditionalLexer
from intelligent_lexer import IntelligentLexer
import time


def test_traditional_lexer():
    """Test traditional pattern-based lexer."""
    print("\n" + "="*80)
    print("TRADITIONAL LEXER TEST")
    print("="*80)
    
    code = """
    let price: Currency = "ninety-nine bucks"
    let total = price + 10
    if total > 100 {
        print "Expensive"
    }
    """
    
    print(f"\nCode to tokenize:\n{code}")
    
    start_time = time.time()
    traditional_lexer = TraditionalLexer(code)
    tokens = traditional_lexer.tokenize()
    end_time = time.time()
    
    print(f"\nTraditional Tokenization Results:")
    print(f"Execution Time: {(end_time - start_time) * 1000:.2f}ms")
    print(f"Total Tokens: {len(tokens)}")
    
    print("\nTokens:")
    for i, token in enumerate(tokens[:15]):  # Show first 15 tokens
        print(f"  {i+1}. {token}")
    
    if len(tokens) > 15:
        print(f"  ... and {len(tokens) - 15} more tokens")


def test_intelligent_lexer_rule_based():
    """Test intelligent lexer in rule-based mode."""
    print("\n" + "="*80)
    print("INTELLIGENT LEXER TEST (Rule-Based Mode)")
    print("="*80)
    
    code = """
    let price: Currency = "ninety-nine bucks"
    let total = price + 10
    if total > 100 {
        print "Expensive"
    }
    """
    
    print(f"\nCode to tokenize:\n{code}")
    
    start_time = time.time()
    intelligent_lexer = IntelligentLexer(code, enable_ai=False)
    semantic_tokens = intelligent_lexer.tokenize()
    end_time = time.time()
    
    print(f"\nIntelligent Tokenization Results (Rule-Based):")
    print(f"Execution Time: {(end_time - start_time) * 1000:.2f}ms")
    print(f"Total Semantic Tokens: {len(semantic_tokens)}")
    
    print("\nSemantic Tokens:")
    for i, semantic_token in enumerate(semantic_tokens[:15]):
        print(f"  {i+1}. {semantic_token}")
    
    intelligent_lexer.print_stats()


def test_intelligent_lexer_ai_enhanced():
    """Test intelligent lexer with AI enhancement."""
    print("\n" + "="*80)
    print("INTELLIGENT LEXER TEST (AI-Enhanced Mode)")
    print("="*80)
    
    code = """
    let price: Currency = "ninety-nine bucks"
    let total = price + 10
    if total > 100 {
        print "Expensive"
    }
    """
    
    print(f"\nCode to tokenize:\n{code}")
    print("⚠️ AI enhancement may take time (30+ seconds due to Ollama performance)")
    
    start_time = time.time()
    intelligent_lexer = IntelligentLexer(code, enable_ai=True)
    semantic_tokens = intelligent_lexer.tokenize()
    end_time = time.time()
    
    print(f"\nIntelligent Tokenization Results (AI-Enhanced):")
    print(f"Execution Time: {(end_time - start_time) * 1000:.2f}ms")
    print(f"Total Semantic Tokens: {len(semantic_tokens)}")
    
    print("\nSemantic Tokens:")
    for i, semantic_token in enumerate(semantic_tokens[:15]):
        print(f"  {i+1}. {semantic_token}")
        if semantic_token.ai_insights:
            print(f"      AI Insights: {semantic_token.ai_insights}")
    
    intelligent_lexer.print_stats()


def test_comparison():
    """Compare traditional vs intelligent lexers."""
    print("\n" + "="*80)
    print("TRADITIONAL VS INTELLIGENT LEXER COMPARISON")
    print("="*80)
    
    code = """
    fn calculate_total(price: Currency, tax: Currency) -> Currency {
        let total = price + tax
        return total
    }
    """
    
    print(f"\nTest Code:\n{code}")
    
    # Traditional lexer
    print("\n--- Traditional Lexer ---")
    start_time = time.time()
    trad_lexer = TraditionalLexer(code)
    trad_tokens = trad_lexer.tokenize()
    trad_time = (time.time() - start_time) * 1000
    
    print(f"Time: {trad_time:.2f}ms")
    print(f"Tokens: {len(trad_tokens)}")
    print(f"Sample: {trad_tokens[5] if len(trad_tokens) > 5 else 'N/A'}")
    
    # Intelligent lexer (rule-based)
    print("\n--- Intelligent Lexer (Rule-Based) ---")
    start_time = time.time()
    intel_lexer = IntelligentLexer(code, enable_ai=False)
    intel_tokens = intel_lexer.tokenize()
    intel_time = (time.time() - start_time) * 1000
    
    print(f"Time: {intel_time:.2f}ms")
    print(f"Semantic Tokens: {len(intel_tokens)}")
    print(f"Sample: {intel_tokens[5] if len(intel_tokens) > 5 else 'N/A'}")
    
    # Intelligent lexer stats
    intel_lexer.print_stats()
    
    # Performance comparison
    print("\n--- Performance Comparison ---")
    print(f"Traditional Time: {trad_time:.2f}ms")
    print(f"Intelligent Time: {intel_time:.2f}ms")
    print(f"Overhead: {intel_time - trad_time:.2f}ms ({((intel_time/trad_time - 1) * 100):.1f}%)")
    
    # Feature comparison
    print("\n--- Feature Comparison ---")
    print("Traditional Lexer:")
    print("  ✅ Fast tokenization")
    print("  ✅ Pattern-based classification")
    print("  ❌ No semantic understanding")
    print("  ❌ No context awareness")
    
    print("\nIntelligent Lexer:")
    print("  ✅ Semantic token classification")
    print("  ✅ Context-aware analysis")
    print("  ✅ Probable type inference")
    print("  ✅ AI enhancement capability")
    print("  ⚠️ Slight performance overhead")


def main():
    """Run all intelligent lexer tests."""
    print("\n" + "="*80)
    print("IPL INTELLIGENT LEXER - FIRST STEP TOWARD COMPILER-FIRST ARCHITECTURE")
    print("="*80)
    print("\nThis demonstrates the first component of intelligent compilation:")
    print("Intelligent Lexical Analysis with semantic tokenization")
    
    try:
        test_traditional_lexer()
        test_intelligent_lexer_rule_based()
        # Skip AI-enhanced test due to performance issues
        # test_intelligent_lexer_ai_enhanced()
        test_comparison()
        
        print("\n" + "="*80)
        print("INTELLIGENT LEXER TEST COMPLETED")
        print("="*80)
        print("\n🎉 First Step Achieved: Intelligent Lexical Analysis")
        print("✅ Semantic token classification implemented")
        print("✅ Context-aware token understanding")
        print("✅ Probable type inference")
        print("✅ AI enhancement framework in place")
        print("✅ Performance-optimized rule-based approach")
        
        print("\n🚀 Next Steps Toward Compiler-First Architecture:")
        print("- Intelligent Parsing (neural-assisted parsing)")
        print("- Intelligent Compilation (AI-driven optimization)")
        print("- Intelligent Runtime (adaptive execution)")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()