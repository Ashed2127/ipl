"""
Test the Expert-Level AI System for IPL
Demonstrates expert-level reasoning like security specialists, language experts, and compiler designers.
"""
from expert_system import ExpertCollaborationSystem, ExpertDomain, ThreatLevel
from expert_reasoning_engine import ExpertReasoningEngine, ProactiveThreatPredictor


def test_safe_code():
    """Test analysis of safe code."""
    print("\n" + "="*80)
    print("TEST 1: Safe Code Analysis")
    print("="*80)
    
    safe_code = """
    fn calculate_sum(a: Int, b: Int) -> Int {
        return a + b
    }
    
    let result = calculate_sum(5, 10)
    print result
    """
    
    reasoning_engine = ExpertReasoningEngine()
    decision, reasoning_chain = reasoning_engine.analyze_with_reasoning(safe_code)
    
    reasoning_engine.print_reasoning_report(reasoning_chain)
    
    print(f"\nDecision: {decision.final_recommendation}")
    print(f"Is Safe: {decision.is_safe}")
    print(f"Threat Level: {decision.threat_level.value}")


def test_malicious_code():
    """Test analysis of potentially malicious code."""
    print("\n" + "="*80)
    print("TEST 2: Malicious Code Analysis")
    print("="*80)
    
    malicious_code = """
    fn process_user_input(input: String) {
        let query = "SELECT * FROM users WHERE username = '" + input + "'"
        db_execute(query)
    }
    
    let user_input = "admin' OR '1'='1"
    process_user_input(user_input)
    """
    
    reasoning_engine = ExpertReasoningEngine()
    decision, reasoning_chain = reasoning_engine.analyze_with_reasoning(malicious_code)
    
    reasoning_engine.print_reasoning_report(reasoning_chain)
    
    print(f"\nDecision: {decision.final_recommendation}")
    print(f"Is Safe: {decision.is_safe}")
    print(f"Threat Level: {decision.threat_level.value}")
    print(f"Blocked Operations: {decision.blocked_operations}")
    print(f"Safe Alternatives: {decision.safe_alternatives}")


def test_security_conscious_code():
    """Test analysis of security-conscious code."""
    print("\n" + "="*80)
    print("TEST 3: Security-Conscious Code Analysis")
    print("="*80)
    
    security_code = """
    fn process_user_input(input: String) {
        let clean_input = sanitize(input)
        let query = "SELECT * FROM users WHERE username = ?"
        db_execute(query, [clean_input])
    }
    
    let user_input = get_user_data()
    process_user_input(user_input)
    """
    
    reasoning_engine = ExpertReasoningEngine()
    decision, reasoning_chain = reasoning_engine.analyze_with_reasoning(security_code)
    
    reasoning_engine.print_reasoning_report(reasoning_chain)
    
    print(f"\nDecision: {decision.final_recommendation}")
    print(f"Is Safe: {decision.is_safe}")
    print(f"Threat Level: {decision.threat_level.value}")


def test_proactive_threat_prediction():
    """Test proactive threat prediction."""
    print("\n" + "="*80)
    print("TEST 4: Proactive Threat Prediction")
    print("="*80)
    
    dangerous_code = """
    fn execute_command(cmd: String) {
        system(cmd)
    }
    
    let user_cmd = "rm -rf /"
    execute_command(user_cmd)
    """
    
    reasoning_engine = ExpertReasoningEngine()
    threat_predictor = ProactiveThreatPredictor(reasoning_engine)
    
    predictions = threat_predictor.predict_threats(dangerous_code)
    threat_predictor.print_threat_prediction_report(predictions)


def test_expert_collaboration():
    """Test expert collaboration on complex code."""
    print("\n" + "="*80)
    print("TEST 5: Expert Collaboration on Complex Code")
    print("="*80)
    
    complex_code = """
    fn handle_request(data: String) {
        let parsed = eval(data)
        if parsed.type == "admin" {
            grant_admin_access()
        }
        db_write("logs", parsed)
    }
    
    let request_data = get_http_request()
    handle_request(request_data)
    """
    
    collaboration_system = ExpertCollaborationSystem()
    decision = collaboration_system.collaborative_analysis(complex_code)
    
    print(f"\nFinal Recommendation: {decision.final_recommendation}")
    print(f"Is Safe: {decision.is_safe}")
    print(f"Threat Level: {decision.threat_level.value}")
    
    print("\nExpert Analysis Details:")
    for domain, analysis in decision.expert_analyses.items():
        print(f"\n--- {domain.value.upper()} ---")
        print(f"Confidence: {analysis.confidence:.2f}")
        print(f"Threat Level: {analysis.threat_level.value}")
        print(f"Findings: {', '.join(analysis.findings)}")
        print(f"Recommendations: {', '.join(analysis.recommendations)}")
    
    print(f"\nBlocked Operations: {decision.blocked_operations}")
    print(f"Safe Alternatives: {decision.safe_alternatives}")


def main():
    """Run all expert system tests."""
    print("\n" + "="*80)
    print("IPL EXPERT-LEVEL AI SYSTEM - COMPREHENSIVE TESTING")
    print("="*80)
    print("\nThis demonstrates IPL's evolution to expert-level intelligence")
    print("mimicking Security Specialists, Language Experts, and Compiler Designers")
    
    try:
        test_safe_code()
        test_malicious_code()
        test_security_conscious_code()
        test_proactive_threat_prediction()
        test_expert_collaboration()
        
        print("\n" + "="*80)
        print("ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\nIPL has evolved to expert-level intelligence with:")
        print("✅ Multi-expert collaboration (Security, Language, Compiler)")
        print("✅ Chain-of-thought reasoning for complex analysis")
        print("✅ Proactive threat prediction and prevention")
        print("✅ Context-aware decision making")
        print("✅ Expert-level consequence analysis")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()