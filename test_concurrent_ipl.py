#!/usr/bin/env python3
"""
Concurrent request test to overload server
This will create real overload so ML can learn
"""
import urllib.request
import json
import threading
import time

server_url = "http://localhost:8888"
num_requests = 15
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
                    print(f"❌ Request {request_id}: BLOCKED (active: {data['active_requests']}/{data['capacity']})")
                else:
                    results["sent"] += 1
                    print(f"✅ Request {request_id}: OK (active: {data['active_requests']}/{data['capacity']})")
    except Exception as e:
        with lock:
            results["errors"] += 1
            print(f"⚠️  Request {request_id}: ERROR - {e}")

print(f"Sending {num_requests} concurrent requests to {server_url}")
print("This will overload the server so ML can learn from it")
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
print("")
print("Now run IPL's ML controller - it will have learned from this overload")
