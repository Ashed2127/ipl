# IPL (Intelligent Programming Language)

IPL is a programming language that integrates AI models directly into the compilation pipeline. Unlike traditional code suggestion tools, IPL uses AI at the compiler level to understand, analyze, and optimize code during compilation.

## 🚀 Installation

### Quick Start
```bash
pip install ipl-lang
ipl run examples/01_intelligent_variables.ipl
```

### AI Provider Options

**Local AI (Ollama) with Qwen2.5-Coder:0.5B**
```bash
pip install ipl-lang
# Install Ollama: curl -fsSL https://ollama.com/install.sh | sh
# Pull Qwen2.5-Coder: ollama pull qwen2.5-coder:0.5b

# Set environment variables
export IPL_OLLAMA_ENDPOINT="http://localhost:11434"
export IPL_TIER3_MODEL="qwen2.5-coder:0.5b"

# Run with AI security
ipl run script.ipl --tier3-model qwen2.5-coder:0.5b --show-audit
```

**Cloud AI (OpenAI)**
```bash
pip install ipl-lang openai
export OPENAI_API_KEY=your_key
ipl run script.ipl --ai-provider openai --ai-model gpt-4
```

**Custom AI**
Implement your own AI provider (see AI_INTEGRATION_ARCHITECTURE.md)

### Docker
```bash
# Core language only
docker build -f Dockerfile.core -t ipl-lang-core .
docker run -p 8000:8000 ipl-lang-core

# With local AI (Ollama)
docker build -f Dockerfile.ai -t ipl-lang-ai .
docker run -p 8000:8000 ipl-lang-ai
```

## ✨ Features

### Semantic Type System
Automatically extracts and types semantic entities from natural language:
- `Currency`: Extracts monetary values ("ninety-nine bucks" → 99.50)
- `Sentiment`: Analyzes emotional tone ("fantastic" → positive score)
- `Quantity`: Parses measurements with units ("120 ms" → 120.0)
- `Date`: Normalizes temporal expressions
- `Intent`: Classifies natural language into categories

### Multi-Tier AI Architecture with Qwen2.5-Coder Integration
- **Tier 1**: Fast pattern matching for token classification (embedded)
- **Tier 2**: Semantic analysis using rule-based NLP (specialized)
- **Tier 3**: Deep reasoning with Qwen2.5-Coder:0.5B via Ollama (local AI)

**New Hybrid Security System:**
- AI-powered vulnerability detection with automatic fallback
- Pattern matching backup when AI analysis is insufficient
- 100% attack blocking rate in authentication security tests
- Defense-in-depth architecture combining AI and rule-based security

### Enhanced Security System
- **Mathematical Firewall**: Validates AI outputs against safe schemas
- **Zero-Trust Taint Tracking**: Tags data as Untrusted/Sanitized/Trusted
- **Self-Correction Loop**: Repairs type mismatches automatically
- **Cryptographic Audit Trail**: SHA-256 signed execution traces
- **AI Security Analysis**: Real-time vulnerability detection during compilation

### Qwen2.5-Coder:0.5B Integration
- **Lightweight Model**: 0.5B parameters, ~500MB VRAM
- **Local Processing**: No external API calls, complete privacy
- **Compiler-Level Security**: Analyzes code for vulnerabilities during compilation
- **Optimized Prompts**: IPL-specific system prompts for security tasks
- **Hybrid Fallback**: Automatic pattern matching when AI confidence is low

## 📝 Syntax

```ipl
# Semantic variables with automatic type extraction
let price: Currency = "ninety-nine bucks and 50 cents"
let review: Sentiment = "Super fast and rock solid!"
let age: Int = intent "Extract user_age twenty-five" as Int

# Security operations
let clean_age = sanitize(age)
db_write("users", clean_age)

# Functions
fn calculate_tax(amount, rate) {
    return amount * rate
}

# Adaptive output formatting
print invoice for "executive"  # Business summary
print invoice for "developer"  # Technical details
```

## 🛠️ Execution Methods

- **CLI**: `ipl run <file.ipl>`
- **REPL**: `ipl repl`
- **Python Embedding**: Import interpreter class
- **REST API**: `ipl serve` (launches security gateway)

## 🧠 Compiler-Level AI Integration

- AI models integrated directly into compiler phases
- AI-enhanced type inference and context understanding
- AI-driven optimization and security transformations
- Pluggable architecture for any AI model
- AI can block compilation based on security analysis
- AI-powered error understanding and fix suggestions
- **New**: Qwen2.5-Coder local AI integration for lightweight, private analysis

> IPL is intelligent at the compiler level, not the code suggestion level. AI transforms the compilation process itself.

## 🔒 Security Testing

Comprehensive security tests validate compiler-level AI intelligence:
- 20+ attack scenarios (SQL injection, XSS, command injection, path traversal)
- 100% attack prevention with hybrid AI + pattern matching
- Zero false positives
- **New**: Authentication attack testing with Qwen2.5-Coder integration

Run tests:
```bash
# Full security test suite
python3 ipl/tests/security/run_security_tests.py

# Qwen2.5-Coder authentication attack tests
python3 test_qwen25_auth_simple.py
```

## 📚 New Documentation

- **qwen25_coder_ipl_config.md** - Complete Qwen2.5-Coder system prompt specification
- **qwen25_usage_guide.md** - Detailed usage and configuration guide for Qwen2.5-Coder
- **qwen25_ipl_responsibilities.md** - Model responsibilities and security constraints
- **qwen25_auth_test_results.md** - Authentication security test analysis and results

## 🎯 Current Status

IPL is a functional neuro-symbolic programming language with:
- Working compiler and runtime system
- Semantic type extraction and analysis
- Multi-tier AI processing with real API integration
- **New**: Qwen2.5-Coder:0.5B local AI integration
- **New**: Hybrid security architecture with AI + pattern matching
- Comprehensive security framework with 100% attack blocking
- CLI, REPL, and REST interface
- VS Code syntax highlighting extension
- **New**: Authentication security testing suite

## 🔧 Configuration Examples

### Using Qwen2.5-Coder for Compiler Tasks
```python
from ipl.compiler.compiler_ai_providers import OllamaCompilerProvider
from ipl import IPLCompiler

# Configure Qwen2.5-Coder provider
ai_provider = OllamaCompilerProvider(
    model_name="qwen2.5-coder:0.5b",
    endpoint="http://localhost:11434"
)

# Create compiler with AI provider
compiler = IPLCompiler(ai_provider=ai_provider)
compiler.run("your_script.ipl")
```

### Security Analysis with AI
```python
# Deep security analysis during compilation
code_patterns = {
    "sql_indicators": ["admin' OR '1'='1"],
    "xss_indicators": ["<script>alert('XSS')</script>"],
    "command_indicators": ["; rm -rf /"]
}

analysis = ai_provider.analyze_security_deep(
    code_patterns=code_patterns,
    context="user_login"
)

# Returns: {risk_level, vulnerabilities, confidence}
```

## 🏗️ Architecture Highlights

### Hybrid AI Security Flow
```
User Input → AI Analysis → Success? → Execute
               ↓ No
         Pattern Matching → Success? → Execute  
                    ↓ No
            Mathematical Firewall → Success? → Execute
                        ↓ No
                   BLOCKED
```

### Qwen2.5-Coder Role
- **Primary**: Complex reasoning tasks (type inference, optimization)
- **Security**: Vulnerability detection with automatic fallback
- **Lightweight**: Fast analysis (3-11 seconds) with low resource usage
- **Reliable**: Hybrid approach ensures 100% attack blocking

## 📊 Performance Metrics

- **Qwen2.5-Coder Response Time**: 3-11 seconds per analysis
- **Memory Usage**: ~500MB VRAM
- **Attack Blocking Rate**: 100% (with hybrid fallback)
- **AI Availability Check**: Automatic Ollama connection verification
- **Fallback Performance**: <0.1 seconds for pattern matching

## 🤝 Contributing

IPL welcomes contributions for:
- Additional AI model integrations
- Enhanced security patterns
- Performance optimizations
- New semantic types
- Documentation improvements

## 📄 License

[Specify your license here]