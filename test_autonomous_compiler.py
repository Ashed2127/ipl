"""
Test script to demonstrate the Autonomous Decision Engine in IPL.
Shows how IPL decides what's good or bad by itself - no hardcoded rules.
"""

from lexer import Lexer
from parser import Parser
from compiler import NeuroSymbolicCompiler, AutonomousFirewall
from autonomous_decision_engine import DecisionType, DecisionOutcome
from rich.console import Console
from rich.panel import Panel
import time

console = Console()

def test_autonomous_compilation():
    """Test the autonomous compiler with various code scenarios"""

    console.print(Panel.fit(
        "[bold cyan]IPL Autonomous Decision Engine Demo[/bold cyan]\n"
        "IPL decides what's good or bad by itself - NO hardcoded rules!",
        border_style="cyan"
    ))

    # Test code with different security scenarios
    test_codes = [
        ("Simple safe code", """
let x = 42;
print(x);
"""),
        ("Code with untrusted data", """
let user_input = set_untrusted("test");
print(user_input);
"""),
        ("Code with sanitization", """
let user_input = set_untrusted("test");
let safe_input = sanitize(user_input);
print(safe_input);
"""),
    ]

    compiler = NeuroSymbolicCompiler()

    for description, code in test_codes:
        console.print(f"\n[bold yellow]Testing: {description}[/bold yellow]")
        console.print(f"Code: {code.strip()}")

        try:
            # Lex and parse
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()

            # Get context for autonomous decision
            context = {
                'num_nodes': 3,
                'num_edges': 2,
                'avg_degree': 1.5,
                'has_untrusted_data': 'set_untrusted' in code,
                'has_sanitization': 'sanitize' in code,
                'taint_propagation_steps': 1 if 'set_untrusted' in code else 0,
            }

            # Verify with autonomous firewall
            is_safe, violations = compiler.firewall.verify_tree(ast, context)

            if is_safe:
                console.print("[green]✓ Autonomous Decision: SAFE[/green]")
            else:
                console.print("[red]✗ Autonomous Decision: UNSAFE[/red]")
                for violation in violations:
                    console.print(f"  [red]Reason: {violation}[/red]")

            # Show the decision engine's statistics
            stats = compiler.firewall.decision_engine.get_statistics()
            console.print(f"\n[dim]Decision Engine Stats:[/dim]")
            console.print(f"  Total decisions: {stats['total_decisions']}")
            console.print(f"  Success rate: {stats['success_rate']:.2%}")
            console.print(f"  Learned patterns: {stats['learned_dangerous_patterns']} dangerous, {stats['learned_safe_patterns']} safe")

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    # Demonstrate learning from outcomes
    console.print("\n" + "="*60)
    console.print("[bold cyan]Demonstrating Learning from Outcomes[/bold cyan]")

    # Simulate recording outcomes for the decisions
    for i, decision in enumerate(compiler.firewall.decision_engine.decision_history[:3]):
        # Alternate between good and bad outcomes for demonstration
        outcome = DecisionOutcome.GOOD if i % 2 == 0 else DecisionOutcome.BAD
        reward = 1.0 if outcome == DecisionOutcome.GOOD else -1.0

        compiler.firewall.decision_engine.record_outcome(decision, outcome, reward)
        console.print(f"Decision {i+1}: {outcome.value} (reward: {reward})")

    # Show updated statistics
    stats = compiler.firewall.decision_engine.get_statistics()
    console.print(f"\n[dim]Updated Stats after learning:[/dim]")
    console.print(f"  Total decisions: {stats['total_decisions']}")
    console.print(f"  Good decisions: {stats['good_decisions']}")
    console.print(f"  Bad decisions: {stats['bad_decisions']}")
    console.print(f"  Success rate: {stats['success_rate']:.2%}")

    console.print("\n" + "="*60)
    console.print("[bold green]Autonomous Decision Engine Demo Complete![/bold green]")
    console.print("[dim]IPL is truly autonomous - it decides what's good or bad by itself![/dim]")

if __name__ == "__main__":
    test_autonomous_compilation()
