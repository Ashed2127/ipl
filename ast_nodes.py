"""
Abstract Syntax Tree (AST) definitions for IPL (Intelligent Programming Language / Aether).
"""
from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict, Tuple


class ASTNode:
    pass


@dataclass
class TypeAnnotation(ASTNode):
    name: str                                       # e.g. "Int", "Currency", "Sentiment", "Prob", "Quantity", "Intent"
    generic_arg: Optional[str] = None              # Legacy single generic argument
    generic_args: List[str] = field(default_factory=list) # e.g. ["Refund", "Fraud"] in Intent<Refund, Fraud>
    min_confidence: float = 0.0                     # Confidence threshold, e.g. 0.95 in Prob<Currency, 0.95>


@dataclass
class Expr(ASTNode):
    pass


@dataclass
class Literal(Expr):
    value: Any
    type_name: str                                  # "int", "float", "string", "bool", "null"


@dataclass
class Identifier(Expr):
    name: str


@dataclass
class BinaryOp(Expr):
    left: Expr
    op: str                                         # "+", "-", "*", "/", "%", "==", "!=", "<", "<=", ">", ">=", "~", "and", "or"
    right: Expr


@dataclass
class UnaryOp(Expr):
    op: str                                         # "-", "not"
    operand: Expr


@dataclass
class ListLiteral(Expr):
    elements: List[Expr]


@dataclass
class DictLiteral(Expr):
    pairs: List[Tuple[Expr, Expr]]                  # (key_expr, value_expr)


@dataclass
class MemberAccess(Expr):
    target: Expr
    member: str                                     # e.g. user.name, val.confidence, val.amount


@dataclass
class IndexAccess(Expr):
    target: Expr
    index: Expr                                     # e.g. arr[0], dict["key"]


@dataclass
class FunctionCall(Expr):
    callee: Expr
    args: List[Expr] = field(default_factory=list)


@dataclass
class SanitizationNode(Expr):
    target: Expr
    rule: Optional[str] = None
    line: int = 1


@dataclass
class IntentExpr(Expr):
    intent_prompt: str
    target_type: Optional[TypeAnnotation] = None
    line: int = 1


@dataclass
class Block(ASTNode):
    statements: List[ASTNode]
    line: int = 1


@dataclass
class IfStatement(ASTNode):
    condition: Expr
    then_branch: Block
    elif_branches: List[Tuple[Expr, Block]] = field(default_factory=list)
    else_branch: Optional[Block] = None
    line: int = 1


@dataclass
class ForStatement(ASTNode):
    variable: str
    iterable: Expr
    body: Block
    line: int = 1


@dataclass
class WhileStatement(ASTNode):
    condition: Expr
    body: Block
    line: int = 1


@dataclass
class BreakStatement(ASTNode):
    line: int = 1


@dataclass
class ContinueStatement(ASTNode):
    line: int = 1


@dataclass
class FunctionDef(ASTNode):
    name: str
    params: List[str]
    body: Block
    param_types: Dict[str, Optional[TypeAnnotation]] = field(default_factory=dict)
    return_type: Optional[TypeAnnotation] = None
    line: int = 1


@dataclass
class ReturnStatement(ASTNode):
    value_expr: Optional[Expr] = None
    line: int = 1


@dataclass
class LetStatement(ASTNode):
    name: str
    type_annotation: Optional[TypeAnnotation]
    refinement_expr: Optional[Expr]                 # Invariant condition where 'v' represents value
    value_expr: Expr
    is_mutable: bool = False                        # True if declared with 'var', False if 'let'
    is_trusted: bool = False                        # True if declared with 'trusted'
    line: int = 1


@dataclass
class AssignStatement(ASTNode):
    name: str
    value_expr: Expr
    line: int = 1


@dataclass
class PrintStatement(ASTNode):
    exprs: List[Expr]
    query: Optional[str] = None                     # e.g. "summary of", "explain", "highlight risks in"
    audience: Optional[str] = None                  # e.g. "executive", "developer", "child", "sre", "marketer"
    format_style: Optional[str] = None              # e.g. "table", "bar_chart", "badge", "sentiment", "gauge", "card", "json", "tree"
    line: int = 1


@dataclass
class ImportStatement(ASTNode):
    module_path: str
    alias: Optional[str] = None
    line: int = 1


@dataclass
class Program(ASTNode):
    statements: List[ASTNode]
