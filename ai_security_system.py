"""
Real AI Security System for IPL using Qwen2.5-Coder:0.5b
This replaces pattern-based security with actual AI analysis
"""
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
import re


class AISecurityAnalyzer:
    """
    AI Security Analyzer using Qwen2.5-Coder:0.5b via Ollama
    
    WHAT THE AI MUST DO:
    - Analyze code/intent for security vulnerabilities
    - Understand context and semantic meaning (not just patterns)
    - Detect novel attack variants that rule-based systems miss
    - Make EXECUTE or BLOCK decisions based on actual threat analysis
    - Provide reasoning for security decisions
    
    WHAT THE AI MUST NOT DO:
    - Use hardcoded pattern matching
    - Rely on simple keyword detection
    - Make decisions based solely on regex
    - Use pre-defined rule lists
    - Fall back to traditional signature-based detection
    """
    
    def __init__(self, model_name: str = "qwen2.5-coder:0.5b", 
                 ollama_endpoint: str = "http://localhost:11434"):
        self.model_name = model_name
        self.ollama_endpoint = ollama_endpoint
        self.system_prompt = self._get_security_system_prompt()
        
    def _get_security_system_prompt(self) -> str:
        """Define the AI's role and responsibilities for security analysis."""
        return """You are IPL's Security Decision AI. Your role is to analyze code and make EXECUTE or BLOCK decisions.

YOUR PRIMARY RESPONSIBILITY:
Analyze the given code/intent and determine if it should be EXECUTED or BLOCKED based on security analysis.

WHAT YOU MUST ANALYZE:
1. Injection vulnerabilities (SQL, command, LDAP, etc.)
2. Data exfiltration risks
3. Authentication/authorization bypasses
4. Privilege escalation attempts
5. Data corruption or destruction risks
6. Business logic vulnerabilities
7. Novel attack patterns (not just known signatures)

WHAT YOU MUST NOT DO:
- Do NOT use simple pattern matching or keyword detection
- Do NOT rely solely on regex patterns
- Do NOT use pre-defined rule lists
- Do NOT make decisions based on signature matching
- Do NOT fall back to traditional detection methods

HOW TO ANALYZE:
1. Understand the semantic meaning and context
2. Look for intent behind the code, not just syntax
3. Consider data flow and potential misuse
4. Evaluate the actual security implications
5. Think like an attacker trying to exploit the code

DECISION FORMAT:
Return ONLY a JSON object with this exact structure:
{
    "decision": "EXECUTE" or "BLOCK",
    "confidence": 0.0 to 1.0,
    "reasoning": "Brief explanation of your security analysis",
    "threat_type": "type of threat if blocked, or null if safe",
    "severity": "low/medium/high/critical if blocked, or null if safe"
}

Examples:
SAFE CODE: {"decision": "EXECUTE", "confidence": 0.9, "reasoning": "Legitimate user registration with proper input validation", "threat_type": null, "severity": null}
DANGEROUS CODE: {"decision": "BLOCK", "confidence": 0.95, "reasoning": "SQL injection vulnerability through string concatenation", "threat_type": "SQL_INJECTION", "severity": "critical"}

IMPORTANT: You are the FINAL security authority. Your decision determines whether code executes or not. Be thorough and accurate."""

    def _call_ollama(self, prompt: str) -> str:
        """Make API call to Ollama for AI analysis."""
        url = f"{self.ollama_endpoint}/api/generate"
        
        payload = {
            "model": self.model_name,
            "prompt": f"{self.system_prompt}\n\nCode to analyze:\n{prompt}",
            "stream": False,
            "options": {
                "temperature": 0.2,  # Low temperature for consistent security decisions
                "num_predict": 300,   # Enough for JSON response
                "top_p": 0.9
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

    def analyze_code_for_execution(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main method: AI analyzes code and decides EXECUTE or BLOCK
        
        This is called BEFORE compilation/execution to make the security decision.
        """
        context_info = ""
        if context:
            context_info = f"\nContext: {json.dumps(context, indent=2)}"
        
        prompt = f"Code:\n{code}{context_info}\n\nAnalyze this code and return your decision as JSON."
        
        try:
            ai_response = self._call_ollama(prompt)
            
            # Extract JSON from AI response
            json_match = re.search(r'\{[^{}]*\}', ai_response, re.DOTALL)
            if json_match:
                try:
                    decision_data = json.loads(json_match.group())
                    
                    # Validate the decision structure
                    required_fields = ["decision", "confidence", "reasoning"]
                    if all(field in decision_data for field in required_fields):
                        return {
                            "success": True,
                            "decision": decision_data["decision"].upper(),
                            "confidence": decision_data["confidence"],
                            "reasoning": decision_data["reasoning"],
                            "threat_type": decision_data.get("threat_type"),
                            "severity": decision_data.get("severity"),
                            "raw_response": ai_response
                        }
                except json.JSONDecodeError:
                    pass
            
            # Fallback if JSON parsing fails
            return {
                "success": False,
                "decision": "BLOCK",  # Fail-safe: block if AI response is unclear
                "confidence": 0.5,
                "reasoning": "AI response could not be parsed - blocking for safety",
                "threat_type": "AI_PARSE_ERROR",
                "severity": "high",
                "raw_response": ai_response
            }
            
        except Exception as e:
            # Fail-safe: block if AI analysis fails
            return {
                "success": False,
                "decision": "BLOCK",
                "confidence": 0.5,
                "reasoning": f"AI analysis failed: {str(e)} - blocking for safety",
                "threat_type": "AI_FAILURE",
                "severity": "high",
                "error": str(e)
            }

    def analyze_intent_security(self, intent: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze natural language intent for security before conversion to code.
        This is the FIRST line of defense - analyze intent before code generation.
        """
        context_info = ""
        if context:
            context_info = f"\nContext: {json.dumps(context, indent=2)}"
        
        prompt = f"Intent: {intent}{context_info}\n\nAnalyze this intent for security risks and return your decision as JSON."
        
        return self.analyze_code_for_execution(prompt, context)


# Test the AI security system
if __name__ == "__main__":
    print("🧠 Testing AI Security System with Qwen2.5-Coder:0.5b")
    print("=" * 60)
    
    ai_security = AISecurityAnalyzer()
    
    # Test 1: Safe code
    safe_code = """
    fn register_user(username, password) {
        let hashed_password = sha256(password)
        db_insert("users", username, hashed_password)
        return "User registered successfully"
    }
    """
    
    print("\n🟢 Testing SAFE code:")
    result = ai_security.analyze_code_for_execution(safe_code)
    print(f"Decision: {result['decision']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reasoning: {result['reasoning']}")
    
    # Test 2: SQL injection
    sql_injection = """
    fn login(username, password) {
        let query = "SELECT * FROM users WHERE username = '" + username + "'"
        return db_execute(query)
    }
    """
    
    print("\n🔴 Testing SQL INJECTION code:")
    result = ai_security.analyze_code_for_execution(sql_injection)
    print(f"Decision: {result['decision']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reasoning: {result['reasoning']}")
    print(f"Threat Type: {result.get('threat_type')}")
    
    # Test 3: XSS attack
    xss_attack = """
    fn display_comment(user_input) {
        print "<div>" + user_input + "</div>"
        return "Comment displayed"
    }
    """
    
    print("\n🔴 Testing XSS code:")
    result = ai_security.analyze_code_for_execution(xss_attack)
    print(f"Decision: {result['decision']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reasoning: {result['reasoning']}")
    print(f"Threat Type: {result.get('threat_type')}")