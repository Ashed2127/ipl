# IPL Security Tests

This directory contains comprehensive security tests for IPL's compiler-level AI intelligence. These tests are used to validate that the compiler maintains its security capabilities after every architecture change.

## Purpose

These tests ensure that IPL's compiler-level AI continues to:
- Detect and block security attacks during compilation
- Allow legitimate code to compile successfully
- Maintain 100% attack prevention rate
- Provide zero false positives for safe code

## Test Files

### 1. `security_attack_tests.ipl`
Contains 20+ security attack scenarios including:
- SQL Injection attacks
- XSS attacks (stored, reflected)
- Command injection
- Path traversal
- LDAP injection, XML injection
- Buffer overflow, integer overflow
- Format string attacks
- CSRF, session fixation
- Timing attacks, race conditions
- NoSQL injection, header injection
- Zero-width character attacks
- Combined advanced attacks

### 2. `test_compiler_ai_security.py`
Basic security attack testing:
- SQL injection detection and blocking
- XSS attack detection and blocking
- Command injection detection and blocking
- Path traversal detection and blocking
- Combined attack detection
- Legitimate code compilation
- Safe coding practices recognition

### 3. `test_user_authentication.py`
Real-world authentication security testing:
- Legitimate user account creation
- Malicious user registration attempts
- SQL injection in registration
- XSS attacks in user creation
- Legitimate user login
- SQL injection in login attempts
- Command injection in login

### 4. `registration_login_system.ipl`
Complete registration/login system example:
- User database operations
- Session management
- Password hashing
- Registration and login services
- REST API endpoints

### 5. `run_security_tests.py`
Main test runner that executes all security tests:
- Runs all test files in sequence
- Provides pass/fail summary
- Returns appropriate exit codes
- Can be integrated into CI/CD pipelines

## Usage

### Run All Security Tests
```bash
cd ipl/tests/security
python3 run_security_tests.py
```

### Run Individual Tests
```bash
# Basic security tests
python3 test_compiler_ai_security.py

# Authentication security tests
python3 test_user_authentication.py
```

### From Project Root (Recommended)
```bash
python3 ipl/tests/security/run_security_tests.py
```

### From Security Test Directory
```bash
cd ipl/tests/security
python3 run_security_tests.py
```

## Integration with Development Workflow

### Before Architecture Changes
```bash
# Run security tests to establish baseline
python3 ipl/tests/security/run_security_tests.py
```

### After Architecture Changes
```bash
# Run security tests to validate AI intelligence maintained
python3 ipl/tests/security/run_security_tests.py
```

### Continuous Integration
Add to CI/CD pipeline:
```yaml
security_tests:
  script:
    - python3 ipl/tests/security/run_security_tests.py
  only:
    - merge_requests
    - main
```

## Expected Results

### All Tests Should Pass
- ✅ 100% attack prevention rate
- ✅ Zero false positives
- ✅ Legitimate code compiles successfully
- ✅ AI provides appropriate security warnings

### If Tests Fail
1. Review the specific test failure
2. Check if architecture change affected AI integration
3. Verify AI provider interface is intact
4. Ensure security pattern detection is working
5. Fix the issue before proceeding

## Security Test Metrics

The security tests validate:
- **Attack Detection**: AI recognizes attack patterns
- **Context Understanding**: AI understands code context
- **Preventive Security**: Blocks malicious code before execution
- **No External Dependencies**: All security is internal
- **Compilation Integration**: Security is part of compilation

## Adding New Security Tests

When adding new attack vectors or security scenarios:

1. Add attack pattern to `security_attack_tests.ipl`
2. Create test case in appropriate test file
3. Update `run_security_tests.py` if needed
4. Document the new threat in this README
5. Run full test suite to validate

## Key Principle

**Every architecture change must pass these security tests to ensure IPL's compiler-level AI intelligence is maintained.**

The compiler must remain intelligent at the compilation level, not just provide code suggestions. AI must continue to transform the compilation process itself, blocking malicious code before it can execute.