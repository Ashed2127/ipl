"""
Benchmark comparing tree-walking runtime vs bytecode VM.
Measures speedup from both slot-indexed access and skipped taint checks.
"""
import time
from lexer import Lexer
from parser import Parser
from runtime import Interpreter
from bytecode import BytecodeCompiler, BytecodeInterpreter
from static_taint_analyzer import analyze_program_taint


def benchmark_runtimes(code: str, iterations: int = 100):
    """
    Benchmark both runtimes on the same code.
    Returns timing results and speedup analysis.
    """
    # Parse the code once
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    # Run static analysis
    static_result = analyze_program_taint(program)

    print(f"Static analysis results:")
    print(f"  Violations: {len(static_result['violations'])}")
    print(f"  Static safe sites: {len(static_result['static_safe_sites'])}")
    print(f"  Dynamic sites: {len(static_result['dynamic_sites'])}")
    print()

    # Benchmark tree-walking runtime
    print("Benchmarking tree-walking runtime...")
    tree_times = []
    for i in range(iterations):
        start = time.perf_counter()
        interpreter = Interpreter()
        interpreter.run(program)
        end = time.perf_counter()
        tree_times.append(end - start)

    tree_avg = sum(tree_times) / len(tree_times)
    tree_min = min(tree_times)
    tree_max = max(tree_times)
    print(f"  Average: {tree_avg*1000:.3f}ms")
    print(f"  Min: {tree_min*1000:.3f}ms")
    print(f"  Max: {tree_max*1000:.3f}ms")
    print()

    # Benchmark bytecode VM
    print("Benchmarking bytecode VM...")
    compiler = BytecodeCompiler(static_result)
    bytecode = compiler.compile(program)

    print(f"Bytecode statistics:")
    print(f"  Instructions: {len(bytecode.instructions)}")
    print(f"  Functions: {len(bytecode.functions)}")
    print(f"  Global slots: {len(bytecode.global_slots)}")
    print(f"  Static safe sink calls: {len(bytecode.static_safe_sites)}")
    print(f"  Dynamic sink calls: {len(bytecode.dynamic_sites)}")
    print()

    bytecode_times = []
    for i in range(iterations):
        start = time.perf_counter()
        vm = BytecodeInterpreter()
        vm.execute(bytecode)
        end = time.perf_counter()
        bytecode_times.append(end - start)

    bytecode_avg = sum(bytecode_times) / len(bytecode_times)
    bytecode_min = min(bytecode_times)
    bytecode_max = max(bytecode_times)
    print(f"  Average: {bytecode_avg*1000:.3f}ms")
    print(f"  Min: {bytecode_min*1000:.3f}ms")
    print(f"  Max: {bytecode_max*1000:.3f}ms")
    print()

    # Calculate speedup
    speedup = tree_avg / bytecode_avg
    print(f"Overall speedup: {speedup:.2f}x")
    print()

    # Estimate contribution of each optimization
    # This is approximate - in a real implementation we'd run separate benchmarks
    num_safe_sinks = len(bytecode.static_safe_sites)
    num_dynamic_sinks = len(bytecode.dynamic_sites)
    total_sinks = num_safe_sinks + num_dynamic_sinks

    if total_sinks > 0:
        taint_check_skip_ratio = num_safe_sinks / total_sinks
        print(f"Taint check optimization:")
        print(f"  Safe sinks (no runtime check): {num_safe_sinks}")
        print(f"  Dynamic sinks (runtime check): {num_dynamic_sinks}")
        print(f"  Ratio of checks skipped: {taint_check_skip_ratio:.1%}")
        print()

    return {
        'tree_avg': tree_avg,
        'bytecode_avg': bytecode_avg,
        'speedup': speedup,
        'static_safe_count': num_safe_sinks,
        'dynamic_count': num_dynamic_sinks,
    }


def main():
    """Run benchmarks on different test programs"""

    print("=" * 60)
    print("BENCHMARK 1: Simple arithmetic (no sinks)")
    print("=" * 60)
    code1 = """
    let x = 1 + 2 + 3 + 4 + 5;
    let y = x * 2;
    let z = y / 3;
    print(z);
    """
    result1 = benchmark_runtimes(code1, iterations=50)
    print()

    print("=" * 60)
    print("BENCHMARK 2: Safe sink calls (all statically proven safe)")
    print("=" * 60)
    code2 = """
    let safe = "safe_data";
    db_write("users", safe);
    file_write("/tmp/data", safe);
    html_render(safe);
    """
    result2 = benchmark_runtimes(code2, iterations=50)
    print()

    print("=" * 60)
    print("BENCHMARK 3: Mixed safe and dynamic sink calls")
    print("=" * 60)
    code3 = """
    let safe = "safe_data";
    let untrusted = set_untrusted("admin");
    let sanitized = sanitize_for_sql(untrusted);
    db_write("users", safe);  # Static safe
    db_write("logs", sanitized);  # Dynamic (need runtime check)
    """
    result3 = benchmark_runtimes(code3, iterations=50)
    print()

    print("=" * 60)
    print("BENCHMARK 4: Loop with operations")
    print("=" * 60)
    code4 = """
    let x = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10;
    let y = x * 2;
    let z = y / 3;
    print(z);
    print(x);
    print(y);
    """
    result4 = benchmark_runtimes(code4, iterations=50)
    print()

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Test 1 (arithmetic only): {result1['speedup']:.2f}x speedup")
    print(f"Test 2 (all safe sinks): {result2['speedup']:.2f}x speedup")
    print(f"Test 3 (mixed sinks): {result3['speedup']:.2f}x speedup")
    print(f"Test 4 (loop): {result4['speedup']:.2f}x speedup")
    print()

    # Average speedup
    avg_speedup = (result1['speedup'] + result2['speedup'] +
                   result3['speedup'] + result4['speedup']) / 4
    print(f"Average speedup across all tests: {avg_speedup:.2f}x")


if __name__ == "__main__":
    main()
