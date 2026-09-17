# IPL: Intelligent Programming Language (Aether)

IPL is a **compiler-level AI programming language** that integrates powerful AI models directly into the compilation pipeline. Unlike traditional code suggestion tools, IPL becomes intelligent at the compiler level - AI transforms how the compiler understands, analyzes, and optimizes code during compilation itself.

## Installation

### Quick Start (Core Language)
```bash
# Install IPL core language
pip install ipl-lang

# Run immediately with built-in features
ipl run examples/01_intelligent_variables.ipl
```

### AI Integration (Choose Your AI Provider)
```bash
# Option 1: Local AI (Ollama)
pip install ipl-lang
# Install Ollama separately: curl -fsSL https://ollama.com/install.sh | sh
# Use with IPL: ipl run script.ipl --ai-provider ollama --ai-model qwen2.5-coder:0.5b

# Option 2: Cloud AI (OpenAI)
pip install ipl-lang openai
export OPENAI_API_KEY=your_key
# Use with IPL: ipl run script.ipl --ai-provider openai --ai-model gpt-4

# Option 3: Custom AI Integration
# Implement your own AI provider (see AI_INTEGRATION_ARCHITECTURE.md)
```

### Docker Deployment
```bash
# Core language only
docker build -f Dockerfile.core -t ipl-lang-core .
docker run -p 8000:8000 ipl-lang-core

# With local AI (Ollama)
docker build -f Dockerfile.ai -t ipl-lang-ai .
docker run -p 8000:8000 ipl-lang-ai
```

## Current Functionality

### Core Features
- **Semantic Type System**: Automatically extracts and types semantic entities from natural language
  - `Currency`: Extracts monetary values from text (e.g., "ninety-nine bucks" → 99.50)
  - `Sentiment`: Analyzes emotional tone (e.g., "fantastic" → positive score)
  - `Quantity`: Parses measurements with units (e.g., "120 ms" → 120.0 with unit)
  - `Date`: Normalizes temporal expressions
  - `Intent`: Classifies natural language into predefined categories

- **Multi-Tier AI Architecture**:
  - **Tier 1**: Lightning-fast pattern matching for token classification
  - **Tier 2**: Specialized semantic analysis using rule-based NLP
  - **Tier 3**: Deep reasoning with OpenAI API integration (when API key provided)

- **Security System**:
  - **Mathematical Firewall**: Validates all AI outputs against safe primitive schemas
  - **Zero-Trust Taint Tracking**: Tags data as Untrusted/Sanitized/Trusted
  - **Self-Correction Loop**: Automatically repairs type mismatches between AI intent and declared types
  - **Cryptographic Audit Trail**: SHA-256 signed execution traces

- **Deterministic Runtime**: Safe execution environment with fail-closed security sinks

### Language Syntax
```ipl
# Semantic variables with automatic type extraction
let price: Currency = "ninety-nine bucks and 50 cents"
let review: Sentiment = "Super fast and rock solid!"
let age: Int = intent "Extract user_age twenty-five" as Int

# Security operations
let clean_age = sanitize(age)
db_write("users", clean_age)

# Control flow and functions
fn calculate_tax(amount, rate) {
    return amount * rate
}

# Adaptive output formatting
print invoice for "executive"  # Business summary
print invoice for "developer"  # Technical details
```

### Execution Methods
- **CLI**: `python3 -m cli run <file.ipl>` or `ipl run <file.ipl>`
- **REPL**: `python3 -m cli repl` or `ipl repl`
- **Python Embedding**: Import interpreter class for programmatic execution
- **REST API**: `python3 -m cli serve` or `ipl serve` (launches security gateway)

### Compiler-Level AI Integration
- **AI in Compilation Pipeline**: AI models integrated directly into compiler phases
- **Semantic Analysis**: AI-enhanced type inference and context understanding during compilation
- **Code Transformation**: AI-driven optimization and security transformations during compilation
- **Pluggable Architecture**: Integrate any AI model (local Ollama, cloud OpenAI, or custom)
- **Security Blocking**: AI can block compilation based on deep security analysis
- **Error Recovery**: AI-powered error understanding and fix suggestions during compilation

> **Key Distinction**: IPL is intelligent at the **compiler level**, not the code suggestion level. AI transforms the compilation process itself rather than just providing suggestions.

### Security Testing
IPL includes comprehensive security tests to validate compiler-level AI intelligence:
- **20+ Attack Scenarios**: SQL injection, XSS, command injection, path traversal, etc.
- **100% Attack Prevention**: All malicious code blocked during compilation
- **Zero False Positives**: Legitimate code compiles successfully
- **Run Tests**: `python3 ipl/tests/security/run_security_tests.py`

**Use these tests after every architecture change to ensure IPL's compiler-level AI intelligence is maintained.**

### Current Status
IPL is a functional neuro-symbolic programming language with:
- Working compiler and runtime system
- Semantic type extraction and analysis
- Multi-tier AI processing with real API integration
- Comprehensive security framework
- CLI, REPL, and REST interface
- VS Code syntax highlighting extension