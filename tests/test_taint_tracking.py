"""
Unit Tests for Zero-Trust Data Taint Tracking System in IPL.
Tests:
1. Untrusted Taint Assignment
2. Critical Sink Guardrails (db_write, file_write) & TaintViolationError
3. Deterministic SanitizationNode & Taint Transition
4. Taint Arithmetic & String Propagation
5. Trusted Keyword Exemption
6. Introspection via taint_of built-in
"""
import sys
import unittest
from io import StringIO
from pathlib import Path
from rich.console import Console

_repo_dir = Path(__file__).resolve().parent.parent
if str(_repo_dir.parent) not in sys.path:
    sys.path.insert(0, str(_repo_dir.parent))
if str(_repo_dir) not in sys.path:
    sys.path.insert(0, str(_repo_dir))

try:
    from ipl_lang.lexer import Lexer
    from ipl_lang.parser import Parser
    from ipl_lang.runtime import Interpreter, IValue
    from ipl_lang.taint import TaintLevel, TaintTag, TaintViolationError
except ImportError:
    from lexer import Lexer
    from parser import Parser
    from runtime import Interpreter, IValue
    from taint import TaintLevel, TaintTag, TaintViolationError


class TestTaintPropagation(unittest.TestCase):
    def test_taint_tag_combine(self):
        untrusted = TaintTag(level=TaintLevel.UNTRUSTED, provenance="user_input")
        sanitized = TaintTag(level=TaintLevel.SANITIZED, provenance="validated_input")
        trusted = TaintTag(level=TaintLevel.TRUSTED, provenance="constant")

        # Untrusted + Trusted -> Untrusted
        c1 = TaintTag.combine(untrusted, trusted, "+")
        self.assertEqual(c1.level, TaintLevel.UNTRUSTED)

        # Sanitized + Trusted -> Sanitized
        c2 = TaintTag.combine(sanitized, trusted, "+")
        self.assertEqual(c2.level, TaintLevel.SANITIZED)

        # Trusted + Trusted -> Trusted
        c3 = TaintTag.combine(trusted, trusted, "+")
        self.assertEqual(c3.level, TaintLevel.TRUSTED)

    def test_taint_transition(self):
        raw_tag = TaintTag(level=TaintLevel.UNTRUSTED)
        clean_tag = raw_tag.transition_to(TaintLevel.SANITIZED, "sql_escape_filter")
        self.assertEqual(clean_tag.level, TaintLevel.SANITIZED)
        self.assertEqual(clean_tag.sanitizer_applied, "sql_escape_filter")
        self.assertTrue(any("sql_escape_filter" in h for h in clean_tag.audit_history))


class TestTaintRuntimeSecurity(unittest.TestCase):
    def setUp(self):
        self.output_buf = StringIO()
        self.console = Console(file=self.output_buf, color_system=None, width=120)
        self.interpreter = Interpreter(console=self.console)

    def run_code(self, source: str):
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        self.interpreter.run(program)
        return self.output_buf.getvalue()

    def test_untrusted_intent_taint(self):
        code = """
        let raw_age: Int = intent "extract user_age 42 from document" as Int;
        print "Taint is:", taint_of(raw_age);
        """
        out = self.run_code(code)
        self.assertIn("Taint is: Untrusted", out)

    def test_blocked_sink_untrusted_db_write(self):
        code = """
        let user_data: Int = intent "extract user_age 35" as Int;
        db_write("accounts", user_data);
        """
        with self.assertRaises(TaintViolationError) as ctx:
            self.run_code(code)
        self.assertIn("db_write('accounts')", str(ctx.exception))
        self.assertIn("Untrusted", str(ctx.exception))

    def test_blocked_sink_untrusted_file_write(self):
        code = """
        let payload: Int = intent "extract user_age 21" as Int;
        file_write("/tmp/out.txt", payload);
        """
        with self.assertRaises(TaintViolationError) as ctx:
            self.run_code(code)
        self.assertIn("file_write('/tmp/out.txt')", str(ctx.exception))
        self.assertIn("Untrusted", str(ctx.exception))

    def test_sanitization_node_allows_sink_execution(self):
        code = """
        let raw_age: Int = intent "extract user_age 28 from document" as Int;
        let safe_age = sanitize(raw_age, "range_validator");
        print "Clean taint:", taint_of(safe_age);
        let ok = db_write("users", safe_age);
        print "DB Write success:", ok;
        """
        out = self.run_code(code)
        self.assertIn("Clean taint: Sanitized", out)
        self.assertIn("Successfully committed record", out)
        self.assertIn("DB Write success: True", out)

    def test_file_write_after_sanitization(self):
        code = """
        let raw_str = intent "extract notes from report";
        let safe_str = sanitize(raw_str);
        let ok = file_write("/tmp/verified.txt", safe_str);
        print "File Write success:", ok;
        """
        out = self.run_code(code)
        self.assertIn("Wrote to '/tmp/verified.txt'", out)
        self.assertIn("File Write success: True", out)

    def test_trusted_declaration_bypasses_taint_violation(self):
        code = """
        trusted let admin_token = "SUPER_SECRET_ADMIN_OVERRIDE";
        print "Admin token taint:", taint_of(admin_token);
        let ok = db_write("admin_sessions", admin_token);
        print "DB write ok:", ok;
        """
        out = self.run_code(code)
        self.assertIn("Admin token taint: Trusted", out)
        self.assertIn("DB write ok: True", out)

    def test_taint_propagation_in_runtime_expressions(self):
        code = """
        let untrusted_num: Int = intent "extract age 20" as Int;
        let normal_num = 5;
        let sum = untrusted_num + normal_num;
        print "Sum taint:", taint_of(sum);
        """
        out = self.run_code(code)
        self.assertIn("Sum taint: Untrusted", out)


if __name__ == "__main__":
    unittest.main()
