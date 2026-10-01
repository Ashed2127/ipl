"""
Bytecode VM for IPL with proof-skip optimization.
Uses stack-based instruction set with slot-indexed variable access.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Tuple
from enum import Enum
import time


class OpCode(Enum):
    """Bytecode opcodes for IPL VM"""
    # Stack operations
    PUSH_CONST = 0        # Push constant onto stack
    LOAD_VAR = 1          # Load variable from slot
    STORE_VAR = 2         # Store to variable slot
    POP = 3               # Pop from stack
    DUP = 4               # Duplicate top of stack

    # Binary operations
    ADD = 10
    SUB = 11
    MUL = 12
    DIV = 13
    MOD = 14
    EQ = 15
    NEQ = 16
    LT = 17
    LTE = 18
    GT = 19
    GTE = 20
    AND = 21
    OR = 22

    # Unary operations
    NEG = 30
    NOT = 31

    # Control flow
    JMP = 40              # Unconditional jump
    JZ = 41               # Jump if zero (false)
    JNZ = 42              # Jump if non-zero (true)
    CALL = 43             # Function call
    RET = 44              # Return from function

    # Built-in functions
    BUILTIN_LEN = 50
    BUILTIN_RANGE = 51
    BUILTIN_PRINT = 52

    # Sink functions (with and without taint check)
    DB_WRITE = 60
    DB_WRITE_SAFE = 61    # Skip taint check (statically proven safe)
    FILE_WRITE = 62
    FILE_WRITE_SAFE = 63
    HTML_RENDER = 64
    HTML_RENDER_SAFE = 65
    SHELL_EXEC = 66
    SHELL_EXEC_SAFE = 67

    # Sanitization functions
    SANITIZE_FOR_SQL = 70
    SANITIZE_FOR_HTML = 71
    SANITIZE_FOR_SHELL = 72
    SANITIZE_FOR_FILE = 73
    SANITIZE_STRING = 74

    # Source functions
    SET_UNTRUSTED = 80
    USER_INPUT = 81

    # Taint check (for dynamic_sites)
    CHECK_TAINT = 90     # Check taint against required sink kind

    # Special
    HALT = 255


@dataclass
class Instruction:
    """Single bytecode instruction"""
    opcode: OpCode
    operand: Any = None
    line: int = 0


@dataclass
class FunctionInfo:
    """Information about a compiled function"""
    name: str
    param_slots: List[int]  # Slot indices for parameters
    local_slots: Dict[str, int]  # Variable name -> slot index
    instructions: List[Instruction]
    start_addr: int = 0


@dataclass
class BytecodeProgram:
    """Compiled bytecode program"""
    instructions: List[Instruction] = field(default_factory=list)
    functions: Dict[str, FunctionInfo] = field(default_factory=dict)
    global_slots: Dict[str, int] = field(default_factory=dict)
    static_safe_sites: Set[Tuple[str, int]] = field(default_factory=set)  # (sink_name, instruction_index)
    dynamic_sites: Set[Tuple[str, int]] = field(default_factory=set)  # (sink_name, instruction_index)


class BytecodeCompiler:
    """
    Compiles IPL AST to bytecode with slot-indexed variable access.
    Consults static_taint_analyzer to skip taint checks on static_safe_sites.
    """

    def __init__(self, static_analysis_result: Optional[Dict[str, Any]] = None):
        self.static_analysis = static_analysis_result
        self.program = BytecodeProgram()
        self.current_func: Optional[str] = None
        self.slot_counter = 0
        self.local_slots: Dict[str, int] = {}
        self.instruction_index = 0

    def compile(self, ast_program) -> BytecodeProgram:
        """Compile an AST program to bytecode"""
        from ast_nodes import Program

        if not isinstance(ast_program, Program):
            raise TypeError("Expected Program AST node")

        # First pass: collect all function definitions
        self._collect_functions(ast_program)

        # Second pass: compile main program
        for stmt in ast_program.statements:
            self._compile_statement(stmt)

        # Add HALT at end
        self._emit(OpCode.HALT)

        return self.program

    def _collect_functions(self, program):
        """First pass: collect function signatures"""
        from ast_nodes import FunctionDef

        for stmt in program.statements:
            if isinstance(stmt, FunctionDef):
                # Reset slot counter for this function
                self.slot_counter = 0
                self.local_slots = {}

                # Allocate slots for parameters
                param_slots = []
                for param in stmt.params:
                    slot = self._allocate_slot(param)
                    param_slots.append(slot)

                # Create function info (body will be compiled later)
                func_info = FunctionInfo(
                    name=stmt.name,
                    param_slots=param_slots,
                    local_slots=dict(self.local_slots),
                    instructions=[],
                    start_addr=len(self.program.instructions)
                )
                self.program.functions[stmt.name] = func_info

    def _allocate_slot(self, name: str) -> int:
        """Allocate a slot index for a variable"""
        if name in self.local_slots:
            return self.local_slots[name]
        slot = self.slot_counter
        self.local_slots[name] = slot
        self.slot_counter += 1
        return slot

    def _emit(self, opcode: OpCode, operand: Any = None, line: int = 0) -> int:
        """Emit an instruction and return its index"""
        instr = Instruction(opcode, operand, line)
        self.program.instructions.append(instr)
        idx = self.instruction_index
        self.instruction_index += 1
        return idx

    def _compile_statement(self, stmt):
        """Compile a statement"""
        from ast_nodes import (
            LetStatement, AssignStatement, FunctionDef, IfStatement,
            WhileStatement, ForStatement, ReturnStatement, PrintStatement,
            FunctionCall
        )

        if isinstance(stmt, LetStatement):
            self._compile_let(stmt)
        elif isinstance(stmt, AssignStatement):
            self._compile_assign(stmt)
        elif isinstance(stmt, FunctionDef):
            self._compile_function_def(stmt)
        elif isinstance(stmt, IfStatement):
            self._compile_if(stmt)
        elif isinstance(stmt, WhileStatement):
            self._compile_while(stmt)
        elif isinstance(stmt, ForStatement):
            self._compile_for(stmt)
        elif isinstance(stmt, ReturnStatement):
            self._compile_return(stmt)
        elif isinstance(stmt, PrintStatement):
            self._compile_print(stmt)
        elif isinstance(stmt, FunctionCall):
            self._compile_function_call(stmt)

    def _compile_let(self, stmt):
        """Compile a let statement"""
        from ast_nodes import Identifier, FunctionCall

        slot = self._allocate_slot(stmt.name)

        if stmt.value_expr:
            self._compile_expr(stmt.value_expr)
            self._emit(OpCode.STORE_VAR, slot, stmt.line)

            # Track if this is a source function
            if isinstance(stmt.value_expr, FunctionCall):
                func_name = self._get_function_name(stmt.value_expr.callee)
                if func_name in ["set_untrusted", "user_input"]:
                    # Replace with source instruction
                    self.program.instructions[-1] = Instruction(
                        OpCode.SET_UNTRUSTED if func_name == "set_untrusted" else OpCode.USER_INPUT,
                        slot, stmt.line
                    )

    def _compile_assign(self, stmt):
        """Compile an assignment statement"""
        slot = self._get_slot(stmt.name)
        self._compile_expr(stmt.value_expr)
        self._emit(OpCode.STORE_VAR, slot, stmt.line)

    def _compile_function_def(self, stmt):
        """Compile a function definition"""
        # Restore function's local slots
        if stmt.name in self.program.functions:
            func_info = self.program.functions[stmt.name]
            old_slots = self.local_slots
            old_counter = self.slot_counter
            self.local_slots = dict(func_info.local_slots)
            self.slot_counter = len(self.local_slots)

            # Set current function context
            old_func = self.current_func
            self.current_func = stmt.name

            # Compile body
            for body_stmt in stmt.body.statements:
                self._compile_statement(body_stmt)

            # Add return
            self._emit(OpCode.RET)

            # Restore context
            self.local_slots = old_slots
            self.slot_counter = old_counter
            self.current_func = old_func

    def _compile_if(self, stmt):
        """Compile an if statement"""
        # Compile condition
        self._compile_expr(stmt.condition)

        # Jump to else if false
        jz_idx = self._emit(OpCode.JZ)

        # Compile then branch
        for then_stmt in stmt.then_branch.statements:
            self._compile_statement(then_stmt)

        # Jump to end if else exists
        if stmt.else_branch:
            jmp_idx = self._emit(OpCode.JMP)

        # Patch JZ target
        self.program.instructions[jz_idx].operand = self.instruction_index

        # Compile else branch
        if stmt.else_branch:
            for else_stmt in stmt.else_branch.statements:
                self._compile_statement(else_stmt)

            # Patch JMP target
            self.program.instructions[jmp_idx].operand = self.instruction_index

    def _compile_while(self, stmt):
        """Compile a while statement"""
        loop_start = self.instruction_index

        # Compile condition
        self._compile_expr(stmt.condition)

        # Jump to end if false
        jz_idx = self._emit(OpCode.JZ)

        # Compile body
        for body_stmt in stmt.body.statements:
            self._compile_statement(body_stmt)

        # Jump back to condition
        self._emit(OpCode.JMP, loop_start)

        # Patch JZ target
        self.program.instructions[jz_idx].operand = self.instruction_index

    def _compile_for(self, stmt):
        """Compile a for statement"""
        # For simplicity, translate to while loop
        # In a full implementation, we'd need iterator support
        from ast_nodes import Identifier

        # Allocate slot for loop variable
        var_slot = self._allocate_slot(stmt.variable)

        # Load iterable (simplified - assume it's a list)
        self._compile_expr(stmt.iterable)
        iterable_slot = self._allocate_slot(f"__iter_{stmt.variable}")
        self._emit(OpCode.STORE_VAR, iterable_slot)

        # Simplified: just compile body once (real for needs iterator protocol)
        for body_stmt in stmt.body.statements:
            self._compile_statement(body_stmt)

    def _compile_return(self, stmt):
        """Compile a return statement"""
        if stmt.value_expr:
            self._compile_expr(stmt.value_expr)
        self._emit(OpCode.RET)

    def _compile_print(self, stmt):
        """Compile a print statement"""
        for expr in stmt.exprs:
            self._compile_expr(expr)
        self._emit(OpCode.BUILTIN_PRINT, len(stmt.exprs))

    def _compile_function_call(self, stmt):
        """Compile a function call as a statement"""
        self._compile_expr(stmt)

    def _compile_expr(self, expr):
        """Compile an expression"""
        from ast_nodes import (
            Literal, Identifier, BinaryOp, UnaryOp, FunctionCall
        )

        if isinstance(expr, Literal):
            line = getattr(expr, 'line', 0)
            self._emit(OpCode.PUSH_CONST, expr.value, line)

        elif isinstance(expr, Identifier):
            line = getattr(expr, 'line', 0)
            slot = self._get_slot(expr.name)
            self._emit(OpCode.LOAD_VAR, slot, line)

        elif isinstance(expr, BinaryOp):
            self._compile_expr(expr.left)
            self._compile_expr(expr.right)
            op_map = {
                '+': OpCode.ADD, '-': OpCode.SUB, '*': OpCode.MUL, '/': OpCode.DIV,
                '%': OpCode.MOD, '==': OpCode.EQ, '!=': OpCode.NEQ,
                '<': OpCode.LT, '<=': OpCode.LTE, '>': OpCode.GT, '>=': OpCode.GTE,
                'and': OpCode.AND, 'or': OpCode.OR
            }
            opcode = op_map.get(expr.op, OpCode.ADD)
            line = getattr(expr, 'line', 0)
            self._emit(opcode, line=line)

        elif isinstance(expr, UnaryOp):
            self._compile_expr(expr.operand)
            line = getattr(expr, 'line', 0)
            if expr.op == '-':
                self._emit(OpCode.NEG, line=line)
            elif expr.op == 'not':
                self._emit(OpCode.NOT, line=line)

        elif isinstance(expr, FunctionCall):
            self._compile_function_call_expr(expr)

    def _compile_function_call_expr(self, expr):
        """Compile a function call expression"""
        func_name = self._get_function_name(expr.callee)

        # Compile arguments (push in reverse order for stack)
        for arg in reversed(expr.args):
            self._compile_expr(arg)

        # Check if it's a sink function
        sink_opcodes = {
            'db_write': (OpCode.DB_WRITE, OpCode.DB_WRITE_SAFE),
            'file_write': (OpCode.FILE_WRITE, OpCode.FILE_WRITE_SAFE),
            'html_render': (OpCode.HTML_RENDER, OpCode.HTML_RENDER_SAFE),
            'shell_exec': (OpCode.SHELL_EXEC, OpCode.SHELL_EXEC_SAFE),
        }

        if func_name in sink_opcodes:
            normal_op, safe_op = sink_opcodes[func_name]

            # Check if this call site is statically safe
            is_static_safe = self._is_static_safe_site(func_name, self.instruction_index)

            if is_static_safe:
                opcode = safe_op
                self.program.static_safe_sites.add((func_name, self.instruction_index))
            else:
                opcode = normal_op
                self.program.dynamic_sites.add((func_name, self.instruction_index))

            self._emit(opcode, len(expr.args))

        # Check sanitization functions
        elif func_name == 'sanitize_for_sql':
            self._emit(OpCode.SANITIZE_FOR_SQL)
        elif func_name == 'sanitize_for_html':
            self._emit(OpCode.SANITIZE_FOR_HTML)
        elif func_name == 'sanitize_for_shell':
            self._emit(OpCode.SANITIZE_FOR_SHELL)
        elif func_name == 'sanitize_for_file':
            self._emit(OpCode.SANITIZE_FOR_FILE)
        elif func_name == 'sanitize_string':
            self._emit(OpCode.SANITIZE_STRING)

        # Check source functions
        elif func_name == 'set_untrusted':
            self._emit(OpCode.SET_UNTRUSTED)
        elif func_name == 'user_input':
            self._emit(OpCode.USER_INPUT)

        # Check built-ins
        elif func_name == 'len':
            self._emit(OpCode.BUILTIN_LEN)
        elif func_name == 'range':
            self._emit(OpCode.BUILTIN_RANGE)

        # User-defined function
        elif func_name in self.program.functions:
            self._emit(OpCode.CALL, func_name)

        # Unknown function - defer to runtime
        else:
            self._emit(OpCode.CALL, func_name)

    def _get_function_name(self, callee) -> str:
        """Extract function name from callee expression"""
        from ast_nodes import Identifier
        if isinstance(callee, Identifier):
            return callee.name
        return "unknown"

    def _get_slot(self, name: str) -> int:
        """Get slot index for a variable"""
        if name in self.local_slots:
            return self.local_slots[name]
        # Allocate new slot
        return self._allocate_slot(name)

    def _is_static_safe_site(self, sink_name: str, instruction_index: int) -> bool:
        """
        Check if a sink call site is statically safe according to static analysis.
        Returns True if we can skip the runtime taint check.
        """
        if not self.static_analysis:
            return False

        # Check if this sink call is in static_safe_sites
        for site in self.static_analysis.get('static_safe_sites', []):
            if site.get('sink') == sink_name:
                # For simplicity, assume all static_safe_sites for this sink are safe
                # In a real implementation, we'd need to track which specific call site
                return True

        return False


class BytecodeInterpreter:
    """
    Stack-based bytecode interpreter for IPL.
    Executes compiled bytecode with slot-indexed variable access.
    """

    def __init__(self, console=None):
        self.console = console
        self.stack: List[Any] = []
        self.locals: List[Any] = []  # Slot-indexed local variables
        self.program: Optional[BytecodeProgram] = None
        self.pc: int = 0  # Program counter
        self.running: bool = False
        self.taint_tags: List[Any] = []  # Parallel to stack for taint tracking

    def execute(self, program: BytecodeProgram) -> Any:
        """Execute a bytecode program"""
        self.program = program
        self.stack = []
        self.locals = [None] * (max(program.global_slots.values(), default=0) + 1)
        self.taint_tags = []
        self.pc = 0
        self.running = True

        from taint import TaintTag, TaintLevel

        while self.running and self.pc < len(self.program.instructions):
            instr = self.program.instructions[self.pc]
            self.pc += 1

            try:
                self._execute_instruction(instr)
            except Exception as e:
                print(f"Runtime error at instruction {self.pc - 1}: {e}")
                raise

        return self.stack[-1] if self.stack else None

    def _execute_instruction(self, instr: Instruction):
        """Execute a single instruction"""
        from taint import TaintTag, TaintLevel, SinkKind, TaintViolationError

        opcode = instr.opcode

        # Stack operations
        if opcode == OpCode.PUSH_CONST:
            self.stack.append(instr.operand)
            self.taint_tags.append(TaintTag(level=TaintLevel.TRUSTED, provenance="constant"))

        elif opcode == OpCode.LOAD_VAR:
            slot = instr.operand
            value = self.locals[slot] if slot < len(self.locals) else None
            self.stack.append(value)
            # Preserve taint from slot (simplified - would need separate taint array)
            self.taint_tags.append(TaintTag(level=TaintLevel.TRUSTED, provenance="variable"))

        elif opcode == OpCode.STORE_VAR:
            slot = instr.operand
            value = self.stack.pop()
            taint = self.taint_tags.pop()
            # Ensure locals array is large enough
            while len(self.locals) <= slot:
                self.locals.append(None)
            self.locals[slot] = value

        elif opcode == OpCode.POP:
            self.stack.pop()
            self.taint_tags.pop()

        elif opcode == OpCode.DUP:
            self.stack.append(self.stack[-1])
            self.taint_tags.append(self.taint_tags[-1])

        # Binary operations
        elif opcode in (OpCode.ADD, OpCode.SUB, OpCode.MUL, OpCode.DIV, OpCode.MOD):
            right = self.stack.pop()
            left = self.stack.pop()
            right_taint = self.taint_tags.pop()
            left_taint = self.taint_tags.pop()

            if opcode == OpCode.ADD:
                result = left + right
            elif opcode == OpCode.SUB:
                result = left - right
            elif opcode == OpCode.MUL:
                result = left * right
            elif opcode == OpCode.DIV:
                result = left / right
            elif opcode == OpCode.MOD:
                result = left % right

            self.stack.append(result)
            # Combine taints
            combined_taint = TaintTag.combine(left_taint, right_taint, "binary_op")
            self.taint_tags.append(combined_taint)

        elif opcode in (OpCode.EQ, OpCode.NEQ, OpCode.LT, OpCode.LTE, OpCode.GT, OpCode.GTE):
            right = self.stack.pop()
            left = self.stack.pop()
            right_taint = self.taint_tags.pop()
            left_taint = self.taint_tags.pop()

            if opcode == OpCode.EQ:
                result = left == right
            elif opcode == OpCode.NEQ:
                result = left != right
            elif opcode == OpCode.LT:
                result = left < right
            elif opcode == OpCode.LTE:
                result = left <= right
            elif opcode == OpCode.GT:
                result = left > right
            elif opcode == OpCode.GTE:
                result = left >= right

            self.stack.append(result)
            self.taint_tags.append(TaintTag(level=TaintLevel.TRUSTED, provenance="comparison"))

        elif opcode == OpCode.AND:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left and right)
            self.taint_tags.append(TaintTag(level=TaintLevel.TRUSTED, provenance="and"))

        elif opcode == OpCode.OR:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left or right)
            self.taint_tags.append(TaintTag(level=TaintLevel.TRUSTED, provenance="or"))

        # Unary operations
        elif opcode == OpCode.NEG:
            value = self.stack.pop()
            self.stack.append(-value)

        elif opcode == OpCode.NOT:
            value = self.stack.pop()
            self.stack.append(not value)

        # Control flow
        elif opcode == OpCode.JMP:
            self.pc = instr.operand

        elif opcode == OpCode.JZ:
            if not self.stack.pop():
                self.pc = instr.operand

        elif opcode == OpCode.JNZ:
            if self.stack.pop():
                self.pc = instr.operand

        elif opcode == OpCode.CALL:
            # Simplified: just push a placeholder
            self.stack.append(f"<call {instr.operand}>")

        elif opcode == OpCode.RET:
            # Return from function (simplified)
            pass

        # Built-in functions
        elif opcode == OpCode.BUILTIN_PRINT:
            arg_count = instr.operand
            args = [self.stack.pop() for _ in range(arg_count)]
            args.reverse()
            print(*args)

        # Sink functions (with taint check)
        elif opcode == OpCode.DB_WRITE:
            table = self.stack.pop()
            record = self.stack.pop()
            record_taint = self.taint_tags.pop()

            if not record_taint.is_safe_for_sink(SinkKind.SQL):
                raise TaintViolationError(
                    variable_name=str(record),
                    sink_name=f"db_write('{table}')",
                    taint_level=record_taint.level
                )
            print(f"[DB_WRITE] Committed to table '{table}'")

        elif opcode == OpCode.DB_WRITE_SAFE:
            # Skip taint check (statically proven safe)
            table = self.stack.pop()
            record = self.stack.pop()
            self.taint_tags.pop()
            print(f"[DB_WRITE_SAFE] Committed to table '{table}' (statically safe)")

        elif opcode == OpCode.FILE_WRITE:
            path = self.stack.pop()
            data = self.stack.pop()
            data_taint = self.taint_tags.pop()

            if not data_taint.is_safe_for_sink(SinkKind.FILE):
                raise TaintViolationError(
                    variable_name=str(data),
                    sink_name=f"file_write('{path}')",
                    taint_level=data_taint.level
                )
            print(f"[FILE_WRITE] Wrote to '{path}'")

        elif opcode == OpCode.FILE_WRITE_SAFE:
            path = self.stack.pop()
            data = self.stack.pop()
            self.taint_tags.pop()
            print(f"[FILE_WRITE_SAFE] Wrote to '{path}' (statically safe)")

        elif opcode == OpCode.HTML_RENDER:
            html = self.stack.pop()
            html_taint = self.taint_tags.pop()

            if not html_taint.is_safe_for_sink(SinkKind.HTML):
                raise TaintViolationError(
                    variable_name=str(html),
                    sink_name="html_render",
                    taint_level=html_taint.level
                )
            print(f"[HTML_RENDER] Rendered HTML")

        elif opcode == OpCode.HTML_RENDER_SAFE:
            html = self.stack.pop()
            self.taint_tags.pop()
            print(f"[HTML_RENDER_SAFE] Rendered HTML (statically safe)")

        elif opcode == OpCode.SHELL_EXEC:
            cmd = self.stack.pop()
            cmd_taint = self.taint_tags.pop()

            if not cmd_taint.is_safe_for_sink(SinkKind.SHELL):
                raise TaintViolationError(
                    variable_name=str(cmd),
                    sink_name="shell_exec",
                    taint_level=cmd_taint.level
                )
            print(f"[SHELL_EXEC] Executed shell command")

        elif opcode == OpCode.SHELL_EXEC_SAFE:
            cmd = self.stack.pop()
            self.taint_tags.pop()
            print(f"[SHELL_EXEC_SAFE] Executed shell command (statically safe)")

        # Sanitization functions
        elif opcode == OpCode.SANITIZE_FOR_SQL:
            value = self.stack.pop()
            taint = self.taint_tags.pop()
            from security_engine import SecurityEngine
            sanitized = SecurityEngine.sanitize_for_sql(str(value))
            new_taint = taint.transition_to(TaintLevel.SANITIZED, "sanitize_for_sql", SinkKind.SQL)
            self.stack.append(sanitized)
            self.taint_tags.append(new_taint)

        elif opcode == OpCode.SANITIZE_FOR_HTML:
            value = self.stack.pop()
            taint = self.taint_tags.pop()
            from security_engine import SecurityEngine
            sanitized = SecurityEngine.sanitize_for_html(str(value))
            new_taint = taint.transition_to(TaintLevel.SANITIZED, "sanitize_for_html", SinkKind.HTML)
            self.stack.append(sanitized)
            self.taint_tags.append(new_taint)

        elif opcode == OpCode.SANITIZE_FOR_SHELL:
            value = self.stack.pop()
            taint = self.taint_tags.pop()
            from security_engine import SecurityEngine
            sanitized = SecurityEngine.sanitize_for_shell(str(value))
            new_taint = taint.transition_to(TaintLevel.SANITIZED, "sanitize_for_shell", SinkKind.SHELL)
            self.stack.append(sanitized)
            self.taint_tags.append(new_taint)

        elif opcode == OpCode.SANITIZE_FOR_FILE:
            value = self.stack.pop()
            taint = self.taint_tags.pop()
            from security_engine import SecurityEngine
            sanitized = SecurityEngine.sanitize_for_file(str(value))
            new_taint = taint.transition_to(TaintLevel.SANITIZED, "sanitize_for_file", SinkKind.FILE)
            self.stack.append(sanitized)
            self.taint_tags.append(new_taint)

        elif opcode == OpCode.SANITIZE_STRING:
            value = self.stack.pop()
            taint = self.taint_tags.pop()
            from security_engine import SecurityEngine
            sanitized = SecurityEngine.sanitize_string(str(value))
            new_taint = taint.transition_to(TaintLevel.SANITIZED, "sanitize_string", SinkKind.GENERAL)
            self.stack.append(sanitized)
            self.taint_tags.append(new_taint)

        # Source functions
        elif opcode == OpCode.SET_UNTRUSTED:
            value = self.stack.pop()
            self.stack.append(value)
            self.taint_tags.append(TaintTag(level=TaintLevel.UNTRUSTED, provenance="set_untrusted"))

        elif opcode == OpCode.USER_INPUT:
            self.stack.append("<user_input>")
            self.taint_tags.append(TaintTag(level=TaintLevel.UNTRUSTED, provenance="user_input"))

        # Special
        elif opcode == OpCode.HALT:
            self.running = False

        else:
            raise ValueError(f"Unknown opcode: {opcode}")
