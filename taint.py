"""
Zero-Trust Data Taint Tracking System for IPL (Intelligent Programming Language / Aether).
Strictly separates Untrusted data (neural outputs, external inputs) from Trusted operations.
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import time


class TaintLevel(Enum):
    """Taint classification level for zero-trust security architecture."""
    UNTRUSTED = "Untrusted"    # Raw neural model outputs, unvalidated external data, prompt responses
    SANITIZED = "Sanitized"    # Passed through deterministic SanitizationNode or refinement invariant
    TRUSTED = "Trusted"        # Compile-time constants, hardcoded verified schemas, trusted declarations

    def __lt__(self, other: 'TaintLevel') -> bool:
        hierarchy = {TaintLevel.UNTRUSTED: 0, TaintLevel.SANITIZED: 1, TaintLevel.TRUSTED: 2}
        return hierarchy[self] < hierarchy[other]

    def __le__(self, other: 'TaintLevel') -> bool:
        hierarchy = {TaintLevel.UNTRUSTED: 0, TaintLevel.SANITIZED: 1, TaintLevel.TRUSTED: 2}
        return hierarchy[self] <= hierarchy[other]


@dataclass
class TaintTag:
    """Taint metadata attached to every IValue in the IPL runtime."""
    level: TaintLevel = TaintLevel.UNTRUSTED
    provenance: str = "neural_inference"
    sanitizer_applied: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    audit_history: List[str] = field(default_factory=list)

    def transition_to(self, new_level: TaintLevel, sanitizer_name: str) -> 'TaintTag':
        """Records deterministic sanitization transition."""
        new_history = list(self.audit_history)
        new_history.append(
            f"TaintTransition: {self.level.value} -> {new_level.value} via [{sanitizer_name}] at {time.time():.4f}"
        )
        return TaintTag(
            level=new_level,
            provenance=self.provenance,
            sanitizer_applied=sanitizer_name,
            audit_history=new_history
        )

    @classmethod
    def combine(cls, tag1: 'TaintTag', tag2: 'TaintTag', operation: str) -> 'TaintTag':
        """
        Combines two taint tags. If either operand is UNTRUSTED, result is UNTRUSTED.
        Only if both are TRUSTED does the result remain TRUSTED.
        """
        if tag1.level == TaintLevel.UNTRUSTED or tag2.level == TaintLevel.UNTRUSTED:
            combined_level = TaintLevel.UNTRUSTED
        elif tag1.level == TaintLevel.SANITIZED or tag2.level == TaintLevel.SANITIZED:
            combined_level = TaintLevel.SANITIZED
        else:
            combined_level = TaintLevel.TRUSTED

        history = tag1.audit_history + tag2.audit_history
        history.append(f"TaintCombined: ({tag1.level.value}, {tag2.level.value}) -> {combined_level.value} via op '{operation}'")
        return TaintTag(
            level=combined_level,
            provenance=f"({tag1.provenance} {operation} {tag2.provenance})",
            audit_history=history
        )


class TaintViolationError(Exception):
    """Raised when Untrusted data attempts to enter a sensitive sink without sanitization."""
    def __init__(self, variable_name: str, sink_name: str, taint_level: TaintLevel):
        super().__init__(
            f"[Zero-Trust Taint Violation] Cannot pass {taint_level.value} variable '{variable_name}' "
            f"into critical sink '{sink_name}'. "
            f"Must pass through a deterministic SanitizationNode before execution."
        )
        self.variable_name = variable_name
        self.sink_name = sink_name
        self.taint_level = taint_level
