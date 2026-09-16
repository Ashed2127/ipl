"""
Performance comparison between Hierarchical AI and Traditional processing.
"""
import time
import subprocess
import sys

def run_ipl_file(mode_flag):
    """Run IPL file with specified mode."""
    cmd = ["python3", "cli.py", "run", "test_ai_intelligence.ipl"] + mode_flag
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = (time.time() - start_time) * 1000
    return elapsed, result.returncode == 0

def main():
    print("=" * 60)
    print("PERFORMANCE COMPARISON: Hierarchical AI vs Traditional")
    print("=" * 60)
    
    # Test Hierarchical AI mode
    print("\n🚀 Testing Hierarchical AI Mode...")
    ai_time, ai_success = run_ipl_file([])
    print(f"✓ Hierarchical AI: {ai_time:.2f}ms (Success: {ai_success})")
    
    # Test Traditional mode
    print("\n🔧 Testing Traditional Mode...")
    traditional_time, traditional_success = run_ipl_file(["--traditional"])
    print(f"✓ Traditional: {traditional_time:.2f}ms (Success: {traditional_success})")
    
    # Comparison
    print("\n" + "=" * 60)
    print("COMPARISON RESULTS")
    print("=" * 60)
    print(f"Hierarchical AI:     {ai_time:.2f}ms")
    print(f"Traditional:         {traditional_time:.2f}ms")
    print(f"Difference:          {ai_time - traditional_time:.2f}ms")
    print(f"Performance Ratio:   {ai_time / traditional_time:.2f}x")
    
    if ai_time < traditional_time:
        print(f"🏆 Hierarchical AI is {((traditional_time - ai_time) / traditional_time) * 100:.1f}% faster")
    else:
        print(f"🏆 Traditional is {((ai_time - traditional_time) / ai_time) * 100:.1f}% faster")
    
    print("\nKey Insights:")
    print("• Hierarchical AI uses 3-tier model system for optimal speed/intelligence balance")
    print("• Traditional uses rule-based processing without AI model overhead")
    print("• AI engine provides intelligent caching for repeated operations")
    print("• Token optimization reduces API costs for production deployments")

if __name__ == "__main__":
    main()