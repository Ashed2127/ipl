"""
Simple demonstration of IPL's pluggable AI integration
This shows the architecture without requiring actual AI services to be running
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_providers import (
    OllamaProvider, 
    OpenAIProvider, 
    AnthropicProvider, 
    CustomAIProvider,
    get_ai_provider
)

print("=" * 60)
print("IPL Pluggable AI Integration Demonstration")
print("=" * 60)

# Example 1: Show provider structure
print("\n1. Available AI Provider Types:")
print("-" * 40)
print("✅ OllamaProvider - Local models (Qwen, Llama, etc.)")
print("✅ OpenAIProvider - Cloud API (GPT-4, GPT-3.5, etc.)")
print("✅ AnthropicProvider - Cloud API (Claude, etc.)")
print("✅ CustomAIProvider - Your own AI integration")

# Example 2: Custom AI Integration (Always works)
print("\n2. Custom AI Integration (Always Available):")
print("-" * 40)

def my_business_logic(prompt: str, context: dict) -> dict:
    """Your custom AI logic - could call internal services, etc."""
    print(f"   Processing: '{prompt}'")
    
    # Example business logic
    if "payment" in prompt.lower():
        return {"intent": "payment_processing", "confidence": 0.95}
    elif "security" in prompt.lower():
        return {"intent": "security_analysis", "confidence": 0.90}
    else:
        return {"intent": "general_inquiry", "confidence": 0.80}

custom_provider = CustomAIProvider(
    model_name="my-business-ai",
    process_function=my_business_logic
)

result = custom_provider.process_intent(
    "I need to process a customer payment",
    context={"user_id": "12345"}
)
print(f"   Result: {result}")

# Example 3: Provider Factory
print("\n3. Provider Factory Function:")
print("-" * 40)

# Create different providers
try:
    ollama = get_ai_provider("ollama", model_name="qwen2.5-coder:0.5b")
    print(f"   ✅ Created: {type(ollama).__name__}")
except Exception as e:
    print(f"   ⚠️  Ollama: {e}")

try:
    openai = get_ai_provider("openai", model_name="gpt-4", api_key="test")
    print(f"   ✅ Created: {type(openai).__name__}")
except Exception as e:
    print(f"   ⚠️  OpenAI: {e}")

try:
    custom = get_ai_provider("custom", model_name="my-ai")
    print(f"   ✅ Created: {type(custom).__name__}")
except Exception as e:
    print(f"   ⚠️  Custom: {e}")

# Example 4: Integration Pattern
print("\n4. Integration Pattern with IPL:")
print("-" * 40)

integration_code = '''
# Example: Using AI provider with IPL compiler
from ipl import IPLCompiler
from ai_providers import OllamaProvider

# Choose your AI model
ai_provider = OllamaProvider(model="llama3:8b")

# Integrate with IPL
compiler = IPLCompiler(ai_provider=ai_provider)

# Now IPL has true AI intelligence
compiler.run("intelligent_system.ipl")
'''

print("   " + integration_code.replace("\n", "\n   "))

# Example 5: Benefits
print("\n5. Benefits of Pluggable Architecture:")
print("-" * 40)
print("✅ Developer Choice - Use any AI model you prefer")
print("✅ Cost Control - Local models free, cloud APIs paid")
print("✅ Privacy - Keep data local with local models")
print("✅ No Lock-in - Switch between providers easily")
print("✅ Future-Proof - Works with new AI models as they emerge")
print("✅ Production-Ready - Choose based on your requirements")

print("\n" + "=" * 60)
print("Key Insight: IPL is a programming language designed")
print("for AI integration, not a bundled AI solution.")
print("=" * 60)