# IPL (Intelligent Programming Language)

**IPL is an intelligent programming language that decides any situation by itself whether the decision is good or bad.**

This is the future of programming languages - truly autonomous decision-making with no manual configuration or hardcoded parameters.

## Key Features

- **🧠 Autonomous Decision Engine**: IPL decides what's safe or dangerous by itself - NO hardcoded rules, whitelists, or blacklists
- **🔄 Self-Learning Security**: Learns from experience using Q-learning and reinforcement learning
- **📊 Auto-Configuring Thresholds**: Automatically learns optimal thresholds based on runtime behavior
- **🎯 Zero-Trust Security**: All data starts untrusted and must be explicitly sanitized
- **🔒 Sound Taint Tracking**: Three-level security lattice (UNTRUSTED < SANITIZED < TRUSTED)
- **🧬 Neural Security Analysis**: Local LLM integration via Ollama for intelligent vulnerability detection
- **⚡ Deterministic Runtime**: Same input always produces same output
- **🛡️ Fail-Closed Design**: Security violations block execution
- **📝 Cryptographic Auditing**: SHA-256 signed execution traces
- **🔤 Pattern-Based Semantics**: Currency, Sentiment, Quantity, Date parsing

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

## Autonomous Decision Engine

The core innovation of IPL - it decides what's good or bad by itself:

```python
from autonomous_decision_engine import AutonomousDecisionEngine

# Initialize the autonomous engine
engine = AutonomousDecisionEngine()

# The engine autonomously judges safety
context = {
    'has_untrusted_data': True,
    'has_sanitization': False,
    'taint_propagation_steps': 5,
}

judgment = engine.judge_safety(context)
print(f"Is Safe: {judgment.is_safe}")
print(f"Confidence: {judgment.confidence}")
print(f"Reasoning: {judgment.reasoning}")
print(f"Threat Level: {judgment.threat_level}")

# Record outcome for learning
from autonomous_decision_engine import Decision, DecisionType, DecisionOutcome
decision = Decision(
    decision_id="dec_1",
    decision_type=DecisionType.SECURITY,
    context=context,
    action=judgment.is_safe,
    confidence=judgment.confidence,
    timestamp=time.time()
)
engine.record_outcome(decision, DecisionOutcome.GOOD, reward=1.0)

# The engine learns from experience - no manual configuration needed!
stats = engine.get_statistics()
print(f"Success Rate: {stats['success_rate']:.2%}")
```

**Key capabilities:**
- **No hardcoded rules**: Unlike traditional compilers with fixed whitelists/blacklists, IPL learns what's safe
- **Q-learning**: Uses reinforcement learning to improve decisions over time
- **Auto-configuration**: Thresholds and heuristics are learned from runtime behavior
- **Continuous adaptation**: Adapts to new situations without human intervention

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for complete documentation.
