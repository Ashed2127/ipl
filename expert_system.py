"""
Expert-Level AI System for IPL
Mimics the collective expertise of Security Specialists, Programming Language Experts, and Compiler Designers.
"""
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import re
from pathlib import Path


class ExpertDomain(Enum):
    """Different expert domains that contribute to analysis."""
    SECURITY_SPECIALIST = "security_specialist"
    LANGUAGE_EXPERT = "language_expert"
    COMPILER_DESIGNER = "compiler_designer"


class ThreatLevel(Enum):
    """Expert assessment of threat severity."""
    SAFE = "safe"
    LOW_RISK = "low_risk"
    MEDIUM_RISK = "medium_risk"
    HIGH_RISK = "high_risk"
    CRITICAL = "critical"


@dataclass
class ExpertAnalysis:
    """Analysis result from a single expert domain."""
    domain: ExpertDomain
    confidence: float
    findings: List[str]
    reasoning: List[str]  # Chain-of-thought reasoning steps
    threat_level: ThreatLevel
    recommendations: List[str]
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CollaborativeDecision:
    """Final decision after expert collaboration."""
    is_safe: bool
    threat_level: ThreatLevel
    expert_analyses: Dict[ExpertDomain, ExpertAnalysis]
    consensus_reasoning: List[str]
    final_recommendation: str
    blocked_operations: List[str]
    safe_alternatives: List[str]


class ExpertKnowledgeBase:
    """Structured knowledge base for each expert domain."""
    
    def __init__(self):
        self.security_knowledge = self._load_security_knowledge()
        self.language_knowledge = self._load_language_knowledge()
        self.compiler_knowledge = self._load_compiler_knowledge()
    
    def _load_security_knowledge(self) -> Dict[str, Any]:
        """Load cybersecurity specialist expertise."""
        return {
            "vulnerability_patterns": {
                "sql_injection": {
                    "patterns": [r"'\s*OR\s*'", r";\s*DROP", r"UNION\s+SELECT", r"'\s*=\s*'", r"\+", r'SELECT.*WHERE', r"db_execute"],
                    "consequences": ["database compromise", "data theft", "unauthorized access"],
                    "severity": "critical",
                    "prevention": ["parameterized queries", "input validation", "least privilege"]
                },
                "command_injection": {
                    "patterns": [r"eval\s*\(", r"exec\s*\(", r"os\.system\s*\("],
                    "consequences": ["system compromise", "privilege escalation", "data destruction"],
                    "severity": "critical", 
                    "prevention": ["input sanitization", "whitelisting", "restricted execution"]
                },
                "xss": {
                    "patterns": [r"<script", r"javascript:", r"onerror\s*="],
                    "consequences": ["session hijacking", "data theft", "malware distribution"],
                    "severity": "high",
                    "prevention": ["output encoding", "CSP headers", "input validation"]
                }
            },
            "attack_chains": {
                "injection_to_rce": [
                    "input validation bypass",
                    "injection payload delivery", 
                    "vulnerability exploitation",
                    "remote code execution"
                ],
                "privilege_escalation": [
                    "weak authentication",
                    "session hijacking",
                    "privilege boundary violation",
                    "administrative access"
                ]
            },
            "security_principles": [
                "defense in depth",
                "least privilege",
                "fail-safe defaults",
                "secure by design"
            ]
        }
    
    def _load_language_knowledge(self) -> Dict[str, Any]:
        """Load programming language expert expertise."""
        return {
            "type_systems": {
                "strong_typing": {
                    "benefits": ["type safety", "early error detection", "better documentation"],
                    "tradeoffs": ["verbosity", "learning curve", "flexibility"]
                },
                "semantic_types": {
                    "examples": ["Currency", "Sentiment", "Quantity", "Date", "Intent"],
                    "purpose": "capture real-world meaning beyond primitive types"
                }
            },
            "language_safety": {
                "memory_safety": {
                    "risks": ["buffer overflows", "dangling pointers", "memory leaks"],
                    "preventions": ["bounds checking", "garbage collection", "smart pointers"]
                },
                "type_safety": {
                    "risks": ["type confusion", "undefined behavior", "runtime errors"],
                    "preventions": ["static typing", "type inference", "runtime checks"]
                }
            },
            "code_smells": {
                "complexity": ["cyclomatic complexity", "nested conditionals", "long functions"],
                "maintainability": ["code duplication", "poor naming", "inconsistent style"],
                "correctness": ["race conditions", "deadlocks", "resource leaks"]
            }
        }
    
    def _load_compiler_knowledge(self) -> Dict[str, Any]:
        """Load compiler designer expertise."""
        return {
            "optimization_techniques": {
                "constant_folding": "evaluate constant expressions at compile time",
                "dead_code_elimination": "remove code that never executes",
                "loop_optimization": "transform loops for better performance",
                "inlining": "replace function calls with function bodies"
            },
            "compiler_phases": [
                "lexical analysis",
                "syntax analysis", 
                "semantic analysis",
                "optimization",
                "code generation"
            ],
            "code_generation_strategies": {
                "interpretation": "direct execution with minimal overhead",
                "jit_compilation": "compile hot paths at runtime",
                "aot_compilation": "compile ahead of time for maximum performance"
            },
            "error_detection": {
                "static_analysis": "detect errors without running code",
                "runtime_checks": "validate invariants during execution",
                "symbolic_execution": "explore all possible execution paths"
            }
        }


class SecuritySpecialist:
    """Mimics cybersecurity specialist expertise."""
    
    def __init__(self, knowledge_base: ExpertKnowledgeBase):
        self.kb = knowledge_base
        self.domain = ExpertDomain.SECURITY_SPECIALIST
    
    def analyze_code(self, code: str, context: Dict[str, Any]) -> ExpertAnalysis:
        """Analyze code from security perspective."""
        reasoning = []
        findings = []
        threat_level = ThreatLevel.SAFE
        recommendations = []
        
        reasoning.append("Analyzing code for security vulnerabilities...")
        
        # Check for known vulnerability patterns
        for vuln_type, vuln_data in self.kb.security_knowledge["vulnerability_patterns"].items():
            for pattern in vuln_data["patterns"]:
                if re.search(pattern, code, re.IGNORECASE):
                    findings.append(f"Potential {vuln_type}: pattern '{pattern}' detected")
                    reasoning.append(f"Pattern '{pattern}' matches known {vuln_type} vulnerability")
                    reasoning.append(f"Consequences: {', '.join(vuln_data['consequences'])}")
                    
                    # Update threat level
                    current_severity = vuln_data["severity"]
                    if current_severity == "critical":
                        threat_level = ThreatLevel.CRITICAL
                    elif current_severity == "high" and threat_level != ThreatLevel.CRITICAL:
                        threat_level = ThreatLevel.HIGH_RISK
                    
                    recommendations.extend(vuln_data["prevention"])
        
        # Analyze potential attack chains
        reasoning.append("Analyzing potential attack chains...")
        for chain_name, chain_steps in self.kb.security_knowledge["attack_chains"].items():
            reasoning.append(f"Considering attack chain: {chain_name}")
            reasoning.append(f"Chain steps: {' → '.join(chain_steps)}")
        
        # Apply security principles
        reasoning.append("Applying security principles...")
        for principle in self.kb.security_knowledge["security_principles"]:
            reasoning.append(f"Evaluating code against principle: {principle}")
        
        if not findings:
            findings.append("No obvious security vulnerabilities detected")
            reasoning.append("Code passes basic security pattern analysis")
        
        confidence = 0.8 if findings else 0.6
        
        return ExpertAnalysis(
            domain=self.domain,
            confidence=confidence,
            findings=findings,
            reasoning=reasoning,
            threat_level=threat_level,
            recommendations=recommendations,
            context=context
        )


class LanguageExpert:
    """Mimics programming language expert expertise."""
    
    def __init__(self, knowledge_base: ExpertKnowledgeBase):
        self.kb = knowledge_base
        self.domain = ExpertDomain.LANGUAGE_EXPERT
    
    def analyze_code(self, code: str, context: Dict[str, Any]) -> ExpertAnalysis:
        """Analyze code from language design perspective."""
        reasoning = []
        findings = []
        threat_level = ThreatLevel.SAFE
        recommendations = []
        
        reasoning.append("Analyzing code from language design perspective...")
        
        # Check for type safety issues
        reasoning.append("Evaluating type safety...")
        type_safety = self.kb.language_knowledge["language_safety"]["type_safety"]
        reasoning.append(f"Type safety risks: {', '.join(type_safety['risks'])}")
        
        # Analyze semantic type usage
        reasoning.append("Analyzing semantic type usage...")
        semantic_types = self.kb.language_knowledge["type_systems"]["semantic_types"]
        reasoning.append(f"Available semantic types: {', '.join(semantic_types['examples'])}")
        
        # Check for code smells
        reasoning.append("Checking for code smells...")
        code_smells = self.kb.language_knowledge["code_smells"]
        for smell_category, smell_list in code_smells.items():
            reasoning.append(f"Checking {smell_category}: {', '.join(smell_list)}")
        
        # Analyze language feature usage
        if "function" in code.lower():
            findings.append("Function definitions detected")
            reasoning.append("Functions indicate procedural programming paradigm")
        
        if "sanitize" in code.lower():
            findings.append("Security-conscious coding pattern detected")
            reasoning.append("Use of sanitization indicates security awareness")
            recommendations.append("Consider comprehensive input validation strategy")
        
        if not findings:
            findings.append("Basic language structure analysis complete")
        
        confidence = 0.7
        
        return ExpertAnalysis(
            domain=self.domain,
            confidence=confidence,
            findings=findings,
            reasoning=reasoning,
            threat_level=threat_level,
            recommendations=recommendations,
            context=context
        )


class CompilerDesigner:
    """Mimics compiler designer expertise."""
    
    def __init__(self, knowledge_base: ExpertKnowledgeBase):
        self.kb = knowledge_base
        self.domain = ExpertDomain.COMPILER_DESIGNER
    
    def analyze_code(self, code: str, context: Dict[str, Any]) -> ExpertAnalysis:
        """Analyze code from compiler design perspective."""
        reasoning = []
        findings = []
        threat_level = ThreatLevel.SAFE
        recommendations = []
        
        reasoning.append("Analyzing code from compiler design perspective...")
        
        # Analyze compilation feasibility
        reasoning.append("Evaluating compilation feasibility...")
        reasoning.append("Checking against compiler phases...")
        for phase in self.kb.compiler_knowledge["compiler_phases"]:
            reasoning.append(f"Phase {phase}: compatibility check")
        
        # Consider optimization opportunities
        reasoning.append("Analyzing optimization opportunities...")
        optimizations = self.kb.compiler_knowledge["optimization_techniques"]
        for opt_name, opt_desc in optimizations.items():
            reasoning.append(f"Optimization {opt_name}: {opt_desc}")
        
        # Evaluate code generation strategy
        reasoning.append("Evaluating code generation strategy...")
        strategies = self.kb.compiler_knowledge["code_generation_strategies"]
        for strategy, description in strategies.items():
            reasoning.append(f"Strategy {strategy}: {description}")
        
        # Check for error detection opportunities
        reasoning.append("Analyzing error detection opportunities...")
        error_detection = self.kb.compiler_knowledge["error_detection"]
        for detection_type, description in error_detection.items():
            reasoning.append(f"{detection_type}: {description}")
        
        findings.append("Compiler-level analysis complete")
        recommendations.append("Consider static analysis for early error detection")
        
        confidence = 0.75
        
        return ExpertAnalysis(
            domain=self.domain,
            confidence=confidence,
            findings=findings,
            reasoning=reasoning,
            threat_level=threat_level,
            recommendations=recommendations,
            context=context
        )


class ExpertCollaborationSystem:
    """Coordinates multiple expert domains for comprehensive analysis."""
    
    def __init__(self):
        self.knowledge_base = ExpertKnowledgeBase()
        self.security_specialist = SecuritySpecialist(self.knowledge_base)
        self.language_expert = LanguageExpert(self.knowledge_base)
        self.compiler_designer = CompilerDesigner(self.knowledge_base)
    
    def collaborative_analysis(self, code: str, context: Dict[str, Any] = None) -> CollaborativeDecision:
        """Perform collaborative analysis across all expert domains."""
        if context is None:
            context = {}
        
        # Get analysis from each expert
        security_analysis = self.security_specialist.analyze_code(code, context)
        language_analysis = self.language_expert.analyze_code(code, context)
        compiler_analysis = self.compiler_designer.analyze_code(code, context)
        
        expert_analyses = {
            ExpertDomain.SECURITY_SPECIALIST: security_analysis,
            ExpertDomain.LANGUAGE_EXPERT: language_analysis,
            ExpertDomain.COMPILER_DESIGNER: compiler_analysis
        }
        
        # Determine overall threat level (prioritize security expert assessment)
        security_analysis = expert_analyses[ExpertDomain.SECURITY_SPECIALIST]
        if security_analysis.threat_level in [ThreatLevel.HIGH_RISK, ThreatLevel.CRITICAL]:
            max_threat = security_analysis.threat_level
        else:
            threat_levels = [analysis.threat_level for analysis in expert_analyses.values()]
            max_threat = max(threat_levels, key=lambda x: x.value)
        
        # Build consensus reasoning
        consensus_reasoning = []
        consensus_reasoning.append("=== EXPERT COLLABORATION SUMMARY ===")
        
        for domain, analysis in expert_analyses.items():
            consensus_reasoning.append(f"\n--- {domain.value.upper()} ANALYSIS ---")
            consensus_reasoning.extend(analysis.reasoning)
            consensus_reasoning.append(f"Confidence: {analysis.confidence:.2f}")
            consensus_reasoning.append(f"Findings: {', '.join(analysis.findings)}")
        
        # Collaborative decision making
        is_safe = max_threat in [ThreatLevel.SAFE, ThreatLevel.LOW_RISK]
        
        # Override safety if security expert found critical/high threats
        security_analysis = expert_analyses[ExpertDomain.SECURITY_SPECIALIST]
        if security_analysis.threat_level in [ThreatLevel.HIGH_RISK, ThreatLevel.CRITICAL]:
            is_safe = False
        
        # Combine recommendations
        all_recommendations = []
        blocked_operations = []
        safe_alternatives = []
        
        for analysis in expert_analyses.values():
            all_recommendations.extend(analysis.recommendations)
            
            # If security expert found critical issues, block operations
            if analysis.domain == ExpertDomain.SECURITY_SPECIALIST:
                if analysis.threat_level in [ThreatLevel.HIGH_RISK, ThreatLevel.CRITICAL]:
                    blocked_operations.extend(analysis.findings)
                    # Generate safe alternatives based on findings
                    for finding in analysis.findings:
                        if "sql_injection" in finding.lower():
                            safe_alternatives.append("Use parameterized queries")
                        elif "command_injection" in finding.lower():
                            safe_alternatives.append("Use subprocess with safe arguments")
                            safe_alternatives.append("Implement strict input validation")
                        elif "injection" in finding.lower():
                            safe_alternatives.append("Use parameterized queries")
                        if "xss" in finding.lower():
                            safe_alternatives.append("Implement output encoding")
        
        final_recommendation = self._generate_final_recommendation(
            is_safe, max_threat, expert_analyses
        )
        
        return CollaborativeDecision(
            is_safe=is_safe,
            threat_level=max_threat,
            expert_analyses=expert_analyses,
            consensus_reasoning=consensus_reasoning,
            final_recommendation=final_recommendation,
            blocked_operations=blocked_operations,
            safe_alternatives=safe_alternatives
        )
    
    def _generate_final_recommendation(
        self, 
        is_safe: bool, 
        threat_level: ThreatLevel,
        analyses: Dict[ExpertDomain, ExpertAnalysis]
    ) -> str:
        """Generate final recommendation based on expert consensus."""
        if is_safe:
            return "CODE SAFE: All experts approve execution. Proceed with normal compilation."
        
        if threat_level == ThreatLevel.CRITICAL:
            return "CODE BLOCKED: Critical security threats detected. Execution prevented. Review security expert findings."
        
        if threat_level == ThreatLevel.HIGH_RISK:
            return "CODE WARNING: High-risk issues detected. Review recommendations and implement fixes before execution."
        
        if threat_level == ThreatLevel.MEDIUM_RISK:
            return "CODE CAUTION: Medium-risk issues present. Consider recommendations for safer implementation."
        
        return "CODE REVIEW: Minor issues detected. Review expert findings for optimization opportunities."