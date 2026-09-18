#!/usr/bin/env python3
from ipl.compiler.compiler_ai_providers import OllamaCompilerProvider

provider = OllamaCompilerProvider(model_name='qwen2.5-coder:0.5b')
print('Ollama available:', provider.is_available())

if provider.is_available():
    test_patterns = {
        'sql_indicators': ['Line 1: SELECT * FROM users WHERE username = input'],
        'xss_indicators': ['Line 2: print(script tag with alert']
    }
    result = provider.analyze_security_deep(test_patterns, 'compilation')
    print('AI Security Analysis Result:', result)
else:
    print('Ollama not available, using fallback security analysis')