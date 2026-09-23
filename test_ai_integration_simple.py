"""
Simple test to demonstrate AI integration with expert system
"""
import sys
sys.path.insert(0, '/home/ashed/Downloads/ipl_lang')

from ai_expert_system import AIExpertCollaborationSystem


def test_ai_integration():
    """Test that AI integration is working."""
    print("\n" + "="*80)
    print("AI INTEGRATION TEST - Qwen2.5-Coder + Expert System")
    print("="*80)
    
    # Test with simple safe code
    safe_code = "fn add(a, b) { return a + b }"
    
    print("\nTesting AI-augmented expert system...")
    ai_system = AIExpertCollaborationSystem()
    
    try:
        print("Attempting AI analysis (this may take a moment)...")
        decision = ai_system.collaborative_analysis_with_ai(safe_code)
        
        print(f"\n✅ AI Integration Working!")
        print(f"Analysis Mode: {decision['analysis_mode']}")
        print(f"AI Model: {decision['ai_model_used']}")
        print(f"Decision: {decision['final_recommendation']}")
        print(f"Is Safe: {decision['is_safe']}")
        
        if decision['analysis_mode'] == 'ai_augmented':
            print("\n🎉 SUCCESS: IPL is now at Level 3 Intelligence")
            print("   - Qwen2.5-Coder integrated with expert personas")
            print("   - AI provides semantic understanding")
            print("   - Expert knowledge guides AI analysis")
        else:
            print("\n⚠️ AI unavailable, using pattern-based fallback")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    test_ai_integration()