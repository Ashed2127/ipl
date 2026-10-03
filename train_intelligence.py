"""
Comprehensive Training Script for IPL Intelligence
Builds experience buffer for both Autonomous Decision Engine and Load Controller
"""
import time
import random
from autonomous_decision_engine import (
    AutonomousDecisionEngine,
    Decision,
    DecisionType,
    DecisionOutcome
)
from intelligent_load_controller import IntelligentLoadController, ServerState


def train_autonomous_decision_engine():
    """Train the autonomous decision engine with diverse scenarios"""
    print("=" * 70)
    print("TRAINING AUTONOMOUS DECISION ENGINE")
    print("=" * 70)

    engine = AutonomousDecisionEngine(use_intelligent_components=True)

    # Diverse training scenarios
    scenarios = [
        # (context, expected_safe, description)
        (
            {
                'has_untrusted_data': False,
                'has_sanitization': False,
                'taint_propagation_steps': 0,
                'num_nodes': 10,
                'num_edges': 15,
                'avg_degree': 3.0,
                'execution_count': 100,
                'avg_execution_time_ms': 5.0
            },
            True,
            "Safe code with no untrusted data"
        ),
        (
            {
                'has_untrusted_data': True,
                'has_sanitization': False,
                'taint_propagation_steps': 5,
                'num_nodes': 15,
                'num_edges': 25,
                'avg_degree': 3.3,
                'execution_count': 50,
                'avg_execution_time_ms': 10.0
            },
            False,
            "Untrusted data without sanitization (dangerous)"
        ),
        (
            {
                'has_untrusted_data': True,
                'has_sanitization': True,
                'taint_propagation_steps': 3,
                'num_nodes': 20,
                'num_edges': 30,
                'avg_degree': 3.0,
                'execution_count': 200,
                'avg_execution_time_ms': 8.0
            },
            True,
            "Untrusted data with proper sanitization (safe)"
        ),
        (
            {
                'has_untrusted_data': True,
                'has_sanitization': True,
                'taint_propagation_steps': 20,
                'num_nodes': 50,
                'num_edges': 100,
                'avg_degree': 4.0,
                'execution_count': 1000,
                'avg_execution_time_ms': 50.0
            },
            False,
            "High taint propagation even with sanitization (suspicious)"
        ),
        (
            {
                'has_untrusted_data': False,
                'has_sanitization': True,
                'taint_propagation_steps': 0,
                'num_nodes': 5,
                'num_edges': 5,
                'avg_degree': 2.0,
                'execution_count': 10,
                'avg_execution_time_ms': 1.0
            },
            True,
            "Simple safe code with unnecessary sanitization"
        ),
        (
            {
                'has_untrusted_data': True,
                'has_sanitization': False,
                'taint_propagation_steps': 1,
                'num_nodes': 8,
                'num_edges': 10,
                'avg_degree': 2.5,
                'execution_count': 25,
                'avg_execution_time_ms': 3.0
            },
            False,
            "Minimal taint propagation but no sanitization"
        ),
        (
            {
                'has_untrusted_data': True,
                'has_sanitization': True,
                'taint_propagation_steps': 8,
                'num_nodes': 30,
                'num_edges': 45,
                'avg_degree': 3.0,
                'execution_count': 500,
                'avg_execution_time_ms': 15.0
            },
            True,
            "Moderate taint with sanitization (acceptable)"
        ),
        (
            {
                'has_untrusted_data': False,
                'has_sanitization': False,
                'taint_propagation_steps': 0,
                'num_nodes': 100,
                'num_edges': 200,
                'avg_degree': 4.0,
                'execution_count': 5000,
                'avg_execution_time_ms': 100.0
            },
            True,
            "Large safe program"
        ),
    ]

    # Run each scenario multiple times with variations
    print(f"\nRunning {len(scenarios)} base scenarios with variations...")
    total_decisions = 0

    for i, (context, expected_safe, description) in enumerate(scenarios):
        print(f"\nScenario {i+1}: {description}")

        # Run with slight variations
        for j in range(10):
            # Add small random variations
            varied_context = context.copy()
            varied_context['taint_propagation_steps'] = max(0, context['taint_propagation_steps'] + random.randint(-2, 2))
            varied_context['execution_count'] = max(1, context['execution_count'] + random.randint(-50, 50))
            varied_context['avg_execution_time_ms'] = max(0.1, context['avg_execution_time_ms'] + random.uniform(-2, 2))

            # Make decision
            judgment = engine.judge_safety(varied_context)

            # Record outcome (use expected as ground truth)
            decision = Decision(
                decision_id=f"dec_{total_decisions}",
                decision_type=DecisionType.SECURITY,
                context=varied_context,
                action=judgment.is_safe,
                confidence=judgment.confidence,
                timestamp=time.time()
            )

            # Determine if decision was correct
            is_correct = (judgment.is_safe == expected_safe)
            outcome = DecisionOutcome.GOOD if is_correct else DecisionOutcome.BAD
            reward = 1.0 if is_correct else -1.0

            engine.record_outcome(decision, outcome, reward=reward)
            total_decisions += 1

        print(f"  ✓ Completed 10 variations")

    # Get final statistics
    stats = engine.get_statistics()
    print(f"\n{'='*70}")
    print("AUTONOMOUS DECISION ENGINE TRAINING COMPLETE")
    print(f"{'='*70}")
    print(f"Total decisions: {stats['total_decisions']}")
    print(f"Success rate: {stats['success_rate']:.2%}")
    print(f"Training samples collected: {stats['training_samples_collected']}")
    print(f"Good decisions: {stats['good_decisions']}")
    print(f"Bad decisions: {stats['bad_decisions']}")

    return engine


def train_load_controller():
    """Train the load controller with simulated load scenarios"""
    print("\n" + "=" * 70)
    print("TRAINING INTELLIGENT LOAD CONTROLLER")
    print("=" * 70)

    controller = IntelligentLoadController()

    # Simulate various load scenarios
    print("\nSimulating load scenarios...")

    for i in range(200):
        # Random server state
        capacity = 100
        active_requests = random.randint(0, 150)
        is_overloaded = active_requests > capacity
        response_time = random.uniform(0.1, 5.0) if not is_overloaded else random.uniform(5.0, 20.0)

        state = ServerState(
            active_requests=active_requests,
            capacity=capacity,
            is_overloaded=is_overloaded,
            response_time=response_time,
            timestamp=time.time()
        )

        # Make decision
        decision = controller.make_intelligent_decision(state)

        # Simulate outcome (success if not overloaded when sent, or blocked when overloaded)
        load_ratio = active_requests / capacity
        expected_action = load_ratio < 0.7  # Ground truth: should send if load < 70%
        is_correct = (decision.should_send == expected_action)
        outcome = is_correct  # True = good outcome, False = bad outcome

        # Record experience
        controller.record_experience(state, decision.should_send, outcome)

        if (i + 1) % 50 == 0:
            print(f"  ✓ Processed {i+1} scenarios")

    # Get final metrics
    metrics = controller.get_intelligence_metrics()
    print(f"\n{'='*70}")
    print("LOAD CONTROLLER TRAINING COMPLETE")
    print(f"{'='*70}")
    print(f"Total decisions: {metrics['total_decisions']}")
    print(f"ML decisions: {metrics['ml_decisions']}")
    print(f"Rule-based decisions: {metrics['rule_based_decisions']}")
    print(f"Intelligence rate: {metrics['intelligence_rate']:.2%}")
    print(f"ML trained: {metrics['is_trained']}")
    print(f"Experience buffer size: {metrics['experience_size']}")

    return controller


if __name__ == "__main__":
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "IPL INTELLIGENCE TRAINING SUITE" + " " * 26 + "║")
    print("╚" + "═" * 68 + "╝")

    # Train both components
    auto_engine = train_autonomous_decision_engine()
    load_controller = train_load_controller()

    print("\n" + "=" * 70)
    print("OVERALL TRAINING SUMMARY")
    print("=" * 70)
    print("✓ Autonomous Decision Engine: Trained with 80+ scenarios")
    print("✓ Load Controller: Trained with 200+ load scenarios")
    print("✓ ML models: Active and learning from experience")
    print("=" * 70)
