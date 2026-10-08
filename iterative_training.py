"""
Iterative Training - Train IPL again and again with comprehensive data
Reinforce learning through multiple epochs
"""
import time
import json
from autonomous_decision_engine import (
    AutonomousDecisionEngine,
    Decision,
    DecisionType,
    DecisionOutcome
)


def iterative_training(epochs: int = 3):
    """Train IPL iteratively with comprehensive data"""
    print("=" * 70)
    print(f"ITERATIVE TRAINING - {epochs} EPOCHS")
    print("=" * 70)
    
    start_time = time.time()
    
    # Load comprehensive data
    print("\nLoading comprehensive training data...")
    with open('.ipl_data/comprehensive_training_data.json', 'r') as f:
        all_scenarios = json.load(f)
    
    print(f"Loaded {len(all_scenarios)} scenarios")
    
    # Train for multiple epochs
    for epoch in range(epochs):
        print(f"\n{'='*70}")
        print(f"EPOCH {epoch + 1}/{epochs}")
        print(f"{'='*70}")
        
        epoch_start = time.time()
        
        # Initialize engine (it will load previous state)
        engine = AutonomousDecisionEngine(use_intelligent_components=True)
        
        # Shuffle scenarios for variety
        import random
        random.shuffle(all_scenarios)
        
        total_decisions = 0
        correct_decisions = 0
        
        for i, scenario in enumerate(all_scenarios):
            # Extract context
            context = scenario['features']
            
            # Make decision
            judgment = engine.judge_safety(context)
            
            # Record outcome
            decision = Decision(
                decision_id=f"epoch{epoch}_dec_{total_decisions}",
                decision_type=DecisionType.SECURITY,
                context=context,
                action=judgment.is_safe,
                confidence=judgment.confidence,
                timestamp=time.time()
            )
            
            # Determine if correct
            is_correct = (judgment.is_safe == scenario['expected_safe'])
            if is_correct:
                correct_decisions += 1
            
            outcome = DecisionOutcome.GOOD if is_correct else DecisionOutcome.BAD
            reward = 1.0 if is_correct else -1.0
            
            engine.record_outcome(decision, outcome, reward=reward)
            total_decisions += 1
            
            if (i + 1) % 100 == 0:
                print(f"  ✓ Processed {i+1}/{len(all_scenarios)} scenarios")
        
        # Get statistics
        stats = engine.get_statistics()
        
        epoch_time = time.time() - epoch_start
        print(f"\nEpoch {epoch + 1} Summary:")
        print(f"  Decisions: {stats['total_decisions']}")
        print(f"  Success rate: {stats['success_rate']:.2%}")
        print(f"  Training samples: {stats['training_samples_collected']}")
        print(f"  Time: {epoch_time:.2f}s")
    
    # Final summary
    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print("ITERATIVE TRAINING COMPLETE")
    print("=" * 70)
    print(f"Epochs completed: {epochs}")
    print(f"Total scenarios per epoch: {len(all_scenarios)}")
    print(f"Total training iterations: {len(all_scenarios) * epochs}")
    print(f"Total time: {total_time:.2f}s ({total_time/60:.2f} minutes)")
    print("=" * 70)
    
    return engine


if __name__ == "__main__":
    iterative_training(epochs=3)
