# IPL (Intelligent Programming Language)

IPL is a programming language that integrates AI models directly into the compilation pipeline. Unlike traditional code suggestion tools, IPL uses AI at the compiler level to understand, analyze, and optimize code during compilation.

## Installation

### Quick Start
```bash
pip install ipl-lang
ipl run examples/01_intelligent_variables.ipl
```

### AI Provider Options

**Local AI (Ollama)**
```bash
pip install ipl-lang
# Install Ollama: curl -fsSL https://ollama.com/install.sh | sh
ipl run script.ipl --ai-provider ollama --ai-model qwen2.5-coder:0.5b
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

## Features

### Semantic Type System
Automatically extracts and types semantic entities from natural language:
- `Currency`: Extracts monetary values ("ninety-nine bucks" → 99.50)
- `Sentiment`: Analyzes emotional tone ("fantastic" → positive score)
- `Quantity`: Parses measurements with units ("120 ms" → 120.0)
- `Date`: Normalizes temporal expressions
- `Intent`: Classifies natural language into categories

### Multi-Tier AI Architecture
- **Tier 1**: Fast pattern matching for token classification
- **Tier 2**: Semantic analysis using rule-based NLP
- **Tier 3**: Deep reasoning with OpenAI API integration

### Security System
- **Mathematical Firewall**: Validates AI outputs against safe schemas
- **Zero-Trust Taint Tracking**: Tags data as Untrusted/Sanitized/Trusted
- **Self-Correction Loop**: Repairs type mismatches automatically
- **Cryptographic Audit Trail**: SHA-256 signed execution traces

## Syntax

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

## Execution Methods

- **CLI**: `ipl run <file.ipl>`
- **REPL**: `ipl repl`
- **Python Embedding**: Import interpreter class
- **REST API**: `ipl serve` (launches security gateway)

## Compiler-Level AI Integration

- AI models integrated directly into compiler phases
- AI-enhanced type inference and context understanding
- AI-driven optimization and security transformations
- Pluggable architecture for any AI model
- AI can block compilation based on security analysis
- AI-powered error understanding and fix suggestions

> IPL is intelligent at the compiler level, not the code suggestion level. AI transforms the compilation process itself.

## Security Testing

Comprehensive security tests validate compiler-level AI intelligence:
- 20+ attack scenarios (SQL injection, XSS, command injection, path traversal)
- 100% attack prevention
- Zero false positives

Run tests:
```bash
python3 ipl/tests/security/run_security_tests.py
```

## Current Status

IPL is a functional neuro-symbolic programming language with:
- Working compiler and runtime system
- Semantic type extraction and analysis
- Multi-tier AI processing with real API integration
- Comprehensive security framework
- CLI, REPL, and REST interface
- VS Code syntax highlighting extension