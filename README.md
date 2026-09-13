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

### 6. Self-Healing Variables
Automatic typo correction using edit distance:

```ipl
let customer_feedback: Sentiment = "Great experience!"
print custmer_feedbk  // Automatically resolves to customer_feedback
```

### 7. Immutability Control
`let` for immutable bindings, `var` for mutable:

```ipl
let constant = 42        // Cannot be reassigned
var counter = 1          // Can be reassigned
counter = counter + 1    // Valid
```

## 🚀 Usage

### Running the REPL
```bash
python3 -m ipl_lang.cli repl
# or simply
python3 -m ipl_lang.cli
```

### Running a Script
```bash
python3 -m ipl_lang.cli run examples/01_intelligent_variables.ipl
# or
python3 -m ipl_lang.cli examples/01_intelligent_variables.ipl
```

### Interactive Examples
The REPL includes a help system with examples:
```ipl
ipl> help
```

## 📁 Project Structure

```
ipl_lang/
├── __init__.py              # Package initialization
├── tokens.py                # Token definitions and TokenType enum
├── lexer.py                 # Lexical analysis and tokenization
├── parser.py                # AST construction from tokens
├── ast_nodes.py             # Abstract syntax tree node definitions
├── semantic_engine.py       # Neural-symbolic semantic processing
├── runtime.py               # Interpreter, IValue system, and environment
├── formatter.py             # Rich presentation formatting
├── cli.py                   # Command-line interface and REPL
├── examples/                # Example IPL programs
│   ├── 01_intelligent_variables.ipl
│   ├── 02_intelligent_print_audiences.ipl
│   ├── 03_semantic_queries_and_formats.ipl
│   └── 04_invariants_and_self_healing.ipl
└── tests/                   # Test suite
```

## 🔮 Design Philosophy

IPL is built on the principle that **programming languages should understand intent, not just syntax**. Key design principles:

1. **Neuro-Symbolic Integration**: Combines neural network-style pattern recognition with symbolic logic
2. **Confidence-Aware**: All operations propagate and respect confidence scores
3. **Audience-Adaptive**: Output adapts to who is consuming the information
4. **Self-Healing**: The language helps correct common mistakes automatically
5. **Type-Rich**: Semantic types carry meaning beyond traditional type systems
6. **Query-Native**: Natural language queries are first-class citizens

## 🛠️ Current Focus

The language currently focuses on making **variable declarations** and **print syntax** intelligent:

- **Variables**: Natural language extraction, semantic types, probabilistic confidence, refinement invariants
- **Print**: Audience adaptation, semantic queries, rich formatting, self-healing references

Future expansion areas include:
- Control flow (if/else, loops)
- Functions and closures
- Module system
- Concurrent programming primitives
- Database integration
- API client generation

## 📖 Example Programs

### Intelligent Variables
```ipl
let price: Currency = "ninety-nine bucks and 50 cents"
let review: Sentiment = "Absolutely fantastic build!"
print price
print review
```

### Audience Adaptation
```ipl
let revenue: Currency = "two million dollars"
print revenue for "executive"   // Business summary
print revenue for "child"        // Simple explanation
```

### Semantic Queries
```ipl
let nodes = [{ "cpu": 42 }, { "cpu": 88 }]
print "summary of" nodes
print "highlight risks in" nodes
```

### Invariants
```ipl
let charge: Currency where (v >= 0 and v <= 500) = "three hundred dollars"
print charge
```

## 🧪 Testing

Run the test suite:
```bash
python3 -m pytest tests/
```

## 📝 License

This is an experimental intelligent programming language research project.

## 🤝 Contributing

This is a research prototype. Contributions that advance the neuro-symbolic programming language paradigm are welcome.

---

**IPL: Where Code Meets Intelligence** 🧠⚡