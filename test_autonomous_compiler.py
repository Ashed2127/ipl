"""
Test script to demonstrate the Intelligent Autonomous Decision Engine in IPL.
Shows how IPL uses Neural Networks and Continual Learning to decide what's good or bad.
"""

from lexer import Lexer
from parser import Parser
from compiler import NeuroSymbolicCompiler, AutonomousFirewall
from autonomous_decision_engine import DecisionType, DecisionOutcome, AutonomousDecisionEngine
from rich.console import Console
from rich.panel import Panel
import time

console = Console()

def test_intelligent_learning():
    """Demonstrate the intelligent learning capabilities"""

    console.print(Panel.fit(
        "[bold cyan]IPL Intelligent Autonomous Decision Engine[/bold cyan]\n"
        "Using Neural Networks, Continual Learning, and ML Heuristics\n"
        "NO hardcoded rules - TRUE INTELLIGENCE",
        border_style="cyan"
    ))

    # Initialize the intelligent engine
    console.print("\n[bold yellow]Initializing Intelligent Decision Engine...[/bold yellow]")
    engine = AutonomousDecisionEngine(
        experience_buffer_size=1000,
        learning_rate=0.01,
        exploration_rate=0.15,
        use_intelligent_components=True  # Enable Neural Networks and Continual Learning
    )
    console.print("[green]✓ Neural Networks initialized[/green]")
    console.print("[green]✓ Continual Learning (EWC) initialized[/green]")
    console.print("[green]✓ Heuristic Learner initialized[/green]")

    # Test scenarios
    test_contexts = [
        {
            'name': 'Safe code with no untrusted data',
            'context': {
                'num_nodes': 5,
                'num_edges': 4,
                'avg_degree': 1.6,
                'has_untrusted_data': 0,
                'has_sanitization': 0,
                'taint_propagation_steps': 0,
            }
        },
        {
            'name': 'Code with untrusted data (no sanitization)',
            'context': {
                'num_nodes': 10,
                'num_edges': 8,
                'avg_degree': 1.6,
                'has_untrusted_data': 1,
                'has_sanitization': 0,
                'taint_propagation_steps': 5,
            }
        },
        {
            'name': 'Code with untrusted data (with sanitization)',
            'context': {
                'num_nodes': 12,
                'num_edges': 10,
                'avg_degree': 1.7,
                'has_untrusted_data': 1,
                'has_sanitization': 1,
                'taint_propagation_steps': 2,
            }
        },
    ]

    console.print("\n" + "="*60)
    console.print("[bold cyan]Phase 1: Initial Decisions (Before Learning)[/bold cyan]")
    console.print("="*60)

    decisions = []
    for test in test_contexts:
        console.print(f"\n[bold yellow]Scenario: {test['name']}[/bold yellow]")

        judgment = engine.judge_safety(test['context'])
        console.print(f"  Is Safe: {judgment.is_safe}")
        console.print(f"  Confidence: {judgment.confidence:.3f}")
        console.print(f"  Threat Level: {judgment.threat_level:.3f}")
        console.print(f"  Reasoning: {judgment.reasoning}")
        console.print(f"  Learned From: {', '.join(judgment.learned_from)}")

        # Record decision
        from autonomous_decision_engine import Decision
        decision = Decision(
            decision_id=f"dec_{int(time.time()*1000)}",
            decision_type=DecisionType.SECURITY,
            context=test['context'],
            action=judgment.is_safe,
            confidence=judgment.confidence,
            timestamp=time.time()
        )
        decisions.append((decision, test['context']))

    console.print("\n" + "="*60)
    console.print("[bold cyan]Phase 2: Learning from Outcomes[/bold cyan]")
    console.print("[dim]The Neural Networks will learn from these outcomes...[/dim]")
    console.print("="*60)

    # Simulate outcomes and train
    outcomes = [
        DecisionOutcome.GOOD,   # Safe code is good
        DecisionOutcome.BAD,    # Untrusted without sanitization is bad
        DecisionOutcome.GOOD,   # Untrusted with sanitization is good
    ]

    for i, (decision, context) in enumerate(decisions):
        outcome = outcomes[i]
        reward = 1.0 if outcome == DecisionOutcome.GOOD else -1.0

        console.print(f"\nDecision {i+1}: {outcome.value} (reward: {reward})")
        engine.record_outcome(decision, outcome, reward)
        console.print(f"  [dim]Neural Network weights updated via backpropagation[/dim]")
        console.print(f"  [dim]Fisher Information computed for Continual Learning[/dim]")

    console.print("\n" + "="*60)
    console.print("[bold cyan]Phase 3: Retesting After Learning[/bold cyan]")
    console.print("[dim]The Neural Networks have now learned from experience[/dim]")
    console.print("="*60)

    for test in test_contexts:
        console.print(f"\n[bold yellow]Scenario: {test['name']}[/bold yellow]")

        judgment = engine.judge_safety(test['context'])
        console.print(f"  Is Safe: {judgment.is_safe}")
        console.print(f"  Confidence: {judgment.confidence:.3f}")
        console.print(f"  Threat Level: {judgment.threat_level:.3f}")
        console.print(f"  Reasoning: {judgment.reasoning}")

    # Show statistics
    stats = engine.get_statistics()
    console.print("\n" + "="*60)
    console.print("[bold cyan]Intelligent Engine Statistics[/bold cyan]")
    console.print("="*60)
    console.print(f"  Total decisions: {stats['total_decisions']}")
    console.print(f"  Good decisions: {stats['good_decisions']}")
    console.print(f"  Bad decisions: {stats['bad_decisions']}")
    console.print(f"  Success rate: {stats['success_rate']:.2%}")
    console.print(f"  Learned dangerous patterns: {stats['learned_dangerous_patterns']}")
    console.print(f"  Learned safe patterns: {stats['learned_safe_patterns']}")
    console.print(f"  Training samples collected: {len(engine.training_X)}")

    console.print("\n" + "="*60)
    console.print("[bold green]Intelligent Learning Demo Complete![/bold green]")
    console.print("[dim]IPL uses Neural Networks and Continual Learning - TRUE INTELLIGENCE![/dim]")
    console.print("[dim]Not simple hardcoded code - it learns from experience![/dim]")

if __name__ == "__main__":
    test_intelligent_learning()
