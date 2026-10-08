#!/usr/bin/env python3
"""
VULNERABLE SERVER - NO SECURITY PROTECTIONS
This server intentionally has security flaws for testing purposes.
DO NOT USE IN PRODUCTION.
"""
import http.server
import socketserver
import json
import time
import os
import subprocess
from urllib.parse import parse_qs, unquote

class VulnerableHandler(http.server.BaseHTTPRequestHandler):
    """Handler with intentional security vulnerabilities"""
    
    # Fake database
    users_db = {
        "admin": {"password": "admin123", "role": "admin"},
        "user1": {"password": "pass123", "role": "user"},
        "guest": {"password": "guest", "role": "guest"}
    }
    
    def do_GET(self):
        path = self.path
        
        # Vulnerability 1: Path Traversal
        if path.startswith("/file?"):
            query = parse_qs(path.split("?")[1])
            filename = query.get("filename", [""])[0]
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(content.encode())
            except:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")
            return
        
        # Vulnerability 2: XSS
        if path.startswith("/search?"):
            query = parse_qs(path.split("?")[1])
            search_term = query.get("q", [""])[0]
            html = f"""
            <html>
            <body>
                <h1>Search Results</h1>
                <p>You searched for: {search_term}</p>
                <p>No results found.</p>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
            return
        
        # Vulnerability 3: Information Disclosure
        if path == "/debug":
            debug_info = {
                "server_version": "1.0.0-vulnerable",
                "python_version": "3.12",
                "environment": dict(os.environ),
                "users": self.users_db
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(debug_info, indent=2).encode())
            return
        
        # Vulnerability 4: Server Status (no auth)
        if path == "/status":
            status = {
                "uptime": time.time(),
                "memory": "100MB",
                "connections": 5,
                "secret_key": "super-secret-key-12345"
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status).encode())
            return
        
        # Default response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"""
        <html>
        <body>
            <h1>Vulnerable Server</h1>
            <p>Endpoints:</p>
            <ul>
                <li>GET /file?filename=PATH - Path Traversal</li>
                <li>GET /search?q=QUERY - XSS</li>
                <li>GET /debug - Information Disclosure</li>
                <li>GET /status - Server Status</li>
                <li>POST /login - SQL Injection</li>
                <li>POST /exec - Command Injection</li>
            </ul>
        </body>
        </html>
        """)
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        params = parse_qs(post_data)
        
        # Vulnerability 5: SQL Injection
        if self.path == "/login":
            username = params.get("username", [""])[0]
            password = params.get("password", [""])[0]
            
            # VULNERABLE: Direct string concatenation (simulated SQL)
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            
            # Simulate SQL execution (truly vulnerable - no rule-based checks)
            # In real SQL: ' OR '1'='1 would bypass authentication
            # We simulate this by checking for SQL injection patterns
            sql_injection_patterns = ["' OR '1'='1", "' OR 1=1", "' OR 1=1--", "' OR 1=1#", "admin'--"]
            
            if any(pattern in username for pattern in sql_injection_patterns):
                # SQL injection successful (simulating real database behavior)
                response = {"status": "success", "user": "admin", "query": query, "injection": "SQL_INJECTION_SUCCESS"}
            elif username in self.users_db and self.users_db[username]["password"] == password:
                response = {"status": "success", "user": username, "query": query}
            else:
                response = {"status": "failed", "query": query}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Vulnerability 6: Command Injection
        if self.path == "/exec":
            command = params.get("cmd", [""])[0]
            
            # VULNERABLE: Direct command execution
            try:
                output = subprocess.check_output(command, shell=True, timeout=5).decode()
                response = {"status": "success", "output": output}
            except Exception as e:
                response = {"status": "error", "error": str(e)}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not found")
    
    def log_message(self, format, *args):
        pass

def run_server(port=9999):
    """Start the vulnerable server"""
    with socketserver.ThreadingTCPServer(("", port), VulnerableHandler) as httpd:
        httpd.allow_reuse_address = True
        print(f"⚠️  VULNERABLE SERVER running on port {port}")
        print(f"⚠️  NO SECURITY PROTECTIONS ENABLED")
        print(f"⚠️  FOR TESTING ONLY - DO NOT USE IN PRODUCTION")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
