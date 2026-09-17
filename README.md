# IPL: Intelligent Programming Language (Aether)

IPL is a hybrid neuro-symbolic programming language that combines AI-powered semantic understanding with deterministic security verification. It executes natural language programming through a multi-tier AI architecture with mathematical safety guarantees.

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
- **CLI**: `python3 -m cli run <file.ipl>`
- **REPL**: `python3 -m cli repl`
- **Python Embedding**: Import interpreter class for programmatic execution
- **REST API**: `python3 -m cli serve` (launches security gateway)

### AI Configuration
- **Default**: Uses embedded fast semantic engine (sub-millisecond, no external dependencies)
- **Local LLM**: Connects to Ollama models (default: qwen2.5-coder:0.5b, also supports deepseek, gemma, etc.)
- **OpenAI Integration**: Real AI deep reasoning when API key provided via `--openai-api-key` flag or `OPENAI_API_KEY` environment variable

### Current Status
IPL is a functional neuro-symbolic programming language with:
- Working compiler and runtime system
- Semantic type extraction and analysis
- Multi-tier AI processing with real API integration
- Comprehensive security framework
- CLI, REPL, and REST interface
- VS Code syntax highlighting extension