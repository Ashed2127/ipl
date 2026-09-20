"""
Simulated AI Request Controller for Testing
Simulates AI decisions without requiring Ollama dependency
"""
import time
import json
from typing import Dict, Any, List
from dataclasses import dataclass
from collections import defaultdict
import threading
import random

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from rich.console import Console


@dataclass 
class SimulatedAIDecision:
    """Simulated AI decision for request handling."""
    allow: bool
    confidence: float
    reasoning: str
    decision_time_ms: float
    threat_level: str = "none"


class SimulatedAIRequestController:
    """
    Simulated AI request controller that mimics AI decision-making.
    Uses sophisticated heuristics to simulate AI pattern recognition.
    """
    
    def __init__(self):
        self.request_history: Dict[str, List[Dict]] = defaultdict(list)
        self.decision_history: List[Dict[str, Any]] = []
        self.blocked_ips: set = set()
        self.console = Console()
        self.lock = threading.Lock()
        
    def _get_client_fingerprint(self, ip_address: str, user_agent: str) -> str:
        """Generate a fingerprint for client identification."""
        import hashlib
        fingerprint_data = f"{ip_address}:{user_agent}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
    
    def _analyze_request_pattern(self, fingerprint: str) -> Dict[str, Any]:
        """Analyze request patterns for AI-like decision making."""
        with self.lock:
            requests = self.request_history.get(fingerprint, [])
        
        if not requests:
            return {
                "total_requests": 0,
                "requests_per_minute": 0,
                "pattern_type": "new_client",
                "velocity": 0.0,
                "consistency": 0.0
            }
        
        now = time.time()
        recent_requests = [r for r in requests if now - r["timestamp"] <= 60.0]
        
        # Calculate sophisticated metrics
        if len(recent_requests) > 1:
            timestamps = [r["timestamp"] for r in recent_requests]
            intervals = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
            avg_interval = sum(intervals) / len(intervals) if intervals else 0
            velocity = len(recent_requests) / 60.0 if avg_interval > 0 else 0
        else:
            velocity = 0.0
        
        # Calculate endpoint consistency
        endpoints = [r["endpoint"] for r in recent_requests]
        unique_endpoints = len(set(endpoints))
        consistency = 1.0 - (unique_endpoints / len(endpoints)) if endpoints else 0.0
        
        # AI-like pattern classification
        pattern_type = "normal"
        if velocity > 0.5 and consistency > 0.8:
            pattern_type = "targeted_attack"
        elif velocity > 0.3:
            pattern_type = "high_volume_bot"
        elif len(recent_requests) > 15:
            pattern_type = "suspicious_activity"
        elif consistency > 0.9 and len(recent_requests) > 8:
            pattern_type = "potential_scraper"
            
        return {
            "total_requests": len(requests),
            "requests_per_minute": len(recent_requests),
            "pattern_type": pattern_type,
            "velocity": velocity,
            "consistency": consistency,
            "recent_count": len(recent_requests)
        }
    
    def _make_simulated_ai_decision(self, pattern_analysis: Dict[str, Any]) -> SimulatedAIDecision:
        """Use simulated AI decision-making."""
        start_time = time.time()
        
        # Simulate AI processing time (variable)
        simulated_ai_time = random.uniform(0.5, 3.0)  # 0.5-3ms like real AI
        time.sleep(simulated_ai_time / 1000)  # Convert to seconds
        
        pattern_type = pattern_analysis["pattern_type"]
        velocity = pattern_analysis["velocity"]
        consistency = pattern_analysis["consistency"]
        recent_count = pattern_analysis["recent_count"]
        
        # AI-like decision logic with confidence scoring
        if pattern_type == "targeted_attack":
            confidence = random.uniform(0.85, 0.98)
            return SimulatedAIDecision(
                allow=False,
                confidence=confidence,
                reasoning=f"AI detected targeted attack pattern (velocity: {velocity:.2f}, consistency: {consistency:.2f})",
                decision_time_ms=(time.time() - start_time) * 1000,
                threat_level="critical"
            )
        elif pattern_type == "high_volume_bot":
            confidence = random.uniform(0.75, 0.92)
            return SimulatedAIDecision(
                allow=False,
                confidence=confidence,
                reasoning=f"AI identified high-volume bot activity (velocity: {velocity:.2f})",
                decision_time_ms=(time.time() - start_time) * 1000,
                threat_level="high"
            )
        elif pattern_type == "suspicious_activity":
            confidence = random.uniform(0.60, 0.85)
            # Some false positives for realism
            if random.random() < 0.3:  # 30% chance of allowing
                return SimulatedAIDecision(
                    allow=True,
                    confidence=confidence,
                    reasoning="AI analyzed as suspicious but within acceptable bounds",
                    decision_time_ms=(time.time() - start_time) * 1000,
                    threat_level="low"
                )
            else:
                return SimulatedAIDecision(
                    allow=False,
                    confidence=confidence,
                    reasoning="AI flagged suspicious activity pattern",
                    decision_time_ms=(time.time() - start_time) * 1000,
                    threat_level="medium"
                )
        elif pattern_type == "potential_scraper":
            confidence = random.uniform(0.50, 0.75)
            # Higher tolerance for potential scrapers
            if random.random() < 0.5:  # 50% chance of allowing
                return SimulatedAIDecision(
                    allow=True,
                    confidence=confidence,
                    reasoning="AI detected potential scraping but behavior is borderline",
                    decision_time_ms=(time.time() - start_time) * 1000,
                    threat_level="low"
                )
            else:
                return SimulatedAIDecision(
                    allow=False,
                    confidence=confidence,
                    reasoning="AI blocked potential scraper",
                    decision_time_ms=(time.time() - start_time) * 1000,
                    threat_level="medium"
                )
        else:  # normal
            confidence = random.uniform(0.80, 0.95)
            return SimulatedAIDecision(
                allow=True,
                confidence=confidence,
                reasoning="AI analyzed as normal legitimate traffic",
                decision_time_ms=(time.time() - start_time) * 1000,
                threat_level="none"
            )
    
    def record_request(self, ip_address: str, user_agent: str, endpoint: str, method: str) -> None:
        """Record incoming request for pattern analysis."""
        fingerprint = self._get_client_fingerprint(ip_address, user_agent)
        
        with self.lock:
            self.request_history[fingerprint].append({
                "ip_address": ip_address,
                "user_agent": user_agent,
                "endpoint": endpoint,
                "method": method,
                "timestamp": time.time()
            })
            
            # Clean old requests
            if len(self.request_history[fingerprint]) > 500:
                self.request_history[fingerprint] = self.request_history[fingerprint][-500:]
    
    def should_allow_request(self, ip_address: str, user_agent: str, endpoint: str, method: str) -> tuple[bool, SimulatedAIDecision]:
        """Main decision method: Use simulated AI to determine if request should be allowed."""
        # Record the request
        self.record_request(ip_address, user_agent, endpoint, method)
        
        # Get fingerprint and analyze patterns
        fingerprint = self._get_client_fingerprint(ip_address, user_agent)
        pattern_analysis = self._analyze_request_pattern(fingerprint)
        
        # Make simulated AI decision
        ai_decision = self._make_simulated_ai_decision(pattern_analysis)
        
        # Record decision history
        self.decision_history.append({
            "timestamp": time.time(),
            "fingerprint": fingerprint,
            "ip_address": ip_address,
            "decision": "allow" if ai_decision.allow else "block",
            "confidence": ai_decision.confidence,
            "reasoning": ai_decision.reasoning,
            "pattern_analysis": pattern_analysis,
            "decision_time_ms": ai_decision.decision_time_ms
        })
        
        # Update blocked IPs set
        if not ai_decision.allow:
            self.blocked_ips.add(ip_address)
        
        return ai_decision.allow, ai_decision
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get controller statistics."""
        total_decisions = len(self.decision_history)
        blocked_count = sum(1 for d in self.decision_history if d["decision"] == "block")
        allowed_count = total_decisions - blocked_count
        
        avg_confidence = 0.0
        if total_decisions > 0:
            avg_confidence = sum(d["confidence"] for d in self.decision_history) / total_decisions
        
        avg_decision_time = 0.0
        if total_decisions > 0:
            avg_decision_time = sum(d["decision_time_ms"] for d in self.decision_history) / total_decisions
        
        return {
            "total_requests_analyzed": total_decisions,
            "requests_allowed": allowed_count,
            "requests_blocked": blocked_count,
            "block_rate": blocked_count / total_decisions if total_decisions > 0 else 0.0,
            "blocked_ips_count": len(self.blocked_ips),
            "average_ai_confidence": avg_confidence,
            "average_decision_time_ms": avg_decision_time,
            "unique_clients": len(self.request_history),
            "controller_type": "simulated_ai"
        }


# Global controller instance
request_controller = SimulatedAIRequestController()


async def health_check(request) -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "service": "simulated-ai-request-controller",
        "mode": "simulated-ai"
    })


async def stats_endpoint(request) -> JSONResponse:
    """Get controller statistics."""
    return JSONResponse(request_controller.get_statistics())


async def protected_endpoint(request) -> JSONResponse:
    """Protected endpoint that uses simulated AI request control."""
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    endpoint = "/protected"
    method = request.method
    
    # Make simulated AI decision
    allow, ai_decision = request_controller.should_allow_request(client_ip, user_agent, endpoint, method)
    
    if not allow:
        return JSONResponse({
            "status": "blocked",
            "reason": ai_decision.reasoning,
            "confidence": ai_decision.confidence,
            "threat_level": ai_decision.threat_level,
            "decision_time_ms": ai_decision.decision_time_ms
        }, status_code=429)
    
    return JSONResponse({
        "status": "allowed",
        "message": "Request processed successfully",
        "ai_confidence": ai_decision.confidence,
        "decision_time_ms": ai_decision.decision_time_ms
    })


async def reset_stats_endpoint(request) -> JSONResponse:
    """Reset statistics for testing."""
    request_controller.decision_history.clear()
    request_controller.blocked_ips.clear()
    request_controller.request_history.clear()
    
    return JSONResponse({
        "status": "reset",
        "message": "Statistics cleared"
    })


def create_app() -> Starlette:
    """Create Starlette application."""
    routes = [
        Route("/health", endpoint=health_check, methods=["GET"]),
        Route("/stats", endpoint=stats_endpoint, methods=["GET"]),
        Route("/protected", endpoint=protected_endpoint, methods=["GET", "POST"]),
        Route("/reset-stats", endpoint=reset_stats_endpoint, methods=["POST"]),
    ]
    
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
    
    return Starlette(routes=routes, middleware=middleware)


def run_simulated_ai_server(host: str = "0.0.0.0", port: int = 8888, log_level: str = "info"):
    """Run the simulated AI request controller server."""
    app = create_app()
    console = Console()
    
    console.print(f"[bold cyan]🧠 Simulated AI Request Controller Server[/bold cyan]")
    console.print(f"[dim]Mode: Simulated AI decision-making (no Ollama dependency)[/dim]")
    console.print(f"[bold green]Starting on http://{host}:{port}[/bold green]")
    console.print("[dim]Using AI-like pattern recognition for request control[/dim]\n")
    
    uvicorn.run(app, host=host, port=port, log_level=log_level)


if __name__ == "__main__":
    run_simulated_ai_server()