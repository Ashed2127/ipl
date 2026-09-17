# Developer Guide: Custom AI Integration with IPL

## Overview

IPL is designed as a **programming language with pluggable AI integration**. This guide shows developers how to integrate their preferred AI models with IPL to build intelligent systems.

## Core Concept

Instead of bundling specific AI models, IPL provides a **standardized interface** that allows developers to:

1. **Choose any AI model** (local, cloud, or custom)
2. **Integrate seamlessly** with IPL's compiler and runtime
3. **Switch providers** without changing IPL code
4. **Build intelligent systems** on their own terms

## Quick Start

### Step 1: Install IPL Core
```bash
pip install ipl-lang
```

### Step 2: Choose Your AI Provider

#### Option A: Local AI (Privacy + Cost Control)
```python
from ipl import IPLCompiler
from ai_providers import OllamaProvider

# Use your preferred local model
ai_provider = OllamaProvider(model="llama3:8b")
compiler = IPLCompiler(ai_provider=ai_provider)
compiler.run("my_system.ipl")
```

#### Option B: Cloud AI (Power + Convenience)
```python
from ipl import IPLCompiler
from ai_providers import OpenAIProvider

# Use your preferred cloud model
ai_provider = OpenAIProvider(model="gpt-4", api_key="your-key")
compiler = IPLCompiler(ai_provider=ai_provider)
compiler.run("my_system.ipl")
```

#### Option C: Custom AI (Complete Control)
```python
from ipl import IPLCompiler
from ai_providers import CustomAIProvider

# Your own AI logic
def my_ai_logic(prompt, context):
    # Call your internal AI service
    return {"intent": "custom", "confidence": 0.9}

ai_provider = CustomAIProvider(process_function=my_ai_logic)
compiler = IPLCompiler(ai_provider=ai_provider)
compiler.run("my_system.ipl")
```

## Architecture Deep Dive

### AI Provider Interface

All AI providers implement the same interface:

```python
class AIProvider:
    def process_intent(self, prompt: str, context: dict) -> dict:
        """Process natural language intent"""
        pass
    
    def generate_code(self, requirements: str, language: str) -> str:
        """Generate code from requirements"""
        pass
    
    def analyze_security(self, code: str) -> dict:
        """Analyze code for security issues"""
        pass
    
    def optimize_code(self, code: str) -> dict:
        """Suggest code optimizations"""
        pass
```

### Integration Points

IPL uses AI providers at these points:

1. **Intent Processing**: Understanding natural language commands
2. **Code Generation**: Creating IPL code from requirements
3. **Security Analysis**: Deep security vulnerability detection
4. **Code Optimization**: Performance and style improvements

## Building Custom AI Integrations

### Example 1: Internal AI Service

```python
from ai_providers import AIProvider

class InternalAIProvider(AIProvider):
    """Integration with company's internal AI service"""
    
    def __init__(self, service_url: str, api_key: str):
        super().__init__("internal-ai")
        self.service_url = service_url
        self.api_key = api_key
    
    def _call_internal_service(self, endpoint: str, data: dict) -> dict:
        """Call internal AI service"""
        import requests
        
        response = requests.post(
            f"{self.service_url}/{endpoint}",
            json=data,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()
    
    def process_intent(self, prompt: str, context: dict) -> dict:
        """Process intent using internal service"""
        return self._call_internal_service("intent", {
            "prompt": prompt,
            "context": context
        })
    
    def generate_code(self, requirements: str, language: str = "ipl") -> str:
        """Generate code using internal service"""
        result = self._call_internal_service("generate", {
            "requirements": requirements,
            "language": language
        })
        return result.get("code", "")
    
    def analyze_security(self, code: str) -> dict:
        """Security analysis using internal service"""
        return self._call_internal_service("security", {"code": code})
    
    def optimize_code(self, code: str) -> dict:
        """Code optimization using internal service"""
        return self._call_internal_service("optimize", {"code": code})

# Usage
internal_ai = InternalAIProvider(
    service_url="https://ai.company.com/api/v1",
    api_key="internal-api-key"
)

compiler = IPLCompiler(ai_provider=internal_ai)
```

### Example 2: Hybrid AI Approach

```python
from ai_providers import AIProvider

class HybridAIProvider(AIProvider):
    """Combine multiple AI providers for optimal results"""
    
    def __init__(self, primary: AIProvider, fallback: AIProvider):
        super().__init__("hybrid-ai")
        self.primary = primary
        self.fallback = fallback
    
    def process_intent(self, prompt: str, context: dict) -> dict:
        """Try primary, fallback to secondary"""
        try:
            result = self.primary.process_intent(prompt, context)
            if result.get("confidence", 0) > 0.7:
                return result
        except Exception:
            pass
        
        # Fallback to secondary provider
        return self.fallback.process_intent(prompt, context)
    
    # Implement other methods similarly...

# Usage
fast_local = OllamaProvider(model="qwen:0.5b")
powerful_cloud = OpenAIProvider(model="gpt-4")

hybrid = HybridAIProvider(primary=fast_local, fallback=powerful_cloud)
compiler = IPLCompiler(ai_provider=hybrid)
```

### Example 3: Specialized Domain AI

```python
class MedicalAIProvider(AIProvider):
    """AI provider specialized for medical applications"""
    
    def __init__(self, medical_model_endpoint: str):
        super().__init__("medical-ai")
        self.endpoint = medical_model_endpoint
    
    def process_intent(self, prompt: str, context: dict) -> dict:
        """Process medical-specific intents"""
        # Add medical context
        medical_context = {
            **context,
            "domain": "medical",
            "hipaa_compliant": True
        }
        
        # Call medical AI service
        return self._call_medical_service(prompt, medical_context)
    
    def _call_medical_service(self, prompt: str, context: dict) -> dict:
        """Specialized medical AI processing"""
        # Implementation specific to medical AI service
        pass

# Usage
medical_ai = MedicalAIProvider("https://medical-ai.com/api")
compiler = IPLCompiler(ai_provider=medical_ai)
```

## Production Deployment Patterns

### Pattern 1: Local-First with Cloud Fallback

```python
# Use local AI for speed and privacy, cloud for complex tasks
class ProductionAI:
    def __init__(self):
        self.local = OllamaProvider(model="llama3:8b")
        self.cloud = OpenAIProvider(model="gpt-4")
    
    def get_provider(self, complexity: float):
        """Choose provider based on task complexity"""
        if complexity < 0.7:
            return self.local
        else:
            return self.cloud

production_ai = ProductionAI()
compiler = IPLCompiler(ai_provider=production_ai)
```

### Pattern 2: Cost-Optimized

```python
# Minimize costs by using free local models when possible
class CostOptimizedAI:
    def __init__(self):
        self.free_local = OllamaProvider(model="qwen:0.5b")
        self.paid_cloud = OpenAIProvider(model="gpt-4")
        self.usage_stats = {"local": 0, "cloud": 0}
    
    def process_intent(self, prompt: str, context: dict) -> dict:
        """Try free local first, use paid cloud if needed"""
        try:
            result = self.free_local.process_intent(prompt, context)
            if result.get("confidence", 0) > 0.6:
                self.usage_stats["local"] += 1
                return result
        except:
            pass
        
        # Fallback to paid cloud
        self.usage_stats["cloud"] += 1
        return self.paid_cloud.process_intent(prompt, context)
```

### Pattern 3: Privacy-First

```python
# Ensure sensitive data never leaves local environment
class PrivacyFirstAI:
    def __init__(self):
        self.local = OllamaProvider(model="llama3:8b")
        self.sensitive_keywords = ["ssn", "credit card", "medical"]
    
    def process_intent(self, prompt: str, context: dict) -> dict:
        """Only use local AI for sensitive data"""
        if any(keyword in prompt.lower() for keyword in self.sensitive_keywords):
            return self.local.process_intent(prompt, context)
        else:
            # Could use cloud for non-sensitive data
            return self.local.process_intent(prompt, context)
```

## Testing AI Integrations

### Unit Testing Custom Providers

```python
import unittest
from ai_providers import CustomAIProvider

class TestCustomAIProvider(unittest.TestCase):
    def setUp(self):
        self.provider = CustomAIProvider(model_name="test-ai")
    
    def test_intent_processing(self):
        result = self.provider.process_intent(
            "test prompt",
            context={"test": True}
        )
        self.assertIn("intent", result)
    
    def test_code_generation(self):
        code = self.provider.generate_code(
            "create a function",
            language="ipl"
        )
        self.assertIsInstance(code, str)

if __name__ == "__main__":
    unittest.main()
```

### Integration Testing

```python
def test_ai_integration_with_ipl():
    """Test that custom AI provider works with IPL compiler"""
    from ipl import IPLCompiler
    
    custom_ai = CustomAIProvider(model_name="test-ai")
    compiler = IPLCompiler(ai_provider=custom_ai)
    
    # Test compilation with AI integration
    result = compiler.run("test_script.ipl")
    assert result.success
```

## Best Practices

### 1. Error Handling
```python
class RobustAIProvider(AIProvider):
    def process_intent(self, prompt: str, context: dict) -> dict:
        try:
            return self._call_ai_service(prompt, context)
        except Exception as e:
            # Graceful fallback
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "error": str(e)
            }
```

### 2. Rate Limiting
```python
class RateLimitedAI(AIProvider):
    def __init__(self, base_provider: AIProvider, rate_limit: int):
        self.provider = base_provider
        self.rate_limit = rate_limit
        self.call_count = 0
    
    def process_intent(self, prompt: str, context: dict) -> dict:
        if self.call_count >= self.rate_limit:
            raise Exception("Rate limit exceeded")
        
        self.call_count += 1
        return self.provider.process_intent(prompt, context)
```

### 3. Caching
```python
class CachedAI(AIProvider):
    def __init__(self, base_provider: AIProvider):
        self.provider = base_provider
        self.cache = {}
    
    def process_intent(self, prompt: str, context: dict) -> dict:
        cache_key = f"{prompt}:{str(context)}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = self.provider.process_intent(prompt, context)
        self.cache[cache_key] = result
        return result
```

## Troubleshooting

### Common Issues

**Issue**: AI provider not available
```python
# Solution: Check availability before use
provider = OllamaProvider(model="llama3:8b")
if not provider.is_available():
    print("Provider not available, using fallback")
    provider = CustomAIProvider()
```

**Issue**: Slow response times
```python
# Solution: Add timeouts and async processing
import asyncio

class AsyncAIProvider(AIProvider):
    async def process_intent_async(self, prompt: str, context: dict) -> dict:
        # Async implementation
        pass
```

**Issue**: High costs
```python
# Solution: Implement cost tracking
class CostTrackingAI(AIProvider):
    def __init__(self, base_provider: AIProvider):
        self.provider = base_provider
        self.cost = 0.0
    
    def process_intent(self, prompt: str, context: dict) -> dict:
        result = self.provider.process_intent(prompt, context)
        self.cost += self._estimate_cost(prompt, result)
        return result
```

## Advanced Topics

### Multi-Model Ensembling
```python
class EnsembleAI(AIProvider):
    """Combine multiple AI models for better results"""
    
    def __init__(self, providers: list):
        super().__init__("ensemble")
        self.providers = providers
    
    def process_intent(self, prompt: str, context: dict) -> dict:
        results = []
        for provider in self.providers:
            try:
                result = provider.process_intent(prompt, context)
                results.append(result)
            except:
                continue
        
        # Combine results (voting, averaging, etc.)
        return self._combine_results(results)
```

### Context-Aware Selection
```python
class ContextAwareAI(AIProvider):
    """Choose AI model based on context"""
    
    def __init__(self):
        self.models = {
            "code": OllamaProvider(model="deepseek-coder"),
            "general": OllamaProvider(model="llama3"),
            "creative": OpenAIProvider(model="gpt-4")
        }
    
    def process_intent(self, prompt: str, context: dict) -> dict:
        task_type = context.get("task_type", "general")
        provider = self.models.get(task_type, self.models["general"])
        return provider.process_intent(prompt, context)
```

## Conclusion

IPL's pluggable AI architecture gives developers complete control over their AI integration strategy:

- **Flexibility**: Choose any AI model that fits your needs
- **Control**: Implement custom logic for your specific requirements  
- **Scalability**: Optimize for cost, performance, or privacy
- **Future-Proof**: Easy to adopt new AI models as they emerge

This approach makes IPL a powerful framework for building intelligent systems while letting developers decide how to integrate AI based on their specific requirements.