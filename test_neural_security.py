"""
Test neural security analysis integration with Ollama
"""
from security_engine import SecurityEngine

def test_neural_sql_injection():
    """Test neural detection of SQL injection"""
    print("Testing neural SQL injection detection...")
    
    code = "let user_input = 'admin OR 1=1'; db_write('users', user_input);"
    result = SecurityEngine.neural_vulnerability_detection(code)
    
    print(f"SQL injection detected: {result['sql_injection']}")
    print(f"Neural analysis available: {result['neural_analysis_available']}")
    if result.get('analysis_text'):
        print(f"Analysis: {result['analysis_text'][:200]}...")
    print()

def test_neural_xss():
    """Test neural detection of XSS"""
    print("Testing neural XSS detection...")
    
    code = "let user_input = '<script>alert(1)</script>'; html_render(user_input);"
    result = SecurityEngine.neural_vulnerability_detection(code)
    
    print(f"XSS detected: {result['xss']}")
    print(f"Neural analysis available: {result['neural_analysis_available']}")
    if result.get('analysis_text'):
        print(f"Analysis: {result['analysis_text'][:200]}...")
    print()

def test_execution_safety_with_neural():
    """Test execution safety check with neural analysis"""
    print("Testing execution safety with neural analysis...")
    
    code = "let user_input = 'admin OR 1=1'; db_write('users', user_input);"
    is_safe, warnings = SecurityEngine.check_execution_safety(code, use_neural=True)
    
    print(f"Is safe: {is_safe}")
    print("Warnings:")
    for warning in warnings:
        print(f"  - {warning}")
    print()

def test_safe_code():
    """Test neural analysis on safe code"""
    print("Testing neural analysis on safe code...")
    
    code = "let user_input = 'admin'; let safe = sanitize_for_sql(user_input); db_write('users', safe);"
    result = SecurityEngine.neural_vulnerability_detection(code)
    
    print(f"SQL injection detected: {result['sql_injection']}")
    print(f"XSS detected: {result['xss']}")
    print(f"Neural analysis available: {result['neural_analysis_available']}")
    if result.get('analysis_text'):
        print(f"Analysis: {result['analysis_text'][:200]}...")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("Neural Security Analysis Tests")
    print("=" * 60)
    print()
    
    test_neural_sql_injection()
    test_neural_xss()
    test_execution_safety_with_neural()
    test_safe_code()
    
    print("=" * 60)
    print("Tests completed")
    print("=" * 60)
