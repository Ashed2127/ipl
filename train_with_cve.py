"""
Train IPL with downloaded CVE data
"""
import time
import json
from autonomous_decision_engine import (
    AutonomousDecisionEngine,
    Decision,
    DecisionType,
    DecisionOutcome
)


def train_with_cve_data():
    """Train IPL with CVE data from NVD"""
    print("=" * 70)
    print("TRAINING IPL WITH CVE DATA FROM NVD")
    print("=" * 70)
    
    start_time = time.time()
    
    # Load CVE data
    print("\n[1/3] Loading CVE data...")
    with open('.ipl_data/cve_training_data.json', 'r') as f:
        cve_samples = json.load(f)
    
    print(f"  ✓ Loaded {len(cve_samples)} CVE samples")
    
    # Initialize engine
    print("\n[2/3] Initializing Autonomous Decision Engine...")
    engine = AutonomousDecisionEngine(use_intelligent_components=True)
    
    # Train with CVE data
    print("\n[3/3] Training with CVE data...")
    train_start = time.time()
    
    total_decisions = 0
    correct_decisions = 0
    
    for i, sample in enumerate(cve_samples):
        # Extract context
        context = sample['features']
        
        # Make decision
        judgment = engine.judge_safety(context)
        
        # Record outcome
        decision = Decision(
            decision_id=f"cve_dec_{total_decisions}",
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
        
        if (i + 1) % 10 == 0:
            print(f"  ✓ Processed {i+1}/{len(cve_samples)} CVE samples")
    
    train_time = time.time() - train_start
    print(f"  Training time: {train_time:.2f}s")
    
    # Get statistics
    stats = engine.get_statistics()
    
    # Summary
    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print("CVE TRAINING COMPLETE")
    print("=" * 70)
    print(f"CVE samples trained: {len(cve_samples)}")
    print(f"Total decisions: {stats['total_decisions']}")
    print(f"Success rate: {stats['success_rate']:.2%}")
    print(f"Training samples: {stats['training_samples_collected']}")
    print(f"Total time: {total_time:.2f}s ({total_time/60:.2f} minutes)")
    print("=" * 70)
    
    return engine


if __name__ == "__main__":
    train_with_cve_data()
