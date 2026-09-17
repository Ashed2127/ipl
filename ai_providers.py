"""
Pluggable AI Integration Layer for IPL
Allows developers to integrate any AI model of their choice
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json
import urllib.request
import os


class AIProvider(ABC):
    """Base interface for all AI integrations with IPL"""
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.config = kwargs
        
    @abstractmethod
    def process_intent(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process natural language intent and return structured data"""
        pass
    
    @abstractmethod
    def generate_code(self, requirements: str, language: str = "ipl") -> str:
        """Generate code from natural language requirements"""
        pass
    
    @abstractmethod
    def analyze_security(self, code: str) -> Dict[str, Any]:
        """Perform deep security analysis on code"""
        pass
    
    @abstractmethod
    def optimize_code(self, code: str) -> Dict[str, Any]:
        """Suggest code optimizations"""
        pass
    
    def is_available(self) -> bool:
        """Check if the AI provider is available and configured"""
        return True


class OllamaProvider(AIProvider):
    """Integration with local Ollama models"""
    
    def __init__(self, model_name: str = "qwen2.5-coder:0.5b", 
                 endpoint: str = "http://localhost:11434", **kwargs):
        super().__init__(model_name, **kwargs)
        self.endpoint = endpoint
        
    def is_available(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            req = urllib.request.Request(f"{self.endpoint}/api/tags")
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    result = json.loads(resp.read().decode())
                    models = [m["name"] for m in result.get("models", [])]
                    return self.model_name in models
        except Exception:
            return False
        return False
    
    def _call_ollama(self, prompt: str, system_prompt: str = "") -> str:
        """Make API call to Ollama"""
        url = f"{self.endpoint}/api/generate"
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 500
            }
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
                return result.get("response", "")
        except Exception as e:
            raise Exception(f"Ollama API call failed: {e}")
    
    def process_intent(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process intent using Ollama model"""
        system_prompt = "You are an intent classifier. Extract the main intent from the text. Return JSON with 'intent' and 'confidence' keys."
        
        try:
            response = self._call_ollama(prompt, system_prompt)
            # Try to parse JSON response
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                # Fallback to simple analysis
                return {
                    "intent": "general",
                    "confidence": 0.7,
                    "raw_response": response
                }
        except Exception as e:
            return {"error": str(e), "intent": "unknown", "confidence": 0.0}
    
    def generate_code(self, requirements: str, language: str = "ipl") -> str:
        """Generate IPL code from requirements"""
        system_prompt = f"You are an expert {language} programmer. Generate clean, secure code based on requirements."
        
        try:
            response = self._call_ollama(requirements, system_prompt)
            return response
        except Exception as e:
            return f"# Error generating code: {e}"
    
    def analyze_security(self, code: str) -> Dict[str, Any]:
        """Analyze code for security issues"""
        system_prompt = "You are a security expert. Analyze the code for vulnerabilities. Return JSON with 'vulnerabilities' list and 'severity' assessment."
        
        try:
            response = self._call_ollama(code, system_prompt)
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                return {
                    "vulnerabilities": [],
                    "analysis": response,
                    "severity": "unknown"
                }
        except Exception as e:
            return {"error": str(e), "vulnerabilities": []}
    
    def optimize_code(self, code: str) -> Dict[str, Any]:
        """Suggest code optimizations"""
        system_prompt = "You are a code optimization expert. Suggest improvements for performance, readability, and best practices."
        
        try:
            response = self._call_ollama(code, system_prompt)
            return {
                "suggestions": response,
                "model_used": self.model_name
            }
        except Exception as e:
            return {"error": str(e), "suggestions": []}


class OpenAIProvider(AIProvider):
    """Integration with OpenAI API"""
    
    def __init__(self, model_name: str = "gpt-4", api_key: Optional[str] = None, **kwargs):
        super().__init__(model_name, **kwargs)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required")
    
    def is_available(self) -> bool:
        """Check if OpenAI API key is configured"""
        return bool(self.api_key)
    
    def _call_openai(self, messages: List[Dict[str, str]]) -> str:
        """Make API call to OpenAI"""
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except ImportError:
            raise Exception("OpenAI library not installed. Install with: pip install openai")
        except Exception as e:
            raise Exception(f"OpenAI API call failed: {e}")
    
    def process_intent(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process intent using OpenAI model"""
        system_prompt = "You are an intent classifier. Extract the main intent from the text. Return JSON with 'intent' and 'confidence' keys."
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = self._call_openai(messages)
            
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                return {
                    "intent": "general",
                    "confidence": 0.8,
                    "raw_response": response
                }
        except Exception as e:
            return {"error": str(e), "intent": "unknown", "confidence": 0.0}
    
    def generate_code(self, requirements: str, language: str = "ipl") -> str:
        """Generate IPL code from requirements"""
        system_prompt = f"You are an expert {language} programmer. Generate clean, secure code based on requirements."
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": requirements}
            ]
            
            return self._call_openai(messages)
        except Exception as e:
            return f"# Error generating code: {e}"
    
    def analyze_security(self, code: str) -> Dict[str, Any]:
        """Analyze code for security issues"""
        system_prompt = "You are a security expert. Analyze the code for vulnerabilities. Return JSON with 'vulnerabilities' list and 'severity' assessment."
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": code}
            ]
            
            response = self._call_openai(messages)
            
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                return {
                    "vulnerabilities": [],
                    "analysis": response,
                    "severity": "unknown"
                }
        except Exception as e:
            return {"error": str(e), "vulnerabilities": []}
    
    def optimize_code(self, code: str) -> Dict[str, Any]:
        """Suggest code optimizations"""
        system_prompt = "You are a code optimization expert. Suggest improvements for performance, readability, and best practices."
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": code}
            ]
            
            response = self._call_openai(messages)
            
            return {
                "suggestions": response,
                "model_used": self.model_name
            }
        except Exception as e:
            return {"error": str(e), "suggestions": []}


class AnthropicProvider(AIProvider):
    """Integration with Anthropic Claude API"""
    
    def __init__(self, model_name: str = "claude-3-opus-20240229", 
                 api_key: Optional[str] = None, **kwargs):
        super().__init__(model_name, **kwargs)
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key required")
    
    def is_available(self) -> bool:
        """Check if Anthropic API key is configured"""
        return bool(self.api_key)
    
    def _call_anthropic(self, messages: List[Dict[str, str]]) -> str:
        """Make API call to Anthropic"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model=self.model_name,
                max_tokens=1024,
                messages=messages
            )
            
            return response.content[0].text
        except ImportError:
            raise Exception("Anthropic library not installed. Install with: pip install anthropic")
        except Exception as e:
            raise Exception(f"Anthropic API call failed: {e}")
    
    def process_intent(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process intent using Anthropic model"""
        system_prompt = "You are an intent classifier. Extract the main intent from the text. Return JSON with 'intent' and 'confidence' keys."
        
        try:
            messages = [
                {"role": "user", "content": f"{system_prompt}\n\n{prompt}"}
            ]
            
            response = self._call_anthropic(messages)
            
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                return {
                    "intent": "general",
                    "confidence": 0.8,
                    "raw_response": response
                }
        except Exception as e:
            return {"error": str(e), "intent": "unknown", "confidence": 0.0}
    
    def generate_code(self, requirements: str, language: str = "ipl") -> str:
        """Generate IPL code from requirements"""
        system_prompt = f"You are an expert {language} programmer. Generate clean, secure code based on requirements."
        
        try:
            messages = [
                {"role": "user", "content": f"{system_prompt}\n\n{requirements}"}
            ]
            
            return self._call_anthropic(messages)
        except Exception as e:
            return f"# Error generating code: {e}"
    
    def analyze_security(self, code: str) -> Dict[str, Any]:
        """Analyze code for security issues"""
        system_prompt = "You are a security expert. Analyze the code for vulnerabilities. Return JSON with 'vulnerabilities' list and 'severity' assessment."
        
        try:
            messages = [
                {"role": "user", "content": f"{system_prompt}\n\n{code}"}
            ]
            
            response = self._call_anthropic(messages)
            
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                return {
                    "vulnerabilities": [],
                    "analysis": response,
                    "severity": "unknown"
                }
        except Exception as e:
            return {"error": str(e), "vulnerabilities": []}
    
    def optimize_code(self, code: str) -> Dict[str, Any]:
        """Suggest code optimizations"""
        system_prompt = "You are a code optimization expert. Suggest improvements for performance, readability, and best practices."
        
        try:
            messages = [
                {"role": "user", "content": f"{system_prompt}\n\n{code}"}
            ]
            
            response = self._call_anthropic(messages)
            
            return {
                "suggestions": response,
                "model_used": self.model_name
            }
        except Exception as e:
            return {"error": str(e), "suggestions": []}


class CustomAIProvider(AIProvider):
    """Template for custom AI integrations"""
    
    def __init__(self, model_name: str = "custom", process_function=None, **kwargs):
        super().__init__(model_name, **kwargs)
        self.process_function = process_function
    
    def process_intent(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Use custom processing function"""
        if self.process_function:
            return self.process_function(prompt, context)
        return {"intent": "custom", "confidence": 0.5}
    
    def generate_code(self, requirements: str, language: str = "ipl") -> str:
        """Custom code generation"""
        return f"# Custom code generation for: {requirements}"
    
    def analyze_security(self, code: str) -> Dict[str, Any]:
        """Custom security analysis"""
        return {"vulnerabilities": [], "note": "Custom security analysis"}
    
    def optimize_code(self, code: str) -> Dict[str, Any]:
        """Custom optimization"""
        return {"suggestions": [], "note": "Custom optimization"}


def get_ai_provider(provider_type: str, **kwargs) -> AIProvider:
    """Factory function to create AI providers"""
    providers = {
        "ollama": OllamaProvider,
        "openai": OpenAIProvider, 
        "anthropic": AnthropicProvider,
        "custom": CustomAIProvider
    }
    
    provider_class = providers.get(provider_type.lower())
    if not provider_class:
        raise ValueError(f"Unknown provider type: {provider_type}")
    
    return provider_class(**kwargs)