"""
Unit and Integration Tests for IPL (Intelligent Programming Language / Aether).
Tests Intelligent Variables and Intelligent Print end-to-end.
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
    from ipl_lang.runtime import Interpreter, Environment, IValue
    from ipl_lang.semantic_engine import SemanticEngine
except ImportError:
    from lexer import Lexer
    from parser import Parser
    from runtime import Interpreter, Environment, IValue
    from semantic_engine import SemanticEngine


class TestSemanticEngine(unittest.TestCase):
    def test_currency_extraction(self):
        res1 = SemanticEngine.extract_currency("the service costs ninety-nine bucks and 50 cents")
        self.assertEqual(res1["amount"], 99.50)
        self.assertEqual(res1["currency"], "USD")
        self.assertGreater(res1["confidence"], 0.85)

        res2 = SemanticEngine.extract_currency("approx 8 dollars and 45 cents")
        self.assertEqual(res2["amount"], 8.45)
        self.assertEqual(res2["currency"], "USD")

        res3 = SemanticEngine.extract_currency("around 450 euros")
        self.assertEqual(res3["amount"], 450.0)
        self.assertEqual(res3["currency"], "EUR")

        res4 = SemanticEngine.extract_currency("£25.50")
        self.assertEqual(res4["amount"], 25.50)
        self.assertEqual(res4["currency"], "GBP")

    def test_sentiment_extraction(self):
        pos = SemanticEngine.extract_sentiment("The mechanical keys feel crisp and tactile, absolutely fantastic build!")
        self.assertGreater(pos["score"], 0.5)
        self.assertIn("Positive", pos["label"])

        neg = SemanticEngine.extract_sentiment("App broke on day two and crashed repeatedly, horrible experience.")
        self.assertLess(neg["score"], -0.5)
        self.assertIn("Negative", neg["label"])

        # Test negation handling
        negated = SemanticEngine.extract_sentiment("The performance was not good and not fast.")
        self.assertLess(negated["score"], 0.0)

    def test_quantity_extraction(self):
        q1 = SemanticEngine.extract_quantity("latency is around 450 ms")
        self.assertEqual(q1["value"], 450.0)
        self.assertEqual(q1["unit"], "ms")
        self.assertEqual(q1["dimension"], "time")

        q2 = SemanticEngine.extract_quantity("memory usage is 16 gb")
        self.assertEqual(q2["value"], 16.0)
        self.assertEqual(q2["unit"], "GB")
        self.assertEqual(q2["dimension"], "storage")

    def test_intent_extraction(self):
        intent_data = SemanticEngine.extract_intent("someone used my stolen credit card for unauthorized transactions")
        self.assertEqual(intent_data["intent"], "Fraud")
        self.assertGreater(intent_data["confidence"], 0.80)

        custom_intent = SemanticEngine.extract_intent(
            "please give me my money back for this cancelled order",
            candidates=["Refund", "Support", "Inquiry"]
        )
        self.assertEqual(custom_intent["intent"], "Refund")

    def test_self_healing_variable_match(self):
        scope = {"customer_review": 1, "base_price": 2, "maintenance_window": 3, "total": 4}
        match, conf = SemanticEngine.find_self_healing_variable("totl", scope)
        self.assertEqual(match, "total")
        self.assertGreater(conf, 0.70)

        match2, conf2 = SemanticEngine.find_self_healing_variable("cust_revw", scope)
        self.assertEqual(match2, "customer_review")


class TestIPLInterpreter(unittest.TestCase):
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

    def test_intelligent_variables_and_arithmetic(self):
        code = """
        let price: Currency = "ninety-nine bucks and 50 cents";
        let tax: Currency = "8 dollars and 45 cents";
        let total = price + tax;
        print total;
        """
        out = self.run_code(code)
        self.assertIn("107.95 USD", out)

    def test_quantity_variables_and_arithmetic(self):
        code = """
        let ping1: Quantity = "120 ms";
        let ping2: Quantity = "80 ms";
        let total_latency = ping1 + ping2;
        print total_latency;
        """
        out = self.run_code(code)
        self.assertIn("200 ms", out)

    def test_refinement_invariant_breach(self):
        code = """
        let safe_price: Currency where (v <= 50.0) = "99 dollars";
        print safe_price;
        """
        out = self.run_code(code)
        self.assertIn("Invariant Breach", out)
        self.assertIn("failed condition", out)

    def test_immutability_enforcement(self):
        # 'let' should reject reassignment
        code_let = """
        let x = 10;
        x = 20;
        """
        with self.assertRaises(TypeError):
            self.run_code(code_let)

        # 'var' should allow reassignment
        code_var = """
        var y = 10;
        y = 25;
        print y;
        """
        out = self.run_code(code_var)
        self.assertIn("25", out)

    def test_self_healing_variable_resolution(self):
        code = """
        let customer_review: Sentiment = "Super fast, love it!";
        print custmer_revw;
        """
        out = self.run_code(code)
        self.assertIn("Self-Healing", out)
        self.assertIn("customer_review", out)

    def test_audience_adaptive_print(self):
        code = """
        let cost: Currency = "150 dollars";
        print cost for "executive";
        print cost for "child";
        print cost for "developer";
        """
        out = self.run_code(code)
        self.assertIn("Financial Bottom Line: 150.00 USD", out)
        self.assertIn("shiny coins", out)
        self.assertIn("<IValue::dict>", out)

    def test_semantic_query_print(self):
        code = """
        let report = { "errors": 95, "status": "failing server crash" };
        print "highlight risks in" report;
        print "summary of" report;
        """
        out = self.run_code(code)
        self.assertIn("Risk Analysis Found Critical Triggers", out)
        self.assertIn("Summary: Structured dictionary", out)

    def test_visual_presentation_formats(self):
        code = """
        let items = [ {"name": "Server A", "cost": 100}, {"name": "Server B", "cost": 250} ];
        print items as table;
        let stats = { "cpu": 45, "ram": 85 };
        print stats as bar_chart;
        let status: Prob<String> = "Operational";
        print status as badge;
        let health: Quantity = "75 percent";
        print health as gauge;
        """
        out = self.run_code(code)
        self.assertIn("Server A", out)
        self.assertIn("Proportional Distribution", out)
        self.assertIn("CONFIDENCE", out)
        self.assertIn("Gauge", out)


if __name__ == "__main__":
    unittest.main()
