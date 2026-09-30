"""
Zero-Trust Data Taint Tracking System for IPL (Intelligent Programming Language / Aether).
Strictly separates Untrusted data (neural outputs, external inputs) from Trusted operations.
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import time


class SinkKind(Enum):
    """Types of security-sensitive sinks that require specific sanitization."""
    SQL = "sql"              # Database queries - requires SQL-specific sanitization
    HTML = "html"            # HTML rendering - requires HTML entity encoding
    SHELL = "shell"          # Shell commands - requires argument escaping/allowlist
    FILE = "file"            # File operations - requires path validation
    GENERAL = "general"      # General purpose sanitization (legacy, less safe)


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
    sink_kind: Optional[SinkKind] = None  # For SANITIZED level, which sink is this safe for?
    created_at: float = field(default_factory=time.time)
    audit_history: List[str] = field(default_factory=list)

    def transition_to(self, new_level: TaintLevel, sanitizer_name: str, sink_kind: Optional[SinkKind] = None) -> 'TaintTag':
        """Records deterministic sanitization transition with optional sink kind."""
        new_history = list(self.audit_history)
        sink_info = f" for {sink_kind.value}" if sink_kind else ""
        new_history.append(
            f"TaintTransition: {self.level.value} -> {new_level.value} via [{sanitizer_name}]{sink_info} at {time.time():.4f}"
        )
        return TaintTag(
            level=new_level,
            provenance=self.provenance,
            sanitizer_applied=sanitizer_name,
            sink_kind=sink_kind if new_level == TaintLevel.SANITIZED else None,
            audit_history=new_history
        )

    def is_safe_for_sink(self, required_sink: SinkKind) -> bool:
        """Check if this taint tag is safe for use at a specific sink."""
        if self.level == TaintLevel.TRUSTED:
            return True  # Trusted data is safe for any sink
        if self.level == TaintLevel.UNTRUSTED:
            return False  # Untrusted data is never safe
        if self.level == TaintLevel.SANITIZED:
            if self.sink_kind == required_sink:
                return True  # Sanitized for the correct sink
            if self.sink_kind == SinkKind.GENERAL:
                return True  # General sanitization is accepted but less safe
            return False  # Sanitized for wrong sink
        return False

    @classmethod
    def combine(cls, tag1: 'TaintTag', tag2: 'TaintTag', operation: str) -> 'TaintTag':
        """
        Combines two taint tags. If either operand is UNTRUSTED, result is UNTRUSTED.
        Only if both are TRUSTED does the result remain TRUSTED.
        When combining SANITIZED tags, the sink_kind is reset to GENERAL unless both match.
        """
        if tag1.level == TaintLevel.UNTRUSTED or tag2.level == TaintLevel.UNTRUSTED:
            combined_level = TaintLevel.UNTRUSTED
            combined_sink_kind = None
        elif tag1.level == TaintLevel.SANITIZED or tag2.level == TaintLevel.SANITIZED:
            combined_level = TaintLevel.SANITIZED
            # If both have the same sink kind, preserve it; otherwise use GENERAL
            if tag1.sink_kind == tag2.sink_kind and tag1.sink_kind is not None:
                combined_sink_kind = tag1.sink_kind
            else:
                combined_sink_kind = SinkKind.GENERAL
        else:
            combined_level = TaintLevel.TRUSTED
            combined_sink_kind = None

        history = tag1.audit_history + tag2.audit_history
        history.append(f"TaintCombined: ({tag1.level.value}, {tag2.level.value}) -> {combined_level.value} via op '{operation}'")
        return TaintTag(
            level=combined_level,
            provenance=f"({tag1.provenance} {operation} {tag2.provenance})",
            sink_kind=combined_sink_kind,
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
