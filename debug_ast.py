from lexer import Lexer
from parser import Parser

# Test vulnerable code
vulnerable_code = """
let malicious = set_untrusted("'; DROP TABLE users; --");
db_write("users", malicious);
"""

print("Testing vulnerable code:")
print(vulnerable_code)

lexer = Lexer(vulnerable_code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

print("\nAST structure:")
print(ast)
print(f"\nAST type: {type(ast)}")
print(f"AST class: {ast.__class__.__name__}")

if hasattr(ast, 'statements'):
    print(f"\nNumber of statements: {len(ast.statements)}")
    for i, stmt in enumerate(ast.statements):
        print(f"\nStatement {i}:")
        print(f"  Type: {stmt.__class__.__name__}")
        print(f"  Value: {stmt}")
