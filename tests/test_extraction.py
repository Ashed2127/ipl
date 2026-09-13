import sys
import unittest
from pathlib import Path

# Ensure parent directory is on sys.path
_repo_dir = Path(__file__).resolve().parent.parent
if str(_repo_dir.parent) not in sys.path:
    sys.path.insert(0, str(_repo_dir.parent))
if str(_repo_dir) not in sys.path:
    sys.path.insert(0, str(_repo_dir))

try:
    from ipl_lang.semantic_engine import SemanticEngine
except ImportError:
    from semantic_engine import SemanticEngine


class TestExtractionScript(unittest.TestCase):
    def test_sample_extractions(self):
        test_cases = [
            "the service costs ninety-nine bucks and 50 cents",
            "approx 8 dollars and 45 cents",
            "costs about $99.99",
            "twenty-five dollars",
            "around 450 euros",
            "£25.50",
            "about a dozen",
            "three hundred and forty"
        ]
        for tc in test_cases:
            curr = SemanticEngine.extract_currency(tc)
            num = SemanticEngine.extract_number(tc, as_float=True)
            self.assertIsNotNone(curr)
            self.assertIsNotNone(num)
            self.assertGreater(curr["confidence"], 0.7)


if __name__ == "__main__":
    unittest.main()
