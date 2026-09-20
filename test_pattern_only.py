"""
Test Pattern Controller Only
Simple test to establish baseline performance
"""
import requests
import time
from rich.console import Console
from rich.table import Table


def test_pattern_controller():
    console = Console()
    console.print("[bold cyan]🔍 Testing Pattern Controller Only[/bold cyan]\n")
    
    # Check health
    try:
        resp = requests.get("http://localhost:8889/health", timeout=3)
        if resp.status_code == 200:
            console.print("[green]✓ Pattern Controller running[/green]")
        else:
            console.print("[red]✗ Pattern Controller not healthy[/red]")
            return
    except Exception as e:
        console.print(f"[red]✗ Pattern Controller error: {e}[/red]")
        return
    
    # Reset stats
    try:
        requests.post("http://localhost:8889/reset-stats", timeout=3)
        console.print("[green]✓ Stats reset[/green]\n")
    except:
        console.print("[yellow]Stats reset failed - continuing[/yellow]\n")
    
    # Test with 30 rapid requests
    console.print("[bold yellow]Sending 30 rapid requests...[/bold yellow]")
    blocked = 0
    times = []
    
    for i in range(30):
        try:
            start = time.time()
            resp = requests.get("http://localhost:8889/protected", timeout=2)
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
            
            if resp.status_code == 429:
                blocked += 1
                
            if (i + 1) % 10 == 0:
                console.print(f"  Progress: {i+1}/30, Blocked: {blocked}")
                
        except Exception as e:
            console.print(f"  Request {i+1} failed: {e}")
    
    # Get final stats
    try:
        stats = requests.get("http://localhost:8889/stats", timeout=3).json()
    except:
        stats = {}
    
    # Results
    block_rate = blocked / 30
    avg_time = sum(times) / len(times) if times else 0
    
    console.print(f"\n[bold green]Results:[/bold green]")
    console.print(f"  Blocked: {blocked}/30 ({block_rate:.1%})")
    console.print(f"  Avg response time: {avg_time:.1f}ms")
    console.print(f"  Server stats: {stats}")
    
    return {
        "blocked": blocked,
        "total": 30,
        "block_rate": block_rate,
        "avg_time": avg_time,
        "stats": stats
    }


if __name__ == "__main__":
    test_pattern_controller()