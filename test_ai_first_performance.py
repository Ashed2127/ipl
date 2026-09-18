"""
AI-First Performance Test Suite
Comprehensive comparison between AI-first mode and traditional hardcoded patterns
"""
import sys
import os
import time
import json
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compiler import LocalInferenceRuntime, NeuroSymbolicCompiler
from ast_nodes import TypeAnnotation
from ai_first_config import AIFirstConfig, get_ai_decision_tracker, reset_ai_decision_tracker
from semantic_engine import SemanticEngine


@dataclass
class TestResult:
    """Result of a single test case."""
    test_name: str
    input_text: str
    expected_type: str
    ai_first_result: Any
    pattern_result: Any
    ai_first_time_ms: float
    pattern_time_ms: float
    ai_first_success: bool
    pattern_success: bool
    ai_confidence: float
    difference: str


class AIFirstPerformanceTest:
    """Comprehensive test suite for AI-first vs pattern performance."""
    
    def __init__(self):
        self.test_cases = self._generate_test_cases()
        self.results: List[TestResult] = []
        
    def _generate_test_cases(self) -> List[Dict[str, Any]]:
        """Generate comprehensive test cases covering various scenarios."""
        return [
            # Type Inference Tests
            {
                "name": "Simple Number Extraction",
                "input": "The user is 25 years old",
                "expected_type": "Int",
                "category": "type_inference"
            },
            {
                "name": "Written Number Extraction",
                "input": "The user is twenty-five years old",
                "expected_type": "Int",
                "category": "type_inference"
            },
            {
                "name": "Complex Number Phrase",
                "input": "There are one hundred and fifty items",
                "expected_type": "Int",
                "category": "type_inference"
            },
            {
                "name": "Float Number Extraction",
                "input": "The price is 19.99 dollars",
                "expected_type": "Float",
                "category": "type_inference"
            },
            
            # Currency Extraction Tests
            {
                "name": "Simple Currency",
                "input": "The cost is $50",
                "expected_type": "Currency",
                "category": "currency_extraction"
            },
            {
                "name": "Complex Currency Phrase",
                "input": "The total price comes to forty-five dollars and ninety-nine cents",
                "expected_type": "Currency",
                "category": "currency_extraction"
            },
            {
                "name": "European Currency",
                "input": "The price is €29.99",
                "expected_type": "Currency",
                "category": "currency_extraction"
            },
            
            # Sentiment Analysis Tests
            {
                "name": "Positive Sentiment",
                "input": "The product is amazing and works perfectly",
                "expected_type": "Sentiment",
                "category": "sentiment_analysis"
            },
            {
                "name": "Negative Sentiment",
                "input": "The service is terrible and always fails",
                "expected_type": "Sentiment",
                "category": "sentiment_analysis"
            },
            {
                "name": "Mixed Sentiment",
                "input": "The product is good but the support is bad",
                "expected_type": "Sentiment",
                "category": "sentiment_analysis"
            },
            
            # Quantity Extraction Tests
            {
                "name": "Time Quantity",
                "input": "The latency is 150 milliseconds",
                "expected_type": "Quantity",
                "category": "quantity_extraction"
            },
            {
                "name": "Storage Quantity",
                "input": "The file size is 2.5 gigabytes",
                "expected_type": "Quantity",
                "category": "quantity_extraction"
            },
            {
                "name": "Speed Quantity",
                "input": "The speed is 100 km/h",
                "expected_type": "Quantity",
                "category": "quantity_extraction"
            },
            
            # Complex/Natural Language Tests
            {
                "name": "Natural Language Age",
                "input": "extract the user's age which is 30 from the document",
                "expected_type": "Int",
                "category": "complex_natural_language"
            },
            {
                "name": "Natural Language Price",
                "input": "what is the price mentioned in the text: it costs 99 dollars",
                "expected_type": "Currency",
                "category": "complex_natural_language"
            },
            {
                "name": "Contextual Sentiment",
                "input": "analyze the sentiment: the customer was delighted with the fast service",
                "expected_type": "Sentiment",
                "category": "complex_natural_language"
            },
            
            # Edge Cases
            {
                "name": "No Numbers",
                "input": "There is no numeric information here",
                "expected_type": "Int",
                "category": "edge_cases"
            },
            {
                "name": "Multiple Numbers",
                "input": "There are 25 items here and 50 there",
                "expected_type": "Int",
                "category": "edge_cases"
            },
            {
                "name": "Ambiguous Context",
                "input": "the number could be 25 or maybe 30",
                "expected_type": "Int",
                "category": "edge_cases"
            }
        ]
    
    def run_ai_first_test(self, test_case: Dict[str, Any]) -> Tuple[Any, float, bool, float]:
        """Run test with AI-first mode."""
        config = AIFirstConfig(
            primary_model="qwen2.5-coder:0.5b",
            ai_priority_mode=True,
            ai_confidence_threshold=0.7,
            track_ai_decisions=True,
            log_ai_failures=False
        )
        
        runtime = LocalInferenceRuntime(
            model_name="qwen2.5-coder:0.5b",
            use_hierarchical_ai=True,
            ai_first_config=config
        )
        
        target_type = TypeAnnotation(name=test_case["expected_type"])
        
        start_time = time.time()
        try:
            result = runtime.parse_intent(test_case["input"], target_type)
            execution_time_ms = (time.time() - start_time) * 1000
            
            # Get AI confidence from tracker
            stats = runtime.get_ai_decision_stats()
            confidence = stats.get("average_ai_confidence", 0.0)
            
            return result, execution_time_ms, True, confidence
        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            return str(e), execution_time_ms, False, 0.0
    
    def run_pattern_test(self, test_case: Dict[str, Any]) -> Tuple[Any, float, bool]:
        """Run test with traditional pattern-based approach."""
        config = AIFirstConfig(
            primary_model="embedded-fast-semantic-v1",
            ai_priority_mode=False,  # Disable AI-first
            track_ai_decisions=False
        )
        
        runtime = LocalInferenceRuntime(
            model_name="embedded-fast-semantic-v1",
            use_hierarchical_ai=False,  # Disable hierarchical AI
            ai_first_config=config
        )
        
        target_type = TypeAnnotation(name=test_case["expected_type"])
        
        start_time = time.time()
        try:
            result = runtime.parse_intent(test_case["input"], target_type)
            execution_time_ms = (time.time() - start_time) * 1000
            return result, execution_time_ms, True
        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            return str(e), execution_time_ms, False
    
    def compare_results(self, ai_result: Any, pattern_result: Any, expected_type: str) -> str:
        """Compare AI and pattern results."""
        # Both succeeded
        if isinstance(ai_result, str) and ai_result.startswith("["):
            ai_clean = ai_result
        else:
            ai_clean = str(ai_result.value) if hasattr(ai_result, 'value') else str(ai_result)
        
        if isinstance(pattern_result, str) and pattern_result.startswith("["):
            pattern_clean = pattern_result
        else:
            pattern_clean = str(pattern_result.value) if hasattr(pattern_result, 'value') else str(pattern_result)
        
        if ai_clean == pattern_clean:
            return "IDENTICAL"
        elif ai_clean in pattern_clean or pattern_clean in ai_clean:
            return "SIMILAR"
        else:
            return "DIFFERENT"
    
    def run_comprehensive_test(self) -> List[TestResult]:
        """Run comprehensive test suite comparing AI-first vs patterns."""
        print("=" * 80)
        print("AI-First vs Pattern-Based Performance Test Suite")
        print("=" * 80)
        
        results = []
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\n[{i}/{len(self.test_cases)}] Testing: {test_case['name']}")
            print(f"Input: \"{test_case['input']}\"")
            print(f"Expected Type: {test_case['expected_type']}")
            
            # Reset tracker for clean measurement
            reset_ai_decision_tracker()
            
            # Run AI-first test
            print("  Running AI-first mode...")
            ai_result, ai_time, ai_success, ai_confidence = self.run_ai_first_test(test_case)
            
            # Run pattern test
            print("  Running pattern-based mode...")
            pattern_result, pattern_time, pattern_success = self.run_pattern_test(test_case)
            
            # Compare results
            difference = self.compare_results(ai_result, pattern_result, test_case["expected_type"])
            
            # Store result
            result = TestResult(
                test_name=test_case["name"],
                input_text=test_case["input"],
                expected_type=test_case["expected_type"],
                ai_first_result=ai_result,
                pattern_result=pattern_result,
                ai_first_time_ms=ai_time,
                pattern_time_ms=pattern_time,
                ai_first_success=ai_success,
                pattern_success=pattern_success,
                ai_confidence=ai_confidence,
                difference=difference
            )
            results.append(result)
            
            # Print immediate results
            print(f"  AI-First: {ai_time:.1f}ms, Success: {ai_success}, Confidence: {ai_confidence:.2f}")
            print(f"  Pattern:  {pattern_time:.1f}ms, Success: {pattern_success}")
            print(f"  Comparison: {difference}")
            
            if difference != "IDENTICAL":
                print(f"  AI Result: {ai_result}")
                print(f"  Pattern Result: {pattern_result}")
        
        return results
    
    def generate_performance_report(self, results: List[TestResult]) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        total_tests = len(results)
        
        # Success rates
        ai_success_count = sum(1 for r in results if r.ai_first_success)
        pattern_success_count = sum(1 for r in results if r.pattern_success)
        ai_success_rate = ai_success_count / total_tests
        pattern_success_rate = pattern_success_count / total_tests
        
        # Timing statistics
        ai_times = [r.ai_first_time_ms for r in results]
        pattern_times = [r.pattern_time_ms for r in results]
        
        avg_ai_time = sum(ai_times) / len(ai_times)
        avg_pattern_time = sum(pattern_times) / len(pattern_times)
        
        # Result comparison
        identical_count = sum(1 for r in results if r.difference == "IDENTICAL")
        similar_count = sum(1 for r in results if r.difference == "SIMILAR")
        different_count = sum(1 for r in results if r.difference == "DIFFERENT")
        
        # Average AI confidence
        avg_confidence = sum(r.ai_confidence for r in results) / len(results)
        
        # Performance by category
        category_stats = {}
        for result in results:
            category = next((tc["category"] for tc in self.test_cases if tc["name"] == result.test_name), "general")
            if category not in category_stats:
                category_stats[category] = {
                    "count": 0,
                    "ai_success": 0,
                    "pattern_success": 0,
                    "avg_ai_time": 0,
                    "avg_pattern_time": 0,
                    "identical": 0
                }
            
            stats = category_stats[category]
            stats["count"] += 1
            if result.ai_first_success:
                stats["ai_success"] += 1
            if result.pattern_success:
                stats["pattern_success"] += 1
            stats["avg_ai_time"] += result.ai_first_time_ms
            stats["avg_pattern_time"] += result.pattern_time_ms
            if result.difference == "IDENTICAL":
                stats["identical"] += 1
        
        # Calculate category averages
        for category, stats in category_stats.items():
            if stats["count"] > 0:
                stats["ai_success_rate"] = stats["ai_success"] / stats["count"]
                stats["pattern_success_rate"] = stats["pattern_success"] / stats["count"]
                stats["avg_ai_time"] /= stats["count"]
                stats["avg_pattern_time"] /= stats["count"]
                stats["identical_rate"] = stats["identical"] / stats["count"]
        
        return {
            "summary": {
                "total_tests": total_tests,
                "ai_success_rate": round(ai_success_rate, 3),
                "pattern_success_rate": round(pattern_success_rate, 3),
                "avg_ai_time_ms": round(avg_ai_time, 2),
                "avg_pattern_time_ms": round(avg_pattern_time, 2),
                "avg_ai_confidence": round(avg_confidence, 3),
                "time_improvement": round(((avg_pattern_time - avg_ai_time) / avg_pattern_time) * 100, 1)
            },
            "result_comparison": {
                "identical": identical_count,
                "similar": similar_count,
                "different": different_count,
                "identical_rate": round(identical_count / total_tests, 3)
            },
            "category_breakdown": category_stats,
            "detailed_results": [
                {
                    "name": r.test_name,
                    "input": r.input_text,
                    "expected_type": r.expected_type,
                    "ai_time_ms": round(r.ai_first_time_ms, 2),
                    "pattern_time_ms": round(r.pattern_time_ms, 2),
                    "ai_success": r.ai_first_success,
                    "pattern_success": r.pattern_success,
                    "ai_confidence": round(r.ai_confidence, 3),
                    "difference": r.difference
                }
                for r in results
            ]
        }
    
    def print_report(self, report: Dict[str, Any]):
        """Print formatted performance report."""
        print("\n" + "=" * 80)
        print("AI-FIRST VS PATTERN-BASED PERFORMANCE REPORT")
        print("=" * 80)
        
        summary = report["summary"]
        comparison = report["result_comparison"]
        
        print("\n📊 SUMMARY STATISTICS")
        print("-" * 80)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"AI-First Success Rate: {summary['ai_success_rate']:.1%}")
        print(f"Pattern Success Rate: {summary['pattern_success_rate']:.1%}")
        print(f"Average AI Time: {summary['avg_ai_time_ms']:.2f}ms")
        print(f"Average Pattern Time: {summary['avg_pattern_time_ms']:.2f}ms")
        print(f"Average AI Confidence: {summary['avg_ai_confidence']:.2f}")
        
        if summary['time_improvement'] > 0:
            print(f"⚡ AI-First is {summary['time_improvement']:.1f}% faster")
        else:
            print(f"⚠️ Pattern-based is {abs(summary['time_improvement']):.1f}% faster")
        
        print("\n🔍 RESULT COMPARISON")
        print("-" * 80)
        print(f"Identical Results: {comparison['identical']} ({comparison['identical_rate']:.1%})")
        print(f"Similar Results: {comparison['similar']}")
        print(f"Different Results: {comparison['different']}")
        
        print("\n📈 CATEGORY BREAKDOWN")
        print("-" * 80)
        for category, stats in report["category_breakdown"].items():
            print(f"\n{category.upper()}:")
            print(f"  Tests: {stats['count']}")
            print(f"  AI Success Rate: {stats['ai_success_rate']:.1%}")
            print(f"  Pattern Success Rate: {stats['pattern_success_rate']:.1%}")
            print(f"  Avg AI Time: {stats['avg_ai_time']:.2f}ms")
            print(f"  Avg Pattern Time: {stats['avg_pattern_time']:.2f}ms")
            print(f"  Identical Results: {stats['identical']} ({stats['identical_rate']:.1%})")
        
        print("\n📋 DETAILED RESULTS")
        print("-" * 80)
        for result in report["detailed_results"]:
            status = "✅" if result['ai_success'] and result['pattern_success'] else "⚠️"
            time_diff = result['pattern_time_ms'] - result['ai_time_ms']
            time_indicator = "🚀" if time_diff > 0 else "🐢"
            
            print(f"{status} {result['name']}")
            print(f"   Input: \"{result['input']}\"")
            print(f"   Expected: {result['expected_type']}")
            print(f"   AI: {result['ai_time_ms']:.1f}ms (confidence: {result['ai_confidence']:.2f})")
            print(f"   Pattern: {result['pattern_time_ms']:.1f}ms")
            print(f"   {time_indicator} Time diff: {time_diff:+.1f}ms")
            print(f"   Comparison: {result['difference']}")
            print()


def main():
    """Run the comprehensive AI-first performance test."""
    tester = AIFirstPerformanceTest()
    
    # Run tests
    results = tester.run_comprehensive_test()
    
    # Generate report
    report = tester.generate_performance_report(results)
    
    # Print report
    tester.print_report(report)
    
    # Save report to file
    with open("ai_first_performance_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: ai_first_performance_report.json")
    print("=" * 80)


if __name__ == "__main__":
    main()