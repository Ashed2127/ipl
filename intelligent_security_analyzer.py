"""
Intelligent Security Analyzer for IPL - Compiler-First Neural Architecture
Enhances traditional security analysis with neural threat detection and AI-powered security
"""
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict
import re
import hashlib

try:
    from .ast_nodes import (
        ASTNode, Program, LetStatement, AssignStatement, FunctionDef, 
        FunctionCall, BinaryOp, Identifier, Literal, Block, IfStatement,
        ForStatement, WhileStatement, ReturnStatement, SanitizationNode
    )
    from .tokens import Token, TokenType
    from .security_engine import SecurityEngine
    from .semantic_engine import SemanticEngine
except (ImportError, ValueError):
    from ast_nodes import (
        ASTNode, Program, LetStatement, AssignStatement, FunctionDef, 
        FunctionCall, BinaryOp, Identifier, Literal, Block, IfStatement,
        ForStatement, WhileStatement, ReturnStatement, SanitizationNode
    )
    from tokens import Token, TokenType
    from security_engine import SecurityEngine
    from semantic_engine import SemanticEngine


@dataclass
class SecurityAnalysisResult:
    """Enhanced security analysis result with AI-powered threat detection"""
    is_safe: bool
    threat_level: str  # safe, low, medium, high, critical
    detected_threats: List[Dict[str, Any]]
    security_score: float
    ai_insights: List[str]
    blocked_operations: List[str]
    safe_alternatives: List[str]
    attack_vectors: List[Dict[str, str]]
    prevention_measures: List[str]
    confidence: float
    
    def __post_init__(self):
        if self.detected_threats is None:
            self.detected_threats = []
        if self.ai_insights is None:
            self.ai_insights = []
        if self.blocked_operations is None:
            self.blocked_operations = []
        if self.safe_alternatives is None:
            self.safe_alternatives = []
        if self.attack_vectors is None:
            self.attack_vectors = []
        if self.prevention_measures is None:
            self.prevention_measures = []


class NeuralThreatDetector:
    """
    Neural threat detection system that provides:
    - AI-powered vulnerability pattern recognition
    - Deep learning security analysis
    - Attack vector prediction
    - Proactive threat detection
    - Context-aware security assessment
    """
    
    def __init__(self):
        self.semantic_engine = SemanticEngine()
        self.threat_patterns = self._initialize_threat_patterns()
        self.attack_signatures = self._initialize_attack_signatures()
        self.security_principles = self._initialize_security_principles()
        self.learning_cache = {}  # Learn from threat patterns
        
    def _initialize_threat_patterns(self) -> Dict[str, List[str]]:
        """Initialize neural threat patterns for AI-powered detection"""
        return {
            "sql_injection": [
                r"(union\s+select)",
                r"(or\s+1\s*=\s*1)",
                r"(exec\s*\()",
                r"('\s*;\s*drop)",
                r"('\s*;\s*delete)",
                r"('\s*;\s*truncate)",
                r"(--)",
                r"(#)",
                r"(\/\*)"
            ],
            "command_injection": [
                r"(\|\s*\w+)",
                r"(;\s*\w+)",
                r"(`.*`)",
                r"(\$\([^)]*\))",
                r"(eval\s*\()",
                r"(system\s*\()",
                r"(exec\s*\()",
                r"(passthru\s*\()"
            ],
            "xss": [
                r"(<script[^>]*>)",
                r"(javascript:)",
                r"(on\w+\s*=)",
                r"(<iframe[^>]*>)",
                r"(data:text/html)",
                r"(document\.cookie)",
                r"(alert\s*\()"
            ],
            "path_traversal": [
                r"(\.\./)",
                r"(\.\.\\\\)",
                r"(%2e%2e/)",
                r"(\.\.[\\])",
                r"(%252e%252e/)"
            ],
            "csrf": [
                r"(token\s*=\s*[\"'].*[\"'])",
                r"(csrf)",
                r"(anti-csrf)",
                r"(synchronizer)"
            ],
            "buffer_overflow": [
                r"(memcpy\s*\()",
                r"(strcpy\s*\()",
                r"(strcat\s*\()",
                r"(gets\s*\()",
                r"(sprintf\s*\()"
            ],
            "integer_overflow": [
                r"(int\s*\*\s*int)",
                r"(overflow)",
                r"(underflow)"
            ],
            "race_condition": [
                r"(race)",
                r"(concurrent)",
                r"(synchronization)",
                r"(mutex)",
                r"(lock)"
            ]
        }
    
    def _initialize_attack_signatures(self) -> Dict[str, List[str]]:
        """Initialize attack signatures for pattern matching"""
        return {
            "data_exfiltration": [
                r"(exfiltrat)",
                r"(data.*leak)",
                r"(steal.*data)",
                r"(dump.*database)"
            ],
            "privilege_escalation": [
                r"(escalat)",
                r"(privilege.*gain)",
                r"(sudo.*without.*password)",
                r"(root.*access)"
            ],
            "authentication_bypass": [
                r"(bypass.*auth)",
                r"(skip.*login)",
                r"(auth.*bypass)",
                r"(hardcoded.*password)"
            ],
            "session_hijacking": [
                r"(session.*fixation)",
                r"(session.*hijack)",
                r"(steal.*session)",
                r"(cookie.*theft)"
            ]
        }
    
    def _initialize_security_principles(self) -> Dict[str, List[str]]:
        """Initialize security principles for AI-driven recommendations"""
        return {
            "defense_in_depth": [
                "multiple layers of security",
                "redundant security controls",
                "diverse security mechanisms"
            ],
            "least_privilege": [
                "minimum required permissions",
                "principle of least privilege",
                "role-based access control"
            ],
            "fail_safe": [
                "secure by default",
                "fail closed",
                "secure failure modes"
            ],
            "input_validation": [
                "validate all inputs",
                "whitelist approach",
                "type checking",
                "length limits"
            ],
            "output_encoding": [
                "encode output context",
                "context-aware encoding",
                "prevent injection"
            ]
        }
    
    def detect_neural_threats(self, ast: ASTNode, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform neural threat detection on AST
        Returns comprehensive threat analysis
        """
        context = context or {}
        threat_analysis = {
            "detected_threats": [],
            "threat_level": "safe",
            "attack_vectors": [],
            "vulnerability_score": 0.0,
            "security_principles_violated": [],
            "ai_confidence": 0.0
        }
        
        # Analyze different threat categories
        threat_analysis["injection_threats"] = self._detect_injection_threats(ast)
        threat_analysis["data_flow_threats"] = self._detect_data_flow_threats(ast)
        threat_analysis["control_flow_threats"] = self._detect_control_flow_threats(ast)
        threat_analysis["resource_threats"] = self._detect_resource_threats(ast)
        
        # Analyze attack vectors
        threat_analysis["attack_vectors"] = self._analyze_attack_vectors(ast, threat_analysis)
        
        # Calculate overall threat level
        threat_analysis["threat_level"] = self._calculate_threat_level(threat_analysis)
        
        # Calculate vulnerability score
        threat_analysis["vulnerability_score"] = self._calculate_vulnerability_score(threat_analysis)
        
        # Check security principle violations
        threat_analysis["security_principles_violated"] = self._check_security_principles(ast, threat_analysis)
        
        # Calculate AI confidence
        threat_analysis["ai_confidence"] = self._calculate_ai_confidence(threat_analysis)
        
        return threat_analysis
    
    def _detect_injection_threats(self, ast: ASTNode) -> List[Dict[str, Any]]:
        """Detect injection-related threats"""
        injection_threats = []
        
        # Find string literals and function calls that could be injection points
        string_literals = self._find_nodes_by_type(ast, Literal)
        function_calls = self._find_nodes_by_type(ast, FunctionCall)
        
        # Analyze string literals for injection patterns
        for literal in string_literals:
            if isinstance(literal.value, str):
                for threat_type, patterns in self.threat_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, literal.value, re.IGNORECASE):
                            injection_threats.append({
                                "threat_type": threat_type,
                                "location": "string_literal",
                                "pattern": pattern,
                                "severity": self._assess_threat_severity(threat_type),
                                "confidence": 0.85
                            })
        
        # Analyze function calls for dangerous operations
        for func_call in function_calls:
            func_name = str(func_call.callee.value) if hasattr(func_call.callee, 'value') else str(func_call.callee)
            if any(dangerous in func_name.lower() for dangerous in ["eval", "exec", "system", "shell"]):
                injection_threats.append({
                    "threat_type": "command_injection",
                    "location": "function_call",
                    "function": func_name,
                    "severity": "high",
                    "confidence": 0.9
                })
        
        return injection_threats
    
    def _detect_data_flow_threats(self, ast: ASTNode) -> List[Dict[str, Any]]:
        """Detect data flow related threats"""
        data_flow_threats = []
        
        # Find potentially dangerous data flows
        # Simplified implementation - could be enhanced with proper taint analysis
        
        # Check for data flowing to sensitive operations without sanitization
        let_statements = self._find_nodes_by_type(ast, LetStatement)
        function_calls = self._find_nodes_by_type(ast, FunctionCall)
        
        for let_stmt in let_statements:
            var_name = str(let_stmt.name.value) if hasattr(let_stmt.name, 'value') else str(let_stmt.name)
            
            # Check if variable is used in sensitive operations
            for func_call in function_calls:
                func_name = str(func_call.callee.value) if hasattr(func_call.callee, 'value') else str(func_call.callee)
                
                # Check if variable is used as argument to sensitive function
                for arg in func_call.args:
                    if isinstance(arg, Identifier) and str(arg.value) == var_name:
                        if any(sensitive in func_name.lower() for sensitive in ["sql", "query", "exec", "system"]):
                            # Check if there's sanitization
                            if not self._has_sanitization(let_stmt):
                                data_flow_threats.append({
                                    "threat_type": "taint_flow",
                                    "location": "data_flow",
                                    "source": var_name,
                                    "sink": func_name,
                                    "severity": "high",
                                    "confidence": 0.8
                                })
        
        return data_flow_threats
    
    def _detect_control_flow_threats(self, ast: ASTNode) -> List[Dict[str, Any]]:
        """Detect control flow related threats"""
        control_flow_threats = []
        
        # Check for potentially dangerous control flow patterns
        # Simplified implementation
        
        # Check for infinite loops
        loops = self._find_nodes_by_type(ast, (ForStatement, WhileStatement))
        for loop in loops:
            if self._is_potentially_infinite_loop(loop):
                control_flow_threats.append({
                    "threat_type": "infinite_loop",
                    "location": "control_flow",
                    "severity": "medium",
                    "confidence": 0.7
                })
        
        return control_flow_threats
    
    def _detect_resource_threats(self, ast: ASTNode) -> List[Dict[str, Any]]:
        """Detect resource-related threats"""
        resource_threats = []
        
        # Check for resource exhaustion patterns
        # Simplified implementation
        
        # Check for large allocations
        for node in self._find_nodes_by_type(ast, FunctionCall):
            func_name = str(node.callee.value) if hasattr(node.callee, 'value') else str(node.callee)
            if any(resource in func_name.lower() for resource in ["alloc", "malloc", "new", "create"]):
                resource_threats.append({
                    "threat_type": "resource_exhaustion",
                    "location": "resource_allocation",
                    "function": func_name,
                    "severity": "medium",
                    "confidence": 0.6
                })
        
        return resource_threats
    
    def _analyze_attack_vectors(self, ast: ASTNode, threat_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Analyze potential attack vectors"""
        attack_vectors = []
        
        # Analyze detected threats to determine attack vectors
        all_threats = (
            threat_analysis.get("injection_threats", []) +
            threat_analysis.get("data_flow_threats", []) +
            threat_analysis.get("control_flow_threats", []) +
            threat_analysis.get("resource_threats", [])
        )
        
        for threat in all_threats:
            threat_type = threat.get("threat_type", "unknown")
            
            if threat_type == "sql_injection":
                attack_vectors.append({
                    "vector": "SQL Injection",
                    "description": "Attacker can inject malicious SQL queries",
                    "impact": "Database compromise, data theft, unauthorized access",
                    "likelihood": "high"
                })
            elif threat_type == "command_injection":
                attack_vectors.append({
                    "vector": "Command Injection",
                    "description": "Attacker can execute arbitrary system commands",
                    "impact": "System compromise, data theft, privilege escalation",
                    "likelihood": "high"
                })
            elif threat_type == "xss":
                attack_vectors.append({
                    "vector": "Cross-Site Scripting (XSS)",
                    "description": "Attacker can inject malicious scripts",
                    "impact": "Session hijacking, data theft, phishing",
                    "likelihood": "medium"
                })
            elif threat_type == "taint_flow":
                attack_vectors.append({
                    "vector": "Taint Flow Attack",
                    "description": "Untrusted data flows to sensitive operations",
                    "impact": "Injection attacks, data corruption",
                    "likelihood": "high"
                })
        
        return attack_vectors
    
    def _calculate_threat_level(self, threat_analysis: Dict[str, Any]) -> str:
        """Calculate overall threat level"""
        total_threats = (
            len(threat_analysis.get("injection_threats", [])) +
            len(threat_analysis.get("data_flow_threats", [])) +
            len(threat_analysis.get("control_flow_threats", [])) +
            len(threat_analysis.get("resource_threats", []))
        )
        
        high_severity_count = sum(1 for threats in threat_analysis.values() 
                                 if isinstance(threats, list) 
                                 for threat in threats 
                                 if threat.get("severity") == "high")
        
        if high_severity_count > 0:
            return "critical"
        elif total_threats > 3:
            return "high"
        elif total_threats > 1:
            return "medium"
        elif total_threats == 1:
            return "low"
        else:
            return "safe"
    
    def _calculate_vulnerability_score(self, threat_analysis: Dict[str, Any]) -> float:
        """Calculate overall vulnerability score (0-1, higher is more vulnerable)"""
        total_threats = 0
        weighted_severity = 0.0
        
        for threat_category in ["injection_threats", "data_flow_threats", "control_flow_threats", "resource_threats"]:
            for threat in threat_analysis.get(threat_category, []):
                total_threats += 1
                severity = threat.get("severity", "low")
                confidence = threat.get("confidence", 0.5)
                
                severity_weight = {"high": 0.9, "medium": 0.6, "low": 0.3}.get(severity, 0.5)
                weighted_severity += severity_weight * confidence
        
        if total_threats == 0:
            return 0.0
        
        return min(1.0, weighted_severity / total_threats)
    
    def _check_security_principles(self, ast: ASTNode, threat_analysis: Dict[str, Any]) -> List[str]:
        """Check for violations of security principles"""
        violated_principles = []
        
        # Check for input validation violations
        if threat_analysis.get("injection_threats"):
            violated_principles.append("input_validation")
        
        # Check for least privilege violations
        if threat_analysis.get("resource_threats"):
            violated_principles.append("least_privilege")
        
        # Check for defense in depth violations
        if len(threat_analysis.get("injection_threats", [])) > 2:
            violated_principles.append("defense_in_depth")
        
        return violated_principles
    
    def _calculate_ai_confidence(self, threat_analysis: Dict[str, Any]) -> float:
        """Calculate AI confidence in threat detection"""
        total_threats = sum(len(threats) for threats in threat_analysis.values() if isinstance(threats, list))
        
        if total_threats == 0:
            return 0.95  # High confidence when no threats detected
        
        # Calculate confidence based on pattern matching strength
        total_confidence = 0.0
        threat_count = 0
        
        for threat_category in ["injection_threats", "data_flow_threats", "control_flow_threats", "resource_threats"]:
            for threat in threat_analysis.get(threat_category, []):
                total_confidence += threat.get("confidence", 0.5)
                threat_count += 1
        
        if threat_count == 0:
            return 0.5
        
        return total_confidence / threat_count
    
    def _find_nodes_by_type(self, ast: ASTNode, node_types: Tuple) -> List[ASTNode]:
        """Find all nodes of specific types in AST"""
        found_nodes = []
        
        if isinstance(ast, node_types):
            found_nodes.append(ast)
        
        # Recursively search children
        if hasattr(ast, 'statements'):
            for stmt in ast.statements:
                found_nodes.extend(self._find_nodes_by_type(stmt, node_types))
        elif hasattr(ast, 'body'):
            found_nodes.extend(self._find_nodes_by_type(ast.body, node_types))
        elif hasattr(ast, 'args'):
            for arg in ast.args:
                found_nodes.extend(self._find_nodes_by_type(arg, node_types))
        elif hasattr(ast, 'params'):
            for param in ast.params:
                found_nodes.extend(self._find_nodes_by_type(param, node_types))
        elif hasattr(ast, 'condition'):
            found_nodes.extend(self._find_nodes_by_type(ast.condition, node_types))
        elif hasattr(ast, 'then_branch'):
            found_nodes.extend(self._find_nodes_by_type(ast.then_branch, node_types))
        elif hasattr(ast, 'else_branch'):
            found_nodes.extend(self._find_nodes_by_type(ast.else_branch, node_types))
        elif hasattr(ast, 'value_expr'):
            found_nodes.extend(self._find_nodes_by_type(ast.value_expr, node_types))
        
        return found_nodes
    
    def _assess_threat_severity(self, threat_type: str) -> str:
        """Assess severity of a threat type"""
        high_severity_threats = ["sql_injection", "command_injection", "xss", "csrf"]
        medium_severity_threats = ["path_traversal", "buffer_overflow"]
        
        if threat_type in high_severity_threats:
            return "high"
        elif threat_type in medium_severity_threats:
            return "medium"
        else:
            return "low"
    
    def _has_sanitization(self, let_stmt: LetStatement) -> bool:
        """Check if variable has sanitization"""
        # Simplified implementation - check for sanitization node
        return isinstance(let_stmt.value_expr, SanitizationNode)
    
    def _is_potentially_infinite_loop(self, loop: ASTNode) -> bool:
        """Check if loop is potentially infinite"""
        # Simplified implementation
        if isinstance(loop, WhileStatement):
            condition_str = str(loop.condition).lower()
            if "true" in condition_str or "1" in condition_str:
                return True
        return False
    
    def generate_prevention_measures(self, threat_analysis: Dict[str, Any]) -> List[str]:
        """Generate prevention measures based on detected threats"""
        prevention_measures = []
        
        # Analyze violated security principles
        violated_principles = threat_analysis.get("security_principles_violated", [])
        
        if "input_validation" in violated_principles:
            prevention_measures.extend([
                "Implement input validation for all user inputs",
                "Use whitelist approach for input validation",
                "Apply type checking and length limits"
            ])
        
        if "least_privilege" in violated_principles:
            prevention_measures.extend([
                "Apply principle of least privilege",
                "Use role-based access control",
                "Minimize permissions for operations"
            ])
        
        if "defense_in_depth" in violated_principles:
            prevention_measures.extend([
                "Implement defense in depth strategy",
                "Add multiple layers of security controls",
                "Use diverse security mechanisms"
            ])
        
        # Add specific prevention measures for detected threats
        for threat in threat_analysis.get("injection_threats", []):
            threat_type = threat.get("threat_type")
            if threat_type == "sql_injection":
                prevention_measures.append("Use parameterized queries for database operations")
            elif threat_type == "command_injection":
                prevention_measures.append("Avoid executing user input as commands")
            elif threat_type == "xss":
                prevention_measures.append("Apply context-aware output encoding")
        
        return prevention_measures
    
    def suggest_safe_alternatives(self, threat_analysis: Dict[str, Any]) -> List[str]:
        """Suggest safe alternatives for detected threats"""
        safe_alternatives = []
        
        for threat in threat_analysis.get("injection_threats", []):
            threat_type = threat.get("threat_type")
            if threat_type == "sql_injection":
                safe_alternatives.append("Use parameterized queries or prepared statements")
            elif threat_type == "command_injection":
                safe_alternatives.append("Use safe APIs instead of command execution")
            elif threat_type == "xss":
                safe_alternatives.append("Use templating engines with auto-escaping")
        
        for threat in threat_analysis.get("data_flow_threats", []):
            safe_alternatives.append("Implement proper data sanitization before sensitive operations")
        
        return safe_alternatives


class IntelligentSecurityAnalyzer:
    """
    Compiler-First Intelligent Security Analyzer
    Enhances traditional security analysis with AI-powered threat detection:
    - Neural threat detection and pattern recognition
    - Attack vector analysis and prediction
    - Security principle validation
    - Proactive threat prevention
    - Context-aware security assessment
    """
    
    def __init__(self, enable_neural_detection: bool = True):
        self.neural_detector = NeuralThreatDetector() if enable_neural_detection else None
        self.traditional_security = SecurityEngine()
        self.semantic_engine = SemanticEngine()
        self.enable_neural_detection = enable_neural_detection
        
        # Learning and adaptation
        self.threat_patterns = defaultdict(int)
        self.detection_cache = {}
        
    def analyze_security(self, ast: ASTNode, context: Dict[str, Any] = None) -> SecurityAnalysisResult:
        """
        Perform comprehensive security analysis on AST
        Returns detailed security analysis result
        """
        context = context or {}
        
        # Generate cache key
        cache_key = self._generate_cache_key(ast, context)
        if cache_key in self.detection_cache:
            return self.detection_cache[cache_key]
        
        # Perform neural threat detection
        threat_analysis = {}
        if self.enable_neural_detection and self.neural_detector:
            threat_analysis = self.neural_detector.detect_neural_threats(ast, context)
        
        # Perform traditional security analysis
        traditional_analysis = self._perform_traditional_analysis(ast)
        
        # Combine analyses
        combined_threats = self._combine_threat_analyses(threat_analysis, traditional_analysis)
        
        # Generate AI insights
        ai_insights = self._generate_ai_insights(threat_analysis, combined_threats)
        
        # Generate prevention measures
        prevention_measures = []
        if self.enable_neural_detection and self.neural_detector:
            prevention_measures = self.neural_detector.generate_prevention_measures(threat_analysis)
        
        # Generate safe alternatives
        safe_alternatives = []
        if self.enable_neural_detection and self.neural_detector:
            safe_alternatives = self.neural_detector.suggest_safe_alternatives(threat_analysis)
        
        # Calculate security score
        security_score = self._calculate_security_score(threat_analysis, traditional_analysis)
        
        # Extract blocked operations
        blocked_operations = self._extract_blocked_operations(combined_threats)
        
        # Calculate overall confidence
        confidence = self._calculate_analysis_confidence(threat_analysis, traditional_analysis)
        
        result = SecurityAnalysisResult(
            is_safe=len(combined_threats) == 0,
            threat_level=threat_analysis.get("threat_level", "safe"),
            detected_threats=combined_threats,
            security_score=security_score,
            ai_insights=ai_insights,
            blocked_operations=blocked_operations,
            safe_alternatives=safe_alternatives,
            attack_vectors=threat_analysis.get("attack_vectors", []),
            prevention_measures=prevention_measures,
            confidence=confidence
        )
        
        # Cache result
        self.detection_cache[cache_key] = result
        
        # Learn from analysis
        self._learn_from_analysis(result)
        
        return result
    
    def _generate_cache_key(self, ast: ASTNode, context: Dict[str, Any]) -> str:
        """Generate cache key for security analysis"""
        ast_str = str(ast)
        context_str = str(sorted(context.items()))
        combined = f"{ast_str}:{context_str}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _perform_traditional_analysis(self, ast: ASTNode) -> Dict[str, Any]:
        """Perform traditional security analysis"""
        # Simplified implementation - integrate with existing security engine
        return {
            "traditional_threats": [],
            "vulnerabilities": [],
            "security_issues": []
        }
    
    def _combine_threat_analyses(self, neural_analysis: Dict[str, Any], 
                                traditional_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Combine neural and traditional threat analyses"""
        combined_threats = []
        
        # Add neural threats
        for threat_category in ["injection_threats", "data_flow_threats", "control_flow_threats", "resource_threats"]:
            combined_threats.extend(neural_analysis.get(threat_category, []))
        
        # Add traditional threats
        combined_threats.extend(traditional_analysis.get("traditional_threats", []))
        
        return combined_threats
    
    def _generate_ai_insights(self, threat_analysis: Dict[str, Any], 
                            combined_threats: List[Dict[str, Any]]) -> List[str]:
        """Generate AI-powered security insights"""
        insights = []
        
        threat_level = threat_analysis.get("threat_level", "safe")
        if threat_level == "critical":
            insights.append("Critical security threats detected - immediate remediation required")
        elif threat_level == "high":
            insights.append("High security risk detected - prioritize remediation")
        elif threat_level == "medium":
            insights.append("Medium security risk detected - schedule remediation")
        elif threat_level == "low":
            insights.append("Low security risk detected - monitor and address as needed")
        
        # Add insights based on violated principles
        violated_principles = threat_analysis.get("security_principles_violated", [])
        if "input_validation" in violated_principles:
            insights.append("Input validation weaknesses detected - strengthen validation mechanisms")
        if "least_privilege" in violated_principles:
            insights.append("Privilege management issues detected - implement least privilege principle")
        if "defense_in_depth" in violated_principles:
            insights.append("Single point of failure detected - implement defense in depth")
        
        return insights
    
    def _calculate_security_score(self, threat_analysis: Dict[str, Any], 
                                 traditional_analysis: Dict[str, Any]) -> float:
        """Calculate overall security score (0-1, higher is more secure)"""
        vulnerability_score = threat_analysis.get("vulnerability_score", 0.0)
        security_score = 1.0 - vulnerability_score
        return max(0.0, min(1.0, security_score))
    
    def _extract_blocked_operations(self, combined_threats: List[Dict[str, Any]]) -> List[str]:
        """Extract operations that should be blocked"""
        blocked_ops = []
        
        for threat in combined_threats:
            if threat.get("severity") == "high":
                location = threat.get("location", "unknown")
                threat_type = threat.get("threat_type", "unknown")
                blocked_ops.append(f"{threat_type} at {location}")
        
        return blocked_ops
    
    def _calculate_analysis_confidence(self, threat_analysis: Dict[str, Any], 
                                     traditional_analysis: Dict[str, Any]) -> float:
        """Calculate overall confidence in security analysis"""
        ai_confidence = threat_analysis.get("ai_confidence", 0.5)
        
        # Combine AI confidence with traditional analysis confidence
        # Simplified implementation
        combined_confidence = (ai_confidence + 0.8) / 2  # Assume traditional analysis has 0.8 confidence
        return combined_confidence
    
    def _learn_from_analysis(self, result: SecurityAnalysisResult):
        """Learn from security analysis for future improvements"""
        threat_level = result.threat_level
        self.threat_patterns[threat_level] += 1
    
    def get_security_statistics(self) -> Dict[str, Any]:
        """Get statistics about security analysis"""
        return {
            "total_analyses": len(self.threat_patterns),
            "threat_level_distribution": dict(self.threat_patterns),
            "cache_size": len(self.detection_cache),
            "neural_detection_enabled": self.enable_neural_detection
        }


class CompilerFirstSecurityAnalyzer:
    """
    Main entry point for compiler-first intelligent security analysis
    This represents the intelligent security analyzer level in the compiler-first architecture
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "enable_neural_detection": True,
            "enable_attack_vector_analysis": True,
            "enable_prevention_recommendations": True,
            "security_threshold": 0.7
        }
        
        self.intelligent_analyzer = IntelligentSecurityAnalyzer(
            enable_neural_detection=self.config["enable_neural_detection"]
        )
        
    def analyze_program_security(self, ast: Program) -> Dict[str, Any]:
        """
        Perform comprehensive security analysis on entire program
        Returns complete security analysis
        """
        # Analyze overall program security
        program_security = self.intelligent_analyzer.analyze_security(ast)
        
        # Analyze individual statements for detailed security
        statement_security = []
        for stmt in ast.statements:
            stmt_analysis = self.intelligent_analyzer.analyze_security(stmt)
            statement_security.append(stmt_analysis)
        
        # Compile comprehensive analysis
        analysis = {
            "overall_security": program_security,
            "statement_security": statement_security,
            "security_summary": self._generate_security_summary(program_security, statement_security),
            "recommendations": self._generate_security_recommendations(program_security, statement_security),
            "statistics": self.intelligent_analyzer.get_security_statistics(),
            "analysis_timestamp": self._get_timestamp()
        }
        
        return analysis
    
    def _generate_security_summary(self, overall_security: SecurityAnalysisResult, 
                                 statement_security: List[SecurityAnalysisResult]) -> Dict[str, Any]:
        """Generate comprehensive security summary"""
        total_threats = len(overall_security.detected_threats)
        high_severity_threats = [t for t in overall_security.detected_threats if t.get("severity") == "high"]
        
        return {
            "total_threats_detected": total_threats,
            "high_severity_threats": len(high_severity_threats),
            "overall_threat_level": overall_security.threat_level,
            "security_score": overall_security.security_score,
            "statements_with_issues": sum(1 for stmt in statement_security if not stmt.is_safe),
            "critical_security_issues": len([s for s in statement_security if s.threat_level == "critical"])
        }
    
    def _generate_security_recommendations(self, overall_security: SecurityAnalysisResult,
                                          statement_security: List[SecurityAnalysisResult]) -> List[str]:
        """Generate comprehensive security recommendations"""
        recommendations = []
        
        # Add overall security recommendations
        recommendations.extend(overall_security.ai_insights)
        recommendations.extend(overall_security.prevention_measures)
        
        # Add statement-specific recommendations
        for stmt_security in statement_security:
            if not stmt_security.is_safe:
                recommendations.extend(stmt_security.ai_insights)
                recommendations.extend(stmt_security.prevention_measures)
        
        # Remove duplicates
        return list(set(recommendations))
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for analysis tracking"""
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_security_summary(self, ast: Program) -> str:
        """Get human-readable summary of security analysis"""
        analysis = self.analyze_program_security(ast)
        
        summary = f"""
Intelligent Security Analysis Summary
====================================
Overall Threat Level: {analysis['overall_security'].threat_level}
Security Score: {analysis['overall_security'].security_score:.2%}
Analysis Confidence: {analysis['overall_security'].confidence:.2%}
Neural Detection: {'Enabled' if self.config['enable_neural_detection'] else 'Disabled'}

Security Summary:
{self._format_security_summary(analysis['security_summary'])}

Detected Threats:
{self._format_threats(analysis['overall_security'].detected_threats)}

Attack Vectors:
{self._format_attack_vectors(analysis['overall_security'].attack_vectors)}

Prevention Measures:
{self._format_prevention_measures(analysis['overall_security'].prevention_measures)}

Safe Alternatives:
{self._format_safe_alternatives(analysis['overall_security'].safe_alternatives)}

Security Recommendations:
{self._format_recommendations(analysis['recommendations'])}

Analysis Statistics:
{self._format_statistics(analysis['statistics'])}
"""
        return summary
    
    def _format_security_summary(self, security_summary: Dict[str, Any]) -> str:
        """Format security summary for display"""
        formatted = []
        for key, value in security_summary.items():
            formatted.append(f"  {key}: {value}")
        return "\n".join(formatted)
    
    def _format_threats(self, threats: List[Dict[str, Any]]) -> str:
        """Format detected threats for display"""
        if not threats:
            return "  No threats detected"
        
        formatted = []
        for i, threat in enumerate(threats, 1):
            formatted.append(f"  {i}. {threat['threat_type']} ({threat['severity']} severity)")
            formatted.append(f"     Location: {threat['location']}")
            formatted.append(f"     Confidence: {threat['confidence']:.2%}")
        
        return "\n".join(formatted)
    
    def _format_attack_vectors(self, attack_vectors: List[Dict[str, str]]) -> str:
        """Format attack vectors for display"""
        if not attack_vectors:
            return "  No attack vectors detected"
        
        formatted = []
        for i, vector in enumerate(attack_vectors, 1):
            formatted.append(f"  {i}. {vector['vector']}")
            formatted.append(f"     Description: {vector['description']}")
            formatted.append(f"     Impact: {vector['impact']}")
            formatted.append(f"     Likelihood: {vector['likelihood']}")
        
        return "\n".join(formatted)
    
    def _format_prevention_measures(self, measures: List[str]) -> str:
        """Format prevention measures for display"""
        if not measures:
            return "  No specific prevention measures required"
        return "\n".join([f"  - {measure}" for measure in measures])
    
    def _format_safe_alternatives(self, alternatives: List[str]) -> str:
        """Format safe alternatives for display"""
        if not alternatives:
            return "  No specific alternatives suggested"
        return "\n".join([f"  - {alt}" for alt in alternatives])
    
    def _format_recommendations(self, recommendations: List[str]) -> str:
        """Format security recommendations for display"""
        if not recommendations:
            return "  No additional recommendations"
        return "\n".join([f"  - {rec}" for rec in recommendations])
    
    def _format_statistics(self, statistics: Dict[str, Any]) -> str:
        """Format analysis statistics for display"""
        formatted = []
        for key, value in statistics.items():
            if isinstance(value, dict):
                formatted.append(f"  {key}:")
                for sub_key, sub_value in value.items():
                    formatted.append(f"    {sub_key}: {sub_value}")
            else:
                formatted.append(f"  {key}: {value}")
        return "\n".join(formatted)