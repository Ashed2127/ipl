"""
Basic test to verify bytecode VM works correctly.
"""
from lexer import Lexer
from parser import Parser
from bytecode import BytecodeCompiler, BytecodeInterpreter
from static_taint_analyzer import analyze_program_taint


def test_simple_arithmetic():
    """Test basic arithmetic compilation and execution"""
    code = """
    let x = 1 + 2;
    let y = x * 3;
    print(y);
    """

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    # Run static analysis
    static_result = analyze_program_taint(program)

    # Compile to bytecode
    compiler = BytecodeCompiler(static_result)
    bytecode = compiler.compile(program)

    print(f"Compiled {len(bytecode.instructions)} instructions")

    # Execute
    vm = BytecodeInterpreter()
    vm.execute(bytecode)

    print("Test passed!")


def test_safe_sink():
    """Test that safe sink calls work"""
    code = """
    let safe = "safe_data";
    db_write("users", safe);
    """

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    # Run static analysis
    static_result = analyze_program_taint(program)

    # Compile to bytecode
    compiler = BytecodeCompiler(static_result)
    bytecode = compiler.compile(program)

    print(f"Static safe sites: {len(bytecode.static_safe_sites)}")
    print(f"Dynamic sites: {len(bytecode.dynamic_sites)}")

    # Execute
    vm = BytecodeInterpreter()
    vm.execute(bytecode)

    print("Test passed!")


if __name__ == "__main__":
    print("Test 1: Simple arithmetic")
    test_simple_arithmetic()
    print()

    print("Test 2: Safe sink")
    test_safe_sink()
