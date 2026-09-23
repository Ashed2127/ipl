"""
Intelligent Type System for IPL - Compiler-First Neural Architecture
Enhances traditional type systems with AI-powered inference and advanced type checking
"""
from typing import List, Dict, Any, Optional, Tuple, Set, Union
from dataclasses import dataclass
from collections import defaultdict
import re
import hashlib

try:
    from .ast_nodes import (
        ASTNode, Program, LetStatement, AssignStatement, FunctionDef, 
        FunctionCall, BinaryOp, Identifier, Literal, Block, IfStatement,
        ForStatement, WhileStatement, ReturnStatement, TypeAnnotation
    )
    from .tokens import Token, TokenType
    from .semantic_engine import SemanticEngine
except (ImportError, ValueError):
    from ast_nodes import (
        ASTNode, Program, LetStatement, AssignStatement, FunctionDef, 
        FunctionCall, BinaryOp, Identifier, Literal, Block, IfStatement,
        ForStatement, WhileStatement, ReturnStatement, TypeAnnotation
    )
    from tokens import Token, TokenType
    from semantic_engine import SemanticEngine


@dataclass
class TypeInfo:
    """Enhanced type information with AI-powered insights"""
    type_name: str
    confidence: float
    inferred_from: str
    type_constraints: List[str]
    compatibility: List[str]
    ai_suggestions: List[str]
    semantic_meaning: str
    
    def __post_init__(self):
        if self.type_constraints is None:
            self.type_constraints = []
        if self.compatibility is None:
            self.compatibility = []
        if self.ai_suggestions is None:
            self.ai_suggestions = []


@dataclass
class TypeInferenceResult:
    """Enhanced type inference result with AI-powered analysis"""
    inferred_types: Dict[str, TypeInfo]
    type_conflicts: List[Dict[str, Any]]
    type_suggestions: List[Dict[str, str]]
    consistency_score: float
    ai_insights: List[str]
    optimization_opportunities: List[str]
    confidence: float
    
    def __post_init__(self):
        if self.type_conflicts is None:
            self.type_conflicts = []
        if self.type_suggestions is None:
            self.type_suggestions = []
        if self.ai_insights is None:
            self.ai_insights = []
        if self.optimization_opportunities is None:
            self.optimization_opportunities = []


class NeuralTypeInference:
    """
    Neural type inference system that provides:
    - AI-powered type inference from context
    - Advanced type compatibility analysis
    - Semantic type understanding
    - Intelligent type suggestions
    - Type conflict detection and resolution
    """
    
    def __init__(self):
        self.semantic_engine = SemanticEngine()
        self.type_patterns = self._initialize_type_patterns()
        self.semantic_types = self._initialize_semantic_types()
        self.type_heuristics = self._initialize_type_heuristics()
        self.learning_cache = {}  # Learn from type patterns
        
    def _initialize_type_patterns(self) -> Dict[str, List[str]]:
        """Initialize type patterns for AI-powered inference"""
        return {
            "numeric": [
                r"\b\d+\b",
                r"\b\d+\.\d+\b",
                r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\b"
            ],
            "string": [
                r"['\"].*['\"]",
                r"\b[a-zA-Z]+\b"
            ],
            "boolean": [
                r"\b(true|false)\b",
                r"\b(yes|no)\b"
            ],
            "list": [
                r"\[.*\]",
                r"list\(.*\)"
            ],
            "dict": [
                r"\{.*\}",
                r"dict\(.*\)"
            ],
            "function": [
                r"fn\s+\w+",
                r"def\s+\w+",
                r"function\s+\w+"
            ]
        }
    
    def _initialize_semantic_types(self) -> Dict[str, List[str]]:
        """Initialize semantic type patterns"""
        return {
            "currency": [
                r"\$\d+\.?\d*",
                r"\d+\.?\d*\s*(USD|EUR|GBP|dollars?|euros?|pounds?)"
            ],
            "temporal": [
                r"\b\d{1,2}:\d{2}\b",
                r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
                r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b"
            ],
            "email": [
                r"\b[\w.-]+@[\w.-]+\.\w+\b"
            ],
            "url": [
                r"https?://[\w.-]+(?:\.[\w.-]+)+[/\w .-]*"
            ],
            "ip_address": [
                r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
            ]
        }
    
    def _initialize_type_heuristics(self) -> Dict[str, Any]:
        """Initialize type heuristics for intelligent inference"""
        return {
            "variable_naming": {
                "count": "Int",
                "total": "Int", 
                "sum": "Int",
                "average": "Float",
                "price": "Currency",
                "cost": "Currency",
                "name": "String",
                "email": "String",
                "url": "String",
                "is_valid": "Boolean",
                "has_permission": "Boolean",
                "items": "List",
                "mapping": "Dict"
            },
            "function_naming": {
                "get_": "return_value",
                "set_": "void",
                "is_": "Boolean",
                "has_": "Boolean",
                "calculate": "Float",
                "compute": "Float",
                "validate": "Boolean",
                "parse": "Dict",
                "format": "String"
            }
        }
    
    def infer_types_neurally(self, ast: ASTNode, context: Dict[str, Any] = None) -> TypeInferenceResult:
        """
        Perform neural type inference on AST
        Returns comprehensive type inference result
        """
        context = context or {}
        type_analysis = {
            "inferred_types": {},
            "type_conflicts": [],
            "type_suggestions": [],
            "consistency_score": 0.0,
            "ai_insights": [],
            "optimization_opportunities": []
        }
        
        # Infer types for different AST elements
        type_analysis["variable_types"] = self._infer_variable_types(ast, context)
        type_analysis["function_types"] = self._infer_function_types(ast, context)
        type_analysis["expression_types"] = self._infer_expression_types(ast, context)
        
        # Combine all inferred types
        combined_types = {}
        combined_types.update(type_analysis["variable_types"])
        combined_types.update(type_analysis["function_types"])
        combined_types.update(type_analysis["expression_types"])
        
        # Detect type conflicts
        type_analysis["type_conflicts"] = self._detect_type_conflicts(combined_types)
        
        # Generate type suggestions
        type_analysis["type_suggestions"] = self._generate_type_suggestions(combined_types, type_analysis["type_conflicts"])
        
        # Calculate consistency score
        type_analysis["consistency_score"] = self._calculate_type_consistency(combined_types, type_analysis["type_conflicts"])
        
        # Generate AI insights
        type_analysis["ai_insights"] = self._generate_type_insights(combined_types, type_analysis)
        
        # Generate optimization opportunities
        type_analysis["optimization_opportunities"] = self._generate_type_optimizations(combined_types, type_analysis)
        
        # Convert to TypeInferenceResult
        inferred_types = {name: TypeInfo(**type_info) if isinstance(type_info, dict) else type_info 
                         for name, type_info in combined_types.items()}
        
        result = TypeInferenceResult(
            inferred_types=inferred_types,
            type_conflicts=type_analysis["type_conflicts"],
            type_suggestions=type_analysis["type_suggestions"],
            consistency_score=type_analysis["consistency_score"],
            ai_insights=type_analysis["ai_insights"],
            optimization_opportunities=type_analysis["optimization_opportunities"],
            confidence=self._calculate_inference_confidence(type_analysis)
        )
        
        return result
    
    def _infer_variable_types(self, ast: ASTNode, context: Dict[str, Any]) -> Dict[str, Any]:
        """Infer types for variables"""
        variable_types = {}
        
        # Find all variable declarations
        let_statements = self._find_nodes_by_type(ast, LetStatement)
        
        for let_stmt in let_statements:
            var_name = str(let_stmt.name.value) if hasattr(let_stmt.name, 'value') else str(let_stmt.name)
            
            # Check for explicit type annotation
            if let_stmt.target_type:
                explicit_type = let_stmt.target_type.name
                variable_types[var_name] = {
                    "type_name": explicit_type,
                    "confidence": 1.0,
                    "inferred_from": "explicit_annotation",
                    "type_constraints": [],
                    "compatibility": [explicit_type],
                    "ai_suggestions": [],
                    "semantic_meaning": f"Explicitly typed as {explicit_type}"
                }
            else:
                # Infer type from initialization expression
                if let_stmt.value_expr:
                    inferred_type = self._infer_expression_type(let_stmt.value_expr, context)
                    variable_types[var_name] = inferred_type
                else:
                    # Use naming heuristics
                    heuristic_type = self._apply_naming_heuristics(var_name, "variable")
                    variable_types[var_name] = {
                        "type_name": heuristic_type,
                        "confidence": 0.6,
                        "inferred_from": "naming_heuristic",
                        "type_constraints": [],
                        "compatibility": [heuristic_type],
                        "ai_suggestions": ["Consider adding explicit type annotation"],
                        "semantic_meaning": f"Inferred from variable name pattern"
                    }
        
        return variable_types
    
    def _infer_function_types(self, ast: ASTNode, context: Dict[str, Any]) -> Dict[str, Any]:
        """Infer types for functions"""
        function_types = {}
        
        # Find all function definitions
        function_defs = self._find_nodes_by_type(ast, FunctionDef)
        
        for func_def in function_defs:
            func_name = str(func_def.name.value) if hasattr(func_def.name, 'value') else str(func_def.name)
            
            # Infer return type from function body
            return_type = "unknown"
            if func_def.body:
                return_statements = self._find_nodes_by_type(func_def.body, ReturnStatement)
                if return_statements:
                    # Infer from return statement
                    return_type = self._infer_expression_type(return_statements[0].value_expr, context).get("type_name", "unknown")
                else:
                    # Use naming heuristics
                    return_type = self._apply_naming_heuristics(func_name, "function")
            
            function_types[func_name] = {
                "type_name": f"function -> {return_type}",
                "confidence": 0.7,
                "inferred_from": "function_analysis",
                "type_constraints": [],
                "compatibility": ["function"],
                "ai_suggestions": ["Consider adding explicit return type annotation"],
                "semantic_meaning": f"Function returning {return_type}"
            }
        
        return function_types
    
    def _infer_expression_types(self, ast: ASTNode, context: Dict[str, Any]) -> Dict[str, Any]:
        """Infer types for expressions"""
        expression_types = {}
        
        # Find all expressions and infer their types
        literals = self._find_nodes_by_type(ast, Literal)
        binary_ops = self._find_nodes_by_type(ast, BinaryOp)
        function_calls = self._find_nodes_by_type(ast, FunctionCall)
        
        # Infer literal types
        for i, literal in enumerate(literals):
            expr_key = f"literal_{i}"
            if isinstance(literal.value, int) and not isinstance(literal.value, bool):
                expression_types[expr_key] = {
                    "type_name": "Int",
                    "confidence": 1.0,
                    "inferred_from": "literal_value",
                    "type_constraints": [],
                    "compatibility": ["Int", "Float"],
                    "ai_suggestions": [],
                    "semantic_meaning": "Integer literal"
                }
            elif isinstance(literal.value, float):
                expression_types[expr_key] = {
                    "type_name": "Float",
                    "confidence": 1.0,
                    "inferred_from": "literal_value",
                    "type_constraints": [],
                    "compatibility": ["Float"],
                    "ai_suggestions": [],
                    "semantic_meaning": "Float literal"
                }
            elif isinstance(literal.value, str):
                # Check for semantic types
                semantic_type = self._detect_semantic_type(literal.value)
                if semantic_type:
                    expression_types[expr_key] = {
                        "type_name": semantic_type,
                        "confidence": 0.8,
                        "inferred_from": "semantic_pattern",
                        "type_constraints": [],
                        "compatibility": ["String", semantic_type],
                        "ai_suggestions": [],
                        "semantic_meaning": f"Semantic type: {semantic_type}"
                    }
                else:
                    expression_types[expr_key] = {
                        "type_name": "String",
                        "confidence": 1.0,
                        "inferred_from": "literal_value",
                        "type_constraints": [],
                        "compatibility": ["String"],
                        "ai_suggestions": [],
                        "semantic_meaning": "String literal"
                    }
            elif isinstance(literal.value, bool):
                expression_types[expr_key] = {
                    "type_name": "Boolean",
                    "confidence": 1.0,
                    "inferred_from": "literal_value",
                    "type_constraints": [],
                    "compatibility": ["Boolean"],
                    "ai_suggestions": [],
                    "semantic_meaning": "Boolean literal"
                }
        
        # Infer binary operation types
        for i, binary_op in enumerate(binary_ops):
            expr_key = f"binary_op_{i}"
            if binary_op.operator in ["+", "-", "*", "/"]:
                expression_types[expr_key] = {
                    "type_name": "Float",  # Default to Float for arithmetic
                    "confidence": 0.8,
                    "inferred_from": "operator_semantics",
                    "type_constraints": ["numeric_operands"],
                    "compatibility": ["Int", "Float"],
                    "ai_suggestions": ["Consider explicit type conversion if needed"],
                    "semantic_meaning": "Arithmetic operation result"
                }
            elif binary_op.operator in ["&&", "||", "!"]:
                expression_types[expr_key] = {
                    "type_name": "Boolean",
                    "confidence": 0.9,
                    "inferred_from": "operator_semantics",
                    "type_constraints": ["boolean_operands"],
                    "compatibility": ["Boolean"],
                    "ai_suggestions": [],
                    "semantic_meaning": "Logical operation result"
                }
            elif binary_op.operator in ["<", ">", "<=", ">=", "==", "!="]:
                expression_types[expr_key] = {
                    "type_name": "Boolean",
                    "confidence": 0.95,
                    "inferred_from": "operator_semantics",
                    "type_constraints": ["comparable_operands"],
                    "compatibility": ["Boolean"],
                    "ai_suggestions": [],
                    "semantic_meaning": "Comparison operation result"
                }
        
        return expression_types
    
    def _infer_expression_type(self, expr: ASTNode, context: Dict[str, Any]) -> Dict[str, Any]:
        """Infer type for a single expression"""
        if isinstance(expr, Literal):
            if isinstance(expr.value, int) and not isinstance(expr.value, bool):
                return {
                    "type_name": "Int",
                    "confidence": 1.0,
                    "inferred_from": "literal_value",
                    "type_constraints": [],
                    "compatibility": ["Int", "Float"],
                    "ai_suggestions": [],
                    "semantic_meaning": "Integer literal"
                }
            elif isinstance(expr.value, float):
                return {
                    "type_name": "Float",
                    "confidence": 1.0,
                    "inferred_from": "literal_value",
                    "type_constraints": [],
                    "compatibility": ["Float"],
                    "ai_suggestions": [],
                    "semantic_meaning": "Float literal"
                }
            elif isinstance(expr.value, str):
                semantic_type = self._detect_semantic_type(expr.value)
                if semantic_type:
                    return {
                        "type_name": semantic_type,
                        "confidence": 0.8,
                        "inferred_from": "semantic_pattern",
                        "type_constraints": [],
                        "compatibility": ["String", semantic_type],
                        "ai_suggestions": [],
                        "semantic_meaning": f"Semantic type: {semantic_type}"
                    }
                else:
                    return {
                        "type_name": "String",
                        "confidence": 1.0,
                        "inferred_from": "literal_value",
                        "type_constraints": [],
                        "compatibility": ["String"],
                        "ai_suggestions": [],
                        "semantic_meaning": "String literal"
                    }
            elif isinstance(expr.value, bool):
                return {
                    "type_name": "Boolean",
                    "confidence": 1.0,
                    "inferred_from": "literal_value",
                    "type_constraints": [],
                    "compatibility": ["Boolean"],
                    "ai_suggestions": [],
                    "semantic_meaning": "Boolean literal"
                }
        
        elif isinstance(expr, Identifier):
            # Use naming heuristics for identifiers
            var_name = str(expr.value)
            heuristic_type = self._apply_naming_heuristics(var_name, "variable")
            return {
                "type_name": heuristic_type,
                "confidence": 0.5,
                "inferred_from": "naming_heuristic",
                "type_constraints": [],
                "compatibility": [heuristic_type],
                "ai_suggestions": ["Consider explicit type annotation"],
                "semantic_meaning": f"Inferred from identifier name"
            }
        
        elif isinstance(expr, BinaryOp):
            if expr.operator in ["+", "-", "*", "/"]:
                return {
                    "type_name": "Float",
                    "confidence": 0.8,
                    "inferred_from": "operator_semantics",
                    "type_constraints": ["numeric_operands"],
                    "compatibility": ["Int", "Float"],
                    "ai_suggestions": ["Consider explicit type conversion"],
                    "semantic_meaning": "Arithmetic operation"
                }
            elif expr.operator in ["&&", "||", "!"]:
                return {
                    "type_name": "Boolean",
                    "confidence": 0.9,
                    "inferred_from": "operator_semantics",
                    "type_constraints": ["boolean_operands"],
                    "compatibility": ["Boolean"],
                    "ai_suggestions": [],
                    "semantic_meaning": "Logical operation"
                }
            elif expr.operator in ["<", ">", "<=", ">=", "==", "!="]:
                return {
                    "type_name": "Boolean",
                    "confidence": 0.95,
                    "inferred_from": "operator_semantics",
                    "type_constraints": ["comparable_operands"],
                    "compatibility": ["Boolean"],
                    "ai_suggestions": [],
                    "semantic_meaning": "Comparison operation"
                }
        
        # Default fallback
        return {
            "type_name": "unknown",
            "confidence": 0.3,
            "inferred_from": "fallback",
            "type_constraints": [],
            "compatibility": [],
            "ai_suggestions": ["Consider adding explicit type annotation"],
            "semantic_meaning": "Unknown type"
        }
    
    def _detect_semantic_type(self, value: str) -> Optional[str]:
        """Detect semantic type from string value"""
        for semantic_type, patterns in self.semantic_types.items():
            for pattern in patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    return semantic_type.capitalize()
        return None
    
    def _apply_naming_heuristics(self, name: str, category: str) -> str:
        """Apply naming heuristics for type inference"""
        name_lower = name.lower()
        
        if category == "variable":
            for pattern, type_name in self.type_heuristics["variable_naming"].items():
                if pattern in name_lower:
                    return type_name
        elif category == "function":
            for pattern, type_info in self.type_heuristics["function_naming"].items():
                if name_lower.startswith(pattern):
                    if type_info == "return_value":
                        # Need to infer actual return type
                        return "unknown"
                    return type_info
        
        # Default fallback
        return "unknown"
    
    def _detect_type_conflicts(self, inferred_types: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect type conflicts in inferred types"""
        conflicts = []
        
        # Check for type inconsistencies
        # Simplified implementation - could be enhanced with proper type checking
        
        # Check for variables with conflicting types
        type_by_variable = defaultdict(list)
        for name, type_info in inferred_types.items():
            if isinstance(type_info, dict):
                var_name = name.split("_")[0] if "_" in name else name
                type_by_variable[var_name].append(type_info["type_name"])
        
        for var_name, types in type_by_variable.items():
            if len(set(types)) > 1:
                conflicts.append({
                    "conflict_type": "type_inconsistency",
                    "variable": var_name,
                    "detected_types": list(set(types)),
                    "severity": "medium",
                    "suggestion": f"Resolve type inconsistency for {var_name}"
                })
        
        return conflicts
    
    def _generate_type_suggestions(self, inferred_types: Dict[str, Any], 
                                  conflicts: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate intelligent type suggestions"""
        suggestions = []
        
        # Suggest explicit type annotations for low-confidence inferences
        for name, type_info in inferred_types.items():
            if isinstance(type_info, dict) and type_info.get("confidence", 1.0) < 0.7:
                suggestions.append({
                    "target": name,
                    "suggestion": f"Add explicit type annotation for {name}",
                    "suggested_type": type_info.get("type_name", "unknown"),
                    "reason": "Low inference confidence"
                })
        
        # Suggest resolutions for type conflicts
        for conflict in conflicts:
            suggestions.append({
                "target": conflict["variable"],
                "suggestion": conflict["suggestion"],
                "suggested_type": conflict["detected_types"][0],  # Suggest first detected type
                "reason": "Type conflict detected"
            })
        
        return suggestions
    
    def _calculate_type_consistency(self, inferred_types: Dict[str, Any], 
                                   conflicts: List[Dict[str, Any]]) -> float:
        """Calculate type consistency score"""
        if not inferred_types:
            return 1.0
        
        # Base consistency starts at 1.0
        consistency = 1.0
        
        # Reduce consistency based on conflicts
        consistency -= len(conflicts) * 0.1
        
        # Reduce consistency based on low-confidence inferences
        low_confidence_count = sum(1 for type_info in inferred_types.values() 
                                 if isinstance(type_info, dict) and type_info.get("confidence", 1.0) < 0.7)
        consistency -= low_confidence_count * 0.05
        
        return max(0.0, min(1.0, consistency))
    
    def _generate_type_insights(self, inferred_types: Dict[str, Any], 
                               type_analysis: Dict[str, Any]) -> List[str]:
        """Generate AI-powered type insights"""
        insights = []
        
        # Analyze type diversity
        type_counts = defaultdict(int)
        for type_info in inferred_types.values():
            if isinstance(type_info, dict):
                type_name = type_info.get("type_name", "unknown")
                type_counts[type_name] += 1
        
        if len(type_counts) > 5:
            insights.append("High type diversity detected - consider type consolidation for better maintainability")
        
        # Check for excessive use of unknown types
        unknown_count = type_counts.get("unknown", 0)
        if unknown_count > len(inferred_types) * 0.3:
            insights.append("High proportion of unknown types - consider adding explicit type annotations")
        
        # Check for semantic type usage
        semantic_types = [t for t in type_counts.keys() if t in ["Currency", "Temporal", "Email", "Url"]]
        if semantic_types:
            insights.append(f"Semantic types detected: {', '.join(semantic_types)} - leverage for better type safety")
        
        return insights
    
    def _generate_type_optimizations(self, inferred_types: Dict[str, Any], 
                                    type_analysis: Dict[str, Any]) -> List[str]:
        """Generate type optimization opportunities"""
        optimizations = []
        
        # Suggest type annotations for performance
        for name, type_info in inferred_types.items():
            if isinstance(type_info, dict) and type_info.get("confidence", 1.0) < 0.8:
                optimizations.append(f"Add explicit type annotation for {name} to improve performance")
        
        # Suggest type consolidation
        type_counts = defaultdict(int)
        for type_info in inferred_types.values():
            if isinstance(type_info, dict):
                type_name = type_info.get("type_name", "unknown")
                type_counts[type_name] += 1
        
        if type_counts.get("String", 0) > 5:
            optimizations.append("Consider creating specific string types for different use cases")
        
        return optimizations
    
    def _calculate_inference_confidence(self, type_analysis: Dict[str, Any]) -> float:
        """Calculate overall confidence in type inference"""
        if not type_analysis.get("inferred_types"):
            return 0.5
        
        # Calculate average confidence
        confidences = []
        for type_info in type_analysis["inferred_types"].values():
            if isinstance(type_info, dict):
                confidences.append(type_info.get("confidence", 0.5))
            elif isinstance(type_info, TypeInfo):
                confidences.append(type_info.confidence)
        
        if not confidences:
            return 0.5
        
        return sum(confidences) / len(confidences)
    
    def _find_nodes_by_type(self, ast: ASTNode, node_types: Tuple) -> List[ASTNode]:
        """Find all nodes of specific types in AST"""
        found_nodes = []
        
        if isinstance(ast, node_types):
            found_nodes.append(ast)
        
        # Recursively search children
        if hasattr(ast, 'statements'):
            for stmt in ast.statements:
                found_nodes.extend(self._find_nodes_by_type(stmt, node_types))
        elif hasattr(ast, 'body'):
            found_nodes.extend(self._find_nodes_by_type(ast.body, node_types))
        elif hasattr(ast, 'args'):
            for arg in ast.args:
                found_nodes.extend(self._find_nodes_by_type(arg, node_types))
        elif hasattr(ast, 'params'):
            for param in ast.params:
                found_nodes.extend(self._find_nodes_by_type(param, node_types))
        elif hasattr(ast, 'condition'):
            found_nodes.extend(self._find_nodes_by_type(ast.condition, node_types))
        elif hasattr(ast, 'then_branch'):
            found_nodes.extend(self._find_nodes_by_type(ast.then_branch, node_types))
        elif hasattr(ast, 'else_branch'):
            found_nodes.extend(self._find_nodes_by_type(ast.else_branch, node_types))
        elif hasattr(ast, 'value_expr'):
            found_nodes.extend(self._find_nodes_by_type(ast.value_expr, node_types))
        elif hasattr(ast, 'left'):
            found_nodes.extend(self._find_nodes_by_type(ast.left, node_types))
        elif hasattr(ast, 'right'):
            found_nodes.extend(self._find_nodes_by_type(ast.right, node_types))
        
        return found_nodes


class IntelligentTypeSystem:
    """
    Compiler-First Intelligent Type System
    Enhances traditional type systems with AI-powered capabilities:
    - Neural type inference from context
    - Advanced type compatibility checking
    - Semantic type understanding
    - Intelligent type suggestions
    - Type conflict detection and resolution
    """
    
    def __init__(self, enable_neural_inference: bool = True):
        self.neural_inference = NeuralTypeInference() if enable_neural_inference else None
        self.semantic_engine = SemanticEngine()
        self.enable_neural_inference = enable_neural_inference
        
        # Learning and adaptation
        self.type_patterns = defaultdict(int)
        self.inference_cache = {}
        
    def analyze_types(self, ast: ASTNode, context: Dict[str, Any] = None) -> TypeInferenceResult:
        """
        Perform comprehensive type analysis on AST
        Returns detailed type analysis result
        """
        context = context or {}
        
        # Generate cache key
        cache_key = self._generate_cache_key(ast, context)
        if cache_key in self.inference_cache:
            return self.inference_cache[cache_key]
        
        # Perform neural type inference
        if self.enable_neural_inference and self.neural_inference:
            inference_result = self.neural_inference.infer_types_neurally(ast, context)
        else:
            # Fallback to basic type analysis
            inference_result = self._perform_basic_type_analysis(ast, context)
        
        # Cache result
        self.inference_cache[cache_key] = inference_result
        
        # Learn from analysis
        self._learn_from_analysis(inference_result)
        
        return inference_result
    
    def _generate_cache_key(self, ast: ASTNode, context: Dict[str, Any]) -> str:
        """Generate cache key for type analysis"""
        ast_str = str(ast)
        context_str = str(sorted(context.items()))
        combined = f"{ast_str}:{context_str}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _perform_basic_type_analysis(self, ast: ASTNode, context: Dict[str, Any]) -> TypeInferenceResult:
        """Perform basic type analysis without neural inference"""
        return TypeInferenceResult(
            inferred_types={},
            type_conflicts=[],
            type_suggestions=[],
            consistency_score=0.5,
            ai_insights=["Neural inference disabled - enable for better type analysis"],
            optimization_opportunities=[],
            confidence=0.5
        )
    
    def _learn_from_analysis(self, result: TypeInferenceResult):
        """Learn from type analysis for future improvements"""
        for type_name, type_info in result.inferred_types.items():
            pattern_key = f"{type_name}_{type_info.type_name}"
            self.type_patterns[pattern_key] += 1
    
    def get_type_statistics(self) -> Dict[str, Any]:
        """Get statistics about type analysis"""
        return {
            "total_inferences": len(self.type_patterns),
            "pattern_frequencies": dict(self.type_patterns),
            "cache_size": len(self.inference_cache),
            "neural_inference_enabled": self.enable_neural_inference
        }


class CompilerFirstTypeSystem:
    """
    Main entry point for compiler-first intelligent type system
    This represents the intelligent type system level in the compiler-first architecture
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "enable_neural_inference": True,
            "enable_semantic_types": True,
            "enable_type_suggestions": True,
            "consistency_threshold": 0.8
        }
        
        self.intelligent_type_system = IntelligentTypeSystem(
            enable_neural_inference=self.config["enable_neural_inference"]
        )
        
    def analyze_program_types(self, ast: Program) -> Dict[str, Any]:
        """
        Perform comprehensive type analysis on entire program
        Returns complete type analysis
        """
        # Analyze overall program types
        program_types = self.intelligent_type_system.analyze_types(ast)
        
        # Analyze individual statements for detailed type information
        statement_types = []
        for stmt in ast.statements:
            stmt_analysis = self.intelligent_type_system.analyze_types(stmt)
            statement_types.append(stmt_analysis)
        
        # Compile comprehensive analysis
        analysis = {
            "overall_types": program_types,
            "statement_types": statement_types,
            "type_summary": self._generate_type_summary(program_types, statement_types),
            "recommendations": self._generate_type_recommendations(program_types, statement_types),
            "statistics": self.intelligent_type_system.get_type_statistics(),
            "analysis_timestamp": self._get_timestamp()
        }
        
        return analysis
    
    def _generate_type_summary(self, overall_types: TypeInferenceResult, 
                              statement_types: List[TypeInferenceResult]) -> Dict[str, Any]:
        """Generate comprehensive type summary"""
        total_inferred = len(overall_types.inferred_types)
        high_confidence = sum(1 for t in overall_types.inferred_types.values() 
                           if (isinstance(t, TypeInfo) and t.confidence > 0.8) or
                              (isinstance(t, dict) and t.get("confidence", 0) > 0.8))
        
        type_distribution = defaultdict(int)
        for type_info in overall_types.inferred_types.values():
            if isinstance(type_info, TypeInfo):
                type_distribution[type_info.type_name] += 1
            elif isinstance(type_info, dict):
                type_distribution[type_info.get("type_name", "unknown")] += 1
        
        return {
            "total_types_inferred": total_inferred,
            "high_confidence_inferences": high_confidence,
            "consistency_score": overall_types.consistency_score,
            "type_conflicts": len(overall_types.type_conflicts),
            "type_distribution": dict(type_distribution)
        }
    
    def _generate_type_recommendations(self, overall_types: TypeInferenceResult,
                                      statement_types: List[TypeInferenceResult]) -> List[str]:
        """Generate comprehensive type recommendations"""
        recommendations = []
        
        # Add overall type recommendations
        recommendations.extend(overall_types.ai_insights)
        recommendations.extend(overall_types.optimization_opportunities)
        
        # Add type suggestions
        for suggestion in overall_types.type_suggestions:
            recommendations.append(f"{suggestion['suggestion']}: {suggestion['suggested_type']}")
        
        # Add statement-specific recommendations
        for stmt_type in statement_types:
            recommendations.extend(stmt_type.ai_insights)
        
        # Remove duplicates
        return list(set(recommendations))
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for analysis tracking"""
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_type_summary(self, ast: Program) -> str:
        """Get human-readable summary of type analysis"""
        analysis = self.analyze_program_types(ast)
        
        summary = f"""
Intelligent Type System Analysis Summary
====================================
Consistency Score: {analysis['overall_types'].consistency_score:.2%}
Analysis Confidence: {analysis['overall_types'].confidence:.2%}
Neural Inference: {'Enabled' if self.config['enable_neural_inference'] else 'Disabled'}

Type Summary:
{self._format_type_summary(analysis['type_summary'])}

Inferred Types:
{self._format_inferred_types(analysis['overall_types'].inferred_types)}

Type Conflicts:
{self._format_type_conflicts(analysis['overall_types'].type_conflicts)}

Type Suggestions:
{self._format_type_suggestions(analysis['overall_types'].type_suggestions)}

AI Insights:
{self._format_ai_insights(analysis['overall_types'].ai_insights)}

Type Recommendations:
{self._format_recommendations(analysis['recommendations'])}

Analysis Statistics:
{self._format_statistics(analysis['statistics'])}
"""
        return summary
    
    def _format_type_summary(self, type_summary: Dict[str, Any]) -> str:
        """Format type summary for display"""
        formatted = []
        for key, value in type_summary.items():
            if isinstance(value, dict):
                formatted.append(f"  {key}:")
                for sub_key, sub_value in value.items():
                    formatted.append(f"    {sub_key}: {sub_value}")
            else:
                formatted.append(f"  {key}: {value}")
        return "\n".join(formatted)
    
    def _format_inferred_types(self, inferred_types: Dict[str, TypeInfo]) -> str:
        """Format inferred types for display"""
        if not inferred_types:
            return "  No types inferred"
        
        formatted = []
        for name, type_info in list(inferred_types.items())[:10]:  # Show first 10
            if isinstance(type_info, TypeInfo):
                formatted.append(f"  {name}: {type_info.type_name} (confidence: {type_info.confidence:.2%})")
            elif isinstance(type_info, dict):
                formatted.append(f"  {name}: {type_info.get('type_name', 'unknown')} (confidence: {type_info.get('confidence', 0):.2%})")
        
        if len(inferred_types) > 10:
            formatted.append(f"  ... and {len(inferred_types) - 10} more")
        
        return "\n".join(formatted)
    
    def _format_type_conflicts(self, conflicts: List[Dict[str, Any]]) -> str:
        """Format type conflicts for display"""
        if not conflicts:
            return "  No type conflicts detected"
        
        formatted = []
        for i, conflict in enumerate(conflicts, 1):
            formatted.append(f"  {i}. {conflict['variable']}: {', '.join(conflict['detected_types'])}")
            formatted.append(f"     Severity: {conflict['severity']}")
            formatted.append(f"     Suggestion: {conflict['suggestion']}")
        
        return "\n".join(formatted)
    
    def _format_type_suggestions(self, suggestions: List[Dict[str, str]]) -> str:
        """Format type suggestions for display"""
        if not suggestions:
            return "  No type suggestions"
        
        formatted = []
        for i, suggestion in enumerate(suggestions, 1):
            formatted.append(f"  {i}. {suggestion['target']}: {suggestion['suggestion']}")
            formatted.append(f"     Suggested type: {suggestion['suggested_type']}")
            formatted.append(f"     Reason: {suggestion['reason']}")
        
        return "\n".join(formatted)
    
    def _format_ai_insights(self, insights: List[str]) -> str:
        """Format AI insights for display"""
        if not insights:
            return "  No AI insights available"
        return "\n".join([f"  - {insight}" for insight in insights])
    
    def _format_recommendations(self, recommendations: List[str]) -> str:
        """Format type recommendations for display"""
        if not recommendations:
            return "  No additional recommendations"
        return "\n".join([f"  - {rec}" for rec in recommendations])
    
    def _format_statistics(self, statistics: Dict[str, Any]) -> str:
        """Format analysis statistics for display"""
        formatted = []
        for key, value in statistics.items():
            if isinstance(value, dict):
                formatted.append(f"  {key}:")
                for sub_key, sub_value in value.items():
                    formatted.append(f"    {sub_key}: {sub_value}")
            else:
                formatted.append(f"  {key}: {value}")
        return "\n".join(formatted)