# Qwen2.5-Coder:0.5B Integration Guide for IPL

## Prerequisites

### 1. Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull Qwen2.5-Coder:0.5B Model
```bash
ollama pull qwen2.5-coder:0.5b
```

### 3. Verify Installation
```bash
ollama list
# Should show: qwen2.5-coder:0.5b
```

## Configuration Methods

### Method 1: Environment Variables (Recommended)
Set these environment variables before running IPL:

```bash
export IPL_OLLAMA_ENDPOINT="http://localhost:11434"
export IPL_TIER3_MODEL="qwen2.5-coder:0.5b"
```

### Method 2: Command Line Arguments
```bash
# Run IPL file with Qwen2.5-Coder
python -m ipl run script.ipl --tier3-model qwen2.5-coder:0.5b

# With custom Ollama endpoint
python -m ipl run script.ipl --tier3-model qwen2.5-coder:0.5b --ollama-endpoint http://localhost:11434
```

### Method 3: Python API Integration
```python
from ipl.compiler.compiler_ai_providers import OllamaCompilerProvider
from ipl import IPLCompiler

# Configure Qwen2.5-Coder provider
ai_provider = OllamaCompilerProvider(
    model_name="qwen2.5-coder:0.5b",
    endpoint="http://localhost:11434"
)

# Check if available
if ai_provider.is_available():
    print("✓ Qwen2.5-Coder is available")
    
    # Create compiler with AI provider
    compiler = IPLCompiler(ai_provider=ai_provider)
    
    # Use for compilation
    compiler.run("your_script.ipl")
else:
    print("✗ Qwen2.5-Coder not available")
```

## Usage Examples

### Example 1: Basic IPL Script with AI Analysis
Create a file `example.ipl`:
```ipl
let message: String = "Hello, IPL!"
let count: Int = 42
print(message, count)
```

Run with Qwen2.5-Coder:
```bash
python -m ipl run example.ipl --tier3-model qwen2.5-coder:0.5b --show-audit
```

### Example 2: Security Analysis
Create a file `security_test.ipl`:
```ipl
let user_input: String = sanitize(trusted("user data"))
print(user_input)
```

Run with security analysis:
```bash
python -m ipl run security_test.ipl --tier3-model qwen2.5-coder:0.5b --show-audit
```

The AI will analyze the code for security vulnerabilities through the enhanced system prompt.

### Example 3: Python API for Compiler Tasks
```python
from ipl.compiler.compiler_ai_providers import OllamaCompilerProvider

# Initialize provider
provider = OllamaCompilerProvider(model_name="qwen2.5-coder:0.5b")

if provider.is_available():
    # Semantic Analysis
    ast_data = {
        "type": "Program",
        "statements": [
            {"type": "LetStatement", "name": "x", "value": {"type": "Literal", "value": 42}}
        ]
    }
    semantic_result = provider.analyze_semantics(ast_data, "type_inference")
    print("Semantic Analysis:", semantic_result)
    
    # Security Analysis
    code_patterns = {
        "functions": ["print", "sanitize"],
        "variables": ["user_input"]
    }
    security_result = provider.analyze_security_deep(code_patterns, "user_input_processing")
    print("Security Analysis:", security_result)
    
    # Optimization Suggestions
    code = "let x: Int = 0; for i in 1..10 { x = x + i }"
    optimizations = provider.suggest_transformations(code, ["performance", "memory"])
    print("Optimizations:", optimizations)
```

### Example 4: Error Analysis and Fix Suggestions
```python
from ipl.compiler.compiler_ai_providers import OllamaCompilerProvider

provider = OllamaCompilerProvider(model_name="qwen2.5-coder:0.5b")

if provider.is_available():
    # Simulate compilation error
    error_context = {
        "error_type": "TypeMismatch",
        "line": 5,
        "expected_type": "Int",
        "actual_type": "String",
        "code_snippet": 'let x: Int = "hello"'
    }
    
    error_analysis = provider.analyze_compilation_error(error_context)
    print("Error Analysis:", error_analysis)
    # Will provide specific fix suggestions based on IPL's type system
```

### Example 5: Complex Type Inference
```python
from ipl.compiler.compiler_ai_providers import OllamaCompilerProvider

provider = OllamaCompilerProvider(model_name="qwen2.5-coder:0.5b")

if provider.is_available():
    code_context = {
        "variables": {
            "x": {"type": "Int", "value": 42},
            "y": {"type": "Float", "value": 3.14}
        },
        "operations": ["addition", "comparison"]
    }
    
    type_inference = provider.infer_complex_types(code_context)
    print("Type Inference:", type_inference)
    # Will infer complex type relationships within IPL's type system
```

## CLI Usage with AI Features

### Run with AI Statistics
```bash
python -m ipl run script.ipl --tier3-model qwen2.5-coder:0.5b --show-audit
```

This will show:
- Cryptographic verified audit trace
- Hierarchical AI engine statistics
- Token usage and costs
- Cache performance

### Disable AI if Needed
```bash
python -m ipl run script.ipl --no-hierarchical-ai
```

### Interactive REPL with AI
```bash
python -m ipl repl --tier3-model qwen2.5-coder:0.5b
```

## Integration with Hierarchical AI Engine

The Qwen2.5-Coder model is integrated as the Tier 3 reasoning model in IPL's hierarchical AI architecture:

```python
from ipl.hierarchical_ai_engine import HierarchicalAIEngine

# Initialize with Qwen2.5-Coder
ai_engine = HierarchicalAIEngine(
    ollama_endpoint="http://localhost:11434",
    tier3_model="qwen2.5-coder:0.5b"
)

# The engine will automatically use Qwen2.5-Coder for complex reasoning tasks
# while using faster embedded models for simple pattern matching
```

## Model Behavior Configuration

### Temperature Settings
The model uses conservative settings for deterministic compilation:
- Temperature: 0.3 (for more predictable outputs)
- Max tokens: 500-800 (to prevent excessive generation)

### Timeout Settings
- API timeout: 30 seconds (prevents hanging)
- Connection timeout: 10 seconds (quick failure detection)

## Troubleshooting

### Model Not Available
```bash
# Check Ollama status
ollama list

# Restart Ollama if needed
systemctl restart ollama  # Linux
# or restart the Ollama application

# Pull model again if missing
ollama pull qwen2.5-coder:0.5b
```

### Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Verify endpoint
export IPL_OLLAMA_ENDPOINT="http://localhost:11434"
```

### Slow Performance
- Qwen2.5-Coder:0.5B is lightweight but still has latency
- Consider using the embedded model for simple tasks
- Use caching (automatically enabled in hierarchical AI engine)

## Performance Expectations

With Qwen2.5-Coder:0.5B:
- **Response Time**: 1-3 seconds per API call
- **Memory Usage**: ~500MB VRAM
- **Quality**: Good for specific, well-defined compiler tasks
- **Reliability**: High for structured analysis tasks

## Best Practices

1. **Use for Complex Tasks Only**: Let the hierarchical AI engine automatically choose when to use Qwen2.5-Coder
2. **Provide Clear Context**: Give specific task types and structured input
3. **Handle Fallbacks**: The system automatically falls back to rule-based reasoning if Ollama is unavailable
4. **Monitor Performance**: Use `--show-audit` to track AI usage and effectiveness
5. **Security First**: Remember that all AI suggestions go through IPL's mathematical firewall

## Integration Points

The enhanced Qwen2.5-Coder integration works at these points:

1. **Compilation Pipeline**: Enhanced system prompts guide the model for compiler tasks
2. **Security Analysis**: Model focuses on identifying vulnerabilities without bypassing security
3. **Type Inference**: Works within IPL's strong typing system
4. **Error Analysis**: Provides context-aware fix suggestions
5. **Optimization**: Suggests deterministic optimizations that maintain security

This configuration ensures Qwen2.5-Coder:0.5B provides intelligent, safe assistance for IPL compilation while maintaining the language's security-first architecture.