# IPL (Intelligent Programming Language / Aether)

A neuro-symbolic programming language that combines traditional programming constructs with semantic intelligence, natural language understanding, and adaptive presentation. Built for pair programming with DeepMind AI systems architecture.

## 🧠 Architecture Overview

IPL is designed around the principle that programming languages should understand *intent* and *context*, not just syntax. The architecture consists of seven core components that work together to provide intelligent variable handling, semantic type extraction, and adaptive output formatting.

```
┌─────────────────────────────────────────────────────────────────┐
│                        IPL Architecture                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Source Code ──► Lexer ──► Parser ──► AST ──► Interpreter       │
│                     │        │         │         │               │
│                     │        │         │         │               │
│                     │        │         │         ├─► Runtime     │
│                     │        │         │         │   Environment  │
│                     │        │         │         │               │
│                     │        │         │         ├─► IValue      │
│                     │        │         │         │   System       │
│                     │        │         │         │               │
│                     │        │         │         └─► Formatter   │
│                     │        │         │             Output      │
│                     │        │         │                           │
│                     │        │         └─► Semantic Engine ◄─────┘
│                     │        │               (The "Brain")          │
│                     │        │                                       │
│                     │        └─► AST Nodes                          │
│                     │                                              │
│                     └─► Tokens                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 📦 Core Components

### 1. **Lexer** (`lexer.py`)
Tokenizes source code into a stream of tokens with support for:
- **Keywords**: `let`, `var`, `print`, `where`, `for`, `as`, `prob`, `if`, `else`, etc.
- **Literals**: Numbers, strings, booleans, null
- **Operators**: Arithmetic (`+`, `-`, `*`, `/`, `%`), comparison (`==`, `!=`, `<`, `>`, `<=`, `>=`), logical (`and`, `or`, `not`), fuzzy match (`~`)
- **Delimiters**: Parentheses, brackets, braces, commas, colons, semicolons

**Key Features**:
- Multi-line string support
- Comment handling (`//` and `#`)
- Precise line/column tracking for error reporting

### 2. **Parser** (`parser.py`)
Builds an Abstract Syntax Tree (AST) from tokens using recursive descent parsing:
- **Statements**: Variable declarations (`let`/`var`), assignments, print statements
- **Expressions**: Literals, identifiers, binary/unary operations, lists, dictionaries, member access
- **Type Annotations**: Rich semantic types with generic parameters and confidence thresholds

**Key Features**:
- Operator precedence handling
- Generic type parsing (e.g., `Intent<Fraud, Refund, Support>`)
- Refinement clause parsing (e.g., `where (v >= 0 and v <= 100)`)

### 3. **AST Nodes** (`ast_nodes.py`)
Defines the abstract syntax tree structure:
- **Program**: Root node containing statements
- **Statements**: `LetStatement`, `AssignStatement`, `PrintStatement`
- **Expressions**: `Literal`, `Identifier`, `BinaryOp`, `UnaryOp`, `ListLiteral`, `DictLiteral`, `MemberAccess`
- **Types**: `TypeAnnotation` with support for generics and confidence thresholds

### 4. **Semantic Engine** (`semantic_engine.py`)
The neural-symbolic "brain" of IPL that provides:

#### 4.1 Natural Language Extraction & Type Inference
- **Currency Extraction**: Parses natural language like "ninety-nine bucks and 50 cents" into structured currency data with confidence scores
- **Sentiment Analysis**: Calculates emotional valence [-1.0, 1.0] from text using positive/negative word dictionaries
- **Date Calculation**: Extracts relative/absolute dates from natural language (e.g., "tomorrow at 3pm", "next Friday")
- **Quantity Extraction**: Parses dimensional quantities with units (e.g., "450 ms", "16 GB", "120 km/h")
- **Intent Classification**: Classifies text into semantic categories (Refund, Fraud, Support, Inquiry, etc.)
- **Number Extraction**: Handles written numbers ("twenty-five", "one thousand two hundred")

#### 4.2 Refinement Invariant Engine
- Validates values against invariant predicates declared with `where` clauses
- Provides violation explanations when constraints are breached
- Supports complex conditions with logical operators

#### 4.3 Audience Adaptation Engine
Adapts presentation for different audiences:
- **Executive**: Business-focused summaries with KPIs and strategic recommendations
- **Developer**: Technical debugging information with memory representation details
- **Child**: Simple, friendly explanations with emojis and analogies
- **SRE**: Operational telemetry with SLA status and observability data
- **Marketer**: Highlight-ready content for campaigns and social media
- **Auditor**: Compliance-focused traces with verification status

#### 4.4 Semantic Query Engine
Answers high-level natural language queries:
- `"summary of"` - Provides overviews of data structures
- `"highlight risks in"` - Identifies potential issues and anomalies
- `"explain"` - Offers explanatory insights
- `"key takeaways"` - Extracts main points
- `"health status"` - Reports on system/metric health

#### 4.5 Self-Healing Identifier Matcher
- Uses Levenshtein distance to find similar variable names
- Provides substring matching and acronym resolution
- Automatically suggests corrections for typos with confidence scores

### 5. **Runtime** (`runtime.py`)
The interpreter that executes AST nodes:

#### 5.1 IValue System
Intelligent Value representation that wraps raw data with:
- **Type tags**: Semantic type information (Currency, Sentiment, etc.)
- **Confidence scores**: Bayesian/neural confidence values [0.0, 1.0]
- **Metadata**: Provenance and origin information
- **Invariant violation tracking**: Records constraint breaches
- **Mutability flags**: `let` (immutable) vs `var` (mutable)

#### 5.2 Environment Management
- Lexical scoping with parent-child environment chains
- Variable binding with reassignment protection for immutable variables
- Self-healing symbol resolution for undefined identifiers

#### 5.3 Statement Execution
- **Variable Declaration**: Evaluates expressions, applies type annotations, validates invariants
- **Assignment**: Handles mutable reassignments with type checking
- **Print**: Orchestrates semantic queries, audience adaptation, and formatting

#### 5.4 Expression Evaluation
- Literal evaluation with type inference
- Variable resolution with self-healing
- Arithmetic operations with currency/quantity awareness
- Logical operations with confidence propagation
- Comparison operations including fuzzy semantic matching (`~`)

### 6. **Formatter** (`formatter.py`)
Rich presentation formatting using the Rich library:
- **Tables**: Structured data display with headers
- **Bar Charts**: Proportional Unicode visualizations
- **Badges**: Status indicators with confidence meters
- **Sentiment Cards**: Emotional valence visualization
- **Gauges**: Progress/utilization meters
- **Cards**: Executive-style insight panels
- **Trees**: Hierarchical data structure display
- **JSON**: Syntax-highlighted pretty-printing

### 7. **CLI** (`cli.py`)
Command-line interface providing:
- **REPL Mode**: Interactive development environment with live execution
- **File Execution**: Run IPL scripts from files
- **Error Handling**: Comprehensive lexer, parser, and runtime error reporting
- **Help System**: Built-in examples and documentation

## 🎯 Key Intelligent Features

### 1. Semantic Type System
Variables can be declared with rich semantic types that extract meaning from natural language:

```ipl
let price: Currency = "ninety-nine bucks and 50 cents"
let review: Sentiment = "Absolutely fantastic build, super fast!"
let maintenance: Date = "scheduled for tomorrow at 3pm"
let latency: Quantity = "450 ms"
let intent: Intent<Fraud, Refund, Support> = "someone used my stolen card"
```

### 2. Probabilistic Monad
The `Prob<T>` type wraps values with confidence scores and threshold enforcement:

```ipl
let alert: Prob<String, 0.95> = "unusual spike detected"
// Runtime warning if confidence < 95%
```

### 3. Adaptive Print Statements
Print statements adapt output based on audience and format:

```ipl
print revenue for "executive"     // Business summary
print latency for "sre"           // Operational telemetry
print sentiment for "child"        // Simple, friendly explanation
print data as table               // Rich table formatting
print metrics as bar_chart        // Visual proportional chart
```

### 4. Semantic Queries
Natural language queries directly in print statements:

```ipl
print "summary of" cluster_nodes
print "highlight risks in" diagnostic_incident
print "explain" system_state
```

### 5. Refinement Invariants
Type constraints with `where` clauses:

```ipl
let charge: Currency where (v >= 0 and v <= 500) = "three hundred dollars"
// Runtime validation and violation reporting
```

### 6. Self-Healing Variables & Functions
Automatic typo correction using edit distance and token-prefix matching:

```ipl
let customer_feedback: Sentiment = "Great experience!"
print custmer_feedbk  // Automatically resolves to customer_feedback

fn calculate_discount(price, rate) { return price * rate; }
let d = calc_discount(100, 0.1) // Auto-heals to calculate_discount!
```

### 7. Immutability Control
`let` for immutable bindings, `var` for mutable:

```ipl
let constant = 42        // Cannot be reassigned
var counter = 1          // Can be reassigned
counter = counter + 1    // Valid
```

### 8. Control Flow (Conditionals & Loops)
Full control flow primitives with confidence-aware reasoning:

```ipl
// If / Elif / Else
if confidence(review) >= 0.85 {
    print "High confidence verified"
} elif confidence(review) >= 0.5 {
    print "Moderate signal"
} else {
    print "Low confidence observation"
}

// For loops with lists and range()
for node in cluster_nodes {
    if not node.healthy {
        print "Alert on", node.name
    }
}

// While loops with break & continue
var count = 5
while count > 0 {
    count = count - 1
    if count == 2 { continue }
    print count
}
```

### 9. User-Defined Functions & Built-ins
Functions with first-class semantic type checking, return values, recursion, and built-ins:

```ipl
fn fibonacci(n) {
    if n <= 1 { return n }
    return fibonacci(n - 1) + fibonacci(n - 2)
}

fn process_order(price: Currency, ticket: Intent<Refund, Fraud, Support>) {
    return price
}
```

Built-in library: `len()`, `range()`, `confidence()`, `type_of()`, `keys()`, `values()`, `min()`, `max()`, `abs()`, `round()`, `str()`, `int()`, `float()`, `bool()`, `push()`.

### 10. Hybrid Neuro-Symbolic Compiler Architecture & Zero-Trust Firewall

IPL achieves deterministic safety at compiler speeds through a hybrid neuro-symbolic architecture:

```
 Natural Language Intent
         │
         ▼
 ┌───────────────────────────┐
 │ System 1: Neural Gen      │  (Semantic parser generates candidate AST data)
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │ System 2: Mathematical    │◄─── Fail-closed verification
 │ Firewall & Symbolic Checks│───► Self-Correction Repair Loop
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │ Zero-Trust Taint Tracking │  (Untrusted -> SanitizationNode -> Sinks)
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │ Cryptographic Audit Trace │  (Per-step SHA256 signatures)
 └───────────────────────────┘
```

1. **System 1: Embedded Inference Runtime**: Operates strictly as a semantic parser, translating natural language declarations (e.g., `intent "extract user_age twenty-five from doc" as Int`) into sandboxed, unexecutable candidate AST nodes.
2. **System 2: Symbolic Verification & Mathematical Firewall**: Validates candidate AST nodes against a hardcoded schema of safe primitives (`MathematicalFirewall.SAFE_PRIMITIVES`) and enforces strict type contracts before memory allocation.
3. **Resilience: The Self-Correction Loop**: When symbolic verification detects an error (such as a string representation `"twenty-five"` when an `Int` is required), concrete compiler diagnostics are fed back to System 1 to structurally repair the candidate AST node without crashing.
4. **Zero-Trust Data Taint Tracking**: Neural outputs are assigned `TaintLevel.UNTRUSTED`. Sensitive sinks (`db_write`, `file_write`) fail-closed unless data has passed through a deterministic `SanitizationNode` (`sanitize(expr[, rule])`). The `trusted` keyword allows explicit compile-time exemptions.
5. **Cryptographic Verified Audit Trace**: Produces an immutable, per-step cryptographic trace with SHA256 hashes verifying ingestion, candidate parsing, repair cycles, taint transitions, and sink executions.

```ipl
// Neuro-symbolic intent compilation with self-correction
let age: Int = intent "extract user_age twenty-five from record" as Int

// Data taint tracking & sanitization node
let clean_age = sanitize(age, "int_range_validator")

// Critical sink commit (blocked if untrusted; succeeds once sanitized)
db_write("users", clean_age)

// Render cryptographic audit trace
audit_trace()
```

## 🚀 Usage

### Installation
Install as an editable package to make the `ipl` executable globally available:
```bash
pip install -e . --no-deps --break-system-packages
```

### CLI Subcommands
```bash
# Execute an IPL source file
ipl run examples/08_neuro_symbolic_compiler.ipl

# Execute and display the cryptographic audit trace
ipl audit examples/08_neuro_symbolic_compiler.ipl

# Statically verify AST nodes against the Mathematical Firewall schema
ipl verify examples/08_neuro_symbolic_compiler.ipl

# Compile source and inspect AST contract readiness
ipl compile examples/08_neuro_symbolic_compiler.ipl

# Start the interactive REPL
ipl repl
```

### Interactive Examples
The REPL includes a help system with examples:
```ipl
ipl> help
```

## 📁 Project Structure

```
ipl_lang/
├── pyproject.toml           # Packaging, dependencies, and CLI script entrypoints
├── __init__.py              # Package initialization
├── tokens.py                # Token definitions and TokenType enum
├── lexer.py                 # Lexical analysis and tokenization
├── parser.py                # AST construction with intent, sanitize, and contracts
├── ast_nodes.py             # Abstract syntax tree node definitions (IntentExpr, SanitizationNode, etc.)
├── compiler.py              # Hybrid Neuro-Symbolic Compiler, Firewall, and Audit Trace
├── taint.py                 # Zero-trust data taint tracking and sink enforcement
├── semantic_engine.py       # Neural-symbolic semantic processing and entity extraction
├── runtime.py               # Interpreter, IValue system, zero-trust sinks (db_write, file_write)
├── formatter.py             # Rich presentation formatting
├── security_engine.py       # Security analysis and code sanitization
├── cli.py                   # Command-line interface with run, audit, verify, compile, repl
├── examples/                # Example IPL programs
│   ├── 01_intelligent_variables.ipl
│   ├── 02_intelligent_print_audiences.ipl
│   ├── 03_semantic_queries_and_formats.ipl
│   ├── 04_invariants_and_self_healing.ipl
│   ├── 05_security_demo.ipl
│   ├── 06_control_flow.ipl
│   ├── 07_functions_and_logic.ipl
│   └── 08_neuro_symbolic_compiler.ipl
└── tests/                   # Comprehensive unit & integration test suite (47 tests)
    ├── test_extraction.py
    ├── test_variables_and_print.py
    ├── test_control_flow.py
    ├── test_functions.py
    ├── test_neuro_symbolic_compiler.py
    └── test_taint_tracking.py
```

## 🔮 Design Philosophy

IPL is built on the principle that **programming languages should understand intent, not just syntax**. Key design principles:

1. **Neuro-Symbolic Integration**: Combines neural network-style pattern recognition with symbolic logic
2. **Deterministic Speed**: Locally embedded inference and AST generation avoiding network latency
3. **Mathematical Firewall**: Pure data AST sandboxing with zero-trust execution
4. **Iterative Self-Correction**: Resilient repair loops solving contract violations prior to allocation
5. **Data Taint Tracking**: Untrusted neural outputs mathematically isolated from sensitive sinks
6. **Complete Cryptographic Auditing**: Per-step SHA256 verified trace for mission-critical compliance

## 🛠️ Implemented Core Features

- **Neuro-Symbolic Compiler**: System 1 local inference, System 2 Mathematical Firewall, Self-Correction Loop, and Verified Audit Trace (`compiler.py`).
- **Data Taint Tracking**: `TaintLevel` (`UNTRUSTED`, `SANITIZED`, `TRUSTED`), `TaintViolationError`, `SanitizationNode` (`sanitize()`), `trusted` declarations, and protected sinks (`db_write`, `file_write`).
- **Intelligent Variables**: Natural language extraction (`Currency`, `Quantity`, `Sentiment`, `Date`, `Intent`), probabilistic confidence `Prob<T>`, refinement invariants (`where` clauses), immutability (`let` vs `var`).
- **Adaptive Print**: Audience adaptation (`executive`, `developer`, `sre`, `child`, `marketer`), semantic queries (`"summary of"`, `"highlight risks in"`, `"explain"`), visual presentation (`table`, `bar_chart`, `badge`, `gauge`, `card`, `tree`).
- **Control Flow**: Conditionals (`if`, `elif`, `else`), `for ... in` iteration over lists and `range()`, `while` loops, `break`, `continue`, subscript indexing.
- **Functions & Closures**: User-defined `fn`, recursive calls, return values, semantic type verification on arguments, lexical scope.
- **Built-in Standard Library**: `len()`, `range()`, `confidence()`, `type_of()`, `taint_of()`, `audit_trace()`, `db_write()`, `file_write()`, `keys()`, `values()`, `min()`, `max()`, `abs()`, `round()`, `str()`, `int()`, `float()`, `bool()`, `push()`.
- **Neuro-Symbolic Self-Healing**: Dynamic symbol resolution repairing typos in both variables and function calls.

## 🧪 Testing

Run the comprehensive unit test suite:
```bash
python3 -m unittest discover -s tests
```

## 📝 License

This is an experimental intelligent programming language research project.

## 🤝 Contributing

This is a research prototype. Contributions that advance the neuro-symbolic programming language paradigm are welcome.

---

**IPL: Where Code Meets Intelligence** 🧠⚡