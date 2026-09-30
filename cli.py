#!/usr/bin/env python3
"""
IPL (Intelligent Programming Language / Aether) CLI
Symbolic Compiler Architecture & Deterministic Runtime
"""
import sys
import os
import time
from typing import Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.table import Table

try:
    from .lexer import Lexer, LexerError
    from .parser import Parser, ParserError
    from .runtime import Interpreter
    from .compiler import MathematicalFirewall, NeuroSymbolicCompiler, LocalInferenceRuntime
    from .ast_nodes import FunctionDef, IntentExpr, SanitizationNode
    from .static_taint_analyzer import analyze_program_taint
except (ImportError, ValueError):
    from lexer import Lexer, LexerError
    from parser import Parser, ParserError
    from runtime import Interpreter
    from compiler import MathematicalFirewall, NeuroSymbolicCompiler, LocalInferenceRuntime
    from ast_nodes import FunctionDef, IntentExpr, SanitizationNode
    from static_taint_analyzer import analyze_program_taint


def print_banner(console: Console):
    banner_text = (
        "[bold cyan]⚡ IPL (Intelligent Programming Language / Aether)[/bold cyan]\n"
        "[dim]Symbolic Compiler Architecture & Deterministic Runtime[/dim]\n"
        "[dim]System 1 Semantic Engine | System 2 Mathematical Firewall | Zero-Trust Taint Tracking[/dim]"
    )
    console.print(Panel(banner_text, border_style="cyan"))


def run_source(source: str, interpreter: Interpreter, console: Console, filename: str = "<stdin>") -> bool:
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter.run(program, source_code=source, current_file=filename)
        return True
    except LexerError as le:
        console.print(f"[bold red]Syntax Error:[/bold red] {le}")
        return False
    except ParserError as pe:
        console.print(f"[bold red]Parser Error:[/bold red] {pe}")
        return False
    except Exception as e:
        console.print(f"[bold red]Runtime Exception:[/bold red] {e}")
        return False


def run_file(filepath: str, show_audit: bool = False, model_name: Optional[str] = None):
    console = Console()
    if not os.path.exists(filepath):
        console.print(f"[bold red]File not found:[/bold red] {filepath}")
        sys.exit(1)

    print_banner(console)
    model_disp = model_name or os.environ.get("IPL_MODEL", "embedded-fast-semantic-v1")
    console.print(f"[dim]Executing: {filepath} | Model: [bold cyan]{model_disp}[/bold cyan][/dim]\n")

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    interpreter = Interpreter(console=console, model_name=model_name)
    start_time = time.perf_counter()
    success = run_source(source, interpreter, console, filename=filepath)
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    if show_audit:
        console.print("\n[bold cyan]─── Cryptographic Verified Audit Trace ───[/bold cyan]")
        interpreter.compiler.audit_trace.render_table(console)

    if success:
        console.print(f"\n[dim]⚡ Execution time: [bold green]{elapsed_ms:.2f} ms[/bold green][/dim]")
    else:
        console.print(f"\n[dim]⚡ Execution halted after [bold red]{elapsed_ms:.2f} ms[/bold red][/dim]")


def list_models():
    console = Console()
    print_banner(console)
    console.print("[bold cyan]🔍 Available Models[/bold cyan]\n")

    table = Table(title="🤖 Available Models", border_style="cyan")
    table.add_column("Model Name", style="bold green")
    table.add_column("Type", style="cyan")
    table.add_column("Status", style="yellow")

    table.add_row(
        "embedded-fast-semantic-v1",
        "Deterministic Embedded NLP",
        "[green]Active (Built-in)[/green]"
    )

    console.print(table)
    console.print("\n[dim]To use a model, pass [bold cyan]--model <name>[/bold cyan] or set [bold cyan]export IPL_MODEL=<name>[/bold cyan][/dim]")


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
                f"[dim]Violations:[/dim] {len(violations)}\n"
                f"[dim]Details:[/dim] {', '.join(violations)}",
                title="Firewall Audit Status",
                border_style="red"
            ))
    except Exception as e:
        console.print(f"[bold red]Verification Error:[/bold red] {e}")


def compile_file(filepath: str):
    console = Console()
    if not os.path.exists(filepath):
        console.print(f"[bold red]File not found:[/bold red] {filepath}")
        sys.exit(1)

    print_banner(console)
    console.print(f"[bold cyan]🔨 Compiling:[/bold cyan] {filepath}\n")

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        console.print(f"[green]✓ Lexical Analysis:[/green] {len(tokens)} tokens")
        console.print(f"[green]✓ Parsing:[/green] {len(program.statements)} statements")
        console.print(f"[green]✓ Compilation successful[/green]")
    except Exception as e:
        console.print(f"[bold red]Compilation Error:[/bold red] {e}")


def analyze_taint(filepath: str):
    console = Console()
    if not os.path.exists(filepath):
        console.print(f"[bold red]File not found:[/bold red] {filepath}")
        sys.exit(1)

    print_banner(console)
    console.print(f"[bold cyan]🔍 Static Taint Analysis:[/bold cyan] {filepath}\n")

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        # Run static taint analysis
        results = analyze_program_taint(program)

        # Display results
        console.print(f"[green]✓ Program parsed:[/green] {len(program.statements)} statements\n")

        # Show violations
        if results["violations"]:
            console.print(Panel(
                f"[bold red]⚠️ Static Taint Violations Detected: {len(results['violations'])}[/bold red]",
                title="Taint Analysis Results",
                border_style="red"
            ))
            table = Table(title="Static Violations", border_style="red")
            table.add_column("Sink", style="bold")
            table.add_column("Required Sink", style="cyan")
            table.add_column("Arg Index", style="yellow")
            table.add_column("Taint", style="red")
            table.add_column("Message", style="white")

            for v in results["violations"]:
                table.add_row(
                    v["sink"],
                    v["required_sink"],
                    str(v["arg_index"]),
                    v["taint"],
                    v["message"]
                )
            console.print(table)
        else:
            console.print(Panel(
                "[bold green]✓ No Static Taint Violations Detected[/bold green]",
                title="Taint Analysis Results",
                border_style="green"
            ))

        # Show static safe sites
        if results["static_safe_sites"]:
            console.print(f"\n[green]✓ Statically Verified Safe Sites: {len(results['static_safe_sites'])}[/green]")
            table = Table(title="Static Safe Sites", border_style="green")
            table.add_column("Sink", style="bold")
            table.add_column("Required Sink", style="cyan")
            table.add_column("Location", style="dim")

            for site in results["static_safe_sites"]:
                table.add_row(
                    site["sink"],
                    site["required_sink"],
                    site["location"]
                )
            console.print(table)

        # Show dynamic sites (require runtime check)
        if results["dynamic_sites"]:
            console.print(f"\n[yellow]⚡ Sites Requiring Runtime Check: {len(results['dynamic_sites'])}[/yellow]")
            table = Table(title="Dynamic Taint Check Sites", border_style="yellow")
            table.add_column("Sink", style="bold")
            table.add_column("Required Sink", style="cyan")
            table.add_column("Arg Index", style="yellow")
            table.add_column("Reason", style="white")

            for site in results["dynamic_sites"]:
                table.add_row(
                    site["sink"],
                    site["required_sink"],
                    str(site["arg_index"]),
                    site["reason"]
                )
            console.print(table)

        # Show untrusted sources
        if results["untrusted_sources"]:
            console.print(f"\n[red]⚠️ Untrusted Data Sources: {len(results['untrusted_sources'])}[/red]")
            console.print(f"[dim]Variables: {', '.join(results['untrusted_sources'])}[/dim]")

        # Show sanitized variables
        if results["sanitized_vars"]:
            console.print(f"\n[green]✓ Sanitized Variables: {len(results['sanitized_vars'])}[/green]")
            for var, sink_kind in results["sanitized_vars"].items():
                console.print(f"  [cyan]{var}[/cyan] -> [green]{sink_kind.value}[/green]")

    except Exception as e:
        console.print(f"[bold red]Analysis Error:[/bold red] {e}")
        import traceback
        traceback.print_exc()


def start_repl(model_name: Optional[str] = None):
    console = Console()
    print_banner(console)
    console.print("[dim]Type IPL code or commands. Press Ctrl+C to exit.[/dim]\n")

    interpreter = Interpreter(console=console, model_name=model_name)
    
    while True:
        try:
            source = input("ipl> ")
            if not source.strip():
                continue
            
            if source.strip() in ("exit", "quit"):
                console.print("[dim]Exiting REPL.[/dim]")
                break
            
            run_source(source, interpreter, console, filename="<repl>")
        except KeyboardInterrupt:
            console.print("\n[dim]Exiting REPL.[/dim]")
            break
        except EOFError:
            console.print("\n[dim]Exiting REPL.[/dim]")
            break


def main():
    console = Console()
    
    if len(sys.argv) < 2:
        print_banner(console)
        console.print(
            "[bold]Usage:[/bold]\n"
            "  ipl run <script.ipl> [--model <name>]           Execute an IPL source file\n"
            "  ipl audit <script.ipl> [--model <name>]         Execute and print cryptographic audit trace\n"
            "  ipl models                                   List available models\n"
            "  ipl verify <script.ipl>                      Validate AST via Mathematical Firewall\n"
            "  ipl compile <script.ipl>                     Compile and inspect AST\n"
            "  ipl repl [--model <name>]                      Start interactive REPL\n"
            "  ipl help                                     Show this help message\n"
        )
        sys.exit(0)

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
            "  ipl run <script.ipl> [--model <name>]           Execute an IPL source file\n"
            "  ipl audit <script.ipl> [--model <name>]         Execute and print cryptographic audit trace\n"
            "  ipl models                                   List available models\n"
            "  ipl verify <script.ipl>                      Validate AST via Mathematical Firewall\n"
            "  ipl compile <script.ipl>                     Compile and inspect AST\n"
            "  ipl repl [--model <name>]                      Start interactive REPL\n"
            "  ipl help                                     Show this help message\n"
        )
    else:
        console.print(f"[bold red]Unknown command:[/bold red] {cmd}")
        console.print("Run [bold cyan]ipl help[/bold cyan] for usage information")


if __name__ == "__main__":
    main()
