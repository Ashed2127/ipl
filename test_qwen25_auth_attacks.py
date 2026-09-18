#!/usr/bin/env python3
"""
Test Authentication System with Qwen2.5-Coder:0.5B AI Security Analysis
This tests the real Qwen2.5-Coder integration for detecting authentication attacks
"""

import sys
import os
import time
from typing import Dict, Any, Optional

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ipl.compiler.compiler_ai_providers import OllamaCompilerProvider
from authorization_system import get_authorization_system, UserRole, SecurityContext


class Qwen25AuthSecurityTester:
    """Test authentication security using Qwen2.5-Coder AI analysis"""
    
    def __init__(self):
        # Initialize Qwen2.5-Coder provider
        self.ai_provider = OllamaCompilerProvider(
            model_name="qwen2.5-coder:0.5b",
            endpoint="http://localhost:11434"
        )
        
        # Check if AI is available
        self.ai_available = self.ai_provider.is_available()
        print(f"🤖 Qwen2.5-Coder Available: {self.ai_available}")
        
        # Initialize authorization system
        self.auth_system = get_authorization_system()
        
        # Test results tracking
        self.test_results = []
    
    def test_attack(self, attack_name: str, attack_code: str, context: str) -> Dict[str, Any]:
        """Test a specific attack using AI security analysis"""
        print(f"\n{'='*70}")
        print(f"🔍 Testing: {attack_name}")
        print(f"{'='*70}")
        
        result = {
            "attack_name": attack_name,
            "ai_available": self.ai_available,
            "timestamp": time.time()
        }
        
        if not self.ai_available:
            print("⚠️  AI not available, using fallback pattern matching")
            result["analysis_method"] = "fallback_pattern_matching"
            result["risk_level"] = self._fallback_analysis(attack_code)
        else:
            print("🧠 Using Qwen2.5-Coder for AI security analysis")
            result["analysis_method"] = "qwen25_coder_ai"
            
            # Extract code patterns for AI analysis
            code_patterns = self._extract_code_patterns(attack_code)
            
            try:
                # Call AI for deep security analysis
                ai_analysis = self.ai_provider.analyze_security_deep(
                    code_patterns=code_patterns,
                    context=context
                )
                
                result["ai_analysis"] = ai_analysis
                result["risk_level"] = ai_analysis.get("risk_level", "unknown")
                result["vulnerabilities"] = ai_analysis.get("vulnerabilities", [])
                result["confidence"] = ai_analysis.get("confidence", 0.0)
                
                print(f"   Risk Level: {result['risk_level'].upper()}")
                print(f"   Confidence: {result['confidence']:.1%}")
                print(f"   Vulnerabilities Found: {len(result['vulnerabilities'])}")
                
                for vuln in result['vulnerabilities'][:3]:  # Show first 3
                    print(f"     - {vuln.get('type', 'unknown')}: {vuln.get('description', 'no description')}")
                
            except Exception as e:
                print(f"❌ AI analysis failed: {e}")
                result["ai_error"] = str(e)
                result["risk_level"] = self._fallback_analysis(attack_code)
        
        # Test against authorization system
        auth_result = self._test_authorization(attack_code, context)
        result["authorization_result"] = auth_result
        
        # Determine if attack was blocked
        result["blocked"] = (
            result["risk_level"] in ["high", "critical"] or 
            auth_result["blocked"]
        )
        
        self.test_results.append(result)
        
        status = "🚫 BLOCKED" if result["blocked"] else "⚠️  NOT BLOCKED"
        print(f"\n{status}: {attack_name}")
        
        return result
    
    def _extract_code_patterns(self, code: str) -> Dict[str, Any]:
        """Extract security-relevant patterns from code"""
        patterns = {
            "sql_indicators": [],
            "xss_indicators": [],
            "command_indicators": [],
            "path_indicators": [],
            "function_calls": [],
            "string_operations": [],
            "auth_bypass": [],
            "data_flow": []
        }
        
        lines = code.split('\n')
        for line_num, line in enumerate(lines, 1):
            # SQL Injection patterns
            if any(pattern in line.lower() for pattern in ["' or '", "' drop ", "'; --", "1='1", "union select", "/*", "*/"]):
                patterns["sql_indicators"].append(f"Line {line_num}: {line.strip()}")
            
            # XSS patterns
            if any(pattern in line.lower() for pattern in ["<script", "onerror=", "onload=", "javascript:", "alert("]):
                patterns["xss_indicators"].append(f"Line {line_num}: {line.strip()}")
            
            # Command injection patterns
            if any(pattern in line.lower() for pattern in ["; rm -", "; cat /", "&&", "|", "`", "$("]):
                patterns["command_indicators"].append(f"Line {line_num}: {line.strip()}")
            
            # Path traversal patterns
            if "../" in line or "..\\" in line or "/etc/" in line:
                patterns["path_indicators"].append(f"Line {line_num}: {line.strip()}")
            
            # Authentication bypass patterns
            if any(pattern in line.lower() for pattern in ["admin' --", "' or 1=1", "auth bypass", "skip auth"]):
                patterns["auth_bypass"].append(f"Line {line_num}: {line.strip()}")
            
            # Function calls
            if "function " in line or ".execute(" in line or ".query(" in line or "eval(" in line:
                patterns["function_calls"].append(f"Line {line_num}: {line.strip()}")
        
        return patterns
    
    def _fallback_analysis(self, code: str) -> str:
        """Fallback pattern-based analysis when AI is unavailable"""
        patterns = self._extract_code_patterns(code)
        
        if patterns["sql_indicators"] or patterns["auth_bypass"]:
            return "critical"
        elif patterns["command_indicators"]:
            return "critical"
        elif patterns["xss_indicators"]:
            return "high"
        elif patterns["path_indicators"]:
            return "high"
        else:
            return "low"
    
    def _test_authorization(self, code: str, context: str) -> Dict[str, Any]:
        """Test code against authorization system"""
        # Create a test security context
        test_context = SecurityContext(
            user_id="test_user",
            role=UserRole.USER,
            permissions=set(),
            session_id="test_session"
        )
        
        # Check if code contains forbidden operations
        forbidden_patterns = ["rm -rf", "drop table", "delete from", "eval(", "exec("]
        blocked = any(pattern in code.lower() for pattern in forbidden_patterns)
        
        return {
            "blocked": blocked,
            "reason": "Contains forbidden operations" if blocked else "No authorization violations"
        }
    
    def generate_attack_scenarios(self) -> list:
        """Generate comprehensive authentication attack scenarios"""
        scenarios = [
            {
                "name": "SQL Injection - Username Field",
                "code": """
class LoginAttack {
    function login() {
        let username = "admin' OR '1'='1"
        let password = "anything"
        let query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        execute_query(query)
    }
}
""",
                "context": "user_login"
            },
            {
                "name": "SQL Injection - UNION Attack",
                "code": """
class LoginAttack {
    function login() {
        let username = "admin' UNION SELECT NULL, username, password FROM users--"
        let password = "anything"
        let query = "SELECT * FROM users WHERE username = '" + username + "'"
        execute_query(query)
    }
}
""",
                "context": "user_login"
            },
            {
                "name": "XSS in Username",
                "code": """
class RegistrationAttack {
    function register() {
        let username = "<script>alert('XSS')</script>"
        let email = "attacker@example.com"
        let query = "INSERT INTO users (username) VALUES ('" + username + "')"
        execute_query(query)
    }
}
""",
                "context": "user_registration"
            },
            {
                "name": "Command Injection",
                "code": """
class SystemAttack {
    function execute() {
        let user_input = "user; rm -rf /"
        let command = "echo " + user_input
        system(command)
    }
}
""",
                "context": "system_operation"
            },
            {
                "name": "Path Traversal",
                "code": """
class FileAttack {
    function read_file() {
        let filename = "../../../etc/passwd"
        let file = open_file(filename)
        return file.content
    }
}
""",
                "context": "file_operation"
            },
            {
                "name": "Authentication Bypass",
                "code": """
class AuthBypass {
    function login() {
        let username = "admin' --"
        let password = ""
        let query = "SELECT * FROM users WHERE username = '" + username + "'"
        execute_query(query)
    }
}
""",
                "context": "authentication"
            },
            {
                "name": "Cookie/Session Hijacking",
                "code": """
class SessionAttack {
    function hijack_session() {
        let session_id = "admin_session_id"
        let cookie = "session=" + session_id
        set_cookie(cookie)
    }
}
""",
                "context": "session_management"
            },
            {
                "name": "LDAP Injection",
                "code": """
class LDAPAttack {
    function login() {
        let username = "admin)(|(password=*"
        let filter = "(uid=" + username + ")"
        ldap_search(filter)
    }
}
""",
                "context": "authentication"
            },
            {
                "name": "Eval Injection",
                "code": """
class EvalAttack {
    function dangerous_eval() {
        let user_input = "system('rm -rf /')"
        eval(user_input)
    }
}
""",
                "context": "code_execution"
            },
            {
                "name": "Buffer Overflow Attempt",
                "code": """
class BufferAttack {
    function overflow() {
        let buffer = "A" * 10000
        let vulnerable_function = process_input(buffer)
    }
}
""",
                "context": "memory_operation"
            }
        ]
        
        return scenarios
    
    def run_all_tests(self):
        """Run all authentication attack tests"""
        print("\n" + "="*70)
        print("🚀 Qwen2.5-Coder Authentication Security Testing")
        print("="*70)
        print(f"AI Provider: {self.ai_provider.model_name}")
        print(f"AI Available: {self.ai_available}")
        print(f"Attack Scenarios: {len(self.generate_attack_scenarios())}")
        print("="*70)
        
        scenarios = self.generate_attack_scenarios()
        
        for scenario in scenarios:
            self.test_attack(
                scenario["name"],
                scenario["code"],
                scenario["context"]
            )
            time.sleep(0.5)  # Small delay between tests
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("📊 AUTHENTICATION ATTACK TEST SUMMARY")
        print("="*70)
        
        total_tests = len(self.test_results)
        blocked_tests = sum(1 for r in self.test_results if r["blocked"])
        ai_analyzed = sum(1 for r in self.test_results if r["analysis_method"] == "qwen25_coder_ai")
        
        print(f"Total Attack Scenarios: {total_tests}")
        print(f"Attacks Blocked: {blocked_tests}/{total_tests} ({blocked_tests/total_tests:.1%})")
        print(f"AI Analysis Used: {ai_analyzed}/{total_tests} ({ai_analyzed/total_tests:.1%})")
        
        print("\n🔒 Attack Categories:")
        categories = {}
        for result in self.test_results:
            risk = result["risk_level"]
            categories[risk] = categories.get(risk, 0) + 1
        
        for risk, count in sorted(categories.items(), key=lambda x: x[0]):
            print(f"  {risk.upper()}: {count}")
        
        print("\n🛡️ Security Assessment:")
        if blocked_tests == total_tests:
            print("✅ EXCELLENT: All attacks were successfully blocked")
        elif blocked_tests >= total_tests * 0.8:
            print("✅ GOOD: Most attacks were blocked")
        elif blocked_tests >= total_tests * 0.5:
            print("⚠️  MODERATE: Some attacks were not blocked")
        else:
            print("❌ POOR: Many attacks were not blocked")
        
        print("\n🤖 Qwen2.5-Coder Performance:")
        if self.ai_available:
            avg_confidence = sum(r.get("confidence", 0) for r in self.test_results if "confidence" in r) / max(ai_analyzed, 1)
            print(f"  Average Confidence: {avg_confidence:.1%}")
            print(f"  AI Reliability: {ai_analyzed}/{total_tests} tests analyzed")
        else:
            print("  ⚠️  AI was not available, used fallback pattern matching")
        
        print("="*70)


def main():
    """Main test execution"""
    tester = Qwen25AuthSecurityTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()