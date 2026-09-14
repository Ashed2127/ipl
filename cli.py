"""
Command-line interface (CLI) and REPL for IPL (Intelligent Programming Language / Aether).
"""
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown

try:
    from .lexer import Lexer, LexerError
    from .parser import Parser, ParserError
    from .runtime import Interpreter
    from .compiler import MathematicalFirewall, NeuroSymbolicCompiler
    from .ast_nodes import FunctionDef, IntentExpr, SanitizationNode
except (ImportError, ValueError):
    from lexer import Lexer, LexerError
    from parser import Parser, ParserError
    from runtime import Interpreter
    from compiler import MathematicalFirewall, NeuroSymbolicCompiler
    from ast_nodes import FunctionDef, IntentExpr, SanitizationNode


def print_banner(console: Console):
    banner_text = (
        "[bold cyan]⚡ IPL (Intelligent Programming Language / Aether)[/bold cyan]\n"
        "[dim]Hybrid Neuro-Symbolic Compiler Architecture & Deterministic Runtime[/dim]\n"
        "[dim]System 1 Neural Generation | System 2 Mathematical Firewall | Zero-Trust Taint Tracking[/dim]"
    )
    console.print(Panel(banner_text, border_style="cyan"))


def run_source(source: str, interpreter: Interpreter, console: Console, filename: str = "<stdin>"):
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter.run(program, source_code=source)  # Pass source code for security analysis
    except LexerError as le:
        console.print(f"[bold red]Syntax Error:[/bold red] {le}")
    except ParserError as pe:
        console.print(f"[bold red]Parser Error:[/bold red] {pe}")
    except Exception as e:
        console.print(f"[bold red]Runtime Exception:[/bold red] {e}")


def run_file(filepath: str, show_audit: bool = False, model_name: Optional[str] = None):
    console = Console()
    if not os.path.exists(filepath):
        console.print(f"[bold red]File not found:[/bold red] {filepath}")
        sys.exit(1)

    print_banner(console)
    model_disp = model_name or os.environ.get("IPL_MODEL", "embedded-fast-semantic-v1")
    console.print(f"[dim]Executing: {filepath} | AI Model: [bold cyan]{model_disp}[/bold cyan][/dim]\n")

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    interpreter = Interpreter(console=console, model_name=model_name)
    run_source(source, interpreter, console, filename=filepath)

    if show_audit:
        console.print("\n[bold cyan]─── Cryptographic Verified Audit Trace ───[/bold cyan]")
        interpreter.compiler.audit_trace.render_table(console)


def list_models():
    console = Console()
    print_banner(console)
    console.print("[bold cyan]🔍 Scanning for Local Neural AI Models...[/bold cyan]\n")

    models = LocalInferenceRuntime.list_available_local_models()
    table = Table(title="🤖 Detected Local AI Models (System 1 Compatible)", border_style="cyan")
    table.add_column("Model Name", style="bold green")
    table.add_column("Type", style="cyan")
    table.add_column("Status", style="yellow")
    table.add_column("Usage Command", style="white")

    # Add built-in default
    table.add_row(
        "embedded-fast-semantic-v1",
        "Deterministic Embedded NLP",
        "[green]Active (Built-in)[/green]",
        "ipl run <file.ipl> (default)"
    )

    if models:
        for m in models:
            table.add_row(
                m,
                "Local Neural LLM (Ollama)",
                "[bold green]Available (Local)[/bold green]",
                f"ipl run <file.ipl> --model {m}"
            )
    else:
        table.add_row(
            "[dim]No local Ollama models detected[/dim]",
            "-",
            "[dim]Offline[/dim]",
            "Start Ollama at http://localhost:11434"
        )

    console.print(table)
    console.print("\n[dim]To use a local neural model, pass [bold cyan]--model <name>[/bold cyan] or set [bold cyan]export IPL_MODEL=<name>[/bold cyan][/dim]")


def verify_file(filepath: str):
    console = Console()
    if not os.path.exists(filepath):
        console.print(f"[bold red]File not found:[/bold red] {filepath}")
        sys.exit(1)

    print_banner(console)
    console.print(f"[bold cyan]🔍 Mathematical Firewall Verification:[/bold cyan] {filepath}\n")

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        is_valid, violations = MathematicalFirewall.verify_tree(program)
        if is_valid:
            console.print(Panel(
                f"[bold green]✔ PASSED: Formal Mathematical Firewall Verification Succeeded[/bold green]\n"
                f"[dim]Total AST Statements:[/dim] {len(program.statements)}\n"
                f"[dim]Safety Invariants:[/dim] 100% compliant with Safe Primitives schema.\n"
                f"[dim]Injection Vectors:[/dim] 0 forbidden operations detected.",
                title="Firewall Audit Status",
                border_style="green"
            ))
        else:
            console.print(Panel(
                f"[bold red]✘ BLOCKED: Mathematical Firewall Contract Breaches Detected[/bold red]\n"
                + "\n".join(f"  • [yellow]{v}[/yellow]" for v in violations),
                title="Firewall Rejection",
                border_style="red"
            ))
            sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Verification Error:[/bold red] {e}")
        sys.exit(1)


def compile_file(filepath: str):
    console = Console()
    if not os.path.exists(filepath):
        console.print(f"[bold red]File not found:[/bold red] {filepath}")
        sys.exit(1)

    print_banner(console)
    console.print(f"[bold cyan]⚡ Neuro-Symbolic Compilation:[/bold cyan] {filepath}\n")

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        is_valid, violations = MathematicalFirewall.verify_tree(program)
        if not is_valid:
            console.print(f"[bold red]Compilation Failed: Mathematical Firewall violations:[/bold red]")
            for v in violations:
                console.print(f"  • {v}")
            sys.exit(1)

        # Static inspection
        fn_count = sum(1 for s in program.statements if isinstance(s, FunctionDef))
        console.print(Panel(
            f"[bold green]✔ Compilation Successful[/bold green]\n"
            f"[dim]Parsed AST Statements:[/dim] {len(program.statements)}\n"
            f"[dim]Defined Functions:[/dim] {fn_count}\n"
            f"[dim]Zero-Trust Taint Schema:[/dim] Validated\n"
            f"[dim]Target Runtime:[/dim] IPL Deterministic Neuro-Symbolic VM",
            title="Compilation Report",
            border_style="cyan"
        ))
    except Exception as e:
        console.print(f"[bold red]Compilation Error:[/bold red] {e}")
        sys.exit(1)


def start_repl(model_name: Optional[str] = None):
    console = Console()
    print_banner(console)
    model_disp = model_name or os.environ.get("IPL_MODEL", "embedded-fast-semantic-v1")
    console.print(f"[green]Welcome to the Interactive IPL REPL.[/green] [dim](AI Model: {model_disp})[/dim]")
    console.print("[dim]Type statements like 'let x: Currency = \"twenty bucks\"', 'print x for \"executive\"', or 'exit'.[/dim]\n")

    interpreter = Interpreter(console=console, model_name=model_name)

    while True:
        try:
            line = input("ipl> ").strip()
            if not line:
                continue
            if line.lower() in ("exit", "quit", ":q"):
                console.print("[dim]Exiting IPL REPL. Farewell![/dim]")
                break
            if line.lower() == "help":
                console.print(
                    "[bold]Examples to try:[/bold]\n"
                    "  let item = 'Quantum Laptop'\n"
                    "  let cost: Currency = 'ninety-nine bucks and 50 cents'\n"
                    "  let review: Sentiment = 'Absolutely fantastic build, super fast!'\n"
                    "  let age: Int = intent 'extract user_age twenty-five' as Int\n"
                    "  let clean_age = sanitize(age)\n"
                    "  db_write('users', clean_age)\n"
                    "  audit_trace()\n"
                    "  print cost for 'executive'\n"
                )
                continue

            run_source(line, interpreter, console)
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Session terminated.[/dim]")
            break


def main():
    console = Console()
    if len(sys.argv) < 2:
        start_repl()
        return

    # Extract optional --model flag
    args = list(sys.argv[1:])
    model_name = None
    if "--model" in args:
        m_idx = args.index("--model")
        if m_idx + 1 < len(args):
            model_name = args[m_idx + 1]
            del args[m_idx:m_idx + 2]

    cmd = args[0] if args else "help"
    if cmd in ("models", "list-models"):
        list_models()
    elif cmd in ("run", "exec") and len(args) >= 2:
        run_file(args[1], model_name=model_name)
    elif cmd in ("audit", "trace") and len(args) >= 2:
        run_file(args[1], show_audit=True, model_name=model_name)
    elif cmd in ("verify", "check") and len(args) >= 2:
        verify_file(args[1])
    elif cmd in ("compile", "build") and len(args) >= 2:
        compile_file(args[1])
    elif cmd in ("repl", "interactive"):
        start_repl(model_name=model_name)
    elif cmd in ("help", "--help", "-h"):
        print_banner(console)
        console.print(
            "[bold]Usage:[/bold]\n"
            "  ipl run <script.ipl> [--model <name>]   Execute an IPL source file\n"
            "  ipl audit <script.ipl> [--model <name>] Execute and print cryptographic audit trace\n"
            "  ipl models                              List available local neural models (Ollama)\n"
            "  ipl verify <script.ipl>                 Validate AST via Mathematical Firewall\n"
            "  ipl compile <script.ipl>                Compile and inspect AST contract readiness\n"
            "  ipl repl [--model <name>]               Start interactive REPL\n"
        )
    else:
        # Default assume it's a file if exists
        if os.path.exists(cmd):
            run_file(cmd, model_name=model_name)
        else:
            console.print(f"[red]Unknown command or file: {cmd}[/red]")
            console.print("Run 'ipl --help' for usage.")


if __name__ == "__main__":
    main()
