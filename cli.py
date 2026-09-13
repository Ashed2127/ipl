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
except (ImportError, ValueError):
    from lexer import Lexer, LexerError
    from parser import Parser, ParserError
    from runtime import Interpreter


def print_banner(console: Console):
    banner_text = (
        "[bold cyan]⚡ IPL (Intelligent Programming Language / Aether)[/bold cyan]\n"
        "[dim]A Neuro-Symbolic Language with Intelligent Variables & Adaptive Print[/dim]\n"
        "[dim]Built for Pair Programming with DeepMind AI Systems Architecture[/dim]"
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


def run_file(filepath: str):
    console = Console()
    if not os.path.exists(filepath):
        console.print(f"[bold red]File not found:[/bold red] {filepath}")
        sys.exit(1)

    print_banner(console)
    console.print(f"[dim]Executing: {filepath}[/dim]\n")

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    interpreter = Interpreter(console=console)
    run_source(source, interpreter, console, filename=filepath)


def start_repl():
    console = Console()
    print_banner(console)
    console.print("[green]Welcome to the Interactive IPL REPL.[/green]")
    console.print("[dim]Type statements like 'let x: Currency = \"twenty bucks\"', 'print x for \"executive\"', or 'exit'.[/dim]\n")

    interpreter = Interpreter(console=console)

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
                    "  print cost for 'executive'\n"
                    "  print cost for 'child'\n"
                    "  print review as sentiment\n"
                    "  print cot  (test self-healing typo resolution!)\n"
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

    cmd = sys.argv[1]
    if cmd in ("run", "exec") and len(sys.argv) >= 3:
        run_file(sys.argv[2])
    elif cmd in ("repl", "interactive"):
        start_repl()
    elif cmd in ("help", "--help", "-h"):
        print_banner(console)
        console.print(
            "[bold]Usage:[/bold]\n"
            "  python3 -m ipl_lang.cli run <script.ipl>   Execute an IPL source file\n"
            "  python3 -m ipl_lang.cli repl               Start interactive REPL\n"
        )
    else:
        # Default assume it's a file if exists
        if os.path.exists(cmd):
            run_file(cmd)
        else:
            console.print(f"[red]Unknown command or file: {cmd}[/red]")
            console.print("Run 'python3 -m ipl_lang.cli --help' for usage.")


if __name__ == "__main__":
    main()
