"""
Test suite for Authorization System.
Tests user authentication, role-based access control, context-aware security,
and integration with the hierarchical AI engine.
"""
import sys
import os
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from authorization_system import (
        get_authorization_system, UserRole, Permission, SecurityContext,
        AuthorizationDecision, PolicyEngine, ContextAwareSecurityAnalyzer, AuthorizationSystem
    )
    from compiler import NeuroSymbolicCompiler, LocalInferenceRuntime
    from runtime import Interpreter, IValue
    from rich.console import Console
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class TestAuthorizationSystem(unittest.TestCase):
    """Test core authorization system functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.auth_system = get_authorization_system()
        self.console = Console()
        
    def test_user_authentication(self):
        """Test user authentication with correct and incorrect credentials."""
        # Add a test user using the user database directly
        self.auth_system.user_db.create_user("testuser", "testpass", UserRole.USER, {Permission.READ, Permission.WRITE})
        
        # Test successful authentication
        context = self.auth_system.authenticate_user("testuser", "testpass")
        self.assertIsNotNone(context)
        self.assertEqual(context.user_id, "testuser")
        self.assertEqual(context.role, UserRole.USER)
        
        # Test failed authentication with wrong password
        context = self.auth_system.authenticate_user("testuser", "wrongpass")
        self.assertIsNone(context)
        
        # Test failed authentication with non-existent user
        context = self.auth_system.authenticate_user("nonexistent", "testpass")
        self.assertIsNone(context)
        
        # Clean up
        del self.auth_system.user_db.users["testuser"]
    
    def test_role_based_access_control(self):
        """Test role-based access control permissions."""
        # Add users with different roles
        self.auth_system.user_db.create_user("guest_user", "pass", UserRole.GUEST, {Permission.READ})
        self.auth_system.user_db.create_user("regular_user", "pass", UserRole.USER, {Permission.READ, Permission.WRITE})
        self.auth_system.user_db.create_user("admin_user", "pass", UserRole.ADMIN, {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.EXECUTE, Permission.ADMIN})
        
        # Get security contexts
        guest_context = self.auth_system.authenticate_user("guest_user", "pass")
        user_context = self.auth_system.authenticate_user("regular_user", "pass")
        admin_context = self.auth_system.authenticate_user("admin_user", "pass")
        
        # Test permission checks through context
        guest_has_read = Permission.READ in guest_context.permissions
        user_has_read = Permission.READ in user_context.permissions
        admin_has_read = Permission.READ in admin_context.permissions
        
        self.assertTrue(guest_has_read)  # Guest should have read
        self.assertTrue(user_has_read)   # User should have read
        self.assertTrue(admin_has_read)  # Admin should have read
        
        # Test write permissions
        guest_has_write = Permission.WRITE in guest_context.permissions
        user_has_write = Permission.WRITE in user_context.permissions
        admin_has_write = Permission.WRITE in admin_context.permissions
        
        self.assertFalse(guest_has_write)  # Guest should not have write
        self.assertTrue(user_has_write)     # User should have write
        self.assertTrue(admin_has_write)   # Admin should have write
        
        # Test admin permissions
        guest_has_admin = Permission.ADMIN in guest_context.permissions
        user_has_admin = Permission.ADMIN in user_context.permissions
        admin_has_admin = Permission.ADMIN in admin_context.permissions
        
        self.assertFalse(guest_has_admin)  # Guest should not have admin
        self.assertFalse(user_has_admin)   # User should not have admin
        self.assertTrue(admin_has_admin)   # Admin should have admin
        
        # Clean up
        del self.auth_system.user_db.users["guest_user"]
        del self.auth_system.user_db.users["regular_user"]
        del self.auth_system.user_db.users["admin_user"]
    
    def test_authorization_decision(self):
        """Test authorization decision making."""
        # Add test user
        self.auth_system.user_db.create_user("auth_test", "pass", UserRole.USER, {Permission.READ, Permission.WRITE})
        context = self.auth_system.authenticate_user("auth_test", "pass")
        
        # Test allowed decision
        decision = self.auth_system.authorize_intent(context, "read data", None)
        self.assertTrue(decision.allowed)
        
        # Test denied decision (admin operation)
        decision = self.auth_system.authorize_intent(context, "delete system files", None)
        self.assertFalse(decision.allowed)
        self.assertIn("permission", decision.reason.lower())
        
        # Clean up
        del self.auth_system.user_db.users["auth_test"]
    
    def test_security_context(self):
        """Test security context creation and management."""
        context = SecurityContext(
            user_id="test_user",
            role=UserRole.USER,
            permissions={Permission.READ, Permission.WRITE},
            session_id="test_session",
            ip_address="127.0.0.1",
            user_agent="test_agent"
        )
        
        self.assertEqual(context.user_id, "test_user")
        self.assertEqual(context.role, UserRole.USER)
        self.assertEqual(len(context.permissions), 2)
        self.assertIn(Permission.READ, context.permissions)
        self.assertIn(Permission.WRITE, context.permissions)
        
        # Test to_dict conversion
        context_dict = context.to_dict()
        self.assertEqual(context_dict["user_id"], "test_user")
        self.assertEqual(context_dict["role"], "user")
        self.assertEqual(len(context_dict["permissions"]), 2)
    
    def test_user_management(self):
        """Test user management operations."""
        # Add user
        self.auth_system.user_db.create_user("mgmt_test", "password", UserRole.USER, {Permission.READ, Permission.WRITE})
        
        # Check user exists
        self.assertIn("mgmt_test", self.auth_system.user_db.users)
        user_data = self.auth_system.user_db.users["mgmt_test"]
        self.assertEqual(user_data["role"], UserRole.USER)
        
        # Update user role
        user_data["role"] = UserRole.ADMIN
        user_data["permissions"] = {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.EXECUTE, Permission.ADMIN}
        
        user_data = self.auth_system.user_db.users["mgmt_test"]
        self.assertEqual(user_data["role"], UserRole.ADMIN)
        
        # List users
        users = list(self.auth_system.user_db.users.keys())
        self.assertIn("mgmt_test", users)
        
        # Delete user
        del self.auth_system.user_db.users["mgmt_test"]
        
        # Verify deletion
        self.assertNotIn("mgmt_test", self.auth_system.user_db.users)


class TestAuthorizationIntegration(unittest.TestCase):
    """Test authorization system integration with compiler and runtime."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.console = Console()
        self.compiler = NeuroSymbolicCompiler(console=self.console, enable_authorization=True)
        self.interpreter = Interpreter(console=self.console, enable_authorization=True)
        
        # Add test users
        self.compiler.system1.auth_system.user_db.create_user("test_user", "password", UserRole.USER, {Permission.READ, Permission.WRITE})
        self.compiler.system1.auth_system.user_db.create_user("test_admin", "admin", UserRole.ADMIN, {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.EXECUTE, Permission.ADMIN})
    
    def tearDown(self):
        """Clean up test fixtures."""
        if "test_user" in self.compiler.system1.auth_system.user_db.users:
            del self.compiler.system1.auth_system.user_db.users["test_user"]
        if "test_admin" in self.compiler.system1.auth_system.user_db.users:
            del self.compiler.system1.auth_system.user_db.users["test_admin"]
    
    def test_compiler_authentication(self):
        """Test authentication through compiler."""
        # Test successful authentication
        success = self.compiler.authenticate_user("test_user", "password")
        self.assertTrue(success)
        
        # Verify security context is set
        self.assertIsNotNone(self.compiler.system1.security_context)
        self.assertEqual(self.compiler.system1.security_context.user_id, "test_user")
        
        # Test failed authentication
        success = self.compiler.authenticate_user("test_user", "wrong_password")
        self.assertFalse(success)
    
    def test_runtime_authentication_builtin(self):
        """Test authentication through runtime builtin function."""
        # Test that the authenticate builtin exists
        self.assertIn("authenticate", self.interpreter.global_env.bindings)
    
    def test_authorization_statistics(self):
        """Test authorization statistics collection."""
        # Authenticate user
        self.compiler.authenticate_user("test_user", "password")
        
        # Get statistics
        stats = self.compiler.get_authorization_statistics()
        self.assertIsNotNone(stats)
        self.assertIn("total_authorizations", stats)
        self.assertIn("authorization_results", stats)
    
    def test_security_context_propagation(self):
        """Test security context propagation to runtime environment."""
        # Authenticate through compiler
        self.compiler.authenticate_user("test_user", "password")
        
        # Verify context propagated to interpreter environment
        self.assertIsNotNone(self.interpreter.global_env.security_context)
        self.assertEqual(self.interpreter.global_env.security_context.user_id, "test_user")


class TestSecurityAnalysis(unittest.TestCase):
    """Test security analysis and threat detection."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.auth_system = get_authorization_system()
        self.security_analyzer = self.auth_system.context_analyzer
    
    def test_security_analysis_engine(self):
        """Test security analysis of intents."""
        # Test safe intent
        safe_intent = "read user data"
        analysis = self.security_analyzer.analyze_security_context(safe_intent, None)
        self.assertIsNotNone(analysis)
        self.assertLess(analysis.get("threat_score", 0), 0.5)  # Should be low threat
        
        # Test malicious intent
        malicious_intent = "delete all system files and format disk"
        analysis = self.security_analyzer.analyze_security_context(malicious_intent, None)
        self.assertIsNotNone(analysis)
        self.assertGreater(analysis.get("threat_score", 0), 0.7)  # Should be high threat
    
    def test_threat_detection(self):
        """Test threat detection patterns."""
        # Test SQL injection pattern
        sql_injection = "SELECT * FROM users WHERE '1'='1'"
        analysis = self.security_analyzer.analyze_security_context(sql_injection, None)
        self.assertGreater(analysis.get("threat_score", 0), 0.5)
        
        # Test command injection pattern
        cmd_injection = "rm -rf / && format c:"
        analysis = self.security_analyzer.analyze_security_context(cmd_injection, None)
        self.assertGreater(analysis.get("threat_score", 0), 0.5)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.auth_system = get_authorization_system()
    
    def test_duplicate_user_creation(self):
        """Test creating duplicate users."""
        self.auth_system.user_db.create_user("duplicate", "pass", UserRole.USER, {Permission.READ})
        with self.assertRaises(ValueError):
            self.auth_system.user_db.create_user("duplicate", "pass", UserRole.USER, {Permission.READ})
        del self.auth_system.user_db.users["duplicate"]
    
    def test_nonexistent_user_operations(self):
        """Test operations on non-existent users."""
        self.assertNotIn("nonexistent", self.auth_system.user_db.users)
        
        # Try to get user info for non-existent user
        permissions = self.auth_system.user_db.get_user_permissions("nonexistent")
        self.assertEqual(len(permissions), 0)
    
    def test_null_security_context(self):
        """Test authorization with null security context."""
        decision = self.auth_system.authorize_intent(None, "test operation", None)
        self.assertFalse(decision.allowed)
        self.assertIn("context", decision.reason.lower())
    
    def test_empty_intent_authorization(self):
        """Test authorization with empty intent."""
        self.auth_system.user_db.create_user("test", "pass", UserRole.USER, {Permission.READ})
        context = self.auth_system.authenticate_user("test", "pass")
        
        decision = self.auth_system.authorize_intent(context, "", None)
        self.assertTrue(decision.allowed)  # Empty intent should be allowed
        
        del self.auth_system.user_db.users["test"]


def run_tests():
    """Run all authorization tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestAuthorizationSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestAuthorizationIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)