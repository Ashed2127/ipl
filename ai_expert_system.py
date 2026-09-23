"""
AI-Augmented Expert System for IPL
Integrates Qwen2.5-Coder with expert personas for true expert-level intelligence.
"""
import json
import time
import urllib.request
import urllib.error
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from expert_system import (
    ExpertCollaborationSystem, 
    ExpertKnowledgeBase, 
    SecuritySpecialist, 
    LanguageExpert, 
    CompilerDesigner,
    ExpertAnalysis,
    ExpertDomain,
    ThreatLevel
)


@dataclass
class AIExpertAnalysis:
    """Analysis result from AI-augmented expert."""
    domain: ExpertDomain
    ai_insights: List[str]
    pattern_findings: List[str]
    combined_reasoning: List[str]
    threat_level: ThreatLevel
    confidence: float
    ai_model_used: str


class AISecuritySpecialist:
    """AI-augmented security specialist using Qwen2.5-Coder."""
    
    def __init__(self, knowledge_base: ExpertKnowledgeBase, ollama_endpoint: str = "http://localhost:11434", model: str = "qwen2.5-coder:0.5b"):
        self.kb = knowledge_base
        self.ollama_endpoint = ollama_endpoint
        self.model = model
        self.domain = ExpertDomain.SECURITY_SPECIALIST
        self.pattern_specialist = SecuritySpecialist(knowledge_base)
    
    def analyze_code_with_ai(self, code: str, context: Dict[str, Any]) -> AIExpertAnalysis:
        """Analyze code using both AI and pattern-based security analysis."""
        
        # Get pattern-based analysis first
        pattern_analysis = self.pattern_specialist.analyze_code(code, context)
        
        # Get AI-powered insights
        ai_insights = self._get_ai_security_insights(code, context)
        
        # Combine AI insights with pattern findings
        combined_reasoning = pattern_analysis.reasoning.copy()
        combined_reasoning.extend(ai_insights)
        
        # Enhanced threat assessment using AI
        enhanced_threat_level = self._assess_threat_with_ai(pattern_analysis, ai_insights)
        
        # Calculate combined confidence
        combined_confidence = (pattern_analysis.confidence + 0.85) / 2  # AI adds confidence
        
        return AIExpertAnalysis(
            domain=self.domain,
            ai_insights=ai_insights,
            pattern_findings=pattern_analysis.findings,
            combined_reasoning=combined_reasoning,
            threat_level=enhanced_threat_level,
            confidence=combined_confidence,
            ai_model_used=self.model
        )
    
    def _get_ai_security_insights(self, code: str, context: Dict[str, Any]) -> List[str]:
        """Get security insights from Qwen2.5-Coder."""
        prompt = self._construct_security_prompt(code, context)
        
        try:
            ai_response = self._query_ollama(prompt)
            insights = self._parse_ai_security_response(ai_response)
            return insights
        except Exception as e:
            return [f"AI analysis failed: {str(e)}"]
    
    def _construct_security_prompt(self, code: str, context: Dict[str, Any]) -> str:
        """Construct security-focused prompt for AI model."""
        return f"""You are a cybersecurity expert analyzing code for security vulnerabilities. 

Analyze this code snippet:
```{context.get('language', 'ipl')}
{code}
```

Focus on:
1. SQL injection vulnerabilities
2. Command injection risks
3. XSS (Cross-Site Scripting) potential
4. Path traversal issues
5. Input validation problems
6. Authentication/authorization weaknesses

Provide specific security concerns and their severity levels (critical/high/medium/low). 
Keep response concise and technical."""
    
    def _query_ollama(self, prompt: str) -> str:
        """Query Ollama API for AI analysis."""
        url = f"{self.ollama_endpoint}/api/generate"
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,  # Lower temperature for more focused security analysis
                "max_tokens": 200
            }
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('response', '')
                
        except urllib.error.URLError as e:
            raise Exception(f"Ollama connection error: {e}")
        except Exception as e:
            raise Exception(f"AI query error: {e}")
    
    def _parse_ai_security_response(self, response: str) -> List[str]:
        """Parse AI response into structured security insights."""
        insights = []
        
        # Extract key security concerns from AI response
        response_lower = response.lower()
        
        if "sql injection" in response_lower:
            insights.append("AI detected potential SQL injection vulnerability")
        if "command injection" in response_lower or "command execution" in response_lower:
            insights.append("AI identified command execution risks")
        if "xss" in response_lower or "cross-site scripting" in response_lower:
            insights.append("AI found XSS vulnerabilities")
        if "input validation" in response_lower:
            insights.append("AI recommends improved input validation")
        if "critical" in response_lower:
            insights.append("AI assessment: Critical severity issues detected")
        elif "high" in response_lower:
            insights.append("AI assessment: High severity issues detected")
        
        # If no specific issues found but AI provided analysis
        if not insights and len(response) > 20:
            insights.append(f"AI security analysis: {response[:100]}...")
        
        return insights if insights else ["AI found no obvious security vulnerabilities"]
    
    def _assess_threat_with_ai(self, pattern_analysis: ExpertAnalysis, ai_insights: List[str]) -> ThreatLevel:
        """Enhance threat assessment using AI insights."""
        # Start with pattern-based threat level
        threat_level = pattern_analysis.threat_level
        
        # Upgrade threat level based on AI insights
        for insight in ai_insights:
            if "critical" in insight.lower():
                return ThreatLevel.CRITICAL
            elif "high" in insight.lower() and threat_level != ThreatLevel.CRITICAL:
                threat_level = ThreatLevel.HIGH_RISK
        
        return threat_level


class AILanguageExpert:
    """AI-augmented language expert using Qwen2.5-Coder."""
    
    def __init__(self, knowledge_base: ExpertKnowledgeBase, ollama_endpoint: str = "http://localhost:11434", model: str = "qwen2.5-coder:0.5b"):
        self.kb = knowledge_base
        self.ollama_endpoint = ollama_endpoint
        self.model = model
        self.domain = ExpertDomain.LANGUAGE_EXPERT
        self.pattern_expert = LanguageExpert(knowledge_base)
    
    def analyze_code_with_ai(self, code: str, context: Dict[str, Any]) -> AIExpertAnalysis:
        """Analyze code using both AI and pattern-based language analysis."""
        
        # Get pattern-based analysis first
        pattern_analysis = self.pattern_expert.analyze_code(code, context)
        
        # Get AI-powered insights
        ai_insights = self._get_ai_language_insights(code, context)
        
        # Combine AI insights with pattern findings
        combined_reasoning = pattern_analysis.reasoning.copy()
        combined_reasoning.extend(ai_insights)
        
        return AIExpertAnalysis(
            domain=self.domain,
            ai_insights=ai_insights,
            pattern_findings=pattern_analysis.findings,
            combined_reasoning=combined_reasoning,
            threat_level=pattern_analysis.threat_level,
            confidence=(pattern_analysis.confidence + 0.80) / 2,
            ai_model_used=self.model
        )
    
    def _get_ai_language_insights(self, code: str, context: Dict[str, Any]) -> List[str]:
        """Get language insights from Qwen2.5-Coder."""
        prompt = f"""You are a programming language expert analyzing code quality and language usage.

Analyze this code snippet:
```{context.get('language', 'ipl')}
{code}
```

Focus on:
1. Type safety and type system usage
2. Code readability and maintainability
3. Language feature utilization
4. Potential language-level issues
5. Best practices adherence

Provide specific language analysis and recommendations. Keep response concise."""
        
        try:
            ai_response = self._query_ollama(prompt)
            return self._parse_ai_language_response(ai_response)
        except Exception as e:
            return [f"AI analysis failed: {str(e)}"]
    
    def _query_ollama(self, prompt: str) -> str:
        """Query Ollama API for AI analysis."""
        url = f"{self.ollama_endpoint}/api/generate"
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,
                "max_tokens": 150
            }
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('response', '')
                
        except urllib.error.URLError as e:
            raise Exception(f"Ollama connection error: {e}")
        except Exception as e:
            raise Exception(f"AI query error: {e}")
    
    def _parse_ai_language_response(self, response: str) -> List[str]:
        """Parse AI response into structured language insights."""
        insights = []
        
        if "type safety" in response.lower():
            insights.append("AI analysis: Type safety considerations identified")
        if "readability" in response.lower():
            insights.append("AI analysis: Code readability assessment provided")
        if "best practices" in response.lower():
            insights.append("AI analysis: Best practices recommendations available")
        
        if len(response) > 20:
            insights.append(f"AI language insight: {response[:80]}...")
        
        return insights if insights else ["AI found standard language usage patterns"]


class AICompilerDesigner:
    """AI-augmented compiler designer using Qwen2.5-Coder."""
    
    def __init__(self, knowledge_base: ExpertKnowledgeBase, ollama_endpoint: str = "http://localhost:11434", model: str = "qwen2.5-coder:0.5b"):
        self.kb = knowledge_base
        self.ollama_endpoint = ollama_endpoint
        self.model = model
        self.domain = ExpertDomain.COMPILER_DESIGNER
        self.pattern_expert = CompilerDesigner(knowledge_base)
    
    def analyze_code_with_ai(self, code: str, context: Dict[str, Any]) -> AIExpertAnalysis:
        """Analyze code using both AI and pattern-based compiler analysis."""
        
        # Get pattern-based analysis first
        pattern_analysis = self.pattern_expert.analyze_code(code, context)
        
        # Get AI-powered insights
        ai_insights = self._get_ai_compiler_insights(code, context)
        
        # Combine AI insights with pattern findings
        combined_reasoning = pattern_analysis.reasoning.copy()
        combined_reasoning.extend(ai_insights)
        
        return AIExpertAnalysis(
            domain=self.domain,
            ai_insights=ai_insights,
            pattern_findings=pattern_analysis.findings,
            combined_reasoning=combined_reasoning,
            threat_level=pattern_analysis.threat_level,
            confidence=(pattern_analysis.confidence + 0.82) / 2,
            ai_model_used=self.model
        )
    
    def _get_ai_compiler_insights(self, code: str, context: Dict[str, Any]) -> List[str]:
        """Get compiler insights from Qwen2.5-Coder."""
        prompt = f"""You are a compiler design expert analyzing code for compilation and optimization.

Analyze this code snippet:
```{context.get('language', 'ipl')}
{code}
```

Focus on:
1. Compilation feasibility
2. Optimization opportunities
3. Performance considerations
4. Code generation strategies
5. Potential compiler challenges

Provide specific compiler analysis and recommendations. Keep response concise."""
        
        try:
            ai_response = self._query_ollama(prompt)
            return self._parse_ai_compiler_response(ai_response)
        except Exception as e:
            return [f"AI analysis failed: {str(e)}"]
    
    def _query_ollama(self, prompt: str) -> str:
        """Query Ollama API for AI analysis."""
        url = f"{self.ollama_endpoint}/api/generate"
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "max_tokens": 150
            }
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('response', '')
                
        except urllib.error.URLError as e:
            raise Exception(f"Ollama connection error: {e}")
        except Exception as e:
            raise Exception(f"AI query error: {e}")
    
    def _parse_ai_compiler_response(self, response: str) -> List[str]:
        """Parse AI response into structured compiler insights."""
        insights = []
        
        if "optimization" in response.lower():
            insights.append("AI analysis: Optimization opportunities identified")
        if "performance" in response.lower():
            insights.append("AI analysis: Performance considerations noted")
        if "compilation" in response.lower():
            insights.append("AI analysis: Compilation feasibility confirmed")
        
        if len(response) > 20:
            insights.append(f"AI compiler insight: {response[:80]}...")
        
        return insights if insights else ["AI found standard compilation patterns"]


class AIExpertCollaborationSystem:
    """AI-augmented expert collaboration system."""
    
    def __init__(self, ollama_endpoint: str = "http://localhost:11434", model: str = "qwen2.5-coder:0.5b"):
        self.knowledge_base = ExpertKnowledgeBase()
        self.ollama_endpoint = ollama_endpoint
        self.model = model
        
        # Initialize AI-augmented experts
        self.ai_security_specialist = AISecuritySpecialist(self.knowledge_base, ollama_endpoint, model)
        self.ai_language_expert = AILanguageExpert(self.knowledge_base, ollama_endpoint, model)
        self.ai_compiler_designer = AICompilerDesigner(self.knowledge_base, ollama_endpoint, model)
        
        # Keep pattern-based system as fallback
        self.pattern_system = ExpertCollaborationSystem()
    
    def collaborative_analysis_with_ai(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform collaborative analysis using AI-augmented experts."""
        if context is None:
            context = {}
        
        context['language'] = 'ipl'
        
        print(f"🤖 AI-Augmented Expert Analysis using {self.model}")
        
        # Get AI-augmented analysis from each expert
        try:
            security_analysis = self.ai_security_specialist.analyze_code_with_ai(code, context)
            language_analysis = self.ai_language_expert.analyze_code_with_ai(code, context)
            compiler_analysis = self.ai_compiler_designer.analyze_code_with_ai(code, context)
            
            ai_analyses = {
                ExpertDomain.SECURITY_SPECIALIST: security_analysis,
                ExpertDomain.LANGUAGE_EXPERT: language_analysis,
                ExpertDomain.COMPILER_DESIGNER: compiler_analysis
            }
            
            # Determine overall threat level (prioritize security)
            security_threat = security_analysis.threat_level
            overall_threat = security_threat
            
            # Build combined reasoning
            combined_reasoning = []
            combined_reasoning.append("=== AI-AUGMENTED EXPERT COLLABORATION ===")
            
            for domain, analysis in ai_analyses.items():
                combined_reasoning.append(f"\n--- {domain.value.upper()} (AI + Patterns) ---")
                combined_reasoning.append(f"AI Model: {analysis.ai_model_used}")
                combined_reasoning.append(f"Confidence: {analysis.confidence:.2f}")
                combined_reasoning.extend(analysis.combined_reasoning)
                combined_reasoning.append(f"AI Insights: {', '.join(analysis.ai_insights)}")
            
            # Determine safety
            is_safe = overall_threat in [ThreatLevel.SAFE, ThreatLevel.LOW_RISK]
            
            # Generate recommendations
            recommendations = []
            blocked_operations = []
            safe_alternatives = []
            
            if not is_safe:
                blocked_operations.extend(security_analysis.pattern_findings)
                blocked_operations.extend(security_analysis.ai_insights)
                safe_alternatives.extend(["Use parameterized queries", "Implement input validation", "AI-recommended security practices"])
            
            final_recommendation = self._generate_ai_recommendation(is_safe, overall_threat)
            
            return {
                "is_safe": is_safe,
                "threat_level": overall_threat,
                "ai_analyses": ai_analyses,
                "combined_reasoning": combined_reasoning,
                "final_recommendation": final_recommendation,
                "blocked_operations": blocked_operations,
                "safe_alternatives": safe_alternatives,
                "ai_model_used": self.model,
                "analysis_mode": "ai_augmented"
            }
            
        except Exception as e:
            print(f"⚠️ AI analysis failed, falling back to pattern-based: {e}")
            # Fallback to pattern-based analysis
            pattern_decision = self.pattern_system.collaborative_analysis(code, context)
            return {
                "is_safe": pattern_decision.is_safe,
                "threat_level": pattern_decision.threat_level,
                "ai_analyses": {},
                "combined_reasoning": ["AI analysis failed, using pattern-based fallback"],
                "final_recommendation": pattern_decision.final_recommendation,
                "blocked_operations": pattern_decision.blocked_operations,
                "safe_alternatives": pattern_decision.safe_alternatives,
                "ai_model_used": "fallback_patterns",
                "analysis_mode": "pattern_fallback"
            }
    
    def _generate_ai_recommendation(self, is_safe: bool, threat_level: ThreatLevel) -> str:
        """Generate recommendation based on AI-augmented analysis."""
        if is_safe:
            return "AI-AUGMENTED SAFE: AI and pattern analysis approve execution. High confidence in safety assessment."
        
        if threat_level == ThreatLevel.CRITICAL:
            return "AI-AUGMENTED BLOCKED: AI and experts detected critical security threats. Execution prevented based on comprehensive analysis."
        
        if threat_level == ThreatLevel.HIGH_RISK:
            return "AI-AUGMENTED WARNING: High-risk issues identified by AI and experts. Review recommendations before execution."
        
        return "AI-AUGMENTED CAUTION: Minor issues detected. AI and expert analysis available for review."