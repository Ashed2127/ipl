"""
Simple Pattern-Based Request Controller for Testing
Uses pattern matching instead of AI to test the brute force framework
"""
import time
import json
import hashlib
from typing import Dict, Any, List
from dataclasses import dataclass
from collections import defaultdict
import threading

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from rich.console import Console


@dataclass 
class PatternDecision:
    """Pattern-based decision for request handling."""
    allow: bool
    confidence: float
    reasoning: str
    decision_time_ms: float
    threat_level: str = "none"


class PatternRequestController:
    """
    Pattern-based request controller using rule-based detection.
    This is a simplified version to test the brute force framework.
    """
    
    def __init__(self):
        self.request_history: Dict[str, List[Dict]] = defaultdict(list)
        self.decision_history: List[Dict[str, Any]] = []
        self.blocked_ips: set = set()
        self.console = Console()
        self.lock = threading.Lock()
        
    def _get_client_fingerprint(self, ip_address: str, user_agent: str) -> str:
        """Generate a fingerprint for client identification."""
        fingerprint_data = f"{ip_address}:{user_agent}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16] if 'hashlib' in globals() else f"{ip_address}:{user_agent}"[:16]
    
    def _analyze_request_pattern(self, fingerprint: str) -> Dict[str, Any]:
        """Analyze request patterns for decision making."""
        with self.lock:
            requests = self.request_history.get(fingerprint, [])
        
        if not requests:
            return {
                "total_requests": 0,
                "requests_per_minute": 0,
                "pattern_type": "new_client"
            }
        
        now = time.time()
        recent_requests = [r for r in requests if now - r["timestamp"] <= 60.0]
        
        # Simple pattern detection
        pattern_type = "normal"
        if len(recent_requests) > 30:
            pattern_type = "high_volume"
        if len(recent_requests) > 50:
            pattern_type = "attack_pattern"
            
        return {
            "total_requests": len(requests),
            "requests_per_minute": len(recent_requests),
            "pattern_type": pattern_type,
            "recent_count": len(recent_requests)
        }
    
    def _make_pattern_decision(self, pattern_analysis: Dict[str, Any]) -> PatternDecision:
        """Use pattern-based rules to decide whether to allow or block."""
        start_time = time.time()
        
        # Simple pattern-based rules
        requests_per_minute = pattern_analysis["requests_per_minute"]
        pattern_type = pattern_analysis["pattern_type"]
        
        # Rule-based decision making
        if pattern_type == "attack_pattern":
            return PatternDecision(
                allow=False,
                confidence=0.9,
                reasoning="Attack pattern detected: excessive request rate",
                decision_time_ms=(time.time() - start_time) * 1000,
                threat_level="high"
            )
        elif pattern_type == "high_volume":
            return PatternDecision(
                allow=False,
                confidence=0.7,
                reasoning="High volume traffic detected: potential scraping",
                decision_time_ms=(time.time() - start_time) * 1000,
                threat_level="medium"
            )
        elif requests_per_minute > 10:
            return PatternDecision(
                allow=True,
                confidence=0.6,
                reasoning="Moderate traffic: within acceptable limits",
                decision_time_ms=(time.time() - start_time) * 1000,
                threat_level="low"
            )
        else:
            return PatternDecision(
                allow=True,
                confidence=0.8,
                reasoning="Normal traffic pattern",
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
    
    def should_allow_request(self, ip_address: str, user_agent: str, endpoint: str, method: str) -> tuple[bool, PatternDecision]:
        """Main decision method: Use patterns to determine if request should be allowed."""
        # Record the request
        self.record_request(ip_address, user_agent, endpoint, method)
        
        # Get fingerprint and analyze patterns
        fingerprint = self._get_client_fingerprint(ip_address, user_agent)
        pattern_analysis = self._analyze_request_pattern(fingerprint)
        
        # Make pattern decision
        pattern_decision = self._make_pattern_decision(pattern_analysis)
        
        # Record decision history
        self.decision_history.append({
            "timestamp": time.time(),
            "fingerprint": fingerprint,
            "ip_address": ip_address,
            "decision": "allow" if pattern_decision.allow else "block",
            "confidence": pattern_decision.confidence,
            "reasoning": pattern_decision.reasoning,
            "pattern_analysis": pattern_analysis,
            "decision_time_ms": pattern_decision.decision_time_ms
        })
        
        # Update blocked IPs set
        if not pattern_decision.allow:
            self.blocked_ips.add(ip_address)
        
        return pattern_decision.allow, pattern_decision
    
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
            "average_confidence": avg_confidence,
            "average_decision_time_ms": avg_decision_time,
            "unique_clients": len(self.request_history)
        }


# Global controller instance
import hashlib
request_controller = PatternRequestController()


async def health_check(request) -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "service": "pattern-request-controller",
        "mode": "pattern-based"
    })


async def stats_endpoint(request) -> JSONResponse:
    """Get controller statistics."""
    return JSONResponse(request_controller.get_statistics())


async def protected_endpoint(request) -> JSONResponse:
    """Protected endpoint that uses pattern-based request control."""
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    endpoint = "/protected"
    method = request.method
    
    # Make pattern decision
    allow, pattern_decision = request_controller.should_allow_request(client_ip, user_agent, endpoint, method)
    
    if not allow:
        return JSONResponse({
            "status": "blocked",
            "reason": pattern_decision.reasoning,
            "confidence": pattern_decision.confidence,
            "threat_level": pattern_decision.threat_level,
            "decision_time_ms": pattern_decision.decision_time_ms
        }, status_code=429)
    
    return JSONResponse({
        "status": "allowed",
        "message": "Request processed successfully",
        "confidence": pattern_decision.confidence,
        "decision_time_ms": pattern_decision.decision_time_ms
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


def run_pattern_controller_server(host: str = "0.0.0.0", port: int = 8889, log_level: str = "info"):
    """Run the pattern request controller server."""
    app = create_app()
    console = Console()
    
    console.print(f"[bold cyan]🔍 Pattern-Based Request Controller Server[/bold cyan]")
    console.print(f"[dim]Mode: Pattern-based detection (no AI)[/dim]")
    console.print(f"[bold green]Starting on http://{host}:{port}[/bold green]")
    console.print("[dim]Using pattern matching for request control[/dim]\n")
    
    uvicorn.run(app, host=host, port=port, log_level=log_level)


if __name__ == "__main__":
    run_pattern_controller_server()