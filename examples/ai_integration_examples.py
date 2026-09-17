"""
Examples of integrating different AI providers with IPL
This shows developers how to plug in their preferred AI models
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

# Example 1: Local Ollama Integration
print("=" * 60)
print("Example 1: Local Ollama Integration")
print("=" * 60)

try:
    ollama_provider = OllamaProvider(
        model_name="qwen2.5-coder:0.5b",
        endpoint="http://localhost:11434"
    )
    
    # Quick availability check with timeout
    import socket
    def check_ollama_running():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("localhost", 11434))
            sock.close()
            return result == 0
        except:
            return False
    
    if check_ollama_running() and ollama_provider.is_available():
        print("✅ Ollama provider is available")
        
        # Test intent processing
        result = ollama_provider.process_intent(
            "I need to process a payment of fifty dollars",
            context={"task": "payment_processing"}
        )
        print(f"Intent result: {result}")
        
        # Test code generation
        code = ollama_provider.generate_code(
            "Create a function that validates user input",
            language="ipl"
        )
        print(f"Generated code snippet: {code[:100]}...")
        
    else:
        print("⚠️  Ollama provider not available (this is expected if Ollama isn't running)")
        
except Exception as e:
    print(f"❌ Ollama integration failed: {e}")


# Example 2: OpenAI Integration
print("\n" + "=" * 60)
print("Example 2: OpenAI Integration")
print("=" * 60)

try:
    # Note: Requires OPENAI_API_KEY environment variable
    openai_provider = OpenAIProvider(
        model_name="gpt-4",
        api_key="test_key_12345"  # Test key for demonstration
    )
    
    if openai_provider.is_available():
        print("✅ OpenAI provider is configured")
        
        # Test intent processing
        result = openai_provider.process_intent(
            "Analyze this code for security vulnerabilities",
            context={"task": "security_analysis"}
        )
        print(f"Intent result: {result}")
        
    else:
        print("⚠️  OpenAI API key not configured (set OPENAI_API_KEY environment variable)")
        
except Exception as e:
    print(f"❌ OpenAI integration failed: {e}")


# Example 3: Anthropic Integration
print("\n" + "=" * 60)
print("Example 3: Anthropic Integration")
print("=" * 60)

try:
    # Note: Requires ANTHROPIC_API_KEY environment variable
    anthropic_provider = AnthropicProvider(
        model_name="claude-3-opus-20240229",
        api_key="test_key_12345"  # Test key for demonstration
    )
    
    if anthropic_provider.is_available():
        print("✅ Anthropic provider is configured")
        
        # Test code generation
        code = anthropic_provider.generate_code(
            "Create a secure authentication function",
            language="ipl"
        )
        print(f"Generated code snippet: {code[:100]}...")
        
    else:
        print("⚠️  Anthropic API key not configured (set ANTHROPIC_API_KEY environment variable)")
        
except Exception as e:
    print(f"❌ Anthropic integration failed: {e}")


# Example 4: Custom AI Integration
print("\n" + "=" * 60)
print("Example 4: Custom AI Integration")
print("=" * 60)

def my_custom_ai(prompt: str, context: dict) -> dict:
    """Example custom AI function"""
    # This could call your own AI service, internal models, etc.
    print(f"Custom AI processing: '{prompt}'")
    
    # Simple example logic
    if "payment" in prompt.lower():
        return {"intent": "payment", "confidence": 0.9}
    elif "security" in prompt.lower():
        return {"intent": "security", "confidence": 0.85}
    else:
        return {"intent": "general", "confidence": 0.7}

try:
    custom_provider = CustomAIProvider(
        model_name="my-custom-ai",
        process_function=my_custom_ai
    )
    
    print("✅ Custom AI provider created")
    
    result = custom_provider.process_intent(
        "I need help with payment processing",
        context={}
    )
    print(f"Custom AI result: {result}")
    
except Exception as e:
    print(f"❌ Custom AI integration failed: {e}")


# Example 5: Factory Function Usage
print("\n" + "=" * 60)
print("Example 5: Factory Function Usage")
print("=" * 60)

try:
    # Create provider using factory function
    provider = get_ai_provider(
        "ollama",
        model_name="qwen2.5-coder:0.5b"
    )
    
    print(f"✅ Created provider: {type(provider).__name__}")
    
except Exception as e:
    print(f"❌ Factory function failed: {e}")


# Example 6: Hybrid Approach (Multiple Providers)
print("\n" + "=" * 60)
print("Example 6: Hybrid Approach with Multiple Providers")
print("=" * 60)

class HybridAIProvider:
    """Use multiple AI providers with fallback logic"""
    
    def __init__(self):
        self.providers = []
        print("Setting up hybrid AI provider...")
        
        # Try to add available providers (with quick checks)
        try:
            import socket
            def check_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex(("localhost", port))
                    sock.close()
                    return result == 0
                except:
                    return False
            
            if check_port(11434):
                self.providers.append(("ollama", OllamaProvider()))
                print("✅ Added Ollama provider")
        except Exception as e:
            print(f"⚠️  Could not add Ollama: {e}")
            
        # Check for API keys
        if os.getenv("OPENAI_API_KEY"):
            try:
                self.providers.append(("openai", OpenAIProvider()))
                print("✅ Added OpenAI provider")
            except Exception as e:
                print(f"⚠️  Could not add OpenAI: {e}")
        
        if not self.providers:
            print("⚠️  No AI providers available, adding custom fallback")
            self.providers.append(("custom", CustomAIProvider()))
    
    def process_with_fallback(self, prompt: str, context: dict) -> dict:
        """Try each provider until one succeeds"""
        for name, provider in self.providers:
            try:
                print(f"Trying {name} provider...")
                result = provider.process_intent(prompt, context)
                if result.get("confidence", 0) > 0.5:
                    print(f"✅ Success with {name}")
                    return {**result, "provider_used": name}
            except Exception as e:
                print(f"❌ {name} failed: {e}")
                continue
        
        return {"intent": "unknown", "confidence": 0.0, "provider_used": "none"}

try:
    hybrid = HybridAIProvider()
    
    if hybrid.providers:
        result = hybrid.process_with_fallback(
            "Process a refund request",
            context={"task": "customer_service"}
        )
        print(f"Hybrid result: {result}")
    else:
        print("⚠️  No AI providers available")
        
except Exception as e:
    print(f"❌ Hybrid approach failed: {e}")


print("\n" + "=" * 60)
print("AI Integration Examples Complete")
print("=" * 60)
print("\nKey Takeaways:")
print("1. Developers can choose any AI provider")
print("2. Local models (Ollama) for privacy/cost")
print("3. Cloud APIs (OpenAI/Anthropic) for power")
print("4. Custom integrations for specific needs")
print("5. Hybrid approaches for reliability")
print("6. IPL remains flexible and model-agnostic")