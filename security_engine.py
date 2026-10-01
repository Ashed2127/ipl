"""
Security Engine for IPL (Intelligent Programming Language / Aether).
Built-in malicious code and data detection with optional neural analysis via Ollama.
"""
import re
import subprocess
from typing import Dict, List, Optional, Tuple, Any


class SecurityEngine:
    """Built-in security analysis for code and data threat detection."""
    
    # Dangerous code patterns
    MALICIOUS_PATTERNS = {
        "command_injection": [
            r"eval\s*\(",
            r"exec\s*\(",
            r"__import__\s*\(",
            r"open\s*\([^)]*['\"]w['\"]",
            r"os\.system\s*\(",
            r"subprocess\.",
            r"pickle\.loads",
            r"marshal\.loads",
        ],
        "path_traversal": [
            r"\.\./",
            r"\.\.\\",
            r"/etc/passwd",
            r"/etc/shadow",
            r"windows/system32",
            r"cmd\.exe",
        ],
        "sql_injection": [
            r"'\s*OR\s*'",
            r"'\s*AND\s*'",
            r";\s*DROP",
            r";\s*DELETE",
            r"UNION\s+SELECT",
            r"--\s*$",
            r"/\*.*\*/",
        ],
        "xss": [
            r"<script",
            r"javascript:",
            r"onerror\s*=",
            r"onload\s*=",
            r"document\.cookie",
            r"alert\s*\(",
        ],
        "buffer_overflow": [
            r"[A-Z]{300,}",  # Long uppercase strings
            r"\x00",         # Null bytes
            r"%n",           # Format string
            r"%s%s%s%s%s",   # Multiple format specifiers
        ],
        "obfuscation": [
            r"base64\s*\.",
            r"rot13",
            r"chr\s*\(\d+\)\s*\+",
            r"\\\\x[0-9a-fA-F]{2}",  # Hex escape sequences
            r"\\u[0-9a-fA-F]{4}",   # Unicode escape sequences
        ],
    }
    
    # Suspicious data patterns
    MALICIOUS_DATA_PATTERNS = {
        "credit_card": [
            r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",  # Basic CC pattern
            r"\b3[47]\d{13}\b",  # AMEX
            r"\b4\d{15}\b",      # Visa
            r"\b5\d{15}\b",      # MasterCard
        ],
        "ssn": [
            r"\b\d{3}[-]?\d{2}[-]?\d{4}\b",  # SSN pattern
        ],
        "api_key": [
            r"api[_-]?key\s*[:=]\s*['\"][a-zA-Z0-9]{20,}['\"]",
            r"secret[_-]?key\s*[:=]\s*['\"][a-zA-Z0-9]{20,}['\"]",
            r"access[_-]?token\s*[:=]\s*['\"][a-zA-Z0-9]{20,}['\"]",
            r"sk-[a-zA-Z0-9]{32,}",  # Stripe-like keys
            r"AKIA[0-9A-Z]{16}",     # AWS keys
        ],
        "password": [
            r"password\s*[:=]\s*['\"][^'\"]{8,}['\"]",
            r"passwd\s*[:=]\s*['\"][^'\"]{8,}['\"]",
            r"pwd\s*[:=]\s*['\"][^'\"]{8,}['\"]",
        ],
        "malicious_urls": [
            r"https?://[^\s]*\.exe",
            r"https?://[^\s]*\.bat",
            r"https?://[^\s]*\.scr",
            r"https?://[^\s]*\.pif",
            r"https?://[^\s]*\.vbs",
        ],
        "shell_commands": [
            r"rm\s+-rf",
            r"del\s+/f",
            r"format\s+c:",
            r":>.*\.bash_history",
            r"chmod\s+777",
        ],
    }
    
    # Dangerous keywords and functions
    DANGEROUS_KEYWORDS = {
        "system": "system command execution",
        "shell": "shell access",
        "sudo": "privilege escalation",
        "su": "privilege escalation", 
        "root": "privilege escalation",
        "admin": "privilege escalation",
        "password": "credential exposure",
        "secret": "credential exposure",
        "token": "credential exposure",
        "key": "credential exposure",
        "hack": "malicious intent",
        "exploit": "malicious intent",
        "attack": "malicious intent",
        "bypass": "security circumvention",
        "inject": "injection attack",
        "overflow": "buffer overflow attempt",
    }
    
    @classmethod
    def analyze_code(cls, code: str) -> Dict[str, Any]:
        """
        Analyzes source code for malicious patterns.
        Returns security analysis report.
        """
        findings = {
            "is_malicious": False,
            "threat_level": "safe",  # safe, low, medium, high, critical
            "detected_threats": [],
            "suspicious_patterns": [],
            "dangerous_keywords": [],
            "confidence": 1.0,
        }
        
        threat_score = 0
        
        # Check for malicious code patterns
        for threat_type, patterns in cls.MALICIOUS_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)
                for match in matches:
                    threat_score += 10
                    findings["detected_threats"].append({
                        "type": threat_type,
                        "pattern": pattern,
                        "match": match.group(),
                        "position": match.start(),
                        "line": code[:match.start()].count('\n') + 1
                    })
        
        # Check for dangerous keywords
        for keyword, description in cls.DANGEROUS_KEYWORDS.items():
            if re.search(rf"\b{keyword}\b", code, re.IGNORECASE):
                threat_score += 5
                findings["dangerous_keywords"].append({
                    "keyword": keyword,
                    "description": description,
                    "context": cls._get_context(code, keyword)
                })
        
        # Check for obfuscation indicators
        if cls._detect_obfuscation(code):
            threat_score += 15
            findings["suspicious_patterns"].append({
                "type": "obfuscation",
                "description": "Code obfuscation detected"
            })
        
        # Check for excessive encoding
        if cls._detect_excessive_encoding(code):
            threat_score += 10
            findings["suspicious_patterns"].append({
                "type": "excessive_encoding",
                "description": "Excessive character encoding detected"
            })
        
        # Determine threat level
        if threat_score >= 50:
            findings["threat_level"] = "critical"
            findings["is_malicious"] = True
            findings["confidence"] = 0.95
        elif threat_score >= 30:
            findings["threat_level"] = "high"
            findings["is_malicious"] = True
            findings["confidence"] = 0.85
        elif threat_score >= 15:
            findings["threat_level"] = "medium"
            findings["confidence"] = 0.70
        elif threat_score >= 5:
            findings["threat_level"] = "low"
            findings["confidence"] = 0.50
        else:
            findings["threat_level"] = "safe"
            findings["confidence"] = 0.95
        
        return findings
    
    @classmethod
    def analyze_data(cls, data: str) -> Dict[str, Any]:
        """
        Analyzes data strings for malicious content (PII, credentials, etc.).
        Returns data security analysis report.
        """
        findings = {
            "is_malicious": False,
            "risk_level": "safe",  # safe, low, medium, high, critical
            "detected_risks": [],
            "pii_detected": [],
            "confidence": 1.0,
        }
        
        risk_score = 0
        
        # Check for malicious data patterns
        for risk_type, patterns in cls.MALICIOUS_DATA_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, data, re.IGNORECASE)
                for match in matches:
                    risk_score += 15
                    findings["detected_risks"].append({
                        "type": risk_type,
                        "pattern": pattern,
                        "match": match.group(),
                        "position": match.start()
                    })
        
        # Check for PII patterns
        pii_patterns = {
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "ip_address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
        }
        
        for pii_type, pattern in pii_patterns.items():
            matches = re.finditer(pattern, data)
            for match in matches:
                risk_score += 5
                findings["pii_detected"].append({
                    "type": pii_type,
                    "match": match.group(),
                    "position": match.start()
                })
        
        # Determine risk level
        if risk_score >= 50:
            findings["risk_level"] = "critical"
            findings["is_malicious"] = True
            findings["confidence"] = 0.95
        elif risk_score >= 30:
            findings["risk_level"] = "high"
            findings["is_malicious"] = True
            findings["confidence"] = 0.85
        elif risk_score >= 15:
            findings["risk_level"] = "medium"
            findings["confidence"] = 0.70
        elif risk_score >= 5:
            findings["risk_level"] = "low"
            findings["confidence"] = 0.50
        else:
            findings["risk_level"] = "safe"
            findings["confidence"] = 0.95
        
        return findings
    
    @classmethod
    def _get_context(cls, code: str, keyword: str, context_size: int = 50) -> str:
        """Extract context around a keyword match."""
        idx = code.lower().find(keyword.lower())
        if idx == -1:
            return ""
        start = max(0, idx - context_size)
        end = min(len(code), idx + len(keyword) + context_size)
        return code[start:end]
    
    @classmethod
    def _detect_obfuscation(cls, code: str) -> bool:
        """Detect common obfuscation techniques."""
        # Check for excessive character escaping
        escape_count = code.count('\\x') + code.count('\\u') + code.count('\\U')
        if escape_count > 5:
            return True
        
        # Check for excessive base64-like patterns
        base64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
        if len(re.findall(base64_pattern, code)) > 2:
            return True
        
        # Check for excessive random-looking hex
        hex_pattern = r'0x[0-9a-fA-F]{8,}'
        if len(re.findall(hex_pattern, code)) > 3:
            return True
        
        return False
    
    @classmethod
    def _detect_excessive_encoding(cls, code: str) -> bool:
        """Detect excessive character encoding usage."""
        # Count different encoding types
        encodings = [
            code.count('\\x'),  # Hex escapes
            code.count('\\u'),  # Unicode escapes
            code.count('\\U'),  # Long Unicode escapes
            code.count('\\N'),  # Unicode names
            code.count('\\r'),  # Raw strings
        ]
        
        total = sum(encodings)
        return total > 10
    
    @classmethod
    def sanitize_string(cls, data: str, max_length: int = 1000) -> str:
        """
        Legacy general-purpose sanitization (less safe, sink-agnostic).
        DEPRECATED: Use sink-specific sanitizers instead.
        """
        # Truncate excessive length
        if len(data) > max_length:
            data = data[:max_length] + "... [TRUNCATED]"
        
        # Remove null bytes
        data = data.replace('\x00', '')
        
        # Neutralize potential shell commands
        dangerous_commands = ['rm -rf', 'del /f', 'format c:', 'sudo', 'su']
        for cmd in dangerous_commands:
            data = data.replace(cmd, f"[SANITIZED: {cmd}]")
        
        # Mask potential credit card numbers
        cc_pattern = r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        data = re.sub(cc_pattern, '[REDACTED_CREDIT_CARD]', data)
        
        # Mask potential SSNs
        ssn_pattern = r'\b\d{3}[-]?\d{2}[-]?\d{4}\b'
        data = re.sub(ssn_pattern, '[REDACTED_SSN]', data)
        
        # Mask Stripe-like keys (do this first)
        stripe_pattern = r'sk-[a-zA-Z0-9]{20,}'
        data = re.sub(stripe_pattern, '[REDACTED_API_KEY]', data)
        
        # Mask AWS keys
        aws_pattern = r'AKIA[0-9A-Z]{16}'
        data = re.sub(aws_pattern, '[REDACTED_API_KEY]', data)
        
        # Mask potential API keys
        api_pattern = r'(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*[\'"]?[a-zA-Z0-9]{20,}[\'"]?'
        data = re.sub(api_pattern, '[REDACTED_API_KEY]', data, flags=re.IGNORECASE)
        
        return data

    @classmethod
    def sanitize_for_sql(cls, data: str, max_length: int = 1000) -> str:
        """
        SQL-specific sanitization using parameterized binding principles.
        Removes SQL injection patterns and ensures safe string format.
        """
        # Truncate excessive length
        if len(data) > max_length:
            data = data[:max_length]
        
        # Remove null bytes
        data = data.replace('\x00', '')
        
        # Remove SQL injection patterns
        sql_injection_patterns = [
            r"[';]\s*--",           # Comment termination
            r"[';]\s*#",            # Alternative comment
            r"\bor\s+",             # Boolean operators
            r"\band\s+",            # Boolean operators
            r"\bunion\s+",          # Union queries
            r"\bselect\s+",        # SELECT statements
            r"\binsert\s+",        # INSERT statements
            r"\bupdate\s+",        # UPDATE statements
            r"\bdelete\s+",        # DELETE statements
            r"\bdrop\s+",          # DROP statements
            r"\bexec\s+",          # EXECUTE statements
            r"\bxp_cmdshell",      # SQL Server command execution
            r"\bsp_executesql",    # SQL Server dynamic SQL
            r"\bwaitfor\s+delay",  # Time-based blind SQLi
            r"\bsleep\s*\(",       # Sleep functions
            r"\bbenchmark\s*\(",   # MySQL benchmark injection
        ]
        
        for pattern in sql_injection_patterns:
            data = re.sub(pattern, '', data, flags=re.IGNORECASE)
        
        # Remove common SQL metacharacters
        data = data.replace("'", "''")  # Escape single quotes
        data = data.replace('"', '""')  # Escape double quotes
        data = data.replace('\\', '\\\\')  # Escape backslashes
        
        # Remove semicolons (statement separators)
        data = data.replace(';', '')
        
        return data

    @classmethod
    def sanitize_for_html(cls, data: str, max_length: int = 10000) -> str:
        """
        HTML-specific sanitization using entity encoding.
        Prevents XSS by encoding HTML metacharacters.
        """
        # Truncate excessive length
        if len(data) > max_length:
            data = data[:max_length]
        
        # Remove null bytes
        data = data.replace('\x00', '')
        
        # HTML entity encoding
        html_escape_map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '/': '&#x2F;',
        }
        
        for char, encoded in html_escape_map.items():
            data = data.replace(char, encoded)
        
        # Remove script tags and event handlers
        script_patterns = [
            r'<script[^>]*>.*?</script>',
            r'on\w+\s*=',  # Event handlers like onclick, onerror
            r'javascript:',
            r'data:',
            r'vbscript:',
        ]
        
        for pattern in script_patterns:
            data = re.sub(pattern, '', data, flags=re.IGNORECASE | re.DOTALL)
        
        return data

    @classmethod
    def sanitize_for_shell(cls, data: str, allowed_commands: Optional[List[str]] = None, max_length: int = 1000) -> str:
        """
        Shell-specific sanitization using allowlist approach.
        Only allows commands from the allowlist, rejects everything else.
        """
        # Truncate excessive length
        if len(data) > max_length:
            data = data[:max_length]
        
        # Remove null bytes
        data = data.replace('\x00', '')
        
        # If no allowlist provided, use a very restrictive default
        if allowed_commands is None:
            allowed_commands = ['echo', 'cat', 'ls', 'pwd']
        
        # Remove shell metacharacters
        shell_metacharacters = [';', '&', '|', '`', '$', '(', ')', '<', '>', '\n', '\r']
        for char in shell_metacharacters:
            data = data.replace(char, '')
        
        # Remove dangerous command patterns
        dangerous_patterns = [
            r'\brm\s+',           # Remove command
            r'\bdelete\s+',       # Delete command
            r'\bformat\s+',       # Format command
            r'\bdel\s+',          # Delete command (Windows)
            r'\bsudo\s+',         # Sudo
            r'\bsu\s+',           # Su
            r'\bchmod\s+',        # Chmod
            r'\bchown\s+',        # Chown
            r'\bmv\s+',           # Move
            r'\bcp\s+',           # Copy
            r'\b>+\s*',           # Output redirection
            r'\b<+\s*',           # Input redirection
        ]
        
        for pattern in dangerous_patterns:
            data = re.sub(pattern, '', data, flags=re.IGNORECASE)
        
        # Check if the command is in the allowlist
        if data.split()[0] not in allowed_commands:
            # If not in allowlist, reject entirely
            return ""
        
        return data

    @classmethod
    def sanitize_for_file(cls, data: str, allowed_dirs: Optional[List[str]] = None, max_length: int = 1000) -> str:
        """
        File-specific sanitization using path validation.
        Only allows paths within allowed directories.
        """
        # Truncate excessive length
        if len(data) > max_length:
            data = data[:max_length]
        
        # Remove null bytes
        data = data.replace('\x00', '')
        
        # Remove path traversal attempts
        data = data.replace('..', '')
        data = data.replace('~', '')
        
        # Remove dangerous path patterns
        dangerous_patterns = [
            r'/etc/passwd',
            r'/etc/shadow',
            r'/proc/',
            r'/sys/',
            r'C:\\Windows\\System32',
            r'\\\\',
        ]
        
        for pattern in dangerous_patterns:
            data = re.sub(pattern, '', data, flags=re.IGNORECASE)
        
        # If allowed_dirs provided, validate path is within them
        if allowed_dirs:
            is_allowed = False
            for allowed_dir in allowed_dirs:
                if data.startswith(allowed_dir):
                    is_allowed = True
                    break
            if not is_allowed:
                return ""
        
        return data
    
    @classmethod
    def neural_security_check(cls, code: str, model: str = "CyberCrew/notmythos-8b:mini") -> Optional[str]:
        """
        Perform neural security analysis using local Ollama model.
        
        Args:
            code: The code to analyze
            model: Ollama model to use (default: CyberCrew/notmythos-8b:mini)
            
        Returns:
            Security analysis text or None if analysis fails
        """
        prompt = f"Security check: {code}"
        
        try:
            result = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return None
                
        except subprocess.TimeoutExpired:
            return None
        except Exception:
            return None
    
    @classmethod
    def neural_vulnerability_detection(cls, code: str, model: str = "CyberCrew/notmythos-8b:mini") -> Dict[str, bool]:
        """
        Use neural model to detect various vulnerability types.
        
        Args:
            code: The code to analyze
            model: Ollama model to use
            
        Returns:
            Dictionary with vulnerability detection results
        """
        analysis = cls.neural_security_check(code, model)
        
        if not analysis:
            return {
                "sql_injection": False,
                "xss": False,
                "command_injection": False,
                "path_traversal": False,
                "neural_analysis_available": False
            }
        
        analysis_lower = analysis.lower()
        
        return {
            "sql_injection": any(kw in analysis_lower for kw in ["sql injection", "sql", "database", "unauthorized"]),
            "xss": any(kw in analysis_lower for kw in ["xss", "cross-site", "script", "html", "javascript"]),
            "command_injection": any(kw in analysis_lower for kw in ["command", "shell", "exec", "system", "injection"]),
            "path_traversal": any(kw in analysis_lower for kw in ["path", "traversal", "directory", "file"]),
            "neural_analysis_available": True,
            "analysis_text": analysis
        }
    
    @classmethod
    def check_execution_safety(cls, code: str, use_neural: bool = False) -> Tuple[bool, List[str]]:
        """
        Quick safety check before code execution.
        Returns (is_safe, warning_messages).
        
        Args:
            code: Code to check
            use_neural: If True, also use neural analysis via Ollama
        """
        warnings = []
        
        # Check for eval/exec
        if re.search(r'eval\s*\(', code):
            warnings.append("WARNING: eval() detected - potential code injection risk")
        
        if re.search(r'exec\s*\(', code):
            warnings.append("WARNING: exec() detected - potential code injection risk")
        
        # Check for file operations
        if re.search(r'open\s*\([^)]*[\'"]w[\'"]', code):
            warnings.append("WARNING: File write operation detected")
        
        # Optional neural analysis
        if use_neural:
            neural_results = cls.neural_vulnerability_detection(code)
            if neural_results["neural_analysis_available"]:
                if neural_results["sql_injection"]:
                    warnings.append("NEURAL WARNING: Potential SQL injection detected")
                if neural_results["xss"]:
                    warnings.append("NEURAL WARNING: Potential XSS detected")
                if neural_results["command_injection"]:
                    warnings.append("NEURAL WARNING: Potential command injection detected")
                if neural_results["path_traversal"]:
                    warnings.append("NEURAL WARNING: Potential path traversal detected")
        
        # Check for system commands
        if re.search(r'os\.system\s*\(', code):
            warnings.append("WARNING: System command execution detected")
        
        # Check for imports of dangerous modules
        dangerous_modules = ['os', 'subprocess', 'pickle', 'marshal', 'ctypes']
        for module in dangerous_modules:
            if re.search(rf'import\s+{module}|from\s+{module}', code):
                warnings.append(f"WARNING: Import of potentially dangerous module '{module}'")
        
        is_safe = len(warnings) == 0
        return is_safe, warnings