#!/usr/bin/env python3
"""
Concurrent request test to demonstrate server overload
This sends multiple requests simultaneously to overload the server
"""
import urllib.request
import json
import threading
import time

server_url = "http://localhost:8888"
num_requests = 20
results = {"sent": 0, "blocked": 0, "errors": 0}
lock = threading.Lock()

def send_request(request_id):
    """Send a single request"""
    try:
        req = urllib.request.Request(server_url, data=json.dumps({"action": "test"}).encode(), 
                                     headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            with lock:
                if response.status == 503:
                    results["blocked"] += 1
                    print(f"❌ Request {request_id}: BLOCKED (server overloaded)")
                else:
                    results["sent"] += 1
                    print(f"✅ Request {request_id}: OK (active: {data['active_requests']}/{data['capacity']})")
    except Exception as e:
        with lock:
            results["errors"] += 1
            print(f"⚠️  Request {request_id}: ERROR - {e}")

print(f"Sending {num_requests} concurrent requests to {server_url}")
print("Server capacity: 5 concurrent requests")
print("---")

# Create threads for concurrent requests
threads = []
for i in range(num_requests):
    t = threading.Thread(target=send_request, args=(i+1,))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

print("---")
print(f"Test complete:")
print(f"  Requests sent successfully: {results['sent']}")
print(f"  Requests blocked (overload): {results['blocked']}")
print(f"  Errors: {results['errors']}")
