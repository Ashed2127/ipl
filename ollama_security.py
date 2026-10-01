"""
Ollama-based Neural Security Analysis for IPL
Integrates local LLM models for intelligent security analysis
"""
import subprocess
import json
from typing import Optional, Dict, Any


class OllamaSecurityAnalyzer:
    """Neural security analysis using local Ollama models"""
    
    def __init__(self, model: str = "CyberCrew/notmythos-8b:mini"):
        self.model = model
        
    def analyze_code(self, code: str, context: str = "") -> Optional[str]:
        """
        Analyze code for security vulnerabilities using neural model
        
        Args:
            code: The code to analyze
            context: Additional context about the code
            
        Returns:
            Security analysis text or None if analysis fails
        """
        prompt = f"Security check: {code}"
        if context:
            prompt += f" ({context})"
        
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"Ollama error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("Ollama analysis timed out")
            return None
        except Exception as e:
            print(f"Ollama analysis failed: {e}")
            return None
    
    def check_sql_injection(self, code: str) -> bool:
        """Check if code might have SQL injection using neural analysis"""
        analysis = self.analyze_code(code, "Check for SQL injection")
        if analysis:
            keywords = ["sql injection", "vulnerability", "unsafe", "sanitiz"]
            return any(kw.lower() in analysis.lower() for kw in keywords)
        return False
    
    def check_xss(self, code: str) -> bool:
        """Check if code might have XSS using neural analysis"""
        analysis = self.analyze_code(code, "Check for XSS/cross-site scripting")
        if analysis:
            keywords = ["xss", "cross-site", "script", "injection", "unsafe"]
            return any(kw.lower() in analysis.lower() for kw in keywords)
        return False
    
    def suggest_sanitization(self, code: str, sink_type: str) -> Optional[str]:
        """Suggest appropriate sanitization for a given sink type"""
        prompt = f"""Code: {code}
Sink type: {sink_type}
Suggest the appropriate sanitization function to use."""
        
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            return None
            
        except Exception as e:
            print(f"Sanitization suggestion failed: {e}")
            return None


# Test the integration
if __name__ == "__main__":
    analyzer = OllamaSecurityAnalyzer()
    
    # Test SQL injection detection
    print("Testing SQL injection detection...")
    code1 = "let user_input = 'admin OR 1=1'; db_write('users', user_input);"
    result1 = analyzer.analyze_code(code1)
    print(f"Analysis: {result1}\n")
    
    # Test safe code
    print("Testing safe code...")
    code2 = "let user_input = 'admin'; let safe = sanitize_for_sql(user_input); db_write('users', safe);"
    result2 = analyzer.analyze_code(code2)
    print(f"Analysis: {result2}\n")
    
    # Test XSS detection
    print("Testing XSS detection...")
    code3 = "let user_input = '<script>alert(1)</script>'; html_render(user_input);"
    result3 = analyzer.analyze_code(code3, "Check for XSS")
    print(f"Analysis: {result3}\n")
