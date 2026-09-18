"""
AI Decision Quality Analyzer
Advanced analysis and visualization of AI decision-making patterns
"""
import json
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime
import statistics

from ai_first_config import AIDecisionTracker, get_ai_decision_tracker


@dataclass
class DecisionPattern:
    """Pattern identified in AI decision making."""
    pattern_type: str
    frequency: int
    avg_confidence: float
    avg_time_ms: float
    success_rate: float
    examples: List[str] = field(default_factory=list)


@dataclass
class QualityMetric:
    """Quality metric for AI decisions."""
    metric_name: str
    value: float
    threshold: float
    status: str  # "good", "warning", "critical"
    trend: str  # "improving", "stable", "declining"


class AIDecisionAnalyzer:
    """Advanced analyzer for AI decision quality and patterns."""
    
    def __init__(self, tracker: Optional[AIDecisionTracker] = None):
        self.tracker = tracker or get_ai_decision_tracker()
        self.historical_data: List[Dict[str, Any]] = []
        self.patterns: List[DecisionPattern] = []
        self.quality_metrics: List[QualityMetric] = []
    
    def capture_snapshot(self) -> Dict[str, Any]:
        """Capture current snapshot of decision statistics."""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "statistics": self.tracker.get_statistics()
        }
        self.historical_data.append(snapshot)
        return snapshot
    
    def analyze_patterns(self) -> List[DecisionPattern]:
        """Analyze patterns in AI decision making."""
        stats = self.tracker.get_statistics()
        patterns = []
        
        # Analyze by task type
        task_breakdown = stats.get("task_type_breakdown", {})
        
        for task_type, task_stats in task_breakdown.items():
            if task_stats.get("total", 0) > 0:
                success_rate = task_stats.get("successes", 0) / task_stats.get("total", 1)
                avg_confidence = task_stats.get("avg_confidence", 0.0)
                avg_time = task_stats.get("avg_time_ms", 0.0)
                
                # Determine pattern type
                if success_rate > 0.9 and avg_confidence > 0.8:
                    pattern_type = "high_confidence_success"
                elif success_rate < 0.5:
                    pattern_type = "frequent_failure"
                elif avg_time > 1000:
                    pattern_type = "slow_performance"
                elif task_stats.get("fallbacks", 0) / task_stats.get("total", 1) > 0.3:
                    pattern_type = "high_fallback_rate"
                else:
                    pattern_type = "normal_operation"
                
                patterns.append(DecisionPattern(
                    pattern_type=pattern_type,
                    frequency=task_stats.get("total", 0),
                    avg_confidence=avg_confidence,
                    avg_time_ms=avg_time,
                    success_rate=success_rate,
                    examples=[f"Task: {task_type}"]
                ))
        
        self.patterns = patterns
        return patterns
    
    def calculate_quality_metrics(self) -> List[QualityMetric]:
        """Calculate quality metrics for AI decisions."""
        stats = self.tracker.get_statistics()
        metrics = []
        
        # Overall AI success rate
        ai_success_rate = stats.get("ai_success_rate", 0.0)
        metrics.append(QualityMetric(
            metric_name="AI Success Rate",
            value=ai_success_rate,
            threshold=0.8,
            status="good" if ai_success_rate >= 0.8 else ("warning" if ai_success_rate >= 0.6 else "critical"),
            trend=self._calculate_trend("ai_success_rate")
        ))
        
        # Average AI confidence
        avg_confidence = stats.get("average_ai_confidence", 0.0)
        metrics.append(QualityMetric(
            metric_name="Average AI Confidence",
            value=avg_confidence,
            threshold=0.7,
            status="good" if avg_confidence >= 0.7 else ("warning" if avg_confidence >= 0.5 else "critical"),
            trend=self._calculate_trend("average_ai_confidence")
        ))
        
        # Fallback rate
        fallback_rate = stats.get("fallback_rate", 0.0)
        metrics.append(QualityMetric(
            metric_name="Pattern Fallback Rate",
            value=fallback_rate,
            threshold=0.3,
            status="good" if fallback_rate <= 0.3 else ("warning" if fallback_rate <= 0.5 else "critical"),
            trend=self._calculate_trend("fallback_rate", inverse=True)
        ))
        
        # AI usage rate
        ai_usage_rate = stats.get("ai_usage_rate", 0.0)
        metrics.append(QualityMetric(
            metric_name="AI Usage Rate",
            value=ai_usage_rate,
            threshold=0.8,
            status="good" if ai_usage_rate >= 0.8 else ("warning" if ai_usage_rate >= 0.5 else "critical"),
            trend=self._calculate_trend("ai_usage_rate")
        ))
        
        self.quality_metrics = metrics
        return metrics
    
    def _calculate_trend(self, metric_name: str, inverse: bool = False) -> str:
        """Calculate trend based on historical data."""
        if len(self.historical_data) < 2:
            return "stable"
        
        recent_values = []
        for snapshot in self.historical_data[-5:]:  # Last 5 snapshots
            stats = snapshot.get("statistics", {})
            value = stats.get(metric_name, 0.0)
            recent_values.append(value)
        
        if len(recent_values) < 2:
            return "stable"
        
        # Simple trend calculation
        if len(recent_values) >= 3:
            first_half = statistics.mean(recent_values[:len(recent_values)//2])
            second_half = statistics.mean(recent_values[len(recent_values)//2:])
            
            if inverse:
                # For metrics where lower is better (like fallback rate)
                if second_half < first_half * 0.95:
                    return "improving"
                elif second_half > first_half * 1.05:
                    return "declining"
            else:
                # For metrics where higher is better
                if second_half > first_half * 1.05:
                    return "improving"
                elif second_half < first_half * 0.95:
                    return "declining"
        
        return "stable"
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        stats = self.tracker.get_statistics()
        
        # Check AI success rate
        if stats.get("ai_success_rate", 0.0) < 0.7:
            recommendations.append(
                "⚠️ AI success rate is below 70%. Consider adjusting confidence threshold or model selection."
            )
        
        # Check fallback rate
        if stats.get("fallback_rate", 0.0) > 0.4:
            recommendations.append(
                "⚠️ High pattern fallback rate (>40%). AI model may need fine-tuning or prompt optimization."
            )
        
        # Check confidence levels
        if stats.get("average_ai_confidence", 0.0) < 0.6:
            recommendations.append(
                "⚠️ Low average AI confidence. Consider using a larger model or improving prompts."
            )
        
        # Analyze task-specific issues
        task_breakdown = stats.get("task_type_breakdown", {})
        for task_type, task_stats in task_breakdown.items():
            success_rate = task_stats.get("successes", 0) / max(task_stats.get("total", 1), 1)
            if success_rate < 0.5 and task_stats.get("total", 0) > 5:
                recommendations.append(
                    f"⚠️ Task type '{task_type}' has low success rate ({success_rate:.1%}). "
                    f"Consider task-specific model fine-tuning or pattern enhancement."
                )
        
        # Performance recommendations
        for task_type, task_stats in task_breakdown.items():
            avg_time = task_stats.get("avg_time_ms", 0)
            if avg_time > 2000 and task_stats.get("total", 0) > 3:
                recommendations.append(
                    f"⚠️ Task type '{task_type}' has slow performance ({avg_time:.0f}ms avg). "
                    f"Consider caching or model optimization."
                )
        
        if not recommendations:
            recommendations.append("✅ AI decision quality looks good! No immediate recommendations.")
        
        return recommendations
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report."""
        self.capture_snapshot()
        patterns = self.analyze_patterns()
        metrics = self.calculate_quality_metrics()
        recommendations = self.generate_recommendations()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "current_statistics": self.tracker.get_statistics(),
            "identified_patterns": [
                {
                    "pattern_type": p.pattern_type,
                    "frequency": p.frequency,
                    "avg_confidence": p.avg_confidence,
                    "avg_time_ms": p.avg_time_ms,
                    "success_rate": p.success_rate,
                    "examples": p.examples
                }
                for p in patterns
            ],
            "quality_metrics": [
                {
                    "metric_name": m.metric_name,
                    "value": m.value,
                    "threshold": m.threshold,
                    "status": m.status,
                    "trend": m.trend
                }
                for m in metrics
            ],
            "recommendations": recommendations,
            "historical_snapshots": len(self.historical_data)
        }
    
    def print_analysis_report(self):
        """Print formatted analysis report."""
        report = self.generate_comprehensive_report()
        
        print("=" * 80)
        print("🧠 AI DECISION QUALITY ANALYSIS REPORT")
        print("=" * 80)
        print(f"Generated: {report['timestamp']}")
        print(f"Historical Data Points: {report['historical_snapshots']}")
        
        print("\n📊 CURRENT STATISTICS")
        print("-" * 80)
        stats = report['current_statistics']
        print(f"Total Decisions: {stats['total_decisions']}")
        print(f"AI Decisions: {stats['ai_decisions']} ({stats['ai_usage_rate']:.1%})")
        print(f"Pattern Fallbacks: {stats['pattern_fallbacks']} ({stats['fallback_rate']:.1%})")
        print(f"AI Success Rate: {stats['ai_success_rate']:.1%}")
        print(f"Average AI Confidence: {stats['average_ai_confidence']:.2f}")
        
        print("\n🔍 IDENTIFIED PATTERNS")
        print("-" * 80)
        for pattern in report['identified_patterns']:
            emoji = "✅" if pattern['pattern_type'] == "high_confidence_success" else \
                   "⚠️" if pattern['pattern_type'] == "frequent_failure" else \
                   "🐢" if pattern['pattern_type'] == "slow_performance" else \
                   "🔄" if pattern['pattern_type'] == "high_fallback_rate" else "📊"
            
            print(f"{emoji} {pattern['pattern_type'].replace('_', ' ').title()}")
            print(f"   Frequency: {pattern['frequency']}")
            print(f"   Success Rate: {pattern['success_rate']:.1%}")
            print(f"   Avg Confidence: {pattern['avg_confidence']:.2f}")
            print(f"   Avg Time: {pattern['avg_time_ms']:.1f}ms")
            print()
        
        print("\n📈 QUALITY METRICS")
        print("-" * 80)
        for metric in report['quality_metrics']:
            status_emoji = "✅" if metric['status'] == "good" else \
                          "⚠️" if metric['status'] == "warning" else "🚨"
            trend_emoji = "📈" if metric['trend'] == "improving" else \
                         "➡️" if metric['trend'] == "stable" else "📉"
            
            print(f"{status_emoji} {metric['metric_name']}: {metric['value']:.2f} (threshold: {metric['threshold']})")
            print(f"   Status: {metric['status'].upper()} {trend_emoji} {metric['trend'].upper()}")
            print()
        
        print("\n💡 RECOMMENDATIONS")
        print("-" * 80)
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"{i}. {rec}")
        
        print("\n" + "=" * 80)
    
    def export_analysis_data(self, filepath: str = "ai_decision_analysis.json"):
        """Export analysis data to JSON file."""
        report = self.generate_comprehensive_report()
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"📄 Analysis data exported to: {filepath}")


def main():
    """Demonstrate AI decision analysis."""
    # Get the global tracker
    tracker = get_ai_decision_tracker()
    
    # Add some sample data for demonstration
    tracker.record_ai_decision("type_inference", True, 0.85, 45.2)
    tracker.record_ai_decision("type_inference", True, 0.92, 38.7)
    tracker.record_ai_decision("sentiment_analysis", True, 0.78, 52.1)
    tracker.record_ai_decision("sentiment_analysis", False, 0.45, 120.5)
    tracker.record_ai_decision("currency_extraction", True, 0.88, 41.3)
    tracker.record_pattern_fallback("type_inference", "low_confidence")
    tracker.record_pattern_fallback("sentiment_analysis", "ai_failure")
    
    # Create analyzer and generate report
    analyzer = AIDecisionAnalyzer(tracker)
    analyzer.print_analysis_report()
    analyzer.export_analysis_data()


if __name__ == "__main__":
    main()