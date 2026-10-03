"""
Test Load Controller Persistence
"""
import time
from intelligent_load_controller import IntelligentLoadController, ServerState

print("=" * 70)
print("LOAD CONTROLLER PERSISTENCE TEST")
print("=" * 70)

# Clean up
import os
import shutil
if os.path.exists(".ipl_data"):
    shutil.rmtree(".ipl_data")

print("\nSESSION 1: Initial Training")
controller1 = IntelligentLoadController(persistence_path=".ipl_data/load_controller_state.json")

# Record some experiences
for i in range(60):
    state = ServerState(
        active_requests=i * 2,
        capacity=100,
        is_overloaded=i * 2 > 100,
        response_time=0.1 + i * 0.01,
        timestamp=time.time()
    )
    controller1.record_experience(state, i % 2 == 0, i % 3 == 0)

metrics1 = controller1.get_intelligence_metrics()
print(f"Session 1: {metrics1['total_decisions']} decisions, ML trained: {metrics1['is_trained']}")

print("\nSESSION 2: Load State")
controller2 = IntelligentLoadController(persistence_path=".ipl_data/load_controller_state.json")
metrics2 = controller2.get_intelligence_metrics()
print(f"Session 2 (loaded): {metrics2['total_decisions']} decisions, ML trained: {metrics2['is_trained']}")

if metrics2['total_decisions'] == metrics1['total_decisions']:
    print("✓ Load controller persistence working!")
else:
    print("✗ Load controller persistence failed")
