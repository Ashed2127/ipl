#!/usr/bin/env python3
"""
Simple HTTP server with load tracking
Uses only Python standard library
"""
import http.server
import socketserver
import json
import time
from threading import Lock, Thread
import random

# Server state tracking
request_count = 0
max_capacity = 5  # Server can handle 5 concurrent requests
active_requests = 0
lock = Lock()

class LoadAwareHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global request_count, active_requests
        
        with lock:
            request_count += 1
            active_requests += 1
            current_load = active_requests
            total_requests = request_count
        
        # Simulate variable processing time (0.5 to 1.0 seconds)
        processing_time = random.uniform(0.5, 1.0)
        time.sleep(processing_time)
        
        with lock:
            active_requests -= 1
        
        # Check if server is overloaded
        is_overloaded = current_load > max_capacity
        
        response = {
            "request_id": total_requests,
            "active_requests": current_load,
            "is_overloaded": is_overloaded,
            "capacity": max_capacity,
            "status": "OK" if not is_overloaded else "OVERLOADED",
            "processing_time": processing_time
        }
        
        self.send_response(200 if not is_overloaded else 503)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        # Handle POST requests (for load testing)
        self.do_GET()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_server(port=8888):
    """Start the server"""
    with socketserver.ThreadingTCPServer(("", port), LoadAwareHandler) as httpd:
        httpd.allow_reuse_address = True
        print(f"Server running on port {port}")
        print(f"Max capacity: {max_capacity} concurrent requests")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
