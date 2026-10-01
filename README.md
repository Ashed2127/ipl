# IPL (Intelligent Programming Language)

A security-focused programming language with zero-trust taint tracking, symbolic compilation, and neural security analysis via Ollama.

## Key Features

- **Zero-Trust Security**: All data starts untrusted and must be explicitly sanitized
- **Sound Taint Tracking**: Three-level security lattice (UNTRUSTED < SANITIZED < TRUSTED)
- **Neural Security Analysis**: Local LLM integration via Ollama for intelligent vulnerability detection
- **Deterministic Runtime**: Same input always produces same output
- **Fail-Closed Design**: Security violations block execution
- **Cryptographic Auditing**: SHA-256 signed execution traces
- **Pattern-Based Semantics**: Currency, Sentiment, Quantity, Date parsing

## Installation

```bash
# Clone and setup
git clone https://github.com/Ashed2127/ipl.git
cd ipl
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Install Ollama for neural security analysis (optional)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull CyberCrew/notmythos-8b:mini
```

## Usage

### Run IPL programs
```bash
python3 cli.py run examples/authorization_demo.ipl
```

### Interactive REPL
```bash
python3 cli.py repl
```

### Python embedding
```python
from lexer import Lexer
from parser import Parser
from runtime import Interpreter

source = """
let user_input = "admin' OR '1'='1";
let sanitized = sanitize_string(user_input);
db_write("users", sanitized);
"""

lexer = Lexer(source)
tokens = lexer.tokenize()
parser = Parser(tokens)
program = parser.parse()

interpreter = Interpreter()
interpreter.run(program, source_code=source)
```

## Syntax

```ipl
let price: Currency = "ninety-nine bucks and 50 cents"
let clean_age = sanitize_string(age)
db_write("users", clean_age)

fn calculate_tax(amount, rate) {
    return amount * rate
}
```

## Testing

```bash
# Test rule-based security
python3 test_adversarial_attacks.py

# Test neural security analysis (requires Ollama)
python3 test_neural_security.py
```

## Neural Security Analysis

IPL now integrates with local LLM models via Ollama for intelligent vulnerability detection:

```python
from security_engine import SecurityEngine

# Rule-based + neural analysis
code = "let user_input = 'admin OR 1=1'; db_write('users', user_input);"
is_safe, warnings = SecurityEngine.check_execution_safety(code, use_neural=True)

# Pure neural vulnerability detection
result = SecurityEngine.neural_vulnerability_detection(code)
print(f"SQL injection: {result['sql_injection']}")
print(f"XSS: {result['xss']}")
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for complete documentation.
