"""
Brute Force Testing Script for AI Request Controller
Tests the AI's ability to detect and block excessive requests without traditional rate limiting
"""
import asyncio
import aiohttp
import time
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


@dataclass
class TestResult:
    """Result of a single request test."""
    timestamp: float
    status_code: int
    response_time_ms: float
    blocked: bool
    reason: str = ""
    confidence: float = 0.0


class BruteForceTester:
    """
    Brute force tester that floods the AI controller with requests.
    No rate limiting - pure volume to test AI decision making.
    """
    
    def __init__(self, base_url: str = "http://localhost:8888"):
        self.base_url = base_url
        self.console = Console()
        self.results: List[TestResult] = []
        
    async def single_request(self, session: aiohttp.ClientSession, endpoint: str = "/protected") -> TestResult:
        """Make a single request to the server."""
        start_time = time.time()
        
        try:
            async with session.get(f"{self.base_url}{endpoint}") as response:
                response_time = (time.time() - start_time) * 1000
                data = await response.json()
                
                blocked = response.status == 429
                reason = data.get("reason", "")
                confidence = data.get("confidence", 0.0)
                
                return TestResult(
                    timestamp=time.time(),
                    status_code=response.status,
                    response_time_ms=response_time,
                    blocked=blocked,
                    reason=reason,
                    confidence=confidence
                )
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return TestResult(
                timestamp=time.time(),
                status_code=0,
                response_time_ms=response_time,
                blocked=False,
                reason=f"Error: {str(e)}",
                confidence=0.0
            )
    
    async def rapid_fire_test(self, num_requests: int = 100, concurrency: int = 10) -> List[TestResult]:
        """
        Rapid fire test: send many requests concurrently to simulate attack.
        This tests AI's ability to detect rapid-fire patterns.
        """
        self.console.print(f"[bold red]🔥 RAPID FIRE TEST: {num_requests} requests, concurrency: {concurrency}[/bold red]")
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(num_requests):
                task = self.single_request(session, "/protected")
                tasks.append(task)
                
                # Send in batches based on concurrency
                if len(tasks) >= concurrency:
                    batch_results = await asyncio.gather(*tasks)
                    self.results.extend(batch_results)
                    tasks = []
                    
                    # Small delay between batches to avoid overwhelming local machine
                    await asyncio.sleep(0.01)
            
            # Process remaining tasks
            if tasks:
                batch_results = await asyncio.gather(*tasks)
                self.results.extend(batch_results)
        
        return self.results[-num_requests:]
    
    async def sustained_load_test(self, duration_seconds: int = 30, requests_per_second: int = 20) -> List[TestResult]:
        """
        Sustained load test: maintain constant request rate over time.
        This tests AI's ability to detect sustained high-volume patterns.
        """
        self.console.print(f"[bold yellow]⏱️  SUSTAINED LOAD TEST: {duration_seconds}s at {requests_per_second} req/s[/bold yellow]")
        
        async with aiohttp.ClientSession() as session:
            end_time = time.time() + duration_seconds
            test_results = []
            
            while time.time() < end_time:
                # Send burst of requests
                tasks = [self.single_request(session, "/protected") for _ in range(requests_per_second)]
                batch_results = await asyncio.gather(*tasks)
                test_results.extend(batch_results)
                self.results.extend(batch_results)
                
                # Wait to maintain rate
                await asyncio.sleep(1.0)
        
        return test_results
    
    async def endpoint_targeting_test(self, num_requests: int = 200) -> List[TestResult]:
        """
        Target a single endpoint repeatedly.
        This tests AI's ability to detect endpoint-specific attacks.
        """
        self.console.print(f"[bold purple]🎯 ENDPOINT TARGETING TEST: {num_requests} requests to /simulate-load[/bold purple]")
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.single_request(session, "/simulate-load") for _ in range(num_requests)]
            results = await asyncio.gather(*tasks)
            self.results.extend(results)
        
        return results
    
    async def mixed_pattern_test(self, total_requests: int = 300) -> List[TestResult]:
        """
        Mix different attack patterns to test AI's pattern recognition.
        """
        self.console.print(f"[bold blue]🔀 MIXED PATTERN TEST: {total_requests} mixed requests[/bold blue]")
        
        async with aiohttp.ClientSession() as session:
            results = []
            
            for i in range(total_requests):
                # Randomly choose different patterns
                pattern = random.choice(["rapid", "sustained", "targeted"])
                
                if pattern == "rapid":
                    # Send 5 rapid requests
                    tasks = [self.single_request(session, "/protected") for _ in range(5)]
                    batch = await asyncio.gather(*tasks)
                    results.extend(batch)
                    await asyncio.sleep(0.1)
                    
                elif pattern == "sustained":
                    # Send 1 request per second for 3 seconds
                    for _ in range(3):
                        result = await self.single_request(session, "/protected")
                        results.append(result)
                        await asyncio.sleep(1.0)
                        
                else:  # targeted
                    # Target simulate-load endpoint
                    result = await self.single_request(session, "/simulate-load")
                    results.append(result)
                    await asyncio.sleep(0.05)
            
            self.results.extend(results)
        
        return results
    
    async def get_server_stats(self) -> Dict[str, Any]:
        """Get current server statistics."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/stats") as response:
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def reset_server_stats(self) -> bool:
        """Reset server statistics."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/reset-stats") as response:
                    return response.status == 200
        except Exception as e:
            self.console.print(f"[red]Failed to reset stats: {e}[/red]")
            return False
    
    def analyze_results(self, test_name: str, results: List[TestResult]) -> Dict[str, Any]:
        """Analyze test results and provide statistics."""
        if not results:
            return {"error": "No results to analyze"}
        
        total_requests = len(results)
        blocked_requests = sum(1 for r in results if r.blocked)
        allowed_requests = total_requests - blocked_requests
        
        avg_response_time = sum(r.response_time_ms for r in results) / total_requests
        avg_confidence = sum(r.confidence for r in results if r.confidence > 0) / len([r for r in results if r.confidence > 0]) if any(r.confidence > 0 for r in results) else 0.0
        
        # Analyze blocking patterns
        blocking_timeline = []
        for i, result in enumerate(results):
            if result.blocked:
                blocking_timeline.append(i)
        
        # Calculate when blocking started
        blocking_start = min(blocking_timeline) if blocking_timeline else -1
        blocking_rate = blocked_requests / total_requests if total_requests > 0 else 0.0
        
        return {
            "test_name": test_name,
            "total_requests": total_requests,
            "blocked_requests": blocked_requests,
            "allowed_requests": allowed_requests,
            "block_rate": blocking_rate,
            "avg_response_time_ms": avg_response_time,
            "avg_ai_confidence": avg_confidence,
            "blocking_started_at": blocking_start,
            "blocking_timeline": blocking_timeline[:20],  # First 20 blocking events
            "ai_effectiveness": "HIGH" if blocking_rate > 0.7 else "MEDIUM" if blocking_rate > 0.3 else "LOW"
        }
    
    def print_results_table(self, all_analyses: List[Dict[str, Any]]):
        """Print comprehensive results table."""
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
    
    async def run_comprehensive_test(self):
        """Run comprehensive brute force test suite."""
        self.console.print(Panel.fit("[bold cyan]🧠 AI Controller Brute Force Test Suite[/bold cyan]"))
        self.console.print("[dim]Testing AI's ability to detect and block malicious request patterns[/dim]\n")
        
        # Reset server stats before testing
        await self.reset_server_stats()
        self.console.print("[green]✓ Server statistics reset[/green]\n")
        
        all_analyses = []
        
        # Test 1: Rapid Fire Test
        try:
            rapid_results = await self.rapid_fire_test(num_requests=100, concurrency=20)
            rapid_analysis = self.analyze_results("Rapid Fire", rapid_results)
            all_analyses.append(rapid_analysis)
            
            self.console.print(f"[cyan]Rapid Fire: {rapid_analysis['blocked_requests']}/{rapid_analysis['total_requests']} blocked ({rapid_analysis['block_rate']:.1%})[/cyan]")
        except Exception as e:
            self.console.print(f"[red]Rapid Fire test failed: {e}[/red]")
        
        await asyncio.sleep(2)  # Cool down between tests
        
        # Test 2: Sustained Load Test
        try:
            sustained_results = await self.sustained_load_test(duration_seconds=15, requests_per_second=15)
            sustained_analysis = self.analyze_results("Sustained Load", sustained_results)
            all_analyses.append(sustained_analysis)
            
            self.console.print(f"[cyan]Sustained Load: {sustained_analysis['blocked_requests']}/{sustained_analysis['total_requests']} blocked ({sustained_analysis['block_rate']:.1%})[/cyan]")
        except Exception as e:
            self.console.print(f"[red]Sustained Load test failed: {e}[/red]")
        
        await asyncio.sleep(2)
        
        # Test 3: Endpoint Targeting Test
        try:
            targeting_results = await self.endpoint_targeting_test(num_requests=150)
            targeting_analysis = self.analyze_results("Endpoint Targeting", targeting_results)
            all_analyses.append(targeting_analysis)
            
            self.console.print(f"[cyan]Endpoint Targeting: {targeting_analysis['blocked_requests']}/{targeting_analysis['total_requests']} blocked ({targeting_analysis['block_rate']:.1%})[/cyan]")
        except Exception as e:
            self.console.print(f"[red]Endpoint Targeting test failed: {e}[/red]")
        
        await asyncio.sleep(2)
        
        # Test 4: Mixed Pattern Test
        try:
            mixed_results = await self.mixed_pattern_test(total_requests=200)
            mixed_analysis = self.analyze_results("Mixed Pattern", mixed_results)
            all_analyses.append(mixed_analysis)
            
            self.console.print(f"[cyan]Mixed Pattern: {mixed_analysis['blocked_requests']}/{mixed_analysis['total_requests']} blocked ({mixed_analysis['block_rate']:.1%})[/cyan]")
        except Exception as e:
            self.console.print(f"[red]Mixed Pattern test failed: {e}[/red]")
        
        # Get final server stats
        await asyncio.sleep(1)
        server_stats = await self.get_server_stats()
        
        # Print comprehensive results
        self.console.print("\n")
        self.print_results_table(all_analyses)
        
        # Print server statistics
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


async def main():
    """Main entry point."""
    console = Console()
    console.print("[bold cyan]🚀 Starting AI Controller Brute Force Test[/bold cyan]\n")
    
    tester = BruteForceTester(base_url="http://localhost:8888")
    
    try:
        # Check if server is running
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8888/health") as response:
                if response.status == 200:
                    console.print("[green]✓ AI Controller server is running[/green]\n")
                else:
                    console.print("[red]✗ AI Controller server not responding correctly[/red]")
                    return
    except Exception as e:
        console.print(f"[red]✗ Cannot connect to AI Controller server: {e}[/red]")
        console.print("[yellow]Make sure the server is running on http://localhost:8888[/yellow]")
        return
    
    # Run comprehensive test
    await tester.run_comprehensive_test()


if __name__ == "__main__":
    asyncio.run(main())