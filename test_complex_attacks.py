"""
Complex Real-World Security Test
Tests IPL against sophisticated attack patterns and edge cases.
"""

from autonomous_decision_engine import AutonomousDecisionEngine, Decision, DecisionType, DecisionOutcome
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import time

console = Console()

def test_complex_attacks():
    """Test against complex and sophisticated attacks"""

    console.print(Panel.fit(
        "[bold red]COMPLEX REAL-WORLD SECURITY TEST[/bold red]\n"
        "Testing against sophisticated attacks and edge cases",
        border_style="red"
    ))

    # Initialize the intelligent engine
    engine = AutonomousDecisionEngine(
        experience_buffer_size=1000,
        learning_rate=0.01,
        exploration_rate=0.05,  # Lower exploration for more exploitation
        use_intelligent_components=True
    )

    # Complex attack scenarios
    scenarios = [
        {
            'name': 'Second-Order SQL Injection',
            'description': 'SQL injection via stored procedure',
            'context': {
                'num_nodes': 25,
                'num_edges': 35,
                'avg_degree': 2.8,
                'has_untrusted_data': 1,
                'has_sanitization': 0,
                'taint_propagation_steps': 15,
                'execution_count': 50,
                'avg_execution_time_ms': 5.0,
            },
            'expected': DecisionOutcome.BAD,
        },
        {
            'name': 'Blind SQL Injection',
            'description': 'SQL injection without direct output',
            'context': {
                'num_nodes': 20,
                'num_edges': 28,
                'avg_degree': 2.8,
                'has_untrusted_data': 1,
                'has_sanitization': 0,
                'taint_propagation_steps': 10,
                'execution_count': 100,
                'avg_execution_time_ms': 10.0,
            },
            'expected': DecisionOutcome.BAD,
        },
        {
            'name': 'DOM-based XSS',
            'description': 'XSS via DOM manipulation',
            'context': {
                'num_nodes': 30,
                'num_edges': 40,
                'avg_degree': 2.7,
                'has_untrusted_data': 1,
                'has_sanitization': 0,
                'taint_propagation_steps': 20,
                'execution_count': 200,
                'avg_execution_time_ms': 15.0,
            },
            'expected': DecisionOutcome.BAD,
        },
        {
            'name': 'Multi-level Sanitization',
            'description': 'Properly sanitized with multiple layers',
            'context': {
                'num_nodes': 35,
                'num_edges': 45,
                'avg_degree': 2.6,
                'has_untrusted_data': 1,
                'has_sanitization': 1,
                'taint_propagation_steps': 1,
                'execution_count': 500,
                'avg_execution_time_ms': 20.0,
            },
            'expected': DecisionOutcome.GOOD,
        },
        {
            'name': 'Time-based Blind SQL Injection',
            'description': 'SQL injection using timing attacks',
            'context': {
                'num_nodes': 22,
                'num_edges': 30,
                'avg_degree': 2.7,
                'has_untrusted_data': 1,
                'has_sanitization': 0,
                'taint_propagation_steps': 12,
                'execution_count': 1000,
                'avg_execution_time_ms': 50.0,
            },
            'expected': DecisionOutcome.BAD,
        },
        {
            'name': 'Stored XSS',
            'description': 'XSS stored in database',
            'context': {
                'num_nodes': 28,
                'num_edges': 38,
                'avg_degree': 2.7,
                'has_untrusted_data': 1,
                'has_sanitization': 0,
                'taint_propagation_steps': 18,
                'execution_count': 75,
                'avg_execution_time_ms': 8.0,
            },
            'expected': DecisionOutcome.BAD,
        },
        {
            'name': 'Safe with Parameterized Query',
            'description': 'Safe parameterized SQL query',
            'context': {
                'num_nodes': 40,
                'num_edges': 55,
                'avg_degree': 2.75,
                'has_untrusted_data': 1,
                'has_sanitization': 1,
                'taint_propagation_steps': 0,
                'execution_count': 1000,
                'avg_execution_time_ms': 25.0,
            },
            'expected': DecisionOutcome.GOOD,
        },
        {
            'name': 'CSRF Token Bypass Attempt',
            'description': 'Attempt to bypass CSRF protection',
            'context': {
                'num_nodes': 18,
                'num_edges': 24,
                'avg_degree': 2.7,
                'has_untrusted_data': 1,
                'has_sanitization': 0,
                'taint_propagation_steps': 8,
                'execution_count': 10,
                'avg_execution_time_ms': 3.0,
            },
            'expected': DecisionOutcome.BAD,
        },
    ]

    console.print(f"\n[bold yellow]Testing {len(scenarios)} complex attack scenarios...[/bold yellow]")

    # Initial test (before learning)
    table = Table(title="Initial Detection (Before Learning)")
    table.add_column("Attack Type", style="cyan")
    table.add_column("Detected", style="bold")
    table.add_column("Confidence", style="yellow")
    table.add_column("Threat", style="red")
    table.add_column("Correct", style="green")

    decisions = []
    initial_correct = 0

    for scenario in scenarios:
        judgment = engine.judge_safety(scenario['context'])
        is_safe = judgment.is_safe
        expected_safe = scenario['expected'] == DecisionOutcome.GOOD
        is_correct = (is_safe == expected_safe)

        if is_correct:
            initial_correct += 1

        decision = Decision(
            decision_id=f"complex_{int(time.time()*1000)}",
            decision_type=DecisionType.SECURITY,
            context=scenario['context'],
            action=is_safe,
            confidence=judgment.confidence,
            timestamp=time.time()
        )
        decisions.append((decision, scenario['expected']))

        detected_str = "[green]BLOCKED[/green]" if not is_safe else "[red]ALLOWED[/red]"
        correct_str = "[green]✓[/green]" if is_correct else "[red]✗[/red]"
        table.add_row(
            scenario['name'],
            detected_str,
            f"{judgment.confidence:.3f}",
            f"{judgment.threat_level:.3f}",
            correct_str
        )

    console.print("\n")
    console.print(table)
    console.print(f"\nInitial Accuracy: {initial_correct}/{len(scenarios)} ({initial_correct/len(scenarios):.1%})")

    # Learn from outcomes
    console.print("\n" + "="*60)
    console.print("[bold yellow]Learning from Complex Attack Outcomes[/bold yellow]")
    console.print("="*60)

    for decision, expected in decisions:
        is_correct = (decision.action and expected == DecisionOutcome.GOOD) or \
                    (not decision.action and expected == DecisionOutcome.BAD)
        outcome = DecisionOutcome.GOOD if is_correct else DecisionOutcome.BAD
        reward = 1.0 if is_correct else -1.0

        engine.record_outcome(decision, outcome, reward)

    # Retest after learning
    console.print("\n" + "="*60)
    console.print("[bold yellow]Retest After Learning[/bold yellow]")
    console.print("="*60)

    table2 = Table(title="After Learning")
    table2.add_column("Attack Type", style="cyan")
    table2.add_column("Detected", style="bold")
    table.add_column("Confidence", style="yellow")
    table2.add_column("Threat", style="red")
    table2.add_column("Correct", style="green")

    final_correct = 0
    for scenario in scenarios:
        judgment = engine.judge_safety(scenario['context'])
        is_safe = judgment.is_safe
        expected_safe = scenario['expected'] == DecisionOutcome.GOOD
        is_correct = (is_safe == expected_safe)

        if is_correct:
            final_correct += 1

        detected_str = "[green]BLOCKED[/green]" if not is_safe else "[red]ALLOWED[/red]"
        correct_str = "[green]✓[/green]" if is_correct else "[red]✗[/red]"
        table2.add_row(
            scenario['name'],
            detected_str,
            f"{judgment.confidence:.3f}",
            f"{judgment.threat_level:.3f}",
            correct_str
        )

    console.print("\n")
    console.print(table2)
    console.print(f"\nFinal Accuracy: {final_correct}/{len(scenarios)} ({final_correct/len(scenarios):.1%})")

    # Show learned thresholds
    stats = engine.get_statistics()
    console.print("\n" + "="*60)
    console.print("[bold yellow]Learned Thresholds After Complex Testing[/bold yellow]")
    console.print("="*60)

    if 'learnable_thresholds' in stats:
        for key, value in stats['learnable_thresholds'].items():
            console.print(f"  {key}: {value:.4f}")

    console.print("\n" + "="*60)
    if final_correct >= len(scenarios) * 0.8:
        console.print("[green]✓ System successfully detects complex attacks![/green]")
    else:
        console.print("[yellow]⚠ System needs more training on complex patterns[/yellow]")
    console.print("="*60)

if __name__ == "__main__":
    test_complex_attacks()
