#!/usr/bin/env python3
"""
AI-Driven Flask Server with IPL Hierarchical AI for Brute Force Detection
Uses IPL's hierarchical AI engine with Qwen2.5-Coder:0.5b for intelligent attack detection
Minimizes hardcoded rules - lets AI make the decisions
"""

from flask import Flask, request, jsonify
import sys
import os
import time
from datetime import datetime
from typing import Any

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from authorization_system import get_authorization_system, SecurityContext, UserRole, Permission
from hierarchical_ai_engine import get_ai_engine, TaskComplexity, ModelTier

app = Flask(__name__)

# Initialize IPL authorization system with full AI
auth_system = get_authorization_system()

# Initialize IPL's hierarchical AI engine with Qwen2.5-Coder:0.5b
try:
    ai_engine = get_ai_engine(tier3_model="qwen2.5-coder:0.5b")
    print("✅ IPL Hierarchical AI Engine initialized with Qwen2.5-Coder:0.5b")
except Exception as e:
    print(f"⚠️  Failed to initialize AI engine: {e}")
    print("Falling back to basic mode")
    ai_engine = None

# Track minimal data for AI context (not for hardcoded rules)
request_history = {}

class AIBruteForceAnalyzer:
    """AI-driven brute force analyzer using IPL's hierarchical AI engine"""
    
    def __init__(self, ai_engine):
        self.ai_engine = ai_engine
        self.minimal_tracking = {}  # Only track data for AI context, not rules
    
    def analyze_with_ai(self, username: str, ip_address: str, user_agent: str, 
                       attempt_number: int, time_since_last: float) -> dict:
        """
        Use IPL's hierarchical AI engine to analyze login attempt
        Let AI decide if this is a brute force attack
        """
        
        # Prepare context for AI analysis
        attempt_context = {
            "username": username,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "attempt_number": attempt_number,
            "time_since_last_attempt": time_since_last,
            "timestamp": datetime.now().isoformat(),
            "analysis_type": "brute_force_detection"
        }
        
        # Create security context for IPL
        context = SecurityContext(
            user_id=username,
            role=UserRole.GUEST,
            permissions=set(),
            session_id="pending",
            ip_address=ip_address,
            user_agent=user_agent,
            context_data=attempt_context
        )
        
        # Use IPL's hierarchical AI engine for decision
        if self.ai_engine:
            try:
                # Prepare AI prompt for security analysis
                ai_prompt = self._create_ai_security_prompt(attempt_context)
                
                print(f"🧠 Sending to IPL AI Engine: {ai_prompt[:100]}...")
                
                # Process through IPL's hierarchical AI engine
                ai_response = self.ai_engine.process_speculative(
                    ai_prompt,
                    {
                        "task_type": "security_analysis",  # This will trigger COMPLEX complexity
                        "attack_detection": True
                    }
                )
                
                print(f"🧠 AI Response: success={ai_response.success}, tier={ai_response.tier_used.value}")
                
                if ai_response.success:
                    # Parse AI decision
                    ai_decision = self._parse_ai_decision(ai_response.content, attempt_context)
                    
                    return {
                        "ai_driven": True,
                        "decision": ai_decision,
                        "confidence": ai_response.confidence,
                        "tier_used": ai_response.tier_used.value,
                        "execution_time_ms": ai_response.execution_time_ms,
                        "token_usage": ai_response.token_usage.to_dict(),
                        "raw_ai_response": ai_response.content
                    }
                else:
                    # Fallback to basic analysis if AI fails
                    print(f"⚠️  AI response failed: {ai_response.metadata}")
                    return self._fallback_analysis(attempt_context)
                    
            except Exception as e:
                print(f"⚠️  AI analysis failed: {e}")
                import traceback
                traceback.print_exc()
                return self._fallback_analysis(attempt_context)
        else:
            return self._fallback_analysis(attempt_context)
    
    def _create_ai_security_prompt(self, context: dict) -> str:
        """Create security analysis prompt for IPL's AI engine"""
        
        # Force Tier 3 by making it complex enough to need the full AI model
        prompt = f"""You are a security analyst. Analyze this login attempt for brute force attack patterns:

Username: {context['username']}
IP Address: {context['ip_address']}
Attempt Number: {context['attempt_number']}
Time Since Last Attempt: {context['time_since_last_attempt']:.2f}s
Timestamp: {context['timestamp']}

Consider these attack patterns:
1. Credential stuffing: Many passwords for same user
2. Password spray: Same password for many users  
3. Rapid fire: High frequency attempts
4. Timing patterns: Unusual time intervals

Respond in JSON format with:
{{
    "is_attack": true/false,
    "attack_type": "credential_stuffing/password_spray/rapid_fire/none",
    "confidence": 0.0-1.0,
    "reason": "brief explanation",
    "recommendation": "allow/block/monitor"
}}"""
        
        return prompt
    
    def _parse_ai_decision(self, ai_content: Any, context: dict) -> dict:
        """Parse AI response into security decision"""
        
        try:
            # Handle different AI response formats
            if isinstance(ai_content, dict):
                # Direct JSON response
                return {
                    "is_attack": ai_content.get("is_attack", False),
                    "attack_type": ai_content.get("attack_type", "none"),
                    "confidence": ai_content.get("confidence", 0.5),
                    "reason": ai_content.get("reason", "AI analysis"),
                    "recommendation": ai_content.get("recommendation", "monitor")
                }
            elif isinstance(ai_content, str):
                # Try to parse JSON from string
                import json
                try:
                    parsed = json.loads(ai_content)
                    return {
                        "is_attack": parsed.get("is_attack", False),
                        "attack_type": parsed.get("attack_type", "none"),
                        "confidence": parsed.get("confidence", 0.5),
                        "reason": parsed.get("reason", "AI analysis"),
                        "recommendation": parsed.get("recommendation", "monitor")
                    }
                except json.JSONDecodeError:
                    # Fallback: analyze text content
                    return self._analyze_text_response(ai_content, context)
            else:
                # Unknown format, use fallback
                return self._fallback_decision(context)
                
        except Exception as e:
            print(f"⚠️  Failed to parse AI decision: {e}")
            return self._fallback_decision(context)
    
    def _analyze_text_response(self, text: str, context: dict) -> dict:
        """Analyze text-based AI response"""
        text_lower = text.lower()
        
        is_attack = any(keyword in text_lower for keyword in 
                       ["attack", "malicious", "brute force", "suspicious", "block"])
        
        attack_type = "none"
        if "credential" in text_lower or "stuffing" in text_lower:
            attack_type = "credential_stuffing"
        elif "spray" in text_lower:
            attack_type = "password_spray"
        elif "rapid" in text_lower or "fire" in text_lower:
            attack_type = "rapid_fire"
        
        confidence = 0.7 if is_attack else 0.3
        
        return {
            "is_attack": is_attack,
            "attack_type": attack_type,
            "confidence": confidence,
            "reason": "AI text analysis",
            "recommendation": "block" if is_attack else "monitor"
        }
    
    def _fallback_analysis(self, context: dict) -> dict:
        """Fallback analysis when AI is not available"""
        # Minimal fallback - just basic context awareness
        return {
            "ai_driven": False,
            "decision": {
                "is_attack": False,  # Default to allow when AI unavailable
                "attack_type": "none",
                "confidence": 0.1,
                "reason": "AI unavailable - using fallback",
                "recommendation": "allow"
            },
            "confidence": 0.1,
            "tier_used": "fallback",
            "execution_time_ms": 0,
            "token_usage": {},
            "raw_ai_response": None
        }
    
    def _fallback_decision(self, context: dict) -> dict:
        """Fallback decision when parsing fails"""
        return {
            "is_attack": False,
            "attack_type": "none",
            "confidence": 0.2,
            "reason": "AI parsing failed - using safe default",
            "recommendation": "allow"
        }

ai_analyzer = AIBruteForceAnalyzer(ai_engine)

# Minimal tracking for AI context (not for rules)
attempt_tracking = {}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    ai_status = "available" if ai_engine else "unavailable"
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": "IPL AI-Driven Authorization Test Server",
        "ai_engine": ai_status,
        "ai_model": "qwen2.5-coder:0.5b" if ai_engine else "none"
    })

@app.route('/login', methods=['POST'])
def login():
    """Login endpoint with AI-driven brute force detection"""
    
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'unknown')
    
    # Track minimal data for AI context
    current_time = time.time()
    
    if username not in attempt_tracking:
        attempt_tracking[username] = {
            "attempts": [],
            "last_attempt": None
        }
    
    user_tracking = attempt_tracking[username]
    attempt_number = len(user_tracking["attempts"]) + 1
    time_since_last = current_time - user_tracking["last_attempt"] if user_tracking["last_attempt"] else 0
    
    print(f"\n[{datetime.now().isoformat()}] Login attempt #{attempt_number}: {username} from {ip_address}")
    
    # Let IPL's AI engine analyze the attempt
    ai_analysis = ai_analyzer.analyze_with_ai(
        username, ip_address, user_agent, attempt_number, time_since_last
    )
    
    print(f"🧠 AI Analysis: {ai_analysis['decision']['recommendation']} (confidence: {ai_analysis['confidence']:.2f})")
    print(f"   Attack Type: {ai_analysis['decision']['attack_type']}")
    print(f"   Reason: {ai_analysis['decision']['reason']}")
    if ai_analysis.get('ai_driven'):
        print(f"   AI Tier: {ai_analysis['tier_used']}")
        print(f"   Execution Time: {ai_analysis['execution_time_ms']:.2f}ms")
    
    # Respect AI decision
    ai_decision = ai_analysis['decision']
    
    if ai_decision['recommendation'] == "block" and ai_decision['confidence'] > 0.6:
        print(f"❌ AI BLOCKED: {ai_decision['reason']}")
        
        # Record the blocked attempt
        user_tracking["attempts"].append({
            "timestamp": current_time,
            "blocked": True,
            "ai_reason": ai_decision['reason']
        })
        user_tracking["last_attempt"] = current_time
        
        return jsonify({
            "success": False,
            "blocked": True,
            "block_reason": "AI-driven security decision",
            "ai_analysis": ai_analysis
        }), 403
    
    # Attempt authentication
    context = auth_system.authenticate_user(username, password)
    
    if context:
        # Successful login
        user_tracking["attempts"].append({
            "timestamp": current_time,
            "blocked": False,
            "successful": True
        })
        user_tracking["last_attempt"] = current_time
        
        print(f"✅ SUCCESS: User {username} authenticated")
        print(f"   Role: {context.role.value}")
        print(f"   Session ID: {context.session_id}")
        
        return jsonify({
            "success": True,
            "blocked": False,
            "user_id": context.user_id,
            "role": context.role.value,
            "session_id": context.session_id,
            "ai_analysis": ai_analysis
        }), 200
    else:
        # Failed login
        user_tracking["attempts"].append({
            "timestamp": current_time,
            "blocked": False,
            "successful": False
        })
        user_tracking["last_attempt"] = current_time
        
        print(f"❌ FAILED: Authentication failed for {username}")
        
        return jsonify({
            "success": False,
            "blocked": False,
            "error": "Invalid credentials",
            "ai_analysis": ai_analysis
        }), 401

@app.route('/stats', methods=['GET'])
def stats():
    """Get server statistics"""
    ai_stats = ai_engine.get_statistics() if ai_engine else {"message": "AI engine not available"}
    
    return jsonify({
        "attempt_tracking": {
            user: len(tracking["attempts"]) 
            for user, tracking in attempt_tracking.items()
        },
        "ai_engine_stats": ai_stats,
        "auth_system_stats": auth_system.get_statistics()
    })

@app.route('/reset', methods=['POST'])
def reset():
    """Reset test data"""
    attempt_tracking.clear()
    return jsonify({"message": "Test data reset"})

if __name__ == '__main__':
    print("="*70)
    print("🧠 IPL AI-DRIVEN AUTHORIZATION TEST SERVER")
    print("="*70)
    print("Using IPL's Hierarchical AI Engine with Qwen2.5-Coder:0.5b")
    print("Minimal hardcoded rules - AI makes the decisions")
    print("="*70)
    print("Server starting on http://localhost:5000")
    print("Endpoints:")
    print("  - POST /login - Login with AI-driven brute force detection")
    print("  - GET /health - Health check with AI status")
    print("  - GET /stats - View AI and authentication statistics")
    print("  - POST /reset - Reset test data")
    print("="*70)
    
    app.run(host='0.0.0.0', port=5000, debug=True)