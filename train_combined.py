"""
Train IPL with combined synthetic + CVE data for maximum diversity
"""
import time
import json
from autonomous_decision_engine import (
    AutonomousDecisionEngine,
    Decision,
    DecisionType,
    DecisionOutcome
)


def train_combined():
    """Train IPL with both synthetic and CVE data"""
    print("=" * 70)
    print("TRAINING IPL WITH COMBINED DATA (Synthetic + CVE)")
    print("=" * 70)
    
    start_time = time.time()
    
    # Load both datasets
    print("\n[1/3] Loading training data...")
    
    with open('.ipl_data/quick_training_data.json', 'r') as f:
        synthetic_samples = json.load(f)
    print(f"  ✓ Loaded {len(synthetic_samples)} synthetic samples")
    
    with open('.ipl_data/cve_training_data.json', 'r') as f:
        cve_samples = json.load(f)
    print(f"  ✓ Loaded {len(cve_samples)} CVE samples")
    
    # Combine datasets
    all_samples = synthetic_samples + cve_samples
    print(f"  ✓ Total samples: {len(all_samples)}")
    
    # Initialize fresh engine
    print("\n[2/3] Initializing fresh Autonomous Decision Engine...")
    engine = AutonomousDecisionEngine(use_intelligent_components=True)
    
    # Train with combined data
    print("\n[3/3] Training with combined data...")
    train_start = time.time()
    
    total_decisions = 0
    correct_decisions = 0
    
    for i, sample in enumerate(all_samples):
        # Extract context
        context = sample['features']
        
        # Make decision
        judgment = engine.judge_safety(context)
        
        # Record outcome
        decision = Decision(
            decision_id=f"combined_dec_{total_decisions}",
            decision_type=DecisionType.SECURITY,
            context=context,
            action=judgment.is_safe,
            confidence=judgment.confidence,
            timestamp=time.time()
        )
        
        # Determine if correct
        is_correct = (judgment.is_safe == sample['expected_safe'])
        if is_correct:
            correct_decisions += 1
        
        outcome = DecisionOutcome.GOOD if is_correct else DecisionOutcome.BAD
        reward = 1.0 if is_correct else -1.0
        
        engine.record_outcome(decision, outcome, reward=reward)
        total_decisions += 1
        
        if (i + 1) % 50 == 0:
            print(f"  ✓ Processed {i+1}/{len(all_samples)} samples")
    
    train_time = time.time() - train_start
    print(f"  Training time: {train_time:.2f}s")
    
    # Get statistics
    stats = engine.get_statistics()
    
    # Save combined dataset
    with open('.ipl_data/combined_training_data.json', 'w') as f:
        json.dump(all_samples, f, indent=2)
    print(f"\n  ✓ Saved combined dataset to .ipl_data/combined_training_data.json")
    
    # Summary
    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print("COMBINED TRAINING COMPLETE")
    print("=" * 70)
    print(f"Synthetic samples: {len(synthetic_samples)}")
    print(f"CVE samples: {len(cve_samples)}")
    print(f"Total samples: {len(all_samples)}")
    print(f"Total decisions: {stats['total_decisions']}")
    print(f"Success rate: {stats['success_rate']:.2%}")
    print(f"Training samples: {stats['training_samples_collected']}")
    print(f"Total time: {total_time:.2f}s ({total_time/60:.2f} minutes)")
    print("=" * 70)
    
    return engine


if __name__ == "__main__":
    train_combined()
