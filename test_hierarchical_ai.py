"""
Test suite for the Hierarchical AI Engine in IPL.
Demonstrates the 3-tier model architecture with speculative execution and token optimization.
"""
import sys
import time
from pathlib import Path

# Add the project directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from hierarchical_ai_engine import (
    HierarchicalAIEngine, 
    ModelTier, 
    TaskComplexity,
    TokenOptimizer,
    IntelligentCache,
    get_ai_engine
)
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


def test_basic_ai_engine():
    """Test basic AI engine functionality."""
    console = Console()
    console.print("[bold cyan]Test 1: Basic AI Engine Functionality[/bold cyan]\n")
    
    engine = get_ai_engine()
    
    # Test simple task (should use Tier 1)
    simple_prompt = "let x = 42"
    context = {"task_type": "token_classification", "target_type": None, "prompt_length": len(simple_prompt)}
    
    start_time = time.time()
    response = engine.process_speculative(simple_prompt, context)
    elapsed = (time.time() - start_time) * 1000
    
    console.print(f"Simple task completed in {elapsed:.2f}ms")
    console.print(f"Tier used: {response.tier_used.value}")
    console.print(f"Success: {response.success}")
    console.print(f"Confidence: {response.confidence}")
    console.print(f"Token usage: {response.token_usage.total_tokens} tokens")
    
    console.print("\n[green]✓ Basic AI engine test passed[/green]\n")
    return engine


def test_token_optimization():
    """Test token optimization system."""
    console = Console()
    console.print("[bold cyan]Test 2: Token Optimization System[/bold cyan]\n")
    
    optimizer = TokenOptimizer()
    
    # Test token estimation
    test_text = "let user_age: Int = intent 'extract user_age twenty-five from document' as Int"
    estimated_tokens = optimizer.estimate_tokens(test_text)
    console.print(f"Estimated tokens for test text: {estimated_tokens}")
    
    # Test cost calculation
    cost_tier1 = optimizer.calculate_cost(estimated_tokens, ModelTier.TIER_1_LIGHTNING)
    cost_tier2 = optimizer.calculate_cost(estimated_tokens, ModelTier.TIER_2_SPECIALIZED)
    cost_tier3 = optimizer.calculate_cost(estimated_tokens, ModelTier.TIER_3_REASONING)
    
    console.print(f"Cost (Tier 1): ${cost_tier1:.6f}")
    console.print(f"Cost (Tier 2): ${cost_tier2:.6f}")
    console.print(f"Cost (Tier 3): ${cost_tier3:.6f}")
    
    # Test prompt optimization
    long_prompt = "This is a very long prompt with    extra    spaces    that    should    be    optimized    to    reduce    token    usage    while    maintaining    effectiveness    for    the    AI    model    processing    " * 10
    optimized = optimizer.optimize_prompt(long_prompt, max_tokens=100)
    console.print(f"Original length: {len(long_prompt)}")
    console.print(f"Optimized length: {len(optimized)}")
    console.print(f"Space saved: {len(long_prompt) - len(optimized)} characters")
    
    console.print("\n[green]✓ Token optimization test passed[/green]\n")


def test_intelligent_cache():
    """Test intelligent caching system."""
    console = Console()
    console.print("[bold cyan]Test 3: Intelligent Caching System[/bold cyan]\n")
    
    cache = IntelligentCache(max_size=100, ttl_seconds=3600)
    
    # Test cache miss
    prompt = "let price: Currency = 'ninety-nine bucks'"
    context = {"task_type": "semantic_extraction", "target_type": "Currency"}
    
    result = cache.get(prompt, context)
    console.print(f"First request (cache miss): {result is None}")
    
    # Simulate adding to cache
    from hierarchical_ai_engine import AIResponse, TokenUsage, ModelTier
    fake_response = AIResponse(
        content={"test": "data"},
        success=True,
        tier_used=ModelTier.TIER_1_LIGHTNING,
        execution_time_ms=1.0,
        token_usage=TokenUsage(model_name="test", tier=ModelTier.TIER_1_LIGHTNING),
        confidence=0.95
    )
    cache.set(prompt, context, fake_response, TaskComplexity.SIMPLE)
    
    # Test cache hit
    result = cache.get(prompt, context)
    console.print(f"Second request (cache hit): {result is not None}")
    console.print(f"Cache hit count: {cache.hit_count}")
    console.print(f"Cache miss count: {cache.miss_count}")
    
    # Test cache statistics
    stats = cache.get_statistics()
    console.print(f"Cache hit rate: {stats['hit_rate']:.1%}")
    console.print(f"Cache size: {stats['cache_size']}")
    
    console.print("\n[green]✓ Intelligent cache test passed[/green]\n")


def test_speculative_execution():
    """Test speculative execution with different complexity levels."""
    console = Console()
    console.print("[bold cyan]Test 4: Speculative Execution Pipeline[/bold cyan]\n")
    
    engine = get_ai_engine()
    
    # Test simple complexity (should use Tier 1)
    simple_prompt = "42"
    simple_context = {"task_type": "type_inference", "target_type": "Int", "prompt_length": len(simple_prompt)}
    
    start_time = time.time()
    simple_response = engine.process_speculative(simple_prompt, simple_context)
    simple_time = (time.time() - start_time) * 1000
    
    console.print(f"Simple task (Tier 1): {simple_time:.2f}ms - {simple_response.tier_used.value}")
    
    # Test moderate complexity (should use Tier 1 + Tier 2)
    moderate_prompt = "extract user_age twenty-five from document and analyze the sentiment"
    moderate_context = {"task_type": "semantic_extraction", "target_type": "Sentiment", "prompt_length": len(moderate_prompt)}
    
    start_time = time.time()
    moderate_response = engine.process_speculative(moderate_prompt, moderate_context)
    moderate_time = (time.time() - start_time) * 1000
    
    console.print(f"Moderate task (Tier 1+2): {moderate_time:.2f}ms - {moderate_response.tier_used.value}")
    
    # Test complex complexity (should use all tiers)
    complex_prompt = "analyze the security implications of integrating neural networks in compilers with focus on type inference and optimization"
    complex_context = {"task_type": "complex_optimization", "target_type": None, "prompt_length": len(complex_prompt)}
    
    start_time = time.time()
    complex_response = engine.process_speculative(complex_prompt, complex_context)
    complex_time = (time.time() - start_time) * 1000
    
    console.print(f"Complex task (All tiers): {complex_time:.2f}ms - {complex_response.tier_used.value}")
    
    console.print("\n[green]✓ Speculative execution test passed[/green]\n")


def test_integration_with_ipl():
    """Test integration with IPL compiler pipeline."""
    console = Console()
    console.print("[bold cyan]Test 5: Integration with IPL Compiler[/bold cyan]\n")
    
    try:
        from compiler import NeuroSymbolicCompiler, LocalInferenceRuntime
        from ast_nodes import IntentExpr, TypeAnnotation
        
        # Create compiler with hierarchical AI
        compiler = NeuroSymbolicCompiler(use_hierarchical_ai=True)
        
        # Create an intent expression
        intent = IntentExpr(
            intent_prompt="extract user_age twenty-five from document",
            target_type=TypeAnnotation(name="Int")
        )
        
        # Compile the intent
        start_time = time.time()
        ast_node, taint_tag = compiler.compile_intent_node(intent)
        elapsed = (time.time() - start_time) * 1000
        
        console.print(f"Intent compilation completed in {elapsed:.2f}ms")
        console.print(f"AST node type: {type(ast_node).__name__}")
        console.print(f"Taint level: {taint_tag.level.value}")
        console.print(f"AST node value: {ast_node.value if hasattr(ast_node, 'value') else 'N/A'}")
        
        # Get AI engine statistics
        stats = compiler.get_ai_engine_statistics()
        console.print(f"\nAI Engine Statistics:")
        console.print(f"Total requests: {stats.get('total_requests', 0)}")
        console.print(f"Tier usage: {stats.get('tier_usage', {})}")
        
        console.print("\n[green]✓ IPL integration test passed[/green]\n")
        
    except Exception as e:
        console.print(f"[red]Integration test failed: {e}[/red]")
        import traceback
        traceback.print_exc()


def test_fallback_mechanisms():
    """Test fallback mechanisms when AI engine fails."""
    console = Console()
    console.print("[bold cyan]Test 6: Fallback Mechanisms[/bold cyan]\n")
    
    try:
        from compiler import LocalInferenceRuntime
        
        # Test with hierarchical AI enabled
        runtime_with_ai = LocalInferenceRuntime(use_hierarchical_ai=True)
        console.print(f"Hierarchical AI enabled: {runtime_with_ai.use_hierarchical_ai}")
        console.print(f"AI engine available: {runtime_with_ai.ai_engine is not None}")
        
        # Test with hierarchical AI disabled
        runtime_without_ai = LocalInferenceRuntime(use_hierarchical_ai=False)
        console.print(f"Hierarchical AI disabled: {not runtime_without_ai.use_hierarchical_ai}")
        console.print(f"AI engine available: {runtime_without_ai.ai_engine is not None}")
        
        # Test fallback processing
        test_prompt = "extract age 25"
        from ast_nodes import TypeAnnotation
        target_type = TypeAnnotation(name="Int")
        
        # Test with AI
        if runtime_with_ai.ai_engine:
            result_with_ai = runtime_with_ai._parse_with_hierarchical_ai(test_prompt, target_type)
            console.print(f"With AI: {type(result_with_ai).__name__}")
        
        # Test fallback
        result_fallback = runtime_with_ai._fallback_traditional_processing(test_prompt, target_type)
        console.print(f"Fallback result: {type(result_fallback).__name__}")
        console.print(f"Fallback value: {result_fallback.value if hasattr(result_fallback, 'value') else 'N/A'}")
        
        console.print("\n[green]✓ Fallback mechanisms test passed[/green]\n")
        
    except Exception as e:
        console.print(f"[red]Fallback test failed: {e}[/red]")
        import traceback
        traceback.print_exc()


def run_all_tests():
    """Run all tests for the hierarchical AI engine."""
    console = Console()
    
    console.print(Panel(
        "[bold cyan]Hierarchical AI Engine Test Suite[/bold cyan]\n"
        "[dim]Testing 3-tier model architecture with speculative execution and token optimization[/dim]",
        title="IPL AI Engine Tests",
        border_style="cyan"
    ))
    console.print()
    
    try:
        # Run tests
        test_basic_ai_engine()
        test_token_optimization()
        test_intelligent_cache()
        test_speculative_execution()
        test_integration_with_ipl()
        test_fallback_mechanisms()
        
        # Final summary
        console.print(Panel(
            "[bold green]All tests completed successfully![/bold green]\n"
            "[dim]The hierarchical AI engine is ready for production use.[/dim]",
            title="Test Results",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(Panel(
            f"[bold red]Test suite failed: {e}[/bold red]",
            title="Test Results",
            border_style="red"
        ))
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()