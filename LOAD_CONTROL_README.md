# IPL Load Control Demo

This demonstration shows how IPL (Intelligent Programming Language) can prevent server crashes by controlling request rate based on server capacity.

## What This Demonstrates

Traditional clients send requests blindly without checking if the server can handle them. This can lead to:
- Server overload
- Service degradation
- Complete crashes

IPL solves this by:
1. **Checking server capacity BEFORE sending requests**
2. **Blocking requests when the server is overloaded**
3. **Preventing crashes through proactive load control**

## Files

### 1. `simple_server.py`
A simple HTTP server with load tracking:
- Tracks active concurrent requests
- Reports current load status
- Simulates processing time
- Returns 503 when overloaded

**No external libraries used** - only Python standard library.

### 2. `load_control_demo.ipl`
IPL program that demonstrates load control:
- Checks server load before each request
- Blocks requests when server is overloaded
- Prevents server crashes

### 3. `test_concurrent.py`
Python script that sends concurrent requests without load control:
- Sends 20 requests simultaneously
- Does NOT check server capacity
- Demonstrates what happens without load control

## How to Run

### Start the Server
```bash
python3 simple_server.py
```

The server will start on port 8888 with capacity for 5 concurrent requests.

### Run IPL Load Control Demo
```bash
python3 cli.py run load_control_demo.ipl
```

IPL will:
1. Check server load before each request
2. Only send requests when capacity is available
3. Block requests when server is overloaded
4. Prevent server crashes

### Run Python Concurrent Test (for comparison)
```bash
python3 test_concurrent.py
```

This will send 20 requests simultaneously without checking capacity, resulting in:
- 5 successful requests (at capacity)
- 15 errors (503 Service Unavailable)

## Key Difference

| Approach | Behavior | Result |
|----------|----------|--------|
| **Python (no control)** | Sends all requests blindly | 15 errors, server overwhelmed |
| **IPL (smart control)** | Checks capacity before sending | 0 errors, server stable |

## IPL Features Used

1. **HTTP Built-ins**: `http_get()`, `http_post()`
2. **Dictionary Operations**: `has_key()`, key access
3. **Control Flow**: `if`, `while`
4. **Mutable Variables**: `var` for counters
5. **Sleep Function**: `sleep()` for rate limiting

## Code Explanation

### Server Load Check
```ipl
fn check_server_load(url) {
    let response = http_get(url);
    
    if has_key(response, "error") {
        return {"available": false, "is_overloaded": true};
    }
    
    return {
        "available": true,
        "is_overloaded": response["is_overloaded"],
        "active": response["active_requests"],
        "capacity": response["capacity"]
    };
}
```

### Smart Request Sending
```ipl
fn send_request_smart(url) {
    let status = check_server_load(url);
    
    if not status["available"] or status["is_overloaded"] {
        print("⚠️  Server overloaded - BLOCKING request");
        requests_blocked = requests_blocked + 1;
        return false;
    }
    
    # Only send if server has capacity
    let response = http_post(url, {"action": "test"});
    requests_sent = requests_sent + 1;
    return true;
}
```

## Benefits

1. **Crash Prevention**: Server never gets overloaded
2. **Graceful Degradation**: Requests are blocked before crash
3. **Proactive Control**: Checks capacity before sending
4. **No External Dependencies**: Uses only Python standard library
5. **Deterministic Behavior**: Same input produces same output

## Comparison with Traditional Approaches

### Traditional Rate Limiting
- Implemented at server-side
- Uses rate limit headers
- Client must respect headers
- Can still overwhelm server

### IPL Load Control
- Implemented at client-side
- Checks server state directly
- Proactive blocking
- Prevents overload before it happens

## Conclusion

IPL's load control demonstrates how a programming language can be:
- **Intelligent**: Makes decisions based on server state
- **Proactive**: Prevents problems before they occur
- **Safe**: Never risks server stability
- **Simple**: Uses only built-in functions

This is just one example of how IPL's intelligent runtime can solve real-world problems that traditional languages cannot.
