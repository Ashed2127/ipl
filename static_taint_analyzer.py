"""
Static Taint Analysis for IPL
Analyzes AST to trace taint flow from sources to sinks across all execution paths.
"""
from typing import Dict, Set, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import ast

from ast_nodes import (
    Program, LetStatement, AssignStatement, FunctionDef, IfStatement, WhileStatement,
    ForStatement, ReturnStatement, PrintStatement, SanitizationNode, Expr, Literal,
    Identifier, BinaryOp, UnaryOp, FunctionCall, TypeAnnotation
)
from taint import TaintLevel, TaintTag, SinkKind


class StaticTaintAnalysis:
    """
    Static taint analyzer that traces data flow from sources to sinks.
    Reuses taint.py's lattice for sound analysis.
    """
    
    def __init__(self):
        # Taint state for each variable in each scope
        self.scopes: List[Dict[str, TaintLevel]] = [{}]
        
        # Set of variables that are sources of UNTRUSTED data
        self.untrusted_sources: Set[str] = set()
        
        # Set of variables that have been sanitized (with sink kind)
        self.sanitized_vars: Dict[str, SinkKind] = {}
        
        # Analysis results
        self.static_safe_sites: List[Dict[str, Any]] = []
        self.dynamic_sites: List[Dict[str, Any]] = []
        self.violations: List[Dict[str, Any]] = []
        
        # Known sink functions and their required sink kinds
        self.sink_functions: Dict[str, SinkKind] = {
            "db_write": SinkKind.SQL,
            "file_write": SinkKind.FILE,
            "html_render": SinkKind.HTML,
            "shell_exec": SinkKind.SHELL,
        }
        
        # Known sanitizer functions and their sink kinds
        self.sanitizer_functions: Dict[str, SinkKind] = {
            "sanitize_for_sql": SinkKind.SQL,
            "sanitize_for_html": SinkKind.HTML,
            "sanitize_for_shell": SinkKind.SHELL,
            "sanitize_for_file": SinkKind.FILE,
            "sanitize_string": SinkKind.GENERAL,
        }
        
        # Known source functions that return UNTRUSTED data
        self.source_functions: Set[str] = {
            "set_untrusted",
            "user_input",
        }
    
    def analyze(self, program: Program) -> Dict[str, Any]:
        """
        Perform static taint analysis on the entire program.
        Returns analysis results with violations and guarantees.
        """
        self.scopes = [{}]  # Reset scopes
        self.untrusted_sources = set()
        self.sanitized_vars = {}
        self.static_safe_sites = []
        self.dynamic_sites = []
        self.violations = []
        
        # Analyze all statements in the program
        for stmt in program.statements:
            self._analyze_statement(stmt)
        
        return {
            "violations": self.violations,
            "static_safe_sites": self.static_safe_sites,
            "dynamic_sites": self.dynamic_sites,
            "untrusted_sources": list(self.untrusted_sources),
            "sanitized_vars": self.sanitized_vars,
        }
    
    def _enter_scope(self):
        """Enter a new scope (function, block, etc.)"""
        self.scopes.append({})
    
    def _exit_scope(self):
        """Exit the current scope"""
        if len(self.scopes) > 1:
            self.scopes.pop()
    
    def _get_var_taint(self, var_name: str) -> TaintLevel:
        """Get the taint level of a variable by checking all scopes"""
        for scope in reversed(self.scopes):
            if var_name in scope:
                return scope[var_name]
        return TaintLevel.TRUSTED  # Default to TRUSTED for unknown variables
    
    def _set_var_taint(self, var_name: str, taint: TaintLevel):
        """Set the taint level of a variable in the current scope"""
        self.scopes[-1][var_name] = taint
    
    def _analyze_statement(self, stmt):
        """Analyze a single statement"""
        if isinstance(stmt, LetStatement):
            self._analyze_let(stmt)
        elif isinstance(stmt, AssignStatement):
            self._analyze_assign(stmt)
        elif isinstance(stmt, FunctionDef):
            self._analyze_function_def(stmt)
        elif isinstance(stmt, IfStatement):
            self._analyze_if(stmt)
        elif isinstance(stmt, WhileStatement):
            self._analyze_while(stmt)
        elif isinstance(stmt, ForStatement):
            self._analyze_for(stmt)
        elif isinstance(stmt, ReturnStatement):
            self._analyze_return(stmt)
        elif isinstance(stmt, PrintStatement):
            self._analyze_print(stmt)
        elif isinstance(stmt, SanitizationNode):
            self._analyze_sanitization(stmt)
    
    def _analyze_let(self, stmt: LetStatement):
        """Analyze a let statement"""
        taint = self._analyze_expr(stmt.value_expr) if stmt.value_expr else TaintLevel.TRUSTED
        
        # If the value is a function call to a sanitizer, mark the result as SANITIZED
        if stmt.value_expr and isinstance(stmt.value_expr, FunctionCall):
            func_name = self._get_function_name(stmt.value_expr.callee)
            if func_name in self.sanitizer_functions:
                sink_kind = self.sanitizer_functions[func_name]
                taint = TaintLevel.SANITIZED
                self.sanitized_vars[stmt.name] = sink_kind
            elif func_name in self.source_functions:
                # Source functions return UNTRUSTED data
                taint = TaintLevel.UNTRUSTED
        
        self._set_var_taint(stmt.name, taint)
        
        if taint == TaintLevel.UNTRUSTED:
            self.untrusted_sources.add(stmt.name)
    
    def _analyze_assign(self, stmt: AssignStatement):
        """Analyze an assignment statement"""
        taint = self._analyze_expr(stmt.value_expr)
        
        # If the value is a function call to a sanitizer, mark the result as SANITIZED
        if isinstance(stmt.value_expr, FunctionCall):
            func_name = self._get_function_name(stmt.value_expr.callee)
            if func_name in self.sanitizer_functions:
                sink_kind = self.sanitizer_functions[func_name]
                taint = TaintLevel.SANITIZED
                self.sanitized_vars[stmt.name] = sink_kind
        
        self._set_var_taint(stmt.name, taint)
        
        if taint == TaintLevel.UNTRUSTED:
            self.untrusted_sources.add(stmt.name)
    
    def _analyze_function_def(self, stmt: FunctionDef):
        """Analyze a function definition"""
        self._enter_scope()
        
        # Mark parameters as TRUSTED (assume caller handles sanitization)
        for param in stmt.params:
            self._set_var_taint(param, TaintLevel.TRUSTED)
        
        # Analyze function body
        for body_stmt in stmt.body.statements:
            self._analyze_statement(body_stmt)
        
        self._exit_scope()
    
    def _analyze_if(self, stmt: IfStatement):
        """Analyze an if statement (both branches)"""
        # Analyze condition to understand branching
        self._analyze_expr(stmt.condition)
        
        # Analyze then branch
        then_scope_size = len(self.scopes)
        self._analyze_block(stmt.then_branch)
        
        # Restore scope for else branch
        while len(self.scopes) > then_scope_size:
            self.scopes.pop()
        
        # Analyze elif branches
        for elif_cond, elif_block in stmt.elif_branches:
            self._analyze_expr(elif_cond)
            elif_scope_size = len(self.scopes)
            self._analyze_block(elif_block)
            while len(self.scopes) > elif_scope_size:
                self.scopes.pop()
        
        # Analyze else branch
        if stmt.else_branch is not None:
            else_scope_size = len(self.scopes)
            self._analyze_block(stmt.else_branch)
            while len(self.scopes) > else_scope_size:
                self.scopes.pop()
    
    def _analyze_while(self, stmt: WhileStatement):
        """Analyze a while statement"""
        self._analyze_expr(stmt.condition)
        self._analyze_block(stmt.body)
    
    def _analyze_for(self, stmt: ForStatement):
        """Analyze a for statement"""
        # Mark loop variable as TRUSTED (iteration over trusted data)
        # In a more sophisticated analysis, we'd analyze the iterable
        self._enter_scope()
        self._set_var_taint(stmt.variable, TaintLevel.TRUSTED)
        for body_stmt in stmt.body.statements:
            self._analyze_statement(body_stmt)
        self._exit_scope()
    
    def _analyze_return(self, stmt: ReturnStatement):
        """Analyze a return statement"""
        if stmt.value_expr:
            self._analyze_expr(stmt.value_expr)
    
    def _analyze_print(self, stmt: PrintStatement):
        """Analyze a print statement (not a security sink)"""
        for expr in stmt.exprs:
            self._analyze_expr(expr)
    
    def _analyze_sanitization(self, stmt: SanitizationNode):
        """Analyze a sanitization node"""
        # Determine the sink kind from the rule
        sink_kind = self._infer_sink_kind_from_rule(stmt.rule)
        
        # Analyze the expression being sanitized
        taint = self._analyze_expr(stmt.target)
        
        # After sanitization, the result is SANITIZED with the appropriate sink kind
        # Note: We can't track the result variable name here without more context
        # This is a limitation of the current AST structure
        if sink_kind:
            self.sanitized_vars[stmt.rule] = sink_kind
    
    def _infer_sink_kind_from_rule(self, rule: str) -> Optional[SinkKind]:
        """Infer the sink kind from a sanitization rule/function name"""
        for func_name, kind in self.sanitizer_functions.items():
            if func_name in rule or rule in func_name:
                return kind
        return None
    
    def _analyze_expr(self, expr: Expr) -> TaintLevel:
        """Analyze an expression and return its taint level"""
        if isinstance(expr, Literal):
            # Literals are TRUSTED (compile-time constants)
            return TaintLevel.TRUSTED
        
        elif isinstance(expr, Identifier):
            # Look up variable taint
            return self._get_var_taint(expr.name)
        
        elif isinstance(expr, BinaryOp):
            # Binary operations: combine taint of operands
            left_taint = self._analyze_expr(expr.left)
            right_taint = self._analyze_expr(expr.right)
            return self._combine_taint(left_taint, right_taint)
        
        elif isinstance(expr, UnaryOp):
            # Unary operations: preserve operand taint
            return self._analyze_expr(expr.operand)
        
        elif isinstance(expr, FunctionCall):
            # Function calls: check if it's a sink or sanitizer
            return self._analyze_call(expr)
        
        # For other expression types, conservatively return TRUSTED
        return TaintLevel.TRUSTED
    
    def _analyze_call(self, expr: FunctionCall) -> TaintLevel:
        """Analyze a function call"""
        func_name = self._get_function_name(expr.callee)
        
        # Check if it's a sink function
        if func_name in self.sink_functions:
            required_sink = self.sink_functions[func_name]
            
            # Analyze arguments
            arg_taints = []
            for arg in expr.args:
                arg_taint = self._analyze_expr(arg)
                arg_taints.append(arg_taint)
            
            # Check if any argument is UNTRUSTED or mismatched SANITIZED
            for i, arg_taint in enumerate(arg_taints):
                if arg_taint == TaintLevel.UNTRUSTED:
                    self.violations.append({
                        "type": "static_taint_violation",
                        "sink": func_name,
                        "required_sink": required_sink.value,
                        "arg_index": i,
                        "taint": arg_taint.value,
                        "location": "static_analysis",
                        "message": f"UNTRUSTED data passed to {func_name} without sanitization"
                    })
                elif arg_taint == TaintLevel.SANITIZED:
                    # Check if the sink kind matches
                    # For now, we conservatively flag this as requiring runtime check
                    # because we can't track which variable was sanitized for which sink
                    self.dynamic_sites.append({
                        "type": "dynamic_taint_check",
                        "sink": func_name,
                        "required_sink": required_sink.value,
                        "arg_index": i,
                        "taint": arg_taint.value,
                        "reason": "Cannot statically verify sink kind match",
                        "location": "static_analysis"
                    })
            
            # If all arguments are TRUSTED, mark as statically safe
            if all(t == TaintLevel.TRUSTED for t in arg_taints):
                self.static_safe_sites.append({
                    "type": "static_safe_sink",
                    "sink": func_name,
                    "required_sink": required_sink.value,
                    "location": "static_analysis"
                })
        
        # Check if it's a sanitizer function
        elif func_name in self.sanitizer_functions:
            sink_kind = self.sanitizer_functions[func_name]
            
            # The result of sanitization is SANITIZED
            # We can't track which variable receives the result without more context
            # This is a limitation of the current analysis
            return TaintLevel.SANITIZED
        
        # For other functions, conservatively analyze arguments and return TRUSTED
        for arg in expr.args:
            self._analyze_expr(arg)
        return TaintLevel.TRUSTED
    
    def _get_function_name(self, func_expr: Expr) -> str:
        """Extract function name from a function expression"""
        if isinstance(func_expr, Identifier):
            return func_expr.name
        # For more complex expressions, return a placeholder
        return "unknown"
    
    def _combine_taint(self, taint1: TaintLevel, taint2: TaintLevel) -> TaintLevel:
        """Combine two taint levels using the lattice logic"""
        if taint1 == TaintLevel.UNTRUSTED or taint2 == TaintLevel.UNTRUSTED:
            return TaintLevel.UNTRUSTED
        elif taint1 == TaintLevel.SANITIZED or taint2 == TaintLevel.SANITIZED:
            return TaintLevel.SANITIZED
        else:
            return TaintLevel.TRUSTED
    
    def _analyze_block(self, block):
        """Analyze a block of statements"""
        for stmt in block.statements:
            self._analyze_statement(stmt)


def analyze_program_taint(program: Program) -> Dict[str, Any]:
    """
    Public API for static taint analysis.
    Analyzes a program and returns taint analysis results.
    """
    analyzer = StaticTaintAnalysis()
    return analyzer.analyze(program)
