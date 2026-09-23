"""
Simple test for the Neural Compiler - Compiler-First Architecture
Basic functionality test
"""

try:
    from intelligent_lexer import CompilerFirstLexer
    print("✅ Successfully imported CompilerFirstLexer")
    
    # Test basic lexer functionality
    test_code = """
    let user_age = 25
    let user_name = "John"
    let price = 19.99
    """
    
    config = {
        "enable_neural_analysis": True,
        "enable_security_analysis": True,
        "enable_learning": True,
        "confidence_threshold": 0.7
    }
    
    lexer = CompilerFirstLexer(test_code, config)
    print("✅ Successfully created CompilerFirstLexer")
    
    analysis = lexer.analyze_source()
    print("✅ Successfully performed lexical analysis")
    
    print(f"Tokens found: {len(analysis.get('tokens', []))}")
    print(f"Neural analysis enabled: {analysis.get('neural_analysis_enabled', False)}")
    print(f"Security analysis: {analysis.get('security_summary', {}).get('security_analysis', 'N/A')}")
    
    print("\n🎉 Basic intelligent lexer test PASSED!")
    
except Exception as e:
    print(f"❌ Test failed with error: {e}")
    import traceback
    traceback.print_exc()