"""
Compiler-Level AI Integration for IPL
AI providers designed for integration into the compilation pipeline itself
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json
import urllib.request
import os


class CompilerAIProvider(ABC):
    """Base interface for AI providers integrated into compilation pipeline"""
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.config = kwargs
        
    @abstractmethod
    def analyze_semantics(self, ast_representation: dict, task: str) -> dict:
        """AI-powered semantic analysis during compilation"""
        pass
    
    @abstractmethod
    def suggest_transformations(self, code_representation: str, 
                                optimization_goals: list) -> list:
        """AI-driven code transformation suggestions"""
        pass
    
    @abstractmethod
    def analyze_security_deep(self, code_patterns: dict, context: str) -> dict:
        """Deep learning security analysis during compilation"""
        pass
    
    @abstractmethod
    def analyze_compilation_error(self, error_context: dict) -> dict:
        """AI-powered error analysis and fix suggestions"""
        pass
    
    @abstractmethod
    def optimize_memory_layout(self, ast_data: dict) -> dict:
        """AI-driven memory layout optimization"""
        pass
    
    @abstractmethod
    def infer_complex_types(self, code_context: dict) -> dict:
        """Neural type inference for complex scenarios"""
        pass
    
    def is_available(self) -> bool:
        """Check if the AI provider is available and configured"""
        return True


class OllamaCompilerProvider(CompilerAIProvider):
    """Ollama integration for compiler-level AI tasks"""
    
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
                "temperature": 0.3,  # Lower temperature for more deterministic compilation
                "num_predict": 800
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
    
    def analyze_semantics(self, ast_representation: dict, task: str) -> dict:
        """AI-powered semantic analysis during compilation"""
        system_prompt = """You are a compiler AI assistant. Analyze the AST representation for semantic meaning.
Focus on type relationships, variable usage patterns, and code context.
Return JSON with semantic insights."""
        
        prompt = f"""Task: {task}
AST Representation: {json.dumps(ast_representation, indent=2)}

Provide semantic analysis including:
1. Type relationships between variables
2. Data flow patterns
3. Contextual meaning of operations
4. Potential semantic issues
"""
        
        try:
            response = self._call_ollama(prompt, system_prompt)
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                return {
                    "semantic_insights": response,
                    "confidence": 0.7,
                    "analysis_type": task
                }
        except Exception as e:
            return {"error": str(e), "semantic_insights": {}, "confidence": 0.0}
    
    def suggest_transformations(self, code_representation: str, 
                                optimization_goals: list) -> list:
        """AI-driven code transformation suggestions"""
        system_prompt = """You are a compiler optimization AI. Suggest code transformations.
Focus on the specific optimization goals provided.
Return JSON with transformation suggestions."""
        
        prompt = f"""Optimization Goals: {', '.join(optimization_goals)}
Code Representation: {code_representation}

Suggest specific code transformations including:
1. Algorithmic improvements
2. Data structure optimizations
3. Memory layout improvements
4. Performance enhancements
"""
        
        try:
            response = self._call_ollama(prompt, system_prompt)
            try:
                result = json.loads(response)
                return result.get("transformations", [])
            except json.JSONDecodeError:
                return [{
                    "type": "general",
                    "description": response,
                    "confidence": 0.6
                }]
        except Exception as e:
            return [{"error": str(e)}]
    
    def analyze_security_deep(self, code_patterns: dict, context: str) -> dict:
        """Deep learning security analysis during compilation"""
        system_prompt = """You are a compiler security AI. Perform deep security analysis.
Look beyond simple patterns - understand context and intent.
Return JSON with security assessment."""
        
        prompt = f"""Context: {context}
Code Patterns: {json.dumps(code_patterns, indent=2)}

Perform deep security analysis including:
1. Injection vulnerabilities (SQL, command, etc.)
2. Data leakage risks
3. Authentication/authorization issues
4. Cryptographic weaknesses
5. Business logic vulnerabilities
"""
        
        try:
            response = self._call_ollama(prompt, system_prompt)
            try:
                result = json.loads(response)
                return {
                    "vulnerabilities": result.get("vulnerabilities", []),
                    "risk_level": result.get("risk_level", "medium"),
                    "confidence": result.get("confidence", 0.7)
                }
            except json.JSONDecodeError:
                return {
                    "analysis": response,
                    "risk_level": "medium",
                    "confidence": 0.6
                }
        except Exception as e:
            return {"error": str(e), "risk_level": "unknown", "vulnerabilities": []}
    
    def analyze_compilation_error(self, error_context: dict) -> dict:
        """AI-powered error analysis and fix suggestions"""
        system_prompt = """You are a compiler error analysis AI. Understand compilation errors.
Provide contextually appropriate fix suggestions.
Return JSON with error analysis and fixes."""
        
        prompt = f"""Error Context: {json.dumps(error_context, indent=2)}

Analyze this compilation error and provide:
1. Root cause analysis
2. Specific fix suggestions
3. Prevention strategies
4. Code examples if applicable
"""
        
        try:
            response = self._call_ollama(prompt, system_prompt)
            try:
                result = json.loads(response)
                return {
                    "root_cause": result.get("root_cause", ""),
                    "fix_suggestions": result.get("fix_suggestions", []),
                    "prevention": result.get("prevention", "")
                }
            except json.JSONDecodeError:
                return {
                    "analysis": response,
                    "fix_suggestions": ["Review the error context"],
                    "root_cause": "AI analysis failed"
                }
        except Exception as e:
            return {"error": str(e), "fix_suggestions": []}
    
    def optimize_memory_layout(self, ast_data: dict) -> dict:
        """AI-driven memory layout optimization"""
        system_prompt = """You are a compiler memory optimization AI. Optimize memory layout.
Consider data access patterns, cache efficiency, and memory usage.
Return JSON with memory layout suggestions."""
        
        prompt = f"""AST Data: {json.dumps(ast_data, indent=2)}

Suggest memory layout optimizations including:
1. Data structure organization
2. Field ordering for cache efficiency
3. Memory allocation strategies
4. Memory pool recommendations
"""
        
        try:
            response = self._call_ollama(prompt, system_prompt)
            try:
                result = json.loads(response)
                return {
                    "layout_suggestions": result.get("layout_suggestions", []),
                    "estimated_improvement": result.get("estimated_improvement", "")
                }
            except json.JSONDecodeError:
                return {
                    "suggestions": response,
                    "estimated_improvement": "Unknown"
                }
        except Exception as e:
            return {"error": str(e), "layout_suggestions": []}
    
    def infer_complex_types(self, code_context: dict) -> dict:
        """Neural type inference for complex scenarios"""
        system_prompt = """You are a compiler type inference AI. Infer complex types.
Understand semantic relationships beyond simple syntax.
Return JSON with type inference results."""
        
        prompt = f"""Code Context: {json.dumps(code_context, indent=2)}

Perform complex type inference including:
1. Generic type parameters
2. Union and intersection types
3. Dependent types
4. Type relationships and constraints
"""
        
        try:
            response = self._call_ollama(prompt, system_prompt)
            try:
                result = json.loads(response)
                return {
                    "inferred_types": result.get("inferred_types", {}),
                    "type_relationships": result.get("type_relationships", []),
                    "confidence": result.get("confidence", 0.7)
                }
            except json.JSONDecodeError:
                return {
                    "inference": response,
                    "confidence": 0.6
                }
        except Exception as e:
            return {"error": str(e), "inferred_types": {}, "confidence": 0.0}


class OpenAICompilerProvider(CompilerAIProvider):
    """OpenAI integration for compiler-level AI tasks"""
    
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
                temperature=0.3  # Lower temperature for deterministic compilation
            )
            
            return response.choices[0].message.content
        except ImportError:
            raise Exception("OpenAI library not installed. Install with: pip install openai")
        except Exception as e:
            raise Exception(f"OpenAI API call failed: {e}")
    
    def analyze_semantics(self, ast_representation: dict, task: str) -> dict:
        """AI-powered semantic analysis during compilation"""
        system_prompt = "You are a compiler AI assistant. Analyze AST representations for semantic meaning. Return JSON with semantic insights."
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Task: {task}\nAST: {json.dumps(ast_representation, indent=2)}"}
            ]
            
            response = self._call_openai(messages)
            
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                return {
                    "semantic_insights": response,
                    "confidence": 0.8,
                    "analysis_type": task
                }
        except Exception as e:
            return {"error": str(e), "semantic_insights": {}, "confidence": 0.0}
    
    def suggest_transformations(self, code_representation: str, 
                                optimization_goals: list) -> list:
        """AI-driven code transformation suggestions"""
        system_prompt = "You are a compiler optimization AI. Suggest code transformations. Return JSON with transformation suggestions."
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Goals: {optimization_goals}\nCode: {code_representation}"}
            ]
            
            response = self._call_openai(messages)
            
            try:
                result = json.loads(response)
                return result.get("transformations", [])
            except json.JSONDecodeError:
                return [{"type": "general", "description": response, "confidence": 0.7}]
        except Exception as e:
            return [{"error": str(e)}]
    
    def analyze_security_deep(self, code_patterns: dict, context: str) -> dict:
        """Deep learning security analysis during compilation"""
        system_prompt = "You are a compiler security AI. Perform deep security analysis. Return JSON with security assessment."
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\nPatterns: {json.dumps(code_patterns, indent=2)}"}
            ]
            
            response = self._call_openai(messages)
            
            try:
                result = json.loads(response)
                return {
                    "vulnerabilities": result.get("vulnerabilities", []),
                    "risk_level": result.get("risk_level", "medium"),
                    "confidence": result.get("confidence", 0.8)
                }
            except json.JSONDecodeError:
                return {
                    "analysis": response,
                    "risk_level": "medium",
                    "confidence": 0.7
                }
        except Exception as e:
            return {"error": str(e), "risk_level": "unknown", "vulnerabilities": []}
    
    def analyze_compilation_error(self, error_context: dict) -> dict:
        """AI-powered error analysis and fix suggestions"""
        system_prompt = "You are a compiler error analysis AI. Analyze compilation errors. Return JSON with error analysis and fixes."
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Error: {json.dumps(error_context, indent=2)}"}
            ]
            
            response = self._call_openai(messages)
            
            try:
                result = json.loads(response)
                return {
                    "root_cause": result.get("root_cause", ""),
                    "fix_suggestions": result.get("fix_suggestions", []),
                    "prevention": result.get("prevention", "")
                }
            except json.JSONDecodeError:
                return {
                    "analysis": response,
                    "fix_suggestions": ["Review error context"],
                    "root_cause": "Analysis failed"
                }
        except Exception as e:
            return {"error": str(e), "fix_suggestions": []}
    
    def optimize_memory_layout(self, ast_data: dict) -> dict:
        """AI-driven memory layout optimization"""
        system_prompt = "You are a compiler memory optimization AI. Optimize memory layout. Return JSON with layout suggestions."
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"AST Data: {json.dumps(ast_data, indent=2)}"}
            ]
            
            response = self._call_openai(messages)
            
            try:
                result = json.loads(response)
                return {
                    "layout_suggestions": result.get("layout_suggestions", []),
                    "estimated_improvement": result.get("estimated_improvement", "")
                }
            except json.JSONDecodeError:
                return {
                    "suggestions": response,
                    "estimated_improvement": "Unknown"
                }
        except Exception as e:
            return {"error": str(e), "layout_suggestions": []}
    
    def infer_complex_types(self, code_context: dict) -> dict:
        """Neural type inference for complex scenarios"""
        system_prompt = "You are a compiler type inference AI. Infer complex types. Return JSON with type inference results."
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {json.dumps(code_context, indent=2)}"}
            ]
            
            response = self._call_openai(messages)
            
            try:
                result = json.loads(response)
                return {
                    "inferred_types": result.get("inferred_types", {}),
                    "type_relationships": result.get("type_relationships", []),
                    "confidence": result.get("confidence", 0.8)
                }
            except json.JSONDecodeError:
                return {
                    "inference": response,
                    "confidence": 0.7
                }
        except Exception as e:
            return {"error": str(e), "inferred_types": {}, "confidence": 0.0}


class CustomCompilerAIProvider(CompilerAIProvider):
    """Template for custom compiler-level AI integrations"""
    
    def __init__(self, model_name: str = "custom-compiler-ai", 
                 semantic_function=None, **kwargs):
        super().__init__(model_name, **kwargs)
        self.semantic_function = semantic_function
    
    def analyze_semantics(self, ast_representation: dict, task: str) -> dict:
        """Custom semantic analysis"""
        if self.semantic_function:
            return self.semantic_function(ast_representation, task)
        return {"semantic_insights": {}, "confidence": 0.5}
    
    def suggest_transformations(self, code_representation: str, 
                                optimization_goals: list) -> list:
        """Custom transformation suggestions"""
        return [{"type": "custom", "description": "Custom optimization"}]
    
    def analyze_security_deep(self, code_patterns: dict, context: str) -> dict:
        """Custom security analysis"""
        return {"vulnerabilities": [], "risk_level": "low", "confidence": 0.5}
    
    def analyze_compilation_error(self, error_context: dict) -> dict:
        """Custom error analysis"""
        return {"root_cause": "custom analysis", "fix_suggestions": []}
    
    def optimize_memory_layout(self, ast_data: dict) -> dict:
        """Custom memory optimization"""
        return {"layout_suggestions": [], "estimated_improvement": "custom"}
    
    def infer_complex_types(self, code_context: dict) -> dict:
        """Custom type inference"""
        return {"inferred_types": {}, "confidence": 0.5}


def get_compiler_ai_provider(provider_type: str, **kwargs) -> CompilerAIProvider:
    """Factory function to create compiler AI providers"""
    providers = {
        "ollama": OllamaCompilerProvider,
        "openai": OpenAICompilerProvider,
        "custom": CustomCompilerAIProvider
    }
    
    provider_class = providers.get(provider_type.lower())
    if not provider_class:
        raise ValueError(f"Unknown provider type: {provider_type}")
    
    return provider_class(**kwargs)