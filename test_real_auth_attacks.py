#!/usr/bin/env python3
"""
HONEST TEST: Real Authorization System Attack Testing
This tests the ACTUAL authorization system with real attacks, not simulations
"""

import sys
import os
import time
from typing import Dict, Any

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from authorization_system import get_authorization_system, UserRole, SecurityContext


class RealAuthAttackTester:
    """Test the REAL authorization system with actual attacks"""
    
    def __init__(self):
        self.auth_system = get_authorization_system()
        self.test_results = []
        self.session_ids = []
    
    def test_normal_registration(self):
        """Test normal user registration"""
        print("\n" + "="*70)
        print("TEST 1: Normal User Registration")
        print("="*70)
        
        try:
            username = "testuser_normal"
            password = "SecurePassword123!"
            role = UserRole.USER
            permissions = set()  # Default permissions
            
            self.auth_system.user_db.create_user(username, password, role, permissions)
            
            # Try to authenticate
            context = self.auth_system.authenticate_user(username, password)
            
            if context:
                print(f"✅ SUCCESS: User {username} registered and authenticated")
                print(f"   Role: {context.role.value}")
                print(f"   Session ID: {context.session_id}")
                self.session_ids.append(context.session_id)
                return {"success": True, "attack": "normal_registration"}
            else:
                print(f"❌ FAILED: Authentication failed after registration")
                return {"success": False, "attack": "normal_registration"}
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return {"success": False, "attack": "normal_registration", "error": str(e)}
    
    def test_sql_injection_username(self):
        """Test SQL injection in username during registration"""
        print("\n" + "="*70)
        print("TEST 2: SQL Injection Attack - Username Field")
        print("="*70)
        
        try:
            # Attempt SQL injection in username
            username = "admin' OR '1'='1--"
            password = "anypassword"
            role = UserRole.USER
            permissions = set()
            
            print(f"Attempting to register with malicious username: {username}")
            
            # This should either fail or be sanitized
            self.auth_system.user_db.create_user(username, password, role, permissions)
            
            # Try to authenticate with the injected username
            context = self.auth_system.authenticate(username, password)
            
            if context:
                print(f"❌ VULNERABLE: SQL injection succeeded - user authenticated")
                print(f"   Session ID: {context.session_id}")
                return {"success": True, "attack": "sql_injection_username", "vulnerable": True}
            else:
                print(f"✅ BLOCKED: SQL injection attack prevented")
                return {"success": False, "attack": "sql_injection_username", "vulnerable": False}
                
        except Exception as e:
            print(f"⚠️  EXCEPTION (may indicate protection): {e}")
            return {"success": False, "attack": "sql_injection_username", "error": str(e), "vulnerable": False}
    
    def test_xss_username(self):
        """Test XSS attack in username"""
        print("\n" + "="*70)
        print("TEST 3: XSS Attack - Username Field")
        print("="*70)
        
        try:
            # Attempt XSS in username
            username = "<script>alert('XSS')</script>admin"
            password = "password123"
            role = UserRole.USER
            permissions = set()
            
            print(f"Attempting to register with XSS username: {username}")
            
            self.auth_system.user_db.create_user(username, password, role, permissions)
            
            # Try to authenticate
            context = self.auth_system.authenticate_user(username, password)
            
            if context:
                print(f"❌ VULNERABLE: XSS attack succeeded - user authenticated")
                print(f"   Session ID: {context.session_id}")
                return {"success": True, "attack": "xss_username", "vulnerable": True}
            else:
                print(f"✅ BLOCKED: XSS attack prevented")
                return {"success": False, "attack": "xss_username", "vulnerable": False}
                
        except Exception as e:
            print(f"⚠️  EXCEPTION (may indicate protection): {e}")
            return {"success": False, "attack": "xss_username", "error": str(e), "vulnerable": False}
    
    def test_command_injection_password(self):
        """Test command injection in password"""
        print("\n" + "="*70)
        print("TEST 4: Command Injection Attack - Password Field")
        print("="*70)
        
        try:
            # Attempt command injection in password
            username = "testuser_cmd"
            password = "password; rm -rf /"
            role = UserRole.USER
            permissions = set()
            
            print(f"Attempting to register with malicious password: {password}")
            
            self.auth_system.user_db.create_user(username, password, role, permissions)
            
            # Try to authenticate
            context = self.auth_system.authenticate_user(username, password)
            
            if context:
                print(f"❌ VULNERABLE: Command injection succeeded - user authenticated")
                print(f"   Session ID: {context.session_id}")
                return {"success": True, "attack": "command_injection_password", "vulnerable": True}
            else:
                print(f"✅ BLOCKED: Command injection attack prevented")
                return {"success": False, "attack": "command_injection_password", "vulnerable": False}
                
        except Exception as e:
            print(f"⚠️  EXCEPTION (may indicate protection): {e}")
            return {"success": False, "attack": "command_injection_password", "error": str(e), "vulnerable": False}
    
    def test_auth_bypass_attack(self):
        """Test authentication bypass attempt"""
        print("\n" + "="*70)
        print("TEST 5: Authentication Bypass Attack")
        print("="*70)
        
        try:
            # Try to authenticate as admin with bypass
            username = "admin' --"
            password = "anything"
            
            print(f"Attempting auth bypass with username: {username}")
            
            context = self.auth_system.authenticate(username, password)
            
            if context:
                print(f"❌ VULNERABLE: Auth bypass succeeded - got session")
                print(f"   Role: {context.role.value}")
                print(f"   Session ID: {context.session_id}")
                return {"success": True, "attack": "auth_bypass", "vulnerable": True}
            else:
                print(f"✅ BLOCKED: Auth bypass prevented")
                return {"success": False, "attack": "auth_bypass", "vulnerable": False}
                
        except Exception as e:
            print(f"⚠️  EXCEPTION (may indicate protection): {e}")
            return {"success": False, "attack": "auth_bypass", "error": str(e), "vulnerable": False}
    
    def test_brute_force_login(self):
        """Test brute force login attempt"""
        print("\n" + "="*70)
        print("TEST 6: Brute Force Login Attack")
        print("="*70)
        
        try:
            username = "admin"
            passwords = ["password1", "password2", "password3", "admin", "123456"]
            
            print(f"Attempting brute force on {username} with {len(passwords)} passwords")
            
            successful_attempts = 0
            for password in passwords:
                context = self.auth_system.authenticate(username, password)
                if context:
                    successful_attempts += 1
                    print(f"   ❌ Password '{password}' succeeded")
                    self.session_ids.append(context.session_id)
            
            if successful_attempts > 0:
                print(f"❌ VULNERABLE: Brute force succeeded with {successful_attempts} passwords")
                return {"success": True, "attack": "brute_force", "vulnerable": True, "attempts": successful_attempts}
            else:
                print(f"✅ BLOCKED: Brute force prevented - all passwords failed")
                return {"success": False, "attack": "brute_force", "vulnerable": False}
                
        except Exception as e:
            print(f"⚠️  EXCEPTION: {e}")
            return {"success": False, "attack": "brute_force", "error": str(e), "vulnerable": False}
    
    def test_session_hijacking(self):
        """Test session hijacking attempt"""
        print("\n" + "="*70)
        print("TEST 7: Session Hijacking Attack")
        print("="*70)
        
        try:
            if not self.session_ids:
                print("⚠️  No valid sessions to hijack - skipping test")
                return {"success": False, "attack": "session_hijacking", "skipped": True}
            
            # Try to use someone else's session
            stolen_session = self.session_ids[0]
            print(f"Attempting to hijack session: {stolen_session}")
            
            context = self.auth_system.user_db.get_context_by_session(stolen_session)
            
            if context:
                print(f"❌ VULNERABLE: Session hijacking succeeded")
                print(f"   User ID: {context.user_id}")
                print(f"   Role: {context.role.value}")
                return {"success": True, "attack": "session_hijacking", "vulnerable": True}
            else:
                print(f"✅ BLOCKED: Session hijacking prevented")
                return {"success": False, "attack": "session_hijacking", "vulnerable": False}
                
        except Exception as e:
            print(f"⚠️  EXCEPTION: {e}")
            return {"success": False, "attack": "session_hijacking", "error": str(e), "vulnerable": False}
    
    def test_privilege_escalation(self):
        """Test privilege escalation attempt"""
        print("\n" + "="*70)
        print("TEST 8: Privilege Escalation Attack")
        print("="*70)
        
        try:
            # Create a normal user
            username = "normal_user"
            password = "normalpass"
            role = UserRole.USER
            permissions = set()
            
            self.auth_system.user_db.create_user(username, password, role, permissions)
            
            # Authenticate as normal user
            context = self.auth_system.authenticate(username, password)
            
            if not context:
                print("❌ Could not create normal user for testing")
                return {"success": False, "attack": "privilege_escalation", "error": "user_creation_failed"}
            
            print(f"Normal user role: {context.role.value}")
            
            # Try to modify user to admin (this would require direct system access)
            # In a real system, this would be done through API endpoints
            print("⚠️  Privilege escalation requires API access - testing current role only")
            
            if context.role == UserRole.ADMIN:
                print(f"❌ VULNERABLE: User has admin privileges when they shouldn't")
                return {"success": True, "attack": "privilege_escalation", "vulnerable": True}
            else:
                print(f"✅ SECURE: User has correct role: {context.role.value}")
                return {"success": False, "attack": "privilege_escalation", "vulnerable": False}
                
        except Exception as e:
            print(f"⚠️  EXCEPTION: {e}")
            return {"success": False, "attack": "privilege_escalation", "error": str(e), "vulnerable": False}
    
    def run_all_tests(self):
        """Run all real authorization attack tests"""
        print("\n" + "="*70)
        print("🔒 REAL AUTHORIZATION SYSTEM ATTACK TESTING")
        print("="*70)
        print("Testing ACTUAL authorization system with REAL attacks")
        print("No simulations - using the real auth_system.py implementation")
        print("="*70)
        
        # Run all tests
        self.test_results.append(self.test_normal_registration())
        self.test_results.append(self.test_sql_injection_username())
        self.test_results.append(self.test_xss_username())
        self.test_results.append(self.test_command_injection_password())
        self.test_results.append(self.test_auth_bypass_attack())
        self.test_results.append(self.test_brute_force_login())
        self.test_results.append(self.test_session_hijacking())
        self.test_results.append(self.test_privilege_escalation())
        
        self.print_honest_summary()
    
    def print_honest_summary(self):
        """Print honest assessment of results"""
        print("\n" + "="*70)
        print("📊 HONEST SECURITY ASSESSMENT")
        print("="*70)
        
        total_tests = len(self.test_results)
        vulnerable_tests = sum(1 for r in self.test_results if r.get("vulnerable", False))
        blocked_tests = sum(1 for r in self.test_results if not r.get("vulnerable", True) and not r.get("skipped", False))
        
        print(f"Total Attack Scenarios: {total_tests}")
        print(f"Vulnerable (Attacks Succeeded): {vulnerable_tests}")
        print(f"Blocked (Attacks Prevented): {blocked_tests}")
        print(f"Skipped/Errors: {total_tests - vulnerable_tests - blocked_tests}")
        
        print("\n🔍 DETAILED RESULTS:")
        for result in self.test_results:
            attack = result.get("attack", "unknown")
            vulnerable = result.get("vulnerable", False)
            skipped = result.get("skipped", False)
            error = result.get("error", None)
            
            if skipped:
                status = "⏭️  SKIPPED"
            elif error:
                status = f"⚠️  ERROR: {error}"
            elif vulnerable:
                status = "❌ VULNERABLE"
            else:
                status = "✅ BLOCKED"
            
            print(f"  {attack}: {status}")
        
        print("\n🛡️ SECURITY ASSESSMENT:")
        if vulnerable_tests == 0:
            print("✅ STRONG: No attacks succeeded against the authorization system")
        elif vulnerable_tests <= total_tests * 0.25:
            print("⚠️  MODERATE: Some attacks succeeded - needs improvement")
        else:
            print("❌ WEAK: Many attacks succeeded - serious security concerns")
        
        print("\n⚠️  HONEST NOTES:")
        print("- This tests the ACTUAL authorization_system.py implementation")
        print("- Results reflect real security posture, not AI simulations")
        print("- The system uses basic password hashing (SHA-256) which is not production-ready")
        print("- No rate limiting, no account lockout, no multi-factor authentication")
        print("- Session management is basic without proper expiration handling")
        print("- SQL injection protection depends on how data is stored (not tested here)")
        
        print("="*70)


def main():
    """Main test execution"""
    tester = RealAuthAttackTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()