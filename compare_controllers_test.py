"""
Compare AI vs Pattern-Based Request Controllers
Tests both controllers with identical brute force scenarios
"""
import requests
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class ControllerComparison:
    """Compare AI vs Pattern-based controllers."""
    
    def __init__(self, ai_url: str = "http://localhost:8888", pattern_url: str = "http://localhost:8889"):
        self.ai_url = ai_url
        self.pattern_url = pattern_url
        self.console = Console()
        
    def test_controller(self, base_url: str, controller_name: str, num_requests: int = 30) -> dict:
        """Test a single controller with rapid requests."""
        self.console.print(f"[bold cyan]Testing {controller_name} with {num_requests} rapid requests[/bold cyan]")
        
        # Reset stats
        try:
            requests.post(f"{base_url}/reset-stats", timeout=5)
        except:
            pass
        
        results = []
        blocked_count = 0
        
        for i in range(num_requests):
            try:
                start_time = time.time()
                response = requests.get(f"{base_url}/protected", timeout=3)
                response_time = (time.time() - start_time) * 1000
                
                blocked = response.status_code == 429
                if blocked:
                    blocked_count += 1
                
                results.append({
                    "status_code": response.status_code,
                    "blocked": blocked,
                    "response_time_ms": response_time
                })
                
            except Exception as e:
                results.append({
                    "status_code": 0,
                    "blocked": False,
                    "error": str(e)
                })
        
        # Get stats
        try:
            stats = requests.get(f"{base_url}/stats", timeout=5).json()
        except:
            stats = {}
        
        block_rate = blocked_count / num_requests if num_requests > 0 else 0.0
        
        self.console.print(f"  Results: {blocked_count}/{num_requests} blocked ({block_rate:.1%})")
        
        return {
            "controller": controller_name,
            "total_requests": num_requests,
            "blocked_count": blocked_count,
            "block_rate": block_rate,
            "server_stats": stats
        }
    
    def run_comparison(self):
        """Run comparison test."""
        self.console.print(Panel.fit("[bold cyan]🔬 AI vs Pattern Controller Comparison[/bold cyan]"))
        self.console.print("[dim]Testing both controllers with identical brute force scenarios[/dim]\n")
        
        results = []
        
        # Test AI Controller
        try:
            ai_health = requests.get(f"{self.ai_url}/health", timeout=5)
            if ai_health.status_code == 200:
                self.console.print("[green]✓ AI Controller is running[/green]")
                ai_result = self.test_controller(self.ai_url, "AI Controller", num_requests=30)
                results.append(ai_result)
            else:
                self.console.print("[red]✗ AI Controller not responding[/red]")
        except Exception as e:
            self.console.print(f"[red]✗ AI Controller error: {e}[/red]")
        
        self.console.print()
        
        # Test Pattern Controller
        try:
            pattern_health = requests.get(f"{self.pattern_url}/health", timeout=5)
            if pattern_health.status_code == 200:
                self.console.print("[green]✓ Pattern Controller is running[/green]")
                pattern_result = self.test_controller(self.pattern_url, "Pattern Controller", num_requests=30)
                results.append(pattern_result)
            else:
                self.console.print("[red]✗ Pattern Controller not responding[/red]")
        except Exception as e:
            self.console.print(f"[red]✗ Pattern Controller error: {e}[/red]")
        
        # Print comparison table
        if results:
            self.console.print("\n")
            table = Table(title="📊 Controller Comparison Results", border_style="cyan")
            table.add_column("Controller", style="bold cyan", width=20)
            table.add_column("Total Req", style="white", width=10)
            table.add_column("Blocked", style="red", width=10)
            table.add_column("Block Rate", style="yellow", width=12)
            table.add_column("Avg Decision Time", style="green", width=18)
            
            for result in results:
                stats = result.get("server_stats", {})
                avg_time = stats.get("average_decision_time_ms", 0.0)
                
                table.add_row(
                    result["controller"],
                    str(result["total_requests"]),
                    str(result["blocked_count"]),
                    f"{result['block_rate']:.1%}",
                    f"{avg_time:.2f}ms"
                )
            
            self.console.print(table)
            
            # Analysis
            if len(results) == 2:
                ai_block_rate = results[0]["block_rate"]
                pattern_block_rate = results[1]["block_rate"]
                
                self.console.print("\n[bold cyan]🔍 Analysis[/bold cyan]")
                
                if ai_block_rate > pattern_block_rate:
                    improvement = ((ai_block_rate - pattern_block_rate) / pattern_block_rate * 100) if pattern_block_rate > 0 else 0
                    self.console.print(f"[green]AI Controller blocked {improvement:.1f}% more requests than Pattern Controller[/green]")
                    self.console.print("[green]AI shows better attack detection capability[/green]")
                elif pattern_block_rate > ai_block_rate:
                    improvement = ((pattern_block_rate - ai_block_rate) / ai_block_rate * 100) if ai_block_rate > 0 else 0
                    self.console.print(f"[yellow]Pattern Controller blocked {improvement:.1f}% more requests than AI Controller[/yellow]")
                    self.console.print("[yellow]Pattern-based rules are more aggressive in this scenario[/yellow]")
                else:
                    self.console.print("[cyan]Both controllers show similar blocking rates[/cyan]")
        
        return results


def main():
    """Main entry point."""
    console = Console()
    console.print("[bold cyan]🚀 Starting Controller Comparison Test[/bold cyan]\n")
    
    comparison = ControllerComparison()
    comparison.run_comparison()


if __name__ == "__main__":
    main()