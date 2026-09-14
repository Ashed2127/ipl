"""
Unit tests for IPL Module System and Standard Library Built-ins.
Tests importing modules, aliasing, circular protection, and cryptographic/data primitives.
"""

import unittest
import os
import tempfile
import time
from io import StringIO
from rich.console import Console

from lexer import Lexer
from parser import Parser
from runtime import Interpreter, IValue, TaintLevel


class TestImportsAndStdlib(unittest.TestCase):
    def setUp(self):
        self.output_io = StringIO()
        self.console = Console(file=self.output_io, force_terminal=False, color_system=None)
        self.interpreter = Interpreter(console=self.console)

    def _execute(self, source: str, filepath: str = "<test>"):
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        self.interpreter.run(program, source_code=source)
        return self.output_io.getvalue()

    def test_sha256_builtin(self):
        code = '''
        let h = sha256("hello world")
        print h
        '''
        out = self._execute(code)
        # Expected sha256 of "hello world" is b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
        self.assertIn("b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9", out)

    def test_md5_builtin(self):
        code = '''
        let h = md5("hello world")
        print h
        '''
        out = self._execute(code)
        # Expected md5 of "hello world" is 5eb63bbbe01eeed093cb22bb8f5acdc3
        self.assertIn("5eb63bbbe01eeed093cb22bb8f5acdc3", out)

    def test_base64_encode_decode(self):
        code = '''
        let raw = "IPL Secure Token 2026"
        let enc = base64_encode(raw)
        print enc
        let dec = base64_decode(enc)
        print dec
        '''
        out = self._execute(code)
        self.assertIn("SVBMIFNlY3VyZSBUb2tlbiAyMDI2", out)
        self.assertIn("IPL Secure Token 2026", out)

    def test_json_encode_decode(self):
        code = '''
        let payload = {"service": "vault", "status": "active"}
        let json_str = json_encode(payload)
        print json_str
        let recovered = json_decode(json_str)
        print recovered["service"]
        '''
        out = self._execute(code)
        self.assertIn('"service": "vault"', out)
        self.assertIn("vault", out)

    def test_now_builtin(self):
        code = '''
        let ts = now()
        print ts
        '''
        out = self._execute(code)
        # Verify ISO 8601 format
        self.assertIn("T", out)
        self.assertIn("+00:00", out)

    def test_module_import_with_alias(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            mod_path = os.path.join(tmpdir, "math_mod.ipl")
            with open(mod_path, "w", encoding="utf-8") as f:
                f.write('''
                fn double_num(x) {
                    return x * 2
                }
                let const_val = 100
                ''')

            main_code = f'''
            import "{mod_path}" as m
            let result = m.double_num(21)
            print result
            print m.const_val
            '''
            out = self._execute(main_code)
            self.assertIn("42", out)
            self.assertIn("100", out)

    def test_module_import_direct(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            mod_path = os.path.join(tmpdir, "helper.ipl")
            with open(mod_path, "w", encoding="utf-8") as f:
                f.write('''
                fn greet(name) {
                    return "Hello " + name
                }
                ''')

            main_code = f'''
            import "{mod_path}"
            let msg = greet("World")
            print msg
            '''
            out = self._execute(main_code)
            self.assertIn("Hello World", out)

    def test_circular_import_safety(self):
        # Ensure importing the same module multiple times doesn't loop infinitely
        with tempfile.TemporaryDirectory() as tmpdir:
            mod_path = os.path.join(tmpdir, "cycle.ipl")
            with open(mod_path, "w", encoding="utf-8") as f:
                f.write(f'''
                import "{mod_path}"
                let cycle_val = 999
                ''')

            main_code = f'''
            import "{mod_path}" as c
            print c.cycle_val
            '''
            out = self._execute(main_code)
            self.assertIn("999", out)


if __name__ == "__main__":
    unittest.main()
