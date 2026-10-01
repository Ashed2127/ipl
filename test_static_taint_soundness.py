"""
Tests for Phase 1: Sound Static Taint Analysis
Tests the four critical soundness requirements:
1. Branch join (lattice meet)
2. Loop fixpoint
3. Interprocedural calls
4. Unresolvable calls
"""
import unittest
from lexer import Lexer
from parser import Parser
from static_taint_analyzer import StaticTaintAnalysis, analyze_program_taint
from taint import TaintLevel


class TestBranchJoin(unittest.TestCase):
    """Test 1: Branch join must use lattice meet (conservative merge)"""

    def test_branch_join_lattice_meet(self):
        """
        Variable sanitized on one branch only should be UNTRUSTED after merge.
        if condition:
            x = sanitize_for_sql(untrusted)  # SANITIZED
        else:
            x = untrusted  # UNTRUSTED
        # After merge: x should be UNTRUSTED (lattice meet)
        db_write("users", x)  # Should be violation
        """
        code = """
        let untrusted = set_untrusted("admin");
        if some_condition {
            let x = sanitize_for_sql(untrusted);
        } else {
            let x = untrusted;
        }
        db_write("users", x);
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        result = analyze_program_taint(program)

        # Should detect violation because x is UNTRUSTED after merge
        self.assertTrue(any(v['sink'] == 'db_write' for v in result['violations']),
                       "Branch join should use lattice meet - UNTRUSTED on one branch = UNTRUSTED after merge")


class TestLoopFixpoint(unittest.TestCase):
    """Test 2: Loop must iterate to fixpoint, not single pass"""

    def test_loop_fixpoint_reassignment(self):
        """
        Variable reassigned based on tainted data on iteration 2.
        x = trusted
        while condition {
            x = untrusted  # On iteration 2, x becomes UNTRUSTED
        }
        db_write("users", x)  # Should be violation
        """
        code = """
        let untrusted = set_untrusted("admin");
        let x = "safe";
        while true {
            x = untrusted;
        }
        db_write("users", x);
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        result = analyze_program_taint(program)

        # Should detect violation because x becomes UNTRUSTED in loop
        self.assertTrue(any(v['sink'] == 'db_write' for v in result['violations']),
                       "Loop must iterate to fixpoint - reassignment should be detected")


class TestInterproceduralCalls(unittest.TestCase):
    """Test 3: Taint must propagate through function calls"""

    def test_interprocedural_taint_propagation(self):
        """
        Tainted value passed through helper function to sink.
        fn helper(input) {
            return input;  # Propagate taint
        }
        let untrusted = set_untrusted("admin");
        let x = helper(untrusted);  # x should be UNTRUSTED
        db_write("users", x)  # Should be violation
        """
        code = """
        fn helper(input) {
            return input;
        }
        let untrusted = set_untrusted("admin");
        let x = helper(untrusted);
        db_write("users", x);
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        result = analyze_program_taint(program)

        # Should detect violation because taint propagates through function
        self.assertTrue(any(v['sink'] == 'db_write' for v in result['violations']),
                       "Taint must propagate through function calls")


class TestUnresolvableCalls(unittest.TestCase):
    """Test 4: Indirect calls must be dynamic_sites, never static_safe"""

    def test_indirect_call_to_sink(self):
        """
        Call through variable holding function reference.
        let sink_func = db_write;
        let untrusted = set_untrusted("admin");
        sink_func("users", untrusted);  # Should be dynamic_site, not static_safe
        """
        code = """
        let sink_func = db_write;
        let untrusted = set_untrusted("admin");
        sink_func("users", untrusted);
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        result = analyze_program_taint(program)

        # Should NOT be in static_safe_sites (could be in dynamic_sites or violations)
        safe_sites = [s for s in result['static_safe_sites'] if 'sink_func' in str(s)]
        self.assertEqual(len(safe_sites), 0,
                        "Indirect calls must be dynamic_sites, never static_safe")


if __name__ == "__main__":
    unittest.main(verbosity=2)
