"""
Unit tests for IPL Security Gateway & REST API.
Tests ASGI endpoints using asyncio and Starlette application interface.
"""

import unittest
import asyncio
import json
from gateway import create_app


class TestIPLGateway(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

    def _call(self, path: str, method: str = "GET", body=None):
        req_body = json.dumps(body).encode("utf-8") if body is not None else b""
        messages = []

        scope = {
            "type": "http",
            "http_version": "1.1",
            "method": method,
            "path": path,
            "raw_path": path.encode("ascii"),
            "query_string": b"",
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(req_body)).encode("ascii")),
            ],
            "client": ("127.0.0.1", 12345),
            "server": ("127.0.0.1", 8000),
        }

        async def receive():
            return {"type": "http.request", "body": req_body, "more_body": False}

        async def send(message):
            messages.append(message)

        async def run_asgi():
            await self.app(scope, receive, send)
            res_body = b"".join(
                m.get("body", b"") for m in messages if m["type"] == "http.response.body"
            )
            status = next(m["status"] for m in messages if m["type"] == "http.response.start")
            return status, json.loads(res_body.decode("utf-8"))

        return asyncio.run(run_asgi())

    def test_health_check(self):
        status, res = self._call("/health")
        self.assertEqual(status, 200)
        self.assertEqual(res["status"], "healthy")
        self.assertEqual(res["service"], "ipl-security-gateway")

    def test_root_info(self):
        status, res = self._call("/")
        self.assertEqual(status, 200)
        self.assertIn("endpoints", res)

    def test_models_list(self):
        status, res = self._call("/api/v1/models")
        self.assertEqual(status, 200)
        self.assertIn("models", res)
        self.assertGreaterEqual(res["count"], 1)
        # Verify embedded model is present
        model_names = [m["name"] for m in res["models"]]
        self.assertIn("embedded-fast-semantic-v1", model_names)

    def test_verify_endpoint_success(self):
        code = "let x: Int = 42\nprint x"
        status, res = self._call("/api/v1/verify", "POST", {"source": code})
        self.assertEqual(status, 200)
        self.assertTrue(res["valid"])
        self.assertEqual(len(res["violations"]), 0)

    def test_verify_endpoint_syntax_error(self):
        bad_code = "let x: = broken !!!"
        status, res = self._call("/api/v1/verify", "POST", {"source": bad_code})
        self.assertEqual(status, 422)
        self.assertFalse(res["valid"])

    def test_execute_endpoint_valid_run(self):
        code = 'let val: Currency = intent "convert 500 dollars" as Currency\nprint val'
        status, res = self._call("/api/v1/execute", "POST", {"source": code, "audit": True})
        self.assertEqual(status, 200)
        self.assertEqual(res["status"], "success")
        self.assertIn("500.00 USD", res["output"])
        self.assertIn("audit_trace", res)
        self.assertIsInstance(res["audit_trace"], list)
        self.assertGreater(len(res["audit_trace"]), 0)

    def test_execute_endpoint_taint_violation(self):
        # Passing an untrusted intent directly into a zero-trust sink (db_write)
        code = """
        let raw_data: String = intent "fetch untrusted user data" as String
        db_write("users", raw_data)
        """
        status, res = self._call("/api/v1/execute", "POST", {"source": code})
        self.assertEqual(status, 403)
        self.assertEqual(res["status"], "blocked")
        self.assertEqual(res["error_type"], "TaintViolationError")
        self.assertIn("Zero-Trust Taint Violation", res["error"])

    def test_execute_endpoint_sanitized_intent_success(self):
        # Sanitizing untrusted intent before writing to db_write succeeds
        code = """
        let raw_data: String = intent "fetch user name Alice" as String
        let safe_data = sanitize(raw_data)
        db_write("users", safe_data)
        """
        status, res = self._call("/api/v1/execute", "POST", {"source": code})
        self.assertEqual(status, 200)
        self.assertEqual(res["status"], "success")
        self.assertIn("Zero-Trust DB Sink Verified", res["output"])


if __name__ == "__main__":
    unittest.main()
