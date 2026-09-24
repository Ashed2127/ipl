"""
IPL Security Gateway & REST Microservice
Exposes REST endpoints for remote agent execution, formal verification,
and local neural model introspection using Starlette and Uvicorn.
"""

import time
import json
from typing import Optional, Dict, Any, List
from rich.console import Console

from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn

try:
    from .lexer import Lexer, LexerError
    from .parser import Parser, ParserError
    from .runtime import Interpreter
    from .compiler import MathematicalFirewall, LocalInferenceRuntime
    from .taint import TaintViolationError
except (ImportError, ValueError):
    from lexer import Lexer, LexerError
    from parser import Parser, ParserError
    from runtime import Interpreter
    from compiler import MathematicalFirewall, LocalInferenceRuntime
    from taint import TaintViolationError


async def health_check(request) -> JSONResponse:
    """System health and status check."""
    return JSONResponse({
        "status": "healthy",
        "service": "ipl-security-gateway",
        "version": "0.2.0",
        "architecture": "Neuro-Symbolic Deterministic Runtime"
    })


async def root_info(request) -> JSONResponse:
    """Service directory and API metadata."""
    return JSONResponse({
        "name": "IPL (Intelligent Programming Language / Aether) API Gateway",
        "version": "0.2.0",
        "endpoints": {
            "GET /health": "Health and service readiness",
            "GET /api/v1/models": "List available local neural models (Ollama / Embedded)",
            "POST /api/v1/verify": "Formal verification against Mathematical Firewall invariants",
            "POST /api/v1/execute": "Execute an IPL script with zero-trust taint tracking and verified audit trace"
        },
        "docs": "https://github.com/Ashed2127/ipl"
    })


async def list_models_endpoint(request) -> JSONResponse:
    """List available local neural models and built-in embedded runtime."""
    local_models = LocalInferenceRuntime.list_available_local_models()
    models = [
        {
            "name": "embedded-fast-semantic-v1",
            "type": "Embedded Deterministic NLP",
            "status": "active",
            "latency": "<1ms"
        }
    ]
    for m in local_models:
        models.append({
            "name": m,
            "type": "Local Neural LLM (Ollama)",
            "status": "available",
            "latency": "~200ms - 800ms"
        })

    return JSONResponse({
        "default_model": "embedded-fast-semantic-v1",
        "models": models,
        "count": len(models)
    })


async def verify_endpoint(request) -> JSONResponse:
    """
    Formal Mathematical Firewall Verification.
    Payload: {"source": "let x = 10\\n..."}
    """
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    source = data.get("source", "")
    if not source:
        return JSONResponse({"error": "Missing 'source' field in request body"}, status_code=400)

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        is_valid, violations = MathematicalFirewall.verify_tree(program)
        return JSONResponse({
            "valid": is_valid,
            "violations": violations,
            "statement_count": len(program.statements),
            "status": "verified" if is_valid else "rejected"
        })
    except LexerError as le:
        return JSONResponse({
            "valid": False,
            "error_type": "LexerError",
            "error": str(le),
            "violations": [f"Lexer syntax error: {le}"]
        }, status_code=422)
    except ParserError as pe:
        return JSONResponse({
            "valid": False,
            "error_type": "ParserError",
            "error": str(pe),
            "violations": [f"Parser grammar error: {pe}"]
        }, status_code=422)
    except Exception as e:
        return JSONResponse({
            "valid": False,
            "error_type": type(e).__name__,
            "error": str(e),
            "violations": [f"Verification exception: {e}"]
        }, status_code=500)


async def execute_endpoint(request) -> JSONResponse:
    """
    Execute an IPL program in a secure sandbox.
    Payload: {
        "source": "let x: Currency = '100 USD'\\nprint x",
        "model": "embedded-fast-semantic-v1",
        "audit": true
    }
    """
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    source = data.get("source", "")
    model_name = data.get("model", None)
    include_audit = data.get("audit", True)

    if not source:
        return JSONResponse({"error": "Missing 'source' field in request body"}, status_code=400)

    start_time = time.perf_counter()
    capture_console = Console(record=True, force_terminal=False, width=120)
    interpreter = Interpreter(console=capture_console, model_name=model_name)

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        # Run interpreter
        interpreter.run(program, source_code=source)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        output_text = capture_console.export_text()

        audit_steps = []
        if include_audit and hasattr(interpreter, "compiler") and interpreter.compiler.audit_trace:
            for s in interpreter.compiler.audit_trace.steps:
                audit_steps.append({
                    "step": s.step_number,
                    "phase": s.phase,
                    "status": s.status,
                    "details": s.details,
                    "timestamp": s.timestamp,
                    "signature": s.signature
                })

        return JSONResponse({
            "status": "success",
            "output": output_text,
            "execution_time_ms": round(elapsed_ms, 2),
            "model_used": model_name or "embedded-fast-semantic-v1",
            "audit_trace": audit_steps
        })

    except TaintViolationError as tve:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        output_text = capture_console.export_text()
        return JSONResponse({
            "status": "blocked",
            "error_type": "TaintViolationError",
            "error": str(tve),
            "output": output_text,
            "execution_time_ms": round(elapsed_ms, 2)
        }, status_code=403)

    except (LexerError, ParserError) as pe:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return JSONResponse({
            "status": "error",
            "error_type": type(pe).__name__,
            "error": str(pe),
            "execution_time_ms": round(elapsed_ms, 2)
        }, status_code=422)

    except PermissionError as pe:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        output_text = capture_console.export_text()
        return JSONResponse({
            "status": "blocked",
            "error_type": "PermissionError",
            "error": str(pe),
            "output": output_text,
            "execution_time_ms": round(elapsed_ms, 2)
        }, status_code=403)

    except Exception as e:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        output_text = capture_console.export_text()
        return JSONResponse({
            "status": "error",
            "error_type": type(e).__name__,
            "error": str(e),
            "output": output_text,
            "execution_time_ms": round(elapsed_ms, 2)
        }, status_code=500)


def create_app() -> Starlette:
    """Create and configure Starlette microservice application."""
    routes = [
        Route("/", endpoint=root_info, methods=["GET"]),
        Route("/health", endpoint=health_check, methods=["GET"]),
        Route("/api/v1/models", endpoint=list_models_endpoint, methods=["GET"]),
        Route("/api/v1/verify", endpoint=verify_endpoint, methods=["POST"]),
        Route("/api/v1/execute", endpoint=execute_endpoint, methods=["POST"]),
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


def run_gateway(host: str = "0.0.0.0", port: int = 8000, log_level: str = "info"):
    """Run IPL Gateway using Uvicorn server."""
    app = create_app()
    console = Console()
    console.print(f"[bold cyan]⚡ Starting IPL Security Gateway on http://{host}:{port}[/bold cyan]")
    console.print("[dim]Endpoints available: /health, /api/v1/models, /api/v1/verify, /api/v1/execute[/dim]\n")
    uvicorn.run(app, host=host, port=port, log_level=log_level)


if __name__ == "__main__":
    run_gateway()
