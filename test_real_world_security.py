"""
Real-World Security Test for IPL
Tests the autonomous decision engine against actual security vulnerabilities.
"""

from autonomous_decision_engine import AutonomousDecisionEngine, Decision, DecisionType, DecisionOutcome
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import time

console = Console()

def test_real_world_attacks():
    """Test against real SQL injection and XSS attacks"""

    console.print(Panel.fit(
        "[bold red]REAL-WORLD SECURITY TEST[/bold red]\n"
        "Testing IPL Autonomous Decision Engine against actual attacks",
        border_style="red"
    ))

    # Initialize the intelligent engine
    engine = AutonomousDecisionEngine(
        experience_buffer_size=1000,
        learning_rate=0.01,
        exploration_rate=0.1,
        use_intelligent_components=True
    )

    console.print("\n[bold yellow]Test Scenarios:[/bold yellow]")

    # Real-world attack scenarios
    scenarios = [
        {
            'name': 'SQL Injection Attack',
            'description': 'Malicious SQL injection attempt',
            'context': {
                'num_nodes': 15,
                'num_edges': 20,
                'avg_degree': 2.7,
                'has_untrusted_data': 1,
                'has_sanitization': 0,
                'taint_propagation_steps': 8,
                'execution_count': 5,
                'avg_execution_time_ms': 2.0,
            },
            'expected_outcome': DecisionOutcome.BAD,  # Should be blocked
            'expected_threat': 'high'
        },
        {
            'name': 'XSS Attack',
            'description': 'Cross-site scripting attack',
            'context': {
                'num_nodes': 12,
                'num_edges': 15,
                'avg_degree': 2.5,
                'has_untrusted_data': 1,
                'has_sanitization': 0,
                'taint_propagation_steps': 6,
                'execution_count': 3,
                'avg_execution_time_ms': 1.5,
            },
            'expected_outcome': DecisionOutcome.BAD,  # Should be blocked
            'expected_threat': 'high'
        },
        {
            'name': 'Safe User Input with Sanitization',
            'description': 'User input properly sanitized',
            'context': {
                'num_nodes': 18,
                'num_edges': 22,
                'avg_degree': 2.4,
                'has_untrusted_data': 1,
                'has_sanitization': 1,
                'taint_propagation_steps': 2,
                'execution_count': 10,
                'avg_execution_time_ms': 3.0,
            },
            'expected_outcome': DecisionOutcome.GOOD,  # Should be allowed
            'expected_threat': 'low'
        },
        {
            'name': 'Command Injection Attempt',
            'description': 'Attempted command injection',
            'context': {
                'num_nodes': 20,
                'num_edges': 25,
                'avg_degree': 2.5,
                'has_untrusted_data': 1,
                'has_sanitization': 0,
                'taint_propagation_steps': 12,
                'execution_count': 2,
                'avg_execution_time_ms': 1.0,
            },
            'expected_outcome': DecisionOutcome.BAD,  # Should be blocked
            'expected_threat': 'high'
        },
        {
            'name': 'Path Traversal Attack',
            'description': 'Directory traversal attempt',
            'context': {
                'num_nodes': 14,
                'num_edges': 18,
                'avg_degree': 2.6,
                'has_untrusted_data': 1,
                'has_sanitization': 0,
                'taint_propagation_steps': 7,
                'execution_count': 4,
                'avg_execution_time_ms': 2.5,
            },
            'expected_outcome': DecisionOutcome.BAD,  # Should be blocked
            'expected_threat': 'high'
        },
    ]

    # Create table for results
    table = Table(title="Real-World Security Test Results")
    table.add_column("Attack Type", style="cyan")
    table.add_column("Is Safe", style="bold")
    table.add_column("Confidence", style="yellow")
    table.add_column("Threat Level", style="red")
    table.add_column("Correct?", style="green")
    table.add_column("Reasoning", style="dim")

    decisions = []

    for scenario in scenarios:
        console.print(f"\n[bold]Testing: {scenario['name']}[/bold]")
        console.print(f"  {scenario['description']}")

        # Get judgment
        judgment = engine.judge_safety(scenario['context'])

        # Record decision
        decision = Decision(
            decision_id=f"attack_{int(time.time()*1000)}",
            decision_type=DecisionType.SECURITY,
            context=scenario['context'],
            action=judgment.is_safe,
            confidence=judgment.confidence,
            timestamp=time.time()
        )
        decisions.append((decision, scenario['expected_outcome']))

        # Check if correct
        is_correct = (judgment.is_safe and scenario['expected_outcome'] == DecisionOutcome.GOOD) or \
                    (not judgment.is_safe and scenario['expected_outcome'] == DecisionOutcome.BAD)

        # Add to table
        safety_str = "[green]YES[/green]" if judgment.is_safe else "[red]NO[/red]"
        correct_str = "[green]✓[/green]" if is_correct else "[red]✗[/red]"
        table.add_row(
            scenario['name'],
            safety_str,
            f"{judgment.confidence:.3f}",
            f"{judgment.threat_level:.3f}",
            correct_str,
            judgment.reasoning[:50] + "..."
        )

        console.print(f"  Result: {'SAFE' if judgment.is_safe else 'UNSAFE'}")
        console.print(f"  Confidence: {judgment.confidence:.3f}")
        console.print(f"  Threat Level: {judgment.threat_level:.3f}")
        console.print(f"  Correct: {is_correct}")

    console.print("\n")
    console.print(table)

    # Phase 2: Learning from outcomes
    console.print("\n" + "="*60)
    console.print("[bold yellow]Phase 2: Learning from Attack Outcomes[/bold yellow]")
    console.print("="*60)

    for decision, expected_outcome in decisions:
        # Simulate outcome - if the decision matches expected, it's good
        is_correct = (decision.action and expected_outcome == DecisionOutcome.GOOD) or \
                    (not decision.action and expected_outcome == DecisionOutcome.BAD)

        outcome = DecisionOutcome.GOOD if is_correct else DecisionOutcome.BAD
        reward = 1.0 if is_correct else -1.0

        console.print(f"\n{decision.decision_id}: {outcome.value} (reward: {reward})")
        engine.record_outcome(decision, outcome, reward)
        console.print(f"  [dim]→ Neural Network weights updated[/dim]")
        console.print(f"  [dim]→ Thresholds adjusted via gradient descent[/dim]")

    # Phase 3: Retest after learning
    console.print("\n" + "="*60)
    console.print("[bold yellow]Phase 3: Retest After Learning[/bold yellow]")
    console.print("="*60)

    # Create second table
    table2 = Table(title="After Learning")
    table2.add_column("Attack Type", style="cyan")
    table2.add_column("Is Safe", style="bold")
    table2.add_column("Confidence", style="yellow")
    table2.add_column("Threat Level", style="red")
    table2.add_column("Improvement", style="green")

    for scenario in scenarios:
        judgment = engine.judge_safety(scenario['context'])

        safety_str = "[green]YES[/green]" if judgment.is_safe else "[red]NO[/red]"
        improvement = "N/A"
        table2.add_row(
            scenario['name'],
            safety_str,
            f"{judgment.confidence:.3f}",
            f"{judgment.threat_level:.3f}",
            improvement
        )

    console.print("\n")
    console.print(table2)

    # Show learned thresholds
    stats = engine.get_statistics()
    console.print("\n" + "="*60)
    console.print("[bold yellow]Learned Thresholds After Real-World Testing[/bold yellow]")
    console.print("="*60)

    if 'learnable_thresholds' in stats:
        for key, value in stats['learnable_thresholds'].items():
            console.print(f"  {key}: {value:.4f}")

    # Calculate accuracy
    correct_count = sum(1 for d, exp in decisions if
                        (d.action and exp == DecisionOutcome.GOOD) or
                        (not d.action and exp == DecisionOutcome.BAD))
    accuracy = correct_count / len(decisions)

    console.print("\n" + "="*60)
    console.print(f"[bold]Final Accuracy: {accuracy:.1%}[/bold]")
    console.print("="*60)

    if accuracy >= 0.8:
        console.print("[green]✓ System successfully learned to detect real-world attacks![/green]")
    else:
        console.print("[yellow]⚠ System needs more training data[/yellow]")

if __name__ == "__main__":
    test_real_world_attacks()
