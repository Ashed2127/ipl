"""
Intelligent Security Analyzer for IPL
Based on research: "Towards intelligent compiler optimization" (Kovac et al.)
and GNN-based program analysis

This module implements:
- GNN-based security vulnerability detection
- Hybrid static/dynamic security analysis
- Learned pattern recognition for security threats
- Integration with IPL compiler pipeline
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time

from program_graph import ProgramGraph, build_program_graph, NodeType, EdgeType
from gnn_engine import GNNEngine, SecurityPattern, GNNModelType
from statistics_collector import StatisticsCollector, SecurityCheckStatistic


class SecurityDecision(Enum):
    """Security decision types"""
    EXECUTE = "execute"
    BLOCK = "block"
    WARN = "warn"


class ThreatSeverity(Enum):
    """Threat severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SecurityAnalysisResult:
    """Result of security analysis"""
    decision: SecurityDecision
    confidence: float
    threat_type: Optional[str]
    severity: Optional[ThreatSeverity]
    reasoning: str
    detected_patterns: List[str]
    static_violations: List[Dict[str, Any]]
    gnn_prediction: Optional[Dict[str, Any]]
    analysis_time_ms: float


class IntelligentSecurityAnalyzer:
    """
    Intelligent security analyzer using GNN-based analysis.

    Replaces the simple LLM-based security analysis with a
    more sophisticated GNN approach that learns from program graphs.
    Based on Kovac et al.'s GNN-based compiler optimization research.
    """

    def __init__(self,
                 gnn_engine: Optional[GNNEngine] = None,
                 statistics_collector: Optional[StatisticsCollector] = None,
                 enable_gnn: bool = True,
                 enable_static: bool = True,
                 confidence_threshold: float = 0.7):
        """
        Initialize intelligent security analyzer.

        Args:
            gnn_engine: GNN engine for pattern learning
            statistics_collector: Statistics collector for continual learning
            enable_gnn: Enable GNN-based analysis
            enable_static: Enable static analysis
            confidence_threshold: Threshold for blocking execution
        """
        self.gnn_engine = gnn_engine
        self.statistics_collector = statistics_collector
        self.enable_gnn = enable_gnn
        self.enable_static = enable_static
        self.confidence_threshold = confidence_threshold

        # Fallback to simple pattern matching if GNN not available
        self.use_fallback = not enable_gnn or gnn_engine is None

    def analyze_code(self,
                    ast_root,
                    source_code: str,
                    program_hash: str) -> SecurityAnalysisResult:
        """
        Analyze code for security vulnerabilities.

        Args:
            ast_root: AST root node
            source_code: Source code string
            program_hash: Hash of the program

        Returns:
            Security analysis result
        """
        start_time = time.time()

        # Build program graph
        program_graph = build_program_graph(ast_root)

        # Perform static analysis
        static_violations = []
        if self.enable_static:
            static_violations = self._static_analysis(program_graph)

        # Perform GNN-based analysis
        gnn_prediction = None
        detected_patterns = []

        if self.enable_gnn and not self.use_fallback and self.gnn_engine:
            try:
                gnn_prediction = self.gnn_engine.predict_security(program_graph)
                detected_patterns = self._extract_detected_patterns(gnn_prediction)
            except Exception as e:
                print(f"GNN analysis failed: {e}, falling back to static analysis")
                self.use_fallback = True

        # Combine results and make decision
        decision, threat_type, severity, reasoning = self._make_decision(
            static_violations,
            gnn_prediction,
            detected_patterns
        )

        # Calculate confidence
        confidence = self._calculate_confidence(
            static_violations,
            gnn_prediction,
            decision
        )

        analysis_time = (time.time() - start_time) * 1000

        # Record statistics
        if self.statistics_collector:
            self._record_statistics(
                program_hash,
                decision,
                threat_type,
                severity,
                confidence,
                analysis_time,
                detected_patterns
            )

        return SecurityAnalysisResult(
            decision=decision,
            confidence=confidence,
            threat_type=threat_type,
            severity=severity,
            reasoning=reasoning,
            detected_patterns=detected_patterns,
            static_violations=static_violations,
            gnn_prediction=gnn_prediction,
            analysis_time_ms=analysis_time
        )

    def _static_analysis(self, program_graph: ProgramGraph) -> List[Dict[str, Any]]:
        """
        Perform static taint analysis on program graph.

        Args:
            program_graph: Program graph

        Returns:
            List of static violations
        """
        violations = []

        # Find all sink nodes
        for node_id in program_graph.graph.nodes():
            node_data = program_graph.graph.nodes[node_id]
            node_type = node_data.get('node_type')

            if node_type == 'sink':
                # Check if data flow from source to sink without sanitization
                function_name = node_data.get('function_name', 'unknown')

                # Find data flow paths
                sources = []
                for src_id in program_graph.graph.nodes():
                    src_data = program_graph.graph.nodes[src_id]
                    if src_data.get('node_type') == 'source':
                        sources.append(src_id)

                for source_id in sources:
                    path = program_graph.get_data_flow_path(source_id, node_id)
                    if path:
                        # Check if sanitizer in path
                        has_sanitizer = any(
                            program_graph.graph.nodes[n].get('node_type') == 'sanitizer'
                            for n in path
                        )

                        if not has_sanitizer:
                            violations.append({
                                'sink': function_name,
                                'source': program_graph.graph.nodes[source_id].get('variable_name', 'unknown'),
                                'path_length': len(path),
                                'violation_type': self._map_sink_to_threat(function_name)
                            })

        # Additional check: if there's a source but no sanitizer anywhere, flag as violation
        has_source = any(
            program_graph.graph.nodes[n].get('node_type') == 'source'
            for n in program_graph.graph.nodes()
        )
        has_sanitizer = any(
            program_graph.graph.nodes[n].get('node_type') == 'sanitizer'
            for n in program_graph.graph.nodes()
        )
        has_sink = any(
            program_graph.graph.nodes[n].get('node_type') == 'sink'
            for n in program_graph.graph.nodes()
        )

        if has_source and has_sink and not has_sanitizer:
            # This is a violation - untrusted data going to sink without sanitization
            violations.append({
                'sink': 'multiple',
                'source': 'untrusted',
                'path_length': 0,
                'violation_type': 'MISSING_SANITIZATION'
            })

        return violations

    def _map_sink_to_threat(self, sink_name: str) -> str:
        """Map sink function to threat type"""
        threat_map = {
            'db_write': 'SQL_INJECTION',
            'db_execute': 'SQL_INJECTION',
            'file_write': 'PATH_TRAVERSAL',
            'html_render': 'XSS',
            'shell_exec': 'COMMAND_INJECTION',
            'system': 'COMMAND_INJECTION',
            'exec': 'COMMAND_INJECTION'
        }
        return threat_map.get(sink_name, 'UNKNOWN_THREAT')

    def _extract_detected_patterns(self, gnn_prediction: Dict[str, Any]) -> List[str]:
        """Extract detected patterns from GNN prediction"""
        patterns = []

        if gnn_prediction and 'all_probabilities' in gnn_prediction:
            probs = gnn_prediction['all_probabilities']
            pattern_names = [p.value for p in SecurityPattern]

            for i, prob in enumerate(probs):
                if i < len(pattern_names) and prob > 0.3:
                    patterns.append(f"{pattern_names[i]} ({prob:.2f})")

        return patterns

    def _make_decision(self,
                      static_violations: List[Dict[str, Any]],
                      gnn_prediction: Optional[Dict[str, Any]],
                      detected_patterns: List[str]) -> Tuple[SecurityDecision, Optional[str], Optional[ThreatSeverity], str]:
        """
        Make security decision based on analysis results.

        Args:
            static_violations: Static analysis violations
            gnn_prediction: GNN prediction results
            detected_patterns: Detected security patterns

        Returns:
            Tuple of (decision, threat_type, severity, reasoning)
        """
        # Check for critical static violations
        critical_violations = [v for v in static_violations if v['violation_type'] in ['SQL_INJECTION', 'COMMAND_INJECTION']]
        if critical_violations:
            threat_type = critical_violations[0]['violation_type']
            return (
                SecurityDecision.BLOCK,
                threat_type,
                ThreatSeverity.CRITICAL,
                f"Critical {threat_type} detected via static analysis: {len(critical_violations)} violations"
            )

        # Check GNN prediction if available
        if gnn_prediction and not gnn_prediction.get('is_safe', True):
            threat_type = gnn_prediction.get('prediction', 'UNKNOWN')
            confidence = gnn_prediction.get('confidence', 0.0)

            if confidence > self.confidence_threshold:
                severity = self._map_confidence_to_severity(confidence)
                return (
                    SecurityDecision.BLOCK,
                    threat_type,
                    severity,
                    f"GNN detected {threat_type} with {confidence:.2f} confidence"
                )

        # Check for less critical violations
        if static_violations:
            threat_type = static_violations[0]['violation_type']
            return (
                SecurityDecision.WARN,
                threat_type,
                ThreatSeverity.MEDIUM,
                f"Potential {threat_type} detected: {len(static_violations)} violations"
            )

        # No threats detected
        return (
            SecurityDecision.EXECUTE,
            None,
            None,
            "No security threats detected"
        )

    def _calculate_confidence(self,
                             static_violations: List[Dict[str, Any]],
                             gnn_prediction: Optional[Dict[str, Any]],
                             decision: SecurityDecision) -> float:
        """Calculate confidence in the decision"""
        if decision == SecurityDecision.BLOCK:
            if static_violations:
                # High confidence for static violations
                return 0.9
            elif gnn_prediction:
                # Use GNN confidence
                return gnn_prediction.get('confidence', 0.7)
            else:
                return 0.7
        elif decision == SecurityDecision.WARN:
            return 0.6
        else:
            # Execute decision
            if gnn_prediction and gnn_prediction.get('is_safe', True):
                return gnn_prediction.get('confidence', 0.8)
            else:
                return 0.8

    def _map_confidence_to_severity(self, confidence: float) -> ThreatSeverity:
        """Map confidence to threat severity"""
        if confidence > 0.9:
            return ThreatSeverity.CRITICAL
        elif confidence > 0.7:
            return ThreatSeverity.HIGH
        elif confidence > 0.5:
            return ThreatSeverity.MEDIUM
        else:
            return ThreatSeverity.LOW

    def _record_statistics(self,
                          program_hash: str,
                          decision: SecurityDecision,
                          threat_type: Optional[str],
                          severity: Optional[ThreatSeverity],
                          confidence: float,
                          analysis_time_ms: float,
                          detected_patterns: List[str]):
        """Record security check statistics"""
        if not self.statistics_collector:
            return

        check_type = "gnn" if not self.use_fallback else "static"

        stat = SecurityCheckStatistic(
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            program_hash=program_hash,
            check_type=check_type,
            detected_vulnerabilities=detected_patterns,
            false_positives=0,  # Would need ground truth
            false_negatives=0,
            true_positives=1 if decision == SecurityDecision.BLOCK else 0,
            true_negatives=1 if decision == SecurityDecision.EXECUTE else 0,
            confidence_score=confidence,
            processing_time_ms=analysis_time_ms
        )

        self.statistics_collector.record_security_check(stat)

    def get_analysis_summary(self, result: SecurityAnalysisResult) -> str:
        """Get human-readable summary of analysis result"""
        summary = f"Security Decision: {result.decision.value.upper()}\n"
        summary += f"Confidence: {result.confidence:.2f}\n"

        if result.threat_type:
            summary += f"Threat Type: {result.threat_type}\n"
        if result.severity:
            summary += f"Severity: {result.severity.value}\n"

        summary += f"Reasoning: {result.reasoning}\n"
        summary += f"Analysis Time: {result.analysis_time_ms:.2f}ms\n"

        if result.detected_patterns:
            summary += f"Detected Patterns: {', '.join(result.detected_patterns)}\n"

        if result.static_violations:
            summary += f"Static Violations: {len(result.static_violations)}\n"

        return summary


# Test the intelligent security analyzer
if __name__ == "__main__":
    from parser import Parser
    from lexer import Lexer
    from statistics_collector import StatisticsCollector

    print("Testing Intelligent Security Analyzer")

    # Initialize components
    gnn_engine = GNNEngine(device='cpu')
    gnn_engine.initialize_security_classifier(input_dim=20, hidden_dim=64, num_classes=5)

    stats_collector = StatisticsCollector(":memory:")

    analyzer = IntelligentSecurityAnalyzer(
        gnn_engine=gnn_engine,
        statistics_collector=stats_collector,
        enable_gnn=False,  # Disable GNN for testing (needs training)
        enable_static=True,
        confidence_threshold=0.7
    )

    # Test safe code
    safe_code = """
    let username = set_untrusted("admin");
    let safe_username = sanitize_for_sql(username);
    db_write("users", safe_username);
    """

    lexer = Lexer(safe_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    result = analyzer.analyze_code(ast, safe_code, "safe_hash")
    print("\nSafe Code Analysis:")
    print(analyzer.get_analysis_summary(result))

    # Test vulnerable code
    vulnerable_code = """
    let malicious = set_untrusted("'; DROP TABLE users; --");
    db_write("users", malicious);
    """

    lexer = Lexer(vulnerable_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    result = analyzer.analyze_code(ast, vulnerable_code, "vulnerable_hash")
    print("\nVulnerable Code Analysis:")
    print(analyzer.get_analysis_summary(result))

    print("\nIntelligent Security Analyzer test completed!")
