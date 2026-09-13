"""
Unit tests for Control Flow in IPL (if/elif/else, for loops, while loops, break, continue).
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


class TestControlFlow(unittest.TestCase):
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

    def test_if_then_branch(self):
        code = """
        let x = 10;
        if x > 5 {
            print "x is greater than 5";
        }
        """
        out = self.run_code(code)
        self.assertIn("x is greater than 5", out)

    def test_if_else_branch(self):
        code = """
        let x = 3;
        if x > 5 {
            print "greater";
        } else {
            print "smaller or equal";
        }
        """
        out = self.run_code(code)
        self.assertIn("smaller or equal", out)
        self.assertNotIn("greater", out)

    def test_if_elif_else_branch(self):
        code = """
        let score = 75;
        if score >= 90 {
            print "Grade A";
        } elif score >= 70 {
            print "Grade B";
        } else {
            print "Grade C";
        }
        """
        out = self.run_code(code)
        self.assertIn("Grade B", out)
        self.assertNotIn("Grade A", out)
        self.assertNotIn("Grade C", out)

    def test_for_loop_over_list(self):
        code = """
        let items = [10, 20, 30];
        var total = 0;
        for item in items {
            total = total + item;
        }
        print total;
        """
        out = self.run_code(code)
        self.assertIn("60", out)

    def test_for_loop_with_range(self):
        code = """
        var sum = 0;
        for i in range(5) {
            sum = sum + i;
        }
        print sum;
        """
        out = self.run_code(code)
        self.assertIn("10", out)

    def test_while_loop(self):
        code = """
        var count = 3;
        while count > 0 {
            print count;
            count = count - 1;
        }
        print "Liftoff!";
        """
        out = self.run_code(code)
        self.assertIn("3", out)
        self.assertIn("2", out)
        self.assertIn("1", out)
        self.assertIn("Liftoff!", out)

    def test_break_statement(self):
        code = """
        var found = 0;
        for i in [1, 2, 3, 4, 5] {
            if i == 3 {
                found = i;
                break;
            }
        }
        print found;
        """
        out = self.run_code(code)
        self.assertIn("3", out)

    def test_continue_statement(self):
        code = """
        var evens = 0;
        for i in [1, 2, 3, 4] {
            if i % 2 != 0 {
                continue;
            }
            evens = evens + 1;
        }
        print evens;
        """
        out = self.run_code(code)
        self.assertIn("2", out)

    def test_index_access_list_and_dict(self):
        code = """
        let list = ["first", "second", "third"];
        let dict = {"name": "IPL", "version": 2};
        print list[0];
        print list[2];
        print dict["name"];
        """
        out = self.run_code(code)
        self.assertIn("first", out)
        self.assertIn("third", out)
        self.assertIn("IPL", out)


if __name__ == "__main__":
    unittest.main()
