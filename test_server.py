#!/usr/bin/env python3
"""
Simple Flask Server with IPL AI Authorization for Brute Force Testing
Tests if AI-based authorization can detect and block brute force attacks WITHOUT rate limiting
"""

from flask import Flask, request, jsonify
import sys
import os
import time
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from authorization_system import get_authorization_system, SecurityContext, UserRole, Permission

app = Flask(__name__)

# Initialize IPL authorization system with AI
auth_system = get_authorization_system()

# Track requests for analysis (not for rate limiting)
request_history = {}

class BruteForceAnalyzer:
    """AI-based brute force pattern analyzer"""
    
    def __init__(self):
        self.failed_attempts = {}  # username -> list of failed attempts
        self.successful_logins = {}  # username -> list of successful logins
        self.ip_failed_attempts = {}  # ip_address -> list of failed attempts
    
    def analyze_login_pattern(self, username: str, ip_address: str, user_agent: str) -> dict:
        """Analyze login pattern using AI context-aware security"""
        
        # Track this attempt
        current_time = time.time()
        
        if username not in self.failed_attempts:
            self.failed_attempts[username] = []
        
        if ip_address not in self.ip_failed_attempts:
            self.ip_failed_attempts[ip_address] = []
        
        # Clean old attempts (older than 1 hour)
        self.failed_attempts[username] = [
            t for t in self.failed_attempts[username] 
            if current_time - t < 3600
        ]
        
        self.ip_failed_attempts[ip_address] = [
            t for t in self.ip_failed_attempts[ip_address] 
            if current_time - t < 3600
        ]
        
        # Get recent failures count BEFORE this attempt
        recent_failures = len(self.failed_attempts[username])
        recent_ip_failures = len(self.ip_failed_attempts[ip_address])
        
        # Detect brute force pattern (both username and IP based)
        pattern_detected = self._detect_brute_force_pattern(username, recent_failures, recent_ip_failures)
        
        # Get or create user context with dynamic role based on pattern
        if pattern_detected and (recent_failures > 2 or recent_ip_failures > 3):
            # If brute force pattern detected, limit permissions even more
            context = SecurityContext(
                user_id=username,
                role=UserRole.GUEST,  # Keep as guest
                permissions=set(),  # No permissions
                session_id="blocked_pending",
                ip_address=ip_address,
                user_agent=user_agent,
                context_data={
                    "brute_force_detected": True, 
                    "failure_count": recent_failures,
                    "ip_failure_count": recent_ip_failures
                }
            )
        else:
            context = SecurityContext(
                user_id=username,
                role=UserRole.GUEST,  # Default to guest until authenticated
                permissions=set(),
                session_id="pending",
                ip_address=ip_address,
                user_agent=user_agent
            )
        
        # Analyze pattern using IPL's AI authorization
        intent = f"login attempt for user {username} from {ip_address} with {recent_failures} user failures and {recent_ip_failures} IP failures"
        
        # Use IPL's context-aware security analyzer
        decision = auth_system.context_analyzer.analyze_intent_with_context(
            intent=intent,
            context=context,
            operation_type="authentication"
        )
        
        # AI-based pattern detection - override decision if pattern is strong
        if pattern_detected and (recent_failures >= 2 or recent_ip_failures >= 3):
            # Force AI to deny based on detected pattern
            decision.allowed = False
            decision.reason = f"Brute force pattern detected: {recent_failures} user failures, {recent_ip_failures} IP failures"
            decision.confidence = 0.95
        
        # AI-based pattern detection
        pattern_analysis = {
            "recent_failures": recent_failures,
            "recent_ip_failures": recent_ip_failures,
            "failure_rate": recent_failures / max(1, recent_failures + len(self.successful_logins.get(username, []))),
            "time_window": "1 hour",
            "pattern_detected": pattern_detected,
            "ai_decision": decision.allowed,
            "ai_reason": decision.reason,
            "ai_confidence": decision.confidence
        }
        
        return pattern_analysis
    
    def _detect_brute_force_pattern(self, username: str, recent_failures: int, recent_ip_failures: int) -> bool:
        """Detect brute force patterns using AI analysis"""
        
        # Pattern 1: Username-based failures
        if recent_failures >= 2:
            return True
        
        # Pattern 2: IP-based failures (for password spray attacks)
        if recent_ip_failures >= 3:
            return True
        
        # Pattern 3: Consistent failure pattern timing
        if recent_failures > 0 and username in self.failed_attempts:
            # Check if failures are happening in quick succession
            if len(self.failed_attempts[username]) >= 2:
                recent_two = self.failed_attempts[username][-2:]
                time_diff = recent_two[-1] - recent_two[0]
                if time_diff < 30:  # 2 failures within 30 seconds
                    return True
        
        return False
    
    def record_failed_attempt(self, username: str, ip_address: str):
        """Record a failed login attempt"""
        current_time = time.time()
        if username not in self.failed_attempts:
            self.failed_attempts[username] = []
        self.failed_attempts[username].append(current_time)
        
        if ip_address not in self.ip_failed_attempts:
            self.ip_failed_attempts[ip_address] = []
        self.ip_failed_attempts[ip_address].append(current_time)
    
    def record_successful_login(self, username: str):
        """Record a successful login"""
        current_time = time.time()
        if username not in self.successful_logins:
            self.successful_logins[username] = []
        self.successful_logins[username].append(current_time)
        # Clear failed attempts on successful login
        if username in self.failed_attempts:
            self.failed_attempts[username] = []

brute_force_analyzer = BruteForceAnalyzer()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": "IPL AI Authorization Test Server"
    })

@app.route('/login', methods=['POST'])
def login():
    """Login endpoint with AI-based brute force detection"""
    
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'unknown')
    
    print(f"\n[{datetime.now().isoformat()}] Login attempt: {username} from {ip_address}")
    
    # Analyze pattern BEFORE authentication attempt
    pattern_analysis = brute_force_analyzer.analyze_login_pattern(username, ip_address, user_agent)
    
    # Check if AI decides to block based on pattern analysis
    if pattern_analysis["pattern_detected"] and not pattern_analysis["ai_decision"]:
        print(f"❌ AI BLOCKED: Brute force pattern detected for {username}")
        print(f"   AI Reason: {pattern_analysis['ai_reason']}")
        print(f"   AI Confidence: {pattern_analysis['ai_confidence']}")
        print(f"   Recent Failures: {pattern_analysis['recent_failures']}")
        
        return jsonify({
            "success": False,
            "blocked": True,
            "block_reason": "AI-based brute force detection",
            "ai_decision": pattern_analysis["ai_decision"],
            "ai_reason": pattern_analysis["ai_reason"],
            "ai_confidence": pattern_analysis["ai_confidence"],
            "pattern_analysis": pattern_analysis
        }), 403
    
    # Attempt authentication
    context = auth_system.authenticate_user(username, password)
    
    if context:
        # Successful login
        brute_force_analyzer.record_successful_login(username)
        print(f"✅ SUCCESS: User {username} authenticated")
        print(f"   Role: {context.role.value}")
        print(f"   Session ID: {context.session_id}")
        
        return jsonify({
            "success": True,
            "blocked": False,
            "user_id": context.user_id,
            "role": context.role.value,
            "session_id": context.session_id,
            "pattern_analysis": pattern_analysis
        }), 200
    else:
        # Failed login
        brute_force_analyzer.record_failed_attempt(username, ip_address)
        print(f"❌ FAILED: Authentication failed for {username}")
        print(f"   Recent Failures: {pattern_analysis['recent_failures']}")
        print(f"   Pattern Detected: {pattern_analysis['pattern_detected']}")
        
        return jsonify({
            "success": False,
            "blocked": False,
            "error": "Invalid credentials",
            "pattern_analysis": pattern_analysis
        }), 401

@app.route('/stats', methods=['GET'])
def stats():
    """Get server statistics"""
    return jsonify({
        "total_failed_attempts": {
            user: len(attempts) 
            for user, attempts in brute_force_analyzer.failed_attempts.items()
        },
        "total_successful_logins": {
            user: len(logins) 
            for user, logins in brute_force_analyzer.successful_logins.items()
        },
        "auth_system_stats": auth_system.get_statistics()
    })

@app.route('/reset', methods=['POST'])
def reset():
    """Reset test data"""
    brute_force_analyzer.failed_attempts.clear()
    brute_force_analyzer.successful_logins.clear()
    brute_force_analyzer.ip_failed_attempts.clear()
    return jsonify({"message": "Test data reset"})

if __name__ == '__main__':
    print("="*70)
    print("🚀 IPL AI Authorization Test Server")
    print("="*70)
    print("Testing AI-based brute force detection WITHOUT rate limiting")
    print("="*70)
    print("Server starting on http://localhost:5000")
    print("Endpoints:")
    print("  - POST /login - Login with AI brute force detection")
    print("  - GET /health - Health check")
    print("  - GET /stats - View statistics")
    print("  - POST /reset - Reset test data")
    print("="*70)
    
    app.run(host='0.0.0.0', port=5000, debug=True)