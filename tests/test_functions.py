"""
Unit tests for Functions and Builtins in IPL.
"""
import sys
import unittest
from io import StringIO
from pathlib import Path
from rich.console import Console

# Ensure parent directory is on sys.path
_repo_dir = Path(__file__).resolve().parent.parent
if str(_repo_dir.parent) not in sys.path:
    sys.path.insert(0, str(_repo_dir.parent))
if str(_repo_dir) not in sys.path:
    sys.path.insert(0, str(_repo_dir))

try:
    from ipl_lang.lexer import Lexer
    from ipl_lang.parser import Parser
    from ipl_lang.runtime import Interpreter
except ImportError:
    from lexer import Lexer
    from parser import Parser
    from runtime import Interpreter


class TestFunctions(unittest.TestCase):
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

    def test_simple_function(self):
        code = """
        fn add(a, b) {
            return a + b;
        }
        let result = add(15, 27);
        print result;
        """
        out = self.run_code(code)
        self.assertIn("42", out)

    def test_recursive_function_factorial(self):
        code = """
        fn factorial(n) {
            if n <= 1 {
                return 1;
            }
            return n * factorial(n - 1);
        }
        print factorial(5);
        """
        out = self.run_code(code)
        self.assertIn("120", out)

    def test_builtins(self):
        code = """
        let arr = [10, 20, 30, 40];
        print len(arr);
        print min(arr);
        print max(arr);
        print abs(-42);
        print round(3.14159, 2);
        """
        out = self.run_code(code)
        self.assertIn("4", out)
        self.assertIn("10", out)
        self.assertIn("40", out)
        self.assertIn("42", out)
        self.assertIn("3.14", out)

    def test_function_with_semantic_types(self):
        code = """
        fn parse_rebate(claim: Currency) {
            return claim;
        }
        let r = parse_rebate("fifty-five dollars");
        print r;
        """
        out = self.run_code(code)
        self.assertIn("55.00 USD", out)

    def test_type_of_and_confidence_builtins(self):
        code = """
        let cost: Currency = "100 dollars";
        print type_of(cost);
        print confidence(cost) >= 0.8;
        """
        out = self.run_code(code)
        self.assertIn("Currency", out)
        self.assertIn("True", out)

    def test_self_healing_function_call(self):
        code = """
        fn calculate_interest(principal, rate) {
            return principal * rate;
        }
        let interest = calc_interest(1000, 0.05);
        print interest;
        """
        out = self.run_code(code)
        self.assertIn("Self-Healing", out)
        self.assertIn("50", out)


if __name__ == "__main__":
    unittest.main()
