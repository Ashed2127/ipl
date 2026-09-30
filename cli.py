"""
Command-line interface (CLI) and REPL for IPL (Intelligent Programming Language / Aether).
"""
import sys
import os
import time
from typing import Optional, List, Dict, Any
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
except (ImportError, ValueError):
    from lexer import Lexer, LexerError
    from parser import Parser, ParserError
    from runtime import Interpreter
    from compiler import MathematicalFirewall, NeuroSymbolicCompiler, LocalInferenceRuntime
    from ast_nodes import FunctionDef, IntentExpr, SanitizationNode


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
        interpreter.run(program, source_code=source, current_file=filename)  # Pass source code for security analysis
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


def _print_ai_stats(console: Console, stats: Dict[str, Any]):
    """Print hierarchical AI engine statistics."""
    from rich.table import Table
    from rich.panel import Panel
    
    # Overall statistics
    console.print(Panel(f"[bold green]Total Requests:[/bold green] {stats.get('total_requests', 0)}", title="AI Engine Overview"))
    
    # Tier usage
    tier_table = Table(title="Model Tier Usage", border_style="cyan")
    tier_table.add_column("Tier", style="bold")
    tier_table.add_column("Requests", style="green")
    tier_table.add_column("Percentage", style="yellow")
    
    total = sum(stats.get('tier_usage', {}).values())
    for tier, count in stats.get('tier_usage', {}).items():
        percentage = (count / total * 100) if total > 0 else 0
        tier_table.add_row(tier, str(count), f"{percentage:.1f}%")
    
    console.print(tier_table)
    
    # Token statistics
    token_stats = stats.get('token_statistics', {})
    console.print(Panel(
        f"[bold green]Total Tokens:[/bold green] {token_stats.get('total_tokens_used', 0)}\n"
        f"[bold green]Total Cost:[/bold green] ${token_stats.get('total_cost_usd', 0.0):.4f}\n"
        f"[bold green]Avg Tokens/Request:[/bold green] {token_stats.get('average_tokens_per_request', 0):.1f}",
        title="Token Usage & Cost"
    ))
    
    # Cache statistics
    cache_stats = stats.get('cache_statistics', {})
    console.print(Panel(
        f"[bold green]Cache Hit Rate:[/bold green] {cache_stats.get('hit_rate', 0.0):.1%}\n"
        f"[bold green]Cache Size:[/bold green] {cache_stats.get('cache_size', 0)}/{cache_stats.get('max_size', 0)}\n"
        f"[bold green]Hits:[/bold green] {cache_stats.get('hit_count', 0)} | [bold red]Misses:[/bold red] {cache_stats.get('miss_count', 0)}",
        title="Intelligent Cache Performance"
    ))


                
                if auth_system.add_user(username, password, role):
                    console.print(f"[green]✓ User '{username}' added successfully as {role.name}.[/green]")
                else:
                    console.print(f"[red]✗ Failed to add user '{username}'. User may already exist.[/red]")
            
            elif choice == "3":
                username = input("Enter username to delete: ").strip()
                if auth_system.delete_user(username):
                    console.print(f"[green]✓ User '{username}' deleted successfully.[/green]")
                else:
                    console.print(f"[red]✗ Failed to delete user '{username}'. User may not exist.[/red]")
            
            elif choice == "4":
                username = input("Enter username: ").strip()
                console.print("[bold]Available Roles:[/bold]")
                console.print("  1. GUEST")
                console.print("  2. USER")
                console.print("  3. ADMIN")
                console.print("  4. SUPER_ADMIN")
                
                role_choice = input("Select new role (1-4): ").strip()
                role_map = {
                    "1": UserRole.GUEST,
                    "2": UserRole.USER,
                    "3": UserRole.ADMIN,
                    "4": UserRole.SUPER_ADMIN
                }
                
                if role_choice not in role_map:
                    console.print("[red]Invalid role selection.[/red]")
                    continue
                
                role = role_map[role_choice]
                if auth_system.update_user_role(username, role):
                    console.print(f"[green]✓ User '{username}' role updated to {role.name}.[/green]")
                else:
                    console.print(f"[red]✗ Failed to update user '{username}' role. User may not exist.[/red]")
            
            elif choice == "5":
                username = input("Enter username: ").strip()
                user_info = auth_system.get_user_info(username)
                if user_info:
                    console.print(f"[bold cyan]User: {username}[/bold cyan]")
                    console.print(f"Role: {user_info['role']}")
                    console.print(f"Permissions: {', '.join(user_info['permissions'])}")
                else:
                    console.print(f"[red]User '{username}' not found.[/red]")
            
            elif choice == "6":
                console.print("[dim]Exiting user management.[/dim]")
                break
            
            else:
                console.print("[red]Invalid option. Please select 1-6.[/red]")
        
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]User management terminated.[/dim]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


def run_file(filepath: str, show_audit: bool = False, model_name: Optional[str] = None, use_hierarchical_ai: bool = True, enable_authorization: bool = True, tier3_model: Optional[str] = None, username: Optional[str] = None, role_name: Optional[str] = None):
    console = Console()
    if not os.path.exists(filepath):
        console.print(f"[bold red]File not found:[/bold red] {filepath}")
        sys.exit(1)

    print_banner(console)
    model_disp = model_name or os.environ.get("IPL_MODEL", "embedded-fast-semantic-v1")
    ai_mode = "Hierarchical AI Engine" if use_hierarchical_ai else "Traditional Processing"
    user_disp = username or "developer"
    role_disp = role_name or ("admin" if not username else "user")
    auth_mode = f"Enabled (User: {user_disp}, Role: {role_disp})" if enable_authorization else "Disabled"
    tier3_disp = tier3_model or os.environ.get("IPL_TIER3_MODEL", "qwen2.5-coder:0.5b")
    console.print(f"[dim]Executing: {filepath} | AI Model: [bold cyan]{model_disp}[/bold cyan] | Mode: [bold green]{ai_mode}[/bold green] | Auth: [bold yellow]{auth_mode}[/bold yellow] | Tier 3: [bold magenta]{tier3_disp}[/bold magenta][/dim]\n")

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    interpreter = Interpreter(console=console, model_name=model_name, use_hierarchical_ai=use_hierarchical_ai, enable_authorization=enable_authorization, tier3_model=tier3_model)
    if enable_authorization and (username or role_name):
        role_map = {
            "guest": UserRole.GUEST,
            "user": UserRole.USER,
            "admin": UserRole.ADMIN,
            "super_admin": UserRole.SUPER_ADMIN
        }
        target_role = role_map.get((role_name or "admin").lower(), UserRole.ADMIN)
        try:
            from authorization_system import SecurityContext, Permission
        except ImportError:
            from .authorization_system import SecurityContext, Permission
        perms = set(Permission) if target_role in (UserRole.ADMIN, UserRole.SUPER_ADMIN) else ({Permission.READ, Permission.WRITE} if target_role == UserRole.USER else {Permission.READ})
        interpreter.compiler.system1.set_security_context_direct(SecurityContext(
            user_id=username or "developer",
            role=target_role,
            permissions=perms,
            session_id="cli_session"
        ))
    start_time = time.perf_counter()
    success = run_source(source, interpreter, console, filename=filepath)
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    if show_audit:
        console.print("\n[bold cyan]─── Cryptographic Verified Audit Trace ───[/bold cyan]")
        interpreter.compiler.audit_trace.render_table(console)
        
        # Show AI engine statistics if hierarchical AI is enabled
        if use_hierarchical_ai:
            console.print("\n[bold cyan]─── Hierarchical AI Engine Statistics ───[/bold cyan]")
            ai_stats = interpreter.compiler.get_ai_engine_statistics()
            _print_ai_stats(console, ai_stats)
        
        # Show authorization statistics if enabled
        if enable_authorization:
            console.print("\n[bold cyan]─── Authorization System Statistics ───[/bold cyan]")
            auth_stats = interpreter.compiler.get_authorization_statistics()
            _print_auth_stats(console, auth_stats)

    if success:
        console.print(f"\n[dim]⚡ Execution time: [bold green]{elapsed_ms:.2f} ms[/bold green][/dim]")
    else:
        console.print(f"\n[dim]⚡ Execution halted after [bold red]{elapsed_ms:.2f} ms[/bold red][/dim]")


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


def start_repl(model_name: Optional[str] = None, use_hierarchical_ai: bool = True, enable_authorization: bool = True, tier3_model: Optional[str] = None):
    console = Console()
    print_banner(console)
    model_disp = model_name or os.environ.get("IPL_MODEL", "embedded-fast-semantic-v1")
    ai_mode = "Hierarchical AI Engine" if use_hierarchical_ai else "Traditional Processing"
    auth_mode = "Enabled" if enable_authorization else "Disabled"
    tier3_disp = tier3_model or os.environ.get("IPL_TIER3_MODEL", "qwen2.5-coder:0.5b")
    console.print(f"[green]Welcome to the Interactive IPL REPL.[/green] [dim](AI Model: {model_disp} | Mode: {ai_mode} | Auth: {auth_mode} | Tier 3: {tier3_disp})[/dim]")
    console.print("[dim]Type statements like 'let x: Currency = \"twenty bucks\"', 'print x for \"executive\"', or 'exit'.[/dim]\n")

    interpreter = Interpreter(console=console, model_name=model_name, use_hierarchical_ai=use_hierarchical_ai, enable_authorization=enable_authorization, tier3_model=tier3_model)

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
                    "  authenticate('username', 'password')  # Login (if auth enabled)\n"
                    "  auth_stats()  # Show authorization statistics\n"
                    "  auth_log()    # Show authorization audit log\n"
                )
                continue

            start_time = time.perf_counter()
            success = run_source(line, interpreter, console)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            if success:
                console.print(f"[dim]⚡ {elapsed_ms:.2f} ms[/dim]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Session terminated.[/dim]")
            break


def main():
    console = Console()
    if len(sys.argv) < 2:
        start_repl()
        return

    # Extract optional flags
    args = list(sys.argv[1:])
    model_name = None
    use_hierarchical_ai = True
    enable_authorization = True
    tier3_model = None
    
    if "--model" in args:
        m_idx = args.index("--model")
        if m_idx + 1 < len(args):
            model_name = args[m_idx + 1]
            del args[m_idx:m_idx + 2]
    
    if "--no-hierarchical-ai" in args:
        use_hierarchical_ai = False
        args.remove("--no-hierarchical-ai")
    
    if "--traditional" in args:
        use_hierarchical_ai = False
        args.remove("--traditional")
    
    if "--no-authorization" in args:
        enable_authorization = False
        args.remove("--no-authorization")
    
    if "--tier3-model" in args:
        model_idx = args.index("--tier3-model")
        if model_idx + 1 < len(args):
            tier3_model = args[model_idx + 1]
            del args[model_idx:model_idx + 2]

    username = None
    role_name = None
    if "--user" in args:
        u_idx = args.index("--user")
        if u_idx + 1 < len(args):
            username = args[u_idx + 1]
            del args[u_idx:u_idx + 2]

    if "--role" in args:
        r_idx = args.index("--role")
        if r_idx + 1 < len(args):
            role_name = args[r_idx + 1]
            del args[r_idx:r_idx + 2]

    cmd = args[0] if args else "help"
    if cmd in ("models", "list-models"):
        list_models()
    elif cmd in ("users", "user-management", "manage-users"):
        manage_users()
    elif cmd in ("run", "exec") and len(args) >= 2:
        run_file(args[1], model_name=model_name, use_hierarchical_ai=use_hierarchical_ai, enable_authorization=enable_authorization, tier3_model=tier3_model, username=username, role_name=role_name)
    elif cmd in ("audit", "trace") and len(args) >= 2:
        run_file(args[1], show_audit=True, model_name=model_name, use_hierarchical_ai=use_hierarchical_ai, enable_authorization=enable_authorization, tier3_model=tier3_model, username=username, role_name=role_name)
    elif cmd in ("verify", "check") and len(args) >= 2:
        verify_file(args[1])
    elif cmd in ("compile", "build") and len(args) >= 2:
        compile_file(args[1])
    elif cmd in ("serve", "gateway"):
        host = "0.0.0.0"
        port = 8000
        if "--host" in args:
            h_idx = args.index("--host")
            if h_idx + 1 < len(args):
                host = args[h_idx + 1]
        if "--port" in args:
            p_idx = args.index("--port")
            if p_idx + 1 < len(args):
                try:
                    port = int(args[p_idx + 1])
                except ValueError:
                    console.print(f"[red]Invalid port number: {args[p_idx + 1]}[/red]")
                    sys.exit(1)
        try:
            from .gateway import run_gateway
        except (ImportError, ValueError):
            try:
                from gateway import run_gateway
            except ImportError:
                run_gateway = None

        if run_gateway is None:
            console.print("[red]Gateway module not available. Please install starlette and uvicorn.[/red]")
            sys.exit(1)
        run_gateway(host=host, port=port)
    elif cmd in ("repl", "interactive"):
        start_repl(model_name=model_name, use_hierarchical_ai=use_hierarchical_ai, enable_authorization=enable_authorization, tier3_model=tier3_model)
    elif cmd in ("help", "--help", "-h"):
        print_banner(console)
        console.print(
            "[bold]Usage:[/bold]\n"
            "  ipl run <script.ipl> [--model <name>] [--no-hierarchical-ai] [--no-authorization]   Execute an IPL source file\n"
            "  ipl audit <script.ipl> [--model <name>] [--no-hierarchical-ai] [--no-authorization] Execute and print cryptographic audit trace\n"
            "  ipl models                              List available local neural models (Ollama)\n"
            "  ipl users                               User management system\n"
            "  ipl verify <script.ipl>                 Validate AST via Mathematical Firewall\n"
            "  ipl compile <script.ipl>                Compile and inspect AST contract readiness\n"
            "  ipl serve [--host H] [--port P]         Launch REST API Security Gateway\n"
            "  ipl repl [--model <name>] [--no-hierarchical-ai] [--no-authorization]               Start interactive REPL\n"
            "\n[bold]Hierarchical AI Options:[/bold]\n"
            "  --no-hierarchical-ai                   Disable hierarchical AI engine (use traditional processing)\n"
            "  --traditional                           Same as --no-hierarchical-ai\n"
            "\n[bold]Authorization Options:[/bold]\n"
            "  --no-authorization                      Disable authorization system\n"
            "  --user <username>                       Run as specific user (default: developer)\n"
            "  --role <guest|user|admin|super_admin>   Run under specific role (default: admin)\n"
        )
    else:
        # Default assume it's a file if exists
        if os.path.exists(cmd):
            run_file(cmd, model_name=model_name, use_hierarchical_ai=use_hierarchical_ai, enable_authorization=enable_authorization)
        else:
            console.print(f"[red]Unknown command or file: {cmd}[/red]")
            console.print("Run 'ipl --help' for usage.")


if __name__ == "__main__":
    main()
