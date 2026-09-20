"""
Quick Test for AI and Pattern Controllers
Simple direct testing with minimal requests
"""
import requests
import time
from rich.console import Console
from rich.table import Table


def test_controller(base_url: str, name: str, num_requests: int = 15):
    """Quick test of a controller."""
    console = Console()
    console.print(f"[bold cyan]Testing {name} with {num_requests} requests[/bold cyan]")
    
    # Reset
    try:
        requests.post(f"{base_url}/reset-stats", timeout=3)
    except:
        pass
    
    blocked = 0
    total_time = 0
    
    for i in range(num_requests):
        try:
            start = time.time()
            resp = requests.get(f"{base_url}/protected", timeout=2)
            elapsed = (time.time() - start) * 1000
            total_time += elapsed
            
            if resp.status_code == 429:
                blocked += 1
                
        except Exception as e:
            console.print(f"  Request {i+1} failed: {e}")
    
    # Get stats
    try:
        stats = requests.get(f"{base_url}/stats", timeout=3).json()
    except:
        stats = {}
    
    block_rate = blocked / num_requests if num_requests > 0 else 0
    avg_time = total_time / num_requests if num_requests > 0 else 0
    
    console.print(f"  Blocked: {blocked}/{num_requests} ({block_rate:.1%})")
    console.print(f"  Avg response time: {avg_time:.1f}ms")
    console.print(f"  Server block rate: {stats.get('block_rate', 0):.1%}")
    
    return {
        "name": name,
        "blocked": blocked,
        "total": num_requests,
        "block_rate": block_rate,
        "avg_time": avg_time,
        "stats": stats
    }


def main():
    console = Console()
    console.print("[bold cyan]🚀 Quick Controller Test[/bold cyan]\n")
    
    results = []
    
    # Test AI Controller
    try:
        resp = requests.get("http://localhost:8888/health", timeout=3)
        if resp.status_code == 200:
            console.print("[green]✓ AI Controller running[/green]")
            ai_result = test_controller("http://localhost:8888", "AI Controller", 15)
            results.append(ai_result)
        else:
            console.print("[red]✗ AI Controller not healthy[/red]")
    except Exception as e:
        console.print(f"[red]✗ AI Controller error: {e}[/red]")
    
    console.print()
    
    # Test Pattern Controller  
    try:
        resp = requests.get("http://localhost:8889/health", timeout=3)
        if resp.status_code == 200:
            console.print("[green]✓ Pattern Controller running[/green]")
            pattern_result = test_controller("http://localhost:8889", "Pattern Controller", 15)
            results.append(pattern_result)
        else:
            console.print("[red]✗ Pattern Controller not healthy[/red]")
    except Exception as e:
        console.print(f"[red]✗ Pattern Controller error: {e}[/red]")
    
    # Summary
    if results:
        console.print("\n[bold cyan]📊 Summary[/bold cyan]")
        table = Table()
        table.add_column("Controller", style="bold cyan")
        table.add_column("Blocked", style="red")
        table.add_column("Block Rate", style="yellow")
        table.add_column("Avg Time", style="green")
        
        for r in results:
            table.add_row(
                r["name"],
                f"{r['blocked']}/{r['total']}",
                f"{r['block_rate']:.1%}",
                f"{r['avg_time']:.1f}ms"
            )
        
        console.print(table)
        
        if len(results) == 2:
            ai_rate = results[0]["block_rate"]
            pattern_rate = results[1]["block_rate"]
            
            if ai_rate > pattern_rate:
                console.print(f"\n[green]AI Controller blocked more effectively ({ai_rate:.1%} vs {pattern_rate:.1%})[/green]")
            elif pattern_rate > ai_rate:
                console.print(f"\n[yellow]Pattern Controller blocked more aggressively ({pattern_rate:.1%} vs {ai_rate:.1%})[/yellow]")
            else:
                console.print(f"\n[cyan]Both controllers performed similarly ({ai_rate:.1%})[/cyan]")


if __name__ == "__main__":
    main()