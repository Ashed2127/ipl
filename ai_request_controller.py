"""
AI-Powered Request Control Server for IPL
Uses AI model decisions to control/block excessive requests without traditional rate limiting
"""
import time
import json
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime, timedelta
import hashlib
import threading

from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from rich.console import Console

try:
    from ai_security_system import AISecurityAnalyzer
    from ai_first_config import get_ai_first_config, get_ai_decision_tracker
except (ImportError, ValueError):
    from ai_security_system import AISecurityAnalyzer
    from ai_first_config import get_ai_first_config, get_ai_decision_tracker


@dataclass
class RequestProfile:
    """Profile of incoming requests for AI analysis."""
    ip_address: str
    user_agent: str
    endpoint: str
    method: str
    timestamp: float
    request_count: int = 1
    time_window: float = 60.0  # 60 second windows
    patterns: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass 
class AIDecision:
    """AI decision for request handling."""
    allow: bool
    confidence: float
    reasoning: str
    decision_time_ms: float
    threat_level: str = "none"
    suggested_action: str = "allow"


class AIRequestController:
    """
    AI-powered request controller that uses AI model decisions instead of rate limiting.
    
    The AI analyzes request patterns and makes intelligent decisions about whether to allow
    or block requests based on behavior analysis, not simple rate limits.
    """
    
    def __init__(self, model_name: str = "qwen2.5-coder:0.5b", 
                 ollama_endpoint: str = "http://localhost:11434"):
        self.model_name = model_name
        self.ollama_endpoint = ollama_endpoint
        self.ai_security = AISecurityAnalyzer(model_name, ollama_endpoint)
        self.request_history: Dict[str, List[RequestProfile]] = defaultdict(list)
        self.decision_history: List[Dict[str, Any]] = []
        self.blocked_ips: set = set()
        self.console = Console()
        
        # AI-first configuration
        self.ai_config = get_ai_first_config()
        self.decision_tracker = get_ai_decision_tracker()
        
        # Lock for thread safety
        self.lock = threading.Lock()
        
    def _get_client_fingerprint(self, ip_address: str, user_agent: str) -> str:
        """Generate a fingerprint for client identification."""
        fingerprint_data = f"{ip_address}:{user_agent}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
    
    def _analyze_request_pattern(self, fingerprint: str) -> Dict[str, Any]:
        """Analyze request patterns for AI decision making."""
        with self.lock:
            requests = self.request_history.get(fingerprint, [])
            
        if not requests:
            return {
                "total_requests": 0,
                "requests_per_minute": 0,
                "endpoints_accessed": [],
                "time_span": 0,
                "pattern_type": "new_client"
            }
        
        # Calculate statistics
        now = time.time()
        recent_requests = [r for r in requests if now - r.timestamp <= 60.0]
        
        endpoints = list(set([r.endpoint for r in recent_requests]))
        time_span = max([r.timestamp for r in requests]) - min([r.timestamp for r in requests]) if len(requests) > 1 else 0
        
        # Detect patterns
        pattern_type = "normal"
        if len(recent_requests) > 100:
            pattern_type = "high_volume"
        if len(endpoints) == 1 and len(recent_requests) > 50:
            pattern_type = "endpoint_targeted"
        if time_span < 10 and len(recent_requests) > 30:
            pattern_type = "rapid_fire"
            
        return {
            "total_requests": len(requests),
            "requests_per_minute": len(recent_requests),
            "endpoints_accessed": endpoints,
            "time_span": time_span,
            "pattern_type": pattern_type,
            "recent_request_count": len(recent_requests)
        }
    
    def _make_ai_decision(self, request_profile: RequestProfile, pattern_analysis: Dict[str, Any]) -> AIDecision:
        """Use AI model to decide whether to allow or block the request."""
        start_time = time.time()
        
        # Prepare context for AI analysis
        context = {
            "ip_address": request_profile.ip_address,
            "pattern_analysis": pattern_analysis,
            "timestamp": datetime.fromtimestamp(request_profile.timestamp).isoformat(),
            "request_count": request_profile.request_count
        }
        
        # Create analysis prompt for AI
        analysis_prompt = f"""
Request Analysis:
- IP Address: {request_profile.ip_address}
- Endpoint: {request_profile.endpoint}
- Method: {request_profile.method}
- Total Requests: {pattern_analysis['total_requests']}
- Requests/Minute: {pattern_analysis['requests_per_minute']}
- Pattern Type: {pattern_analysis['pattern_type']}
- Time Span: {pattern_analysis['time_span']:.2f}s
- Endpoints Accessed: {', '.join(pattern_analysis['endpoints_accessed'])}

Analyze this request pattern and determine if it represents:
1. Normal legitimate traffic
2. Aggressive scraping/crawling  
3. Brute force attack
4. DDoS attempt
5. Malicious bot activity

Make your decision based on behavioral analysis, not just request counts.
"""
        
        try:
            # Call AI security analyzer
            ai_result = self.ai_security.analyze_code_for_execution(analysis_prompt, context)
            
            decision_time = (time.time() - start_time) * 1000
            
            # Track AI decision
            if self.ai_config.track_ai_decisions:
                self.decision_tracker.record_decision(
                    task_type="request_control",
                    used_ai=True,
                    ai_success=ai_result.get("success", False),
                    confidence=ai_result.get("confidence", 0.0),
                    execution_time_ms=decision_time,
                    fallback_used=False
                )
            
            # Convert AI result to decision
            allow = ai_result.get("decision") == "EXECUTE"
            
            return AIDecision(
                allow=allow,
                confidence=ai_result.get("confidence", 0.0),
                reasoning=ai_result.get("reasoning", "AI analysis completed"),
                decision_time_ms=decision_time,
                threat_level=ai_result.get("severity", "none"),
                suggested_action="allow" if allow else "block"
            )
            
        except Exception as e:
            decision_time = (time.time() - start_time) * 1000
            
            # Fail-safe: allow if AI fails (avoid blocking legitimate traffic)
            self.console.print(f"[yellow]AI decision failed, allowing request: {e}[/yellow]")
            
            return AIDecision(
                allow=True,
                confidence=0.0,
                reasoning=f"AI analysis failed: {str(e)} - fail-safe allow",
                decision_time_ms=decision_time,
                threat_level="unknown",
                suggested_action="allow"
            )
    
    def record_request(self, ip_address: str, user_agent: str, endpoint: str, method: str) -> None:
        """Record incoming request for pattern analysis."""
        fingerprint = self._get_client_fingerprint(ip_address, user_agent)
        
        profile = RequestProfile(
            ip_address=ip_address,
            user_agent=user_agent,
            endpoint=endpoint,
            method=method,
            timestamp=time.time()
        )
        
        with self.lock:
            self.request_history[fingerprint].append(profile)
            
            # Clean old requests (keep last 1000 per client)
            if len(self.request_history[fingerprint]) > 1000:
                self.request_history[fingerprint] = self.request_history[fingerprint][-1000:]
    
    def should_allow_request(self, ip_address: str, user_agent: str, endpoint: str, method: str) -> tuple[bool, AIDecision]:
        """
        Main decision method: Use AI to determine if request should be allowed.
        Returns (allow_decision, ai_decision_object)
        """
        # Record the request
        self.record_request(ip_address, user_agent, endpoint, method)
        
        # Get fingerprint and analyze patterns
        fingerprint = self._get_client_fingerprint(ip_address, user_agent)
        pattern_analysis = self._analyze_request_pattern(fingerprint)
        
        # Make AI decision
        ai_decision = self._make_ai_decision(
            RequestProfile(ip_address, user_agent, endpoint, method, time.time()),
            pattern_analysis
        )
        
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
            "unique_clients": len(self.request_history)
        }


# Global controller instance
request_controller = AIRequestController()


async def health_check(request) -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "service": "ai-request-controller",
        "model": request_controller.model_name,
        "ai_first_mode": request_controller.ai_config.ai_priority_mode
    })


async def stats_endpoint(request) -> JSONResponse:
    """Get controller statistics."""
    return JSONResponse(request_controller.get_statistics())


async def protected_endpoint(request) -> JSONResponse:
    """Protected endpoint that uses AI for request control."""
    # Extract client information
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    endpoint = "/protected"
    method = request.method
    
    # Make AI decision
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


async def simulate_load_endpoint(request) -> JSONResponse:
    """Endpoint for testing load patterns."""
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    endpoint = "/simulate-load"
    method = request.method
    
    allow, ai_decision = request_controller.should_allow_request(client_ip, user_agent, endpoint, method)
    
    if not allow:
        return JSONResponse({
            "status": "blocked",
            "reason": ai_decision.reasoning,
            "confidence": ai_decision.confidence
        }, status_code=429)
    
    # Simulate some work
    await asyncio.sleep(0.01)
    
    return JSONResponse({
        "status": "success",
        "message": "Load simulation completed",
        "ai_decision": {
            "allowed": True,
            "confidence": ai_decision.confidence,
            "reasoning": ai_decision.reasoning
        }
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
        Route("/simulate-load", endpoint=simulate_load_endpoint, methods=["GET"]),
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


def run_ai_controller_server(host: str = "0.0.0.0", port: int = 8888, log_level: str = "info"):
    """Run the AI request controller server."""
    app = create_app()
    console = Console()
    
    console.print(f"[bold cyan]🧠 AI-Powered Request Controller Server[/bold cyan]")
    console.print(f"[dim]Model: {request_controller.model_name}[/dim]")
    console.print(f"[dim]AI-First Mode: {request_controller.ai_config.ai_priority_mode}[/dim]")
    console.print(f"[bold green]Starting on http://{host}:{port}[/bold green]")
    console.print("[dim]No rate limiting - AI decides based on behavior analysis[/dim]\n")
    
    uvicorn.run(app, host=host, port=port, log_level=log_level)


if __name__ == "__main__":
    run_ai_controller_server()