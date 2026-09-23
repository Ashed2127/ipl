"""
Expert Reasoning Engine for IPL
Implements chain-of-thought reasoning for expert-level analysis.
"""
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import re
from expert_system import (
    ExpertCollaborationSystem, 
    CollaborativeDecision, 
    ExpertDomain,
    ThreatLevel
)


@dataclass
class ReasoningStep:
    """Single step in chain-of-thought reasoning."""
    step_number: int
    expert_domain: ExpertDomain
    thought_process: str
    evidence: List[str]
    conclusion: str
    confidence: float


@dataclass
class ReasoningChain:
    """Complete chain of reasoning for a decision."""
    code_snippet: str
    reasoning_steps: List[ReasoningStep]
    final_decision: str
    alternative_perspectives: List[str]
    confidence_score: float


class ExpertReasoningEngine:
    """Chain-of-thought reasoning engine for expert analysis."""
    
    def __init__(self):
        self.collaboration_system = ExpertCollaborationSystem()
        self.reasoning_history: List[ReasoningChain] = []
    
    def analyze_with_reasoning(self, code: str, context: Dict[str, Any] = None) -> Tuple[CollaborativeDecision, ReasoningChain]:
        """Perform expert analysis with detailed chain-of-thought reasoning."""
        if context is None:
            context = {}
        
        # Get collaborative analysis
        decision = self.collaboration_system.collaborative_analysis(code, context)
        
        # Build detailed reasoning chain
        reasoning_chain = self._build_reasoning_chain(code, decision)
        
        # Store reasoning history
        self.reasoning_history.append(reasoning_chain)
        
        return decision, reasoning_chain
    
    def _build_reasoning_chain(self, code: str, decision: CollaborativeDecision) -> ReasoningChain:
        """Build detailed chain-of-thought reasoning from expert analyses."""
        reasoning_steps = []
        step_number = 0
        
        # Process each expert's analysis into reasoning steps
        for domain, analysis in decision.expert_analyses.items():
            for i, reasoning_point in enumerate(analysis.reasoning):
                step_number += 1
                
                # Extract evidence from the code if relevant
                evidence = self._extract_evidence(code, reasoning_point)
                
                # Create reasoning step
                step = ReasoningStep(
                    step_number=step_number,
                    expert_domain=domain,
                    thought_process=reasoning_point,
                    evidence=evidence,
                    conclusion=analysis.findings[i] if i < len(analysis.findings) else "Analysis point",
                    confidence=analysis.confidence
                )
                reasoning_steps.append(step)
        
        # Generate alternative perspectives
        alternative_perspectives = self._generate_alternative_perspectives(decision)
        
        # Calculate overall confidence
        confidence_score = self._calculate_overall_confidence(decision)
        
        return ReasoningChain(
            code_snippet=code,
            reasoning_steps=reasoning_steps,
            final_decision=decision.final_recommendation,
            alternative_perspectives=alternative_perspectives,
            confidence_score=confidence_score
        )
    
    def _extract_evidence(self, code: str, reasoning_point: str) -> List[str]:
        """Extract relevant evidence from code based on reasoning point."""
        evidence = []
        
        # Look for code patterns mentioned in reasoning
        if "injection" in reasoning_point.lower():
            injection_patterns = [r"'\s*OR\s*'", r";\s*DROP", r"eval\s*\(", r"exec\s*\("]
            for pattern in injection_patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    evidence.append(f"Pattern matched: {pattern}")
        
        if "function" in reasoning_point.lower():
            if "fn " in code or "def " in code or "function" in code:
                evidence.append("Function definitions found in code")
        
        if "sanitize" in reasoning_point.lower():
            if "sanitize" in code.lower():
                evidence.append("Sanitization calls detected")
        
        if not evidence:
            evidence.append("No specific code patterns matched")
        
        return evidence
    
    def _generate_alternative_perspectives(self, decision: CollaborativeDecision) -> List[str]:
        """Generate alternative perspectives on the analysis."""
        alternatives = []
        
        # Security perspective alternatives
        security_analysis = decision.expert_analyses[ExpertDomain.SECURITY_SPECIALIST]
        if security_analysis.threat_level == ThreatLevel.SAFE:
            alternatives.append("Security perspective: Code appears safe, but consider edge cases and input validation")
        else:
            alternatives.append(f"Security perspective: Threat level {security_analysis.threat_level.value} requires mitigation")
        
        # Language perspective alternatives
        language_analysis = decision.expert_analyses[ExpertDomain.LANGUAGE_EXPERT]
        alternatives.append(f"Language perspective: Consider type safety and semantic type usage")
        
        # Compiler perspective alternatives
        compiler_analysis = decision.expert_analyses[ExpertDomain.COMPILER_DESIGNER]
        alternatives.append(f"Compiler perspective: Optimization opportunities may exist")
        
        return alternatives
    
    def _calculate_overall_confidence(self, decision: CollaborativeDecision) -> float:
        """Calculate overall confidence score from all expert analyses."""
        confidences = [analysis.confidence for analysis in decision.expert_analyses.values()]
        return sum(confidences) / len(confidences)
    
    def print_reasoning_report(self, reasoning_chain: ReasoningChain):
        """Print detailed reasoning report."""
        print("\n" + "="*80)
        print("EXPERT REASONING ENGINE - DETAILED ANALYSIS REPORT")
        print("="*80)
        
        print(f"\nCode Snippet: {reasoning_chain.code_snippet[:100]}...")
        print(f"\nOverall Confidence: {reasoning_chain.confidence_score:.2f}")
        print(f"Final Decision: {reasoning_chain.final_decision}")
        
        print("\n" + "-"*80)
        print("CHAIN-OF-THOUGHT REASONING STEPS")
        print("-"*80)
        
        for step in reasoning_chain.reasoning_steps:
            print(f"\nStep {step.step_number} [{step.expert_domain.value.upper()}]")
            print(f"  Thought Process: {step.thought_process}")
            print(f"  Evidence: {', '.join(step.evidence)}")
            print(f"  Conclusion: {step.conclusion}")
            print(f"  Confidence: {step.confidence:.2f}")
        
        print("\n" + "-"*80)
        print("ALTERNATIVE PERSPECTIVES")
        print("-"*80)
        for i, perspective in enumerate(reasoning_chain.alternative_perspectives, 1):
            print(f"{i}. {perspective}")
        
        print("\n" + "="*80)
    
    def get_reasoning_summary(self, reasoning_chain: ReasoningChain) -> Dict[str, Any]:
        """Get summary of reasoning for programmatic access."""
        return {
            "code_snippet": reasoning_chain.code_snippet,
            "final_decision": reasoning_chain.final_decision,
            "confidence_score": reasoning_chain.confidence_score,
            "total_reasoning_steps": len(reasoning_chain.reasoning_steps),
            "expert_domains_used": list(set(step.expert_domain for step in reasoning_chain.reasoning_steps)),
            "key_findings": [step.conclusion for step in reasoning_chain.reasoning_steps if step.evidence],
            "alternative_perspectives": reasoning_chain.alternative_perspectives
        }


class ProactiveThreatPredictor:
    """Predicts potential threats before code execution."""
    
    def __init__(self, reasoning_engine: ExpertReasoningEngine):
        self.reasoning_engine = reasoning_engine
        self.threat_predictions: List[Dict[str, Any]] = []
    
    def predict_threats(self, code: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Predict potential threats based on expert analysis."""
        if context is None:
            context = {}
        
        decision, reasoning_chain = self.reasoning_engine.analyze_with_reasoning(code, context)
        
        predictions = []
        
        # Analyze each expert's findings for threat predictions
        for domain, analysis in decision.expert_analyses.items():
            if analysis.threat_level in [ThreatLevel.HIGH_RISK, ThreatLevel.CRITICAL]:
                prediction = {
                    "threat_type": analysis.threat_level.value,
                    "expert_domain": domain.value,
                    "predicted_consequences": self._predict_consequences(analysis),
                    "prevention_measures": analysis.recommendations,
                    "confidence": analysis.confidence,
                    "reasoning_summary": analysis.reasoning[:3]  # Top 3 reasoning points
                }
                predictions.append(prediction)
        
        self.threat_predictions.extend(predictions)
        return predictions
    
    def _predict_consequences(self, analysis) -> List[str]:
        """Predict potential consequences based on analysis."""
        consequences = []
        
        if "injection" in str(analysis.findings).lower():
            consequences.extend([
                "Unauthorized data access",
                "System compromise",
                "Data exfiltration risk"
            ])
        
        if "xss" in str(analysis.findings).lower():
            consequences.extend([
                "Session hijacking",
                "User credential theft",
                "Malware distribution"
            ])
        
        if analysis.threat_level == ThreatLevel.CRITICAL:
            consequences.append("Complete system breach possible")
        
        return consequences if consequences else ["Potential security impact"]
    
    def print_threat_prediction_report(self, predictions: List[Dict[str, Any]]):
        """Print detailed threat prediction report."""
        print("\n" + "="*80)
        print("PROACTIVE THREAT PREDICTION REPORT")
        print("="*80)
        
        if not predictions:
            print("\n✅ No significant threats predicted")
            return
        
        for i, prediction in enumerate(predictions, 1):
            print(f"\n--- Threat Prediction #{i} ---")
            print(f"Threat Level: {prediction['threat_type'].upper()}")
            print(f"Expert Domain: {prediction['expert_domain']}")
            print(f"Confidence: {prediction['confidence']:.2f}")
            
            print("\nPredicted Consequences:")
            for consequence in prediction['predicted_consequences']:
                print(f"  • {consequence}")
            
            print("\nPrevention Measures:")
            for measure in prediction['prevention_measures']:
                print(f"  • {measure}")
            
            print("\nReasoning Summary:")
            for reasoning in prediction['reasoning_summary']:
                print(f"  • {reasoning}")
        
        print("\n" + "="*80)