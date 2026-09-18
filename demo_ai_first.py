"""
AI-First IPL Demo
Demonstrates the new AI-first approach with fallback mechanisms
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compiler import LocalInferenceRuntime, NeuroSymbolicCompiler
from ast_nodes import TypeAnnotation, Program, LetStatement, Literal, PrintStatement
from ai_first_config import AIFirstConfig, get_ai_decision_tracker, reset_ai_decision_tracker
from ai_decision_analyzer import AIDecisionAnalyzer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


def print_header(title: str):
    """Print formatted header."""
    console = Console()
    console.print(Panel.fit(title, style="bold cyan"))


def print_success(message: str):
    """Print success message."""
    console = Console()
    console.print(f"✅ {message}", style="bold green")


def print_warning(message: str):
    """Print warning message."""
    console = Console()
    console.print(f"⚠️ {message}", style="bold yellow")


def print_info(message: str):
    """Print info message."""
    console = Console()
    console.print(f"ℹ️ {message}", style="bold blue")


def demo_ai_first_basic():
    """Demonstrate basic AI-first functionality."""
    print_header("🧠 AI-First Basic Demo")
    
    # Reset tracker for clean demo
    reset_ai_decision_tracker()
    
    # Create AI-first configuration
    config = AIFirstConfig(
        primary_model="qwen2.5-coder:0.5b",
        ai_priority_mode=True,
        ai_confidence_threshold=0.7,
        track_ai_decisions=True,
        log_ai_failures=True
    )
    
    print_info("Creating AI-First LocalInferenceRuntime...")
    runtime = LocalInferenceRuntime(
        model_name="qwen2.5-coder:0.5b",
        use_hierarchical_ai=True,
        ai_first_config=config
    )
    
    print_success("AI-First Runtime initialized successfully")
    print()
    
    # Test various intents
    test_cases = [
        ("The user age is 25", "Int"),
        ("The cost is $99.99", "Currency"),
        ("The product is amazing", "Sentiment"),
        ("The latency is 150ms", "Quantity"),
        ("Extract the number forty-two from the text", "Int")
    ]
    
    print_info("Processing test cases with AI-first approach...")
    print()
    
    for i, (text, expected_type) in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] Processing: \"{text}\"")
        print(f"Expected Type: {expected_type}")
        
        start_time = time.time()
        target_type = TypeAnnotation(name=expected_type)
        result = runtime.parse_intent(text, target_type)
        processing_time = (time.time() - start_time) * 1000
        
        print(f"Result: {result}")
        print(f"Processing Time: {processing_time:.1f}ms")
        print()
    
    # Show statistics
    stats = runtime.get_ai_decision_stats()
    print_info("AI Decision Statistics:")
    print(f"  Total Decisions: {stats['total_decisions']}")
    print(f"  AI Decisions: {stats['ai_decisions']} ({stats['ai_usage_rate']:.1%})")
    print(f"  Pattern Fallbacks: {stats['pattern_fallbacks']} ({stats['fallback_rate']:.1%})")
    print(f"  AI Success Rate: {stats['ai_success_rate']:.1%}")
    print(f"  Average AI Confidence: {stats['average_ai_confidence']:.2f}")
    print()


def demo_ai_vs_pattern_comparison():
    """Demonstrate AI-first vs pattern-based comparison."""
    print_header("🔄 AI-First vs Pattern-Based Comparison")
    
    test_text = "The user is thirty years old"
    expected_type = "Int"
    
    print_info(f"Test Input: \"{test_text}\"")
    print_info(f"Expected Type: {expected_type}")
    print()
    
    # Test with AI-first
    print("🧠 AI-First Mode:")
    reset_ai_decision_tracker()
    
    ai_config = AIFirstConfig(
        primary_model="qwen2.5-coder:0.5b",
        ai_priority_mode=True,
        track_ai_decisions=True,
        log_ai_failures=False
    )
    
    ai_runtime = LocalInferenceRuntime(
        model_name="qwen2.5-coder:0.5b",
        use_hierarchical_ai=True,
        ai_first_config=ai_config
    )
    
    start_time = time.time()
    target_type = TypeAnnotation(name=expected_type)
    ai_result = ai_runtime.parse_intent(test_text, target_type)
    ai_time = (time.time() - start_time) * 1000
    
    ai_stats = ai_runtime.get_ai_decision_stats()
    
    print(f"  Result: {ai_result}")
    print(f"  Time: {ai_time:.1f}ms")
    print(f"  AI Used: {ai_stats['ai_decisions'] > 0}")
    print(f"  Confidence: {ai_stats['average_ai_confidence']:.2f}")
    print()
    
    # Test with pattern-based
    print("📋 Pattern-Based Mode:")
    
    pattern_config = AIFirstConfig(
        primary_model="embedded-fast-semantic-v1",
        ai_priority_mode=False,
        track_ai_decisions=False
    )
    
    pattern_runtime = LocalInferenceRuntime(
        model_name="embedded-fast-semantic-v1",
        use_hierarchical_ai=False,
        ai_first_config=pattern_config
    )
    
    start_time = time.time()
    pattern_result = pattern_runtime.parse_intent(test_text, target_type)
    pattern_time = (time.time() - start_time) * 1000
    
    print(f"  Result: {pattern_result}")
    print(f"  Time: {pattern_time:.1f}ms")
    print()
    
    # Comparison
    print("📊 Comparison:")
    time_diff = pattern_time - ai_time
    if time_diff > 0:
        print_success(f"AI-First is {time_diff:.1f}ms faster")
    else:
        print_warning(f"Pattern-based is {abs(time_diff):.1f}ms faster")
    
    print()


def demo_fallback_mechanism():
    """Demonstrate fallback mechanism when AI fails."""
    print_header("🔄 AI Fallback Mechanism Demo")
    
    reset_ai_decision_tracker()
    
    # Create configuration with low confidence threshold to trigger fallbacks
    config = AIFirstConfig(
        primary_model="qwen2.5-coder:0.5b",
        ai_priority_mode=True,
        ai_confidence_threshold=0.95,  # Very high threshold to force fallbacks
        track_ai_decisions=True,
        log_ai_failures=True
    )
    
    print_info("Creating runtime with high confidence threshold (0.95) to trigger fallbacks...")
    runtime = LocalInferenceRuntime(
        model_name="qwen2.5-coder:0.5b",
        use_hierarchical_ai=True,
        ai_first_config=config
    )
    
    print()
    
    # Test cases that might trigger fallbacks
    test_cases = [
        "The user is twenty-five years old",
        "Extract the number from this complex sentence with multiple meanings",
        "What is the sentiment of this very long and convoluted text that might confuse the AI model?"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] Testing: \"{text[:50]}...\"")
        
        start_time = time.time()
        target_type = TypeAnnotation(name="Int")
        result = runtime.parse_intent(text, target_type)
        processing_time = (time.time() - start_time) * 1000
        
        print(f"  Result: {result}")
        print(f"  Time: {processing_time:.1f}ms")
        print()
    
    # Show fallback statistics
    stats = runtime.get_ai_decision_stats()
    print_info("Fallback Statistics:")
    print(f"  Total Decisions: {stats['total_decisions']}")
    print(f"  AI Decisions: {stats['ai_decisions']}")
    print(f"  Pattern Fallbacks: {stats['pattern_fallbacks']} ({stats['fallback_rate']:.1%})")
    print(f"  Fallback Rate: {stats['fallback_rate']:.1%}")
    print()


def demo_decision_quality_analysis():
    """Demonstrate AI decision quality analysis."""
    print_header("📊 AI Decision Quality Analysis Demo")
    
    reset_ai_decision_tracker()
    
    # Create runtime and process some test cases
    config = AIFirstConfig(
        primary_model="qwen2.5-coder:0.5b",
        ai_priority_mode=True,
        track_ai_decisions=True,
        log_ai_failures=False
    )
    
    runtime = LocalInferenceRuntime(
        model_name="qwen2.5-coder:0.5b",
        use_hierarchical_ai=True,
        ai_first_config=config
    )
    
    print_info("Processing diverse test cases for analysis...")
    
    test_cases = [
        ("The user is 25", "Int"),
        ("The cost is $50", "Currency"),
        ("Great product", "Sentiment"),
        ("150ms latency", "Quantity"),
        ("User age: thirty", "Int"),
        ("Price: 99.99 dollars", "Currency"),
        ("Terrible service", "Sentiment"),
        ("2.5 GB file", "Quantity")
    ]
    
    for text, expected_type in test_cases:
        target_type = TypeAnnotation(name=expected_type)
        runtime.parse_intent(text, target_type)
    
    print_success(f"Processed {len(test_cases)} test cases")
    print()
    
    # Analyze decision quality
    print_info("Analyzing AI decision quality...")
    analyzer = AIDecisionAnalyzer()
    analyzer.print_analysis_report()
    print()


def demo_full_ipl_program():
    """Demonstrate AI-first in a full IPL program compilation."""
    print_header("🚀 Full IPL Program with AI-First")
    
    reset_ai_decision_tracker()
    
    # Create AI-first compiler
    config = AIFirstConfig(
        primary_model="qwen2.5-coder:0.5b",
        ai_priority_mode=True,
        track_ai_decisions=True,
        log_ai_failures=True
    )
    
    print_info("Creating Neuro-Symbolic Compiler with AI-First...")
    compiler = NeuroSymbolicCompiler(
        use_hierarchical_ai=True,
        ai_first_config=config
    )
    
    print_success("Compiler initialized with AI-First mode")
    print()
    
    # Create a simple IPL program using intent expressions
    print_info("Compiling IPL program with intent expressions...")
    
    # This would normally come from parsing IPL code
    # For demo, we'll create AST nodes directly
    program = Program(statements=[
        LetStatement(
            name="user_age",
            value_expr=Literal(value=25, type_name="int"),
            type_annotation=TypeAnnotation(name="Int")
        ),
        LetStatement(
            name="user_sentiment",
            value_expr=Literal(value="The service is great", type_name="string"),
            type_annotation=TypeAnnotation(name="Sentiment")
        ),
        PrintStatement(exprs=[
            Identifier(name="user_age"),
            Identifier(name="user_sentiment")
        ])
    ])
    
    print_info("Program structure created")
    print()
    
    # Show compilation statistics
    stats = compiler.runtime.get_ai_decision_stats()
    print_info("Compilation Statistics:")
    print(f"  AI Decisions Made: {stats['ai_decisions']}")
    print(f"  Pattern Fallbacks: {stats['pattern_fallbacks']}")
    print(f"  AI Success Rate: {stats['ai_success_rate']:.1%}")
    print()


def demo_configuration_options():
    """Demonstrate various configuration options."""
    print_header("⚙️ AI-First Configuration Options")
    
    configurations = [
        ("Default AI-First", AIFirstConfig()),
        ("High Confidence Mode", AIFirstConfig(ai_confidence_threshold=0.9)),
        ("Aggressive AI Mode", AIFirstConfig(ai_confidence_threshold=0.5)),
        ("Pattern Fallback Disabled", AIFirstConfig(enable_pattern_fallback=False)),
        ("Custom Model", AIFirstConfig(primary_model="qwen2.5-coder:0.5b"))
    ]
    
    for name, config in configurations:
        print(f"📋 {name}:")
        print(f"  AI Priority Mode: {config.ai_priority_mode}")
        print(f"  Primary Model: {config.primary_model}")
        print(f"  Confidence Threshold: {config.ai_confidence_threshold}")
        print(f"  Pattern Fallback: {config.enable_pattern_fallback}")
        print(f"  AI Caching: {config.enable_ai_caching}")
        print()


def main():
    """Run all AI-first demonstrations."""
    console = Console()
    
    console.print("\n")
    console.print("🚀 AI-FIRST IPL DEMONSTRATION SUITE", style="bold green")
    console.print("=" * 80)
    console.print("\n")
    
    try:
        # Run demonstrations
        demo_ai_first_basic()
        time.sleep(1)
        
        demo_ai_vs_pattern_comparison()
        time.sleep(1)
        
        demo_fallback_mechanism()
        time.sleep(1)
        
        demo_decision_quality_analysis()
        time.sleep(1)
        
        demo_full_ipl_program()
        time.sleep(1)
        
        demo_configuration_options()
        
        console.print("=" * 80)
        console.print("🎉 AI-FIRST DEMONSTRATION COMPLETE", style="bold green")
        console.print("\n")
        
        console.print("Key Takeaways:", style="bold cyan")
        console.print("1. 🧠 AI-First mode prioritizes AI model decisions over hardcoded patterns")
        console.print("2. 🔄 Automatic fallback to patterns when AI fails or confidence is low")
        console.print("3. 📊 Comprehensive decision tracking and quality analysis")
        console.print("4. ⚙️ Flexible configuration options for different use cases")
        console.print("5. 🚀 Seamless integration with existing IPL compiler architecture")
        console.print("\n")
        
    except Exception as e:
        console.print(f"❌ Error during demonstration: {e}", style="bold red")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()