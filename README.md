# IPL (Intelligent Programming Language)

A security-focused programming language with zero-trust taint tracking and symbolic compilation.

## Key Features

- **Zero-Trust Security**: All data starts untrusted and must be explicitly sanitized
- **Sound Taint Tracking**: Three-level security lattice (UNTRUSTED < SANITIZED < TRUSTED)
- **Deterministic Runtime**: Same input always produces same output
- **Fail-Closed Design**: Security violations block execution
- **Cryptographic Auditing**: SHA-256 signed execution traces
- **Pattern-Based Semantics**: Currency, Sentiment, Quantity, Date parsing

## Installation

```bash
git clone https://github.com/Ashed2127/ipl.git
cd ipl
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
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
python3 test_adversarial_attacks.py
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for complete documentation.
