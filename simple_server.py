#!/usr/bin/env python3
"""
Simple HTTP server with load tracking
Uses only Python standard library
"""
import http.server
import socketserver
import json
import time
from threading import Lock

# Server state tracking
request_count = 0
max_capacity = 10  # Server can handle 10 concurrent requests
active_requests = 0
lock = Lock()

class LoadAwareHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global request_count, active_requests
        
        with lock:
            request_count += 1
            active_requests += 1
            current_load = active_requests
            total_requests = request_count
        
        # Simulate processing time
        time.sleep(0.5)
        
        with lock:
            active_requests -= 1
        
        # Check if server is overloaded
        is_overloaded = current_load > max_capacity
        
        response = {
            "request_id": total_requests,
            "active_requests": current_load,
            "is_overloaded": is_overloaded,
            "capacity": max_capacity,
            "status": "OK" if not is_overloaded else "OVERLOADED"
        }
        
        self.send_response(200 if not is_overloaded else 503)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        # Handle POST requests (for load testing)
        self.do_GET()

def run_server(port=8888):
    """Start the server"""
    with socketserver.ThreadingTCPServer(("", port), LoadAwareHandler) as httpd:
        print(f"Server running on port {port}")
        print(f"Max capacity: {max_capacity} concurrent requests")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
