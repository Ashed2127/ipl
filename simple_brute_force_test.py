"""
Simple Brute Force Test for AI Request Controller
Uses synchronous requests for easier testing without async dependencies
"""
import requests
import time
import threading
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class SimpleBruteForceTester:
    """Simple synchronous brute force tester."""
    
    def __init__(self, base_url: str = "http://localhost:8888"):
        self.base_url = base_url
        self.console = Console()
        self.results: List[Dict[str, Any]] = []
        
    def single_request(self, endpoint: str = "/protected") -> Dict[str, Any]:
        """Make a single request."""
        start_time = time.time()
        
        try:
            response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            data = response.json()
            
            return {
                "timestamp": time.time(),
                "status_code": response.status_code,
                "response_time_ms": response_time,
                "blocked": response.status == 429,
                "reason": data.get("reason", ""),
                "confidence": data.get("confidence", 0.0)
            }
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return {
                "timestamp": time.time(),
                "status_code": 0,
                "response_time_ms": response_time,
                "blocked": False,
                "reason": f"Error: {str(e)}",
                "confidence": 0.0
            }
    
    def rapid_fire_test(self, num_requests: int = 50) -> List[Dict[str, Any]]:
        """Send rapid requests to test AI pattern detection."""
        self.console.print(f"[bold red]🔥 RAPID FIRE TEST: {num_requests} rapid requests[/bold red]")
        
        results = []
        for i in range(num_requests):
            result = self.single_request("/protected")
            results.append(result)
            self.results.append(result)
            
            # Print progress
            if (i + 1) % 10 == 0:
                blocked = sum(1 for r in results if r["blocked"])
                self.console.print(f"  Progress: {i+1}/{num_requests}, Blocked: {blocked}")
        
        return results
    
    def multi_threaded_test(self, num_requests: int = 100, num_threads: int = 10) -> List[Dict[str, Any]]:
        """Multi-threaded test to simulate concurrent requests."""
        self.console.print(f"[bold yellow]⚡ MULTI-THREADED TEST: {num_requests} requests, {num_threads} threads[/bold yellow]")
        
        results = []
        threads = []
        results_lock = threading.Lock()
        
        def worker(thread_id, requests_per_thread):
            thread_results = []
            for i in range(requests_per_thread):
                result = self.single_request("/protected")
                with results_lock:
                    results.append(result)
                    self.results.append(result)
                thread_results.append(result)
            
            blocked = sum(1 for r in thread_results if r["blocked"])
            self.console.print(f"  Thread {thread_id}: {requests_per_thread} requests, {blocked} blocked")
            return thread_results
        
        requests_per_thread = num_requests // num_threads
        
        for i in range(num_threads):
            thread = threading.Thread(target=worker, args=(i, requests_per_thread))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        return results
    
    def sustained_test(self, duration_seconds: int = 20, requests_per_second: int = 10) -> List[Dict[str, Any]]:
        """Sustained load test over time."""
        self.console.print(f"[bold blue]⏱️  SUSTAINED TEST: {duration_seconds}s at {requests_per_second} req/s[/bold blue]")
        
        results = []
        end_time = time.time() + duration_seconds
        
        while time.time() < end_time:
            batch_start = time.time()
            
            # Send a batch of requests
            for _ in range(requests_per_second):
                result = self.single_request("/protected")
                results.append(result)
                self.results.append(result)
            
            # Calculate time taken and wait to maintain rate
            batch_time = time.time() - batch_start
            sleep_time = max(0, 1.0 - batch_time)
            time.sleep(sleep_time)
            
            # Print progress
            elapsed = time.time() - (end_time - duration_seconds)
            blocked = sum(1 for r in results if r["blocked"])
            self.console.print(f"  Progress: {elapsed:.1f}s/{duration_seconds}s, Total: {len(results)}, Blocked: {blocked}")
        
        return results
    
    def get_server_stats(self) -> Dict[str, Any]:
        """Get server statistics."""
        try:
            response = requests.get(f"{self.base_url}/stats", timeout=5)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def reset_server_stats(self) -> bool:
        """Reset server statistics."""
        try:
            response = requests.post(f"{self.base_url}/reset-stats", timeout=5)
            return response.status_code == 200
        except Exception as e:
            self.console.print(f"[red]Failed to reset stats: {e}[/red]")
            return False
    
    def analyze_results(self, test_name: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze test results."""
        if not results:
            return {"error": "No results to analyze"}
        
        total_requests = len(results)
        blocked_requests = sum(1 for r in results if r["blocked"])
        allowed_requests = total_requests - blocked_requests
        
        avg_response_time = sum(r["response_time_ms"] for r in results) / total_requests
        confidences = [r["confidence"] for r in results if r["confidence"] > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        block_rate = blocked_requests / total_requests if total_requests > 0 else 0.0
        
        return {
            "test_name": test_name,
            "total_requests": total_requests,
            "blocked_requests": blocked_requests,
            "allowed_requests": allowed_requests,
            "block_rate": block_rate,
            "avg_response_time_ms": avg_response_time,
            "avg_ai_confidence": avg_confidence,
            "ai_effectiveness": "HIGH" if block_rate > 0.7 else "MEDIUM" if block_rate > 0.3 else "LOW"
        }
    
    def print_results_table(self, all_analyses: List[Dict[str, Any]]):
        """Print results table."""
        table = Table(title="🧠 AI Controller Brute Force Test Results", border_style="cyan")
        table.add_column("Test", style="bold cyan", width=20)
        table.add_column("Total Req", style="white", width=10)
        table.add_column("Blocked", style="red", width=10)
        table.add_column("Block Rate", style="yellow", width=12)
        table.add_column("Avg AI Conf", style="green", width=12)
        table.add_column("Effectiveness", style="bold", width=15)
        
        for analysis in all_analyses:
            effectiveness = analysis["ai_effectiveness"]
            effectiveness_style = "green" if effectiveness == "HIGH" else "yellow" if effectiveness == "MEDIUM" else "red"
            
            table.add_row(
                analysis["test_name"],
                str(analysis["total_requests"]),
                str(analysis["blocked_requests"]),
                f"{analysis['block_rate']:.1%}",
                f"{analysis['avg_ai_confidence']:.2f}",
                f"[{effectiveness_style}]{effectiveness}[/{effectiveness_style}]"
            )
        
        self.console.print(table)
    
    def run_comprehensive_test(self):
        """Run comprehensive test suite."""
        self.console.print(Panel.fit("[bold cyan]🧠 AI Controller Brute Force Test Suite[/bold cyan]"))
        self.console.print("[dim]Testing AI's ability to detect and block malicious request patterns[/dim]\n")
        
        # Reset server stats
        if self.reset_server_stats():
            self.console.print("[green]✓ Server statistics reset[/green]\n")
        
        all_analyses = []
        
        # Test 1: Rapid Fire
        try:
            rapid_results = self.rapid_fire_test(num_requests=50)
            rapid_analysis = self.analyze_results("Rapid Fire", rapid_results)
            all_analyses.append(rapid_analysis)
            self.console.print(f"[cyan]Result: {rapid_analysis['blocked_requests']}/{rapid_analysis['total_requests']} blocked ({rapid_analysis['block_rate']:.1%})[/cyan]\n")
        except Exception as e:
            self.console.print(f"[red]Rapid Fire test failed: {e}[/red]\n")
        
        time.sleep(2)
        
        # Test 2: Multi-threaded
        try:
            multi_results = self.multi_threaded_test(num_requests=100, num_threads=10)
            multi_analysis = self.analyze_results("Multi-threaded", multi_results)
            all_analyses.append(multi_analysis)
            self.console.print(f"[cyan]Result: {multi_analysis['blocked_requests']}/{multi_analysis['total_requests']} blocked ({multi_analysis['block_rate']:.1%})[/cyan]\n")
        except Exception as e:
            self.console.print(f"[red]Multi-threaded test failed: {e}[/red]\n")
        
        time.sleep(2)
        
        # Test 3: Sustained
        try:
            sustained_results = self.sustained_test(duration_seconds=15, requests_per_second=8)
            sustained_analysis = self.analyze_results("Sustained Load", sustained_results)
            all_analyses.append(sustained_analysis)
            self.console.print(f"[cyan]Result: {sustained_analysis['blocked_requests']}/{sustained_analysis['total_requests']} blocked ({sustained_analysis['block_rate']:.1%})[/cyan]\n")
        except Exception as e:
            self.console.print(f"[red]Sustained test failed: {e}[/red]\n")
        
        # Get final server stats
        time.sleep(1)
        server_stats = self.get_server_stats()
        
        # Print results
        self.console.print("\n")
        self.print_results_table(all_analyses)
        
        # Print server stats
        self.console.print("\n[bold cyan]📊 Server Statistics[/bold cyan]")
        stats_table = Table()
        stats_table.add_column("Metric", style="bold cyan")
        stats_table.add_column("Value", style="white")
        
        for key, value in server_stats.items():
            if key != "error":
                stats_table.add_row(key.replace("_", " ").title(), str(value))
        
        self.console.print(stats_table)
        
        # Overall assessment
        total_tested = sum(a["total_requests"] for a in all_analyses)
        total_blocked = sum(a["blocked_requests"] for a in all_analyses)
        overall_block_rate = total_blocked / total_tested if total_tested > 0 else 0.0
        
        self.console.print(f"\n[bold green]Overall Results: {total_blocked}/{total_tested} requests blocked ({overall_block_rate:.1%})[/bold green]")
        
        if overall_block_rate > 0.7:
            self.console.print("[bold green]✅ AI Controller showing HIGH effectiveness in blocking attack patterns[/bold green]")
        elif overall_block_rate > 0.3:
            self.console.print("[bold yellow]⚠️  AI Controller showing MEDIUM effectiveness - some patterns getting through[/bold yellow]")
        else:
            self.console.print("[bold red]❌ AI Controller showing LOW effectiveness - most requests not blocked[/bold red]")
        
        return all_analyses


def main():
    """Main entry point."""
    console = Console()
    console.print("[bold cyan]🚀 Starting Simple AI Controller Brute Force Test[/bold cyan]\n")
    
    tester = SimpleBruteForceTester(base_url="http://localhost:8888")
    
    # Check server
    try:
        response = requests.get("http://localhost:8888/health", timeout=5)
        if response.status_code == 200:
            console.print("[green]✓ AI Controller server is running[/green]\n")
        else:
            console.print("[red]✗ AI Controller server not responding correctly[/red]")
            return
    except Exception as e:
        console.print(f"[red]✗ Cannot connect to AI Controller server: {e}[/red]")
        console.print("[yellow]Make sure the server is running on http://localhost:8888[/yellow]")
        return
    
    # Run tests
    tester.run_comprehensive_test()


if __name__ == "__main__":
    main()