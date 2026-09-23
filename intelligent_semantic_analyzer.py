"""
Intelligent Semantic Analyzer for IPL - Compiler-First Neural Architecture
Enhances traditional semantic analysis with deep understanding and AI-powered insights
"""
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict
import re
import hashlib

try:
    from .semantic_engine import SemanticEngine
    from .ast_nodes import (
        ASTNode, Program, LetStatement, AssignStatement, FunctionDef, 
        FunctionCall, BinaryOp, Identifier, Literal, Block, IfStatement,
        ForStatement, WhileStatement, ReturnStatement, TypeAnnotation
    )
    from .tokens import Token, TokenType
except (ImportError, ValueError):
    from semantic_engine import SemanticEngine
    from ast_nodes import (
        ASTNode, Program, LetStatement, AssignStatement, FunctionDef, 
        FunctionCall, BinaryOp, Identifier, Literal, Block, IfStatement,
        ForStatement, WhileStatement, ReturnStatement, TypeAnnotation
    )
    from tokens import Token, TokenType


@dataclass
class SemanticAnalysisResult:
    """Enhanced semantic analysis result with deep insights"""
    is_valid: bool
    confidence: float
    semantic_type: str
    meaning: str
    context_understanding: Dict[str, Any]
    relationships: List[Dict[str, str]]
    patterns: List[str]
    ai_insights: List[str]
    security_implications: List[str]
    optimization_suggestions: List[str]
    
    def __post_init__(self):
        if self.context_understanding is None:
            self.context_understanding = {}
        if self.relationships is None:
            self.relationships = []
        if self.patterns is None:
            self.patterns = []
        if self.ai_insights is None:
            self.ai_insights = []
        if self.security_implications is None:
            self.security_implications = []
        if self.optimization_suggestions is None:
            self.optimization_suggestions = []


class DeepSemanticUnderstanding:
    """
    Deep semantic understanding system that provides:
    - Context-aware meaning extraction
    - Relationship detection between code elements
    - Pattern recognition in code semantics
    - Intent inference beyond surface syntax
    - Semantic validation and consistency checking
    """
    
    def __init__(self):
        self.semantic_engine = SemanticEngine()
        self.semantic_patterns = self._initialize_semantic_patterns()
        self.intent_patterns = self._initialize_intent_patterns()
        self.learning_cache = {}  # Learn from semantic patterns
        
    def _initialize_semantic_patterns(self) -> Dict[str, List[str]]:
        """Initialize semantic patterns for deep analysis"""
        return {
            "data_processing": [
                r"(process|transform|convert|parse|extract|analyze)",
                r"(filter|map|reduce|aggregate)",
                r"(serialize|deserialize|encode|decode)"
            ],
            "control_flow": [
                r"(if|else|elif|switch|case)",
                r"(for|while|loop|iterate)",
                r"(break|continue|return|exit)"
            ],
            "data_structures": [
                r"(list|array|vector|matrix)",
                r"(dict|map|hash|object)",
                r"(set|collection|bag)"
            ],
            "io_operations": [
                r"(read|write|load|save|file)",
                r"(input|output|print|log)",
                r"(fetch|request|send|receive)"
            ],
            "security_operations": [
                r"(encrypt|decrypt|hash|authenticate)",
                r"(sanitize|validate|verify)",
                r"(authorize|permission|access)"
            ]
        }
    
    def _initialize_intent_patterns(self) -> Dict[str, List[str]]:
        """Initialize intent patterns for code understanding"""
        return {
            "computation": [
                r"(calculate|compute|evaluate|solve)",
                r"(add|subtract|multiply|divide)",
                r"(sum|average|count|total)"
            ],
            "data_manipulation": [
                r"(sort|order|arrange|organize)",
                r"(filter|select|extract|find)",
                r"(transform|convert|change|modify)"
            ],
            "communication": [
                r"(send|transmit|receive|fetch)",
                r"(request|response|call|invoke)",
                r"(connect|disconnect|network)"
            ],
            "storage": [
                r"(save|store|persist|archive)",
                r"(load|retrieve|fetch|read)",
                r"(delete|remove|clear|erase)"
            ],
            "user_interaction": [
                r"(display|show|present|render)",
                r"(input|prompt|ask|request)",
                r"(respond|reply|answer|feedback)"
            ]
        }
    
    def extract_deep_meaning(self, ast_node: ASTNode, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Extract deep semantic meaning from AST node
        Returns comprehensive semantic understanding
        """
        context = context or {}
        meaning_analysis = {
            "primary_intent": None,
            "secondary_intents": [],
            "semantic_role": None,
            "data_flow": [],
            "dependencies": [],
            "side_effects": [],
            "confidence": 0.0
        }
        
        if isinstance(ast_node, FunctionDef):
            meaning_analysis.update(self._analyze_function_semantics(ast_node, context))
        elif isinstance(ast_node, FunctionCall):
            meaning_analysis.update(self._analyze_function_call_semantics(ast_node, context))
        elif isinstance(ast_node, LetStatement):
            meaning_analysis.update(self._analyze_variable_semantics(ast_node, context))
        elif isinstance(ast_node, BinaryOp):
            meaning_analysis.update(self._analyze_operation_semantics(ast_node, context))
        elif isinstance(ast_node, IfStatement):
            meaning_analysis.update(self._analyze_conditional_semantics(ast_node, context))
        elif isinstance(ast_node, (ForStatement, WhileStatement)):
            meaning_analysis.update(self._analyze_loop_semantics(ast_node, context))
        
        return meaning_analysis
    
    def _analyze_function_semantics(self, func_def: FunctionDef, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze semantic meaning of function definition"""
        func_name = func_def.name.value if hasattr(func_def.name, 'value') else str(func_def.name)
        
        # Detect intent from function name
        primary_intent = self._detect_intent_from_name(func_name)
        semantic_role = self._determine_function_role(func_name, func_def)
        
        # Analyze parameter semantics
        parameter_semantics = []
        if hasattr(func_def, 'params') and func_def.params:
            for param in func_def.params:
                param_semantic = self._analyze_parameter_semantic(param)
                parameter_semantics.append(param_semantic)
        
        # Analyze body semantics
        body_intents = []
        if func_def.body:
            body_intents = self._extract_intents_from_block(func_def.body)
        
        return {
            "primary_intent": primary_intent,
            "secondary_intents": body_intents,
            "semantic_role": semantic_role,
            "data_flow": self._analyze_data_flow_in_function(func_def),
            "dependencies": self._extract_function_dependencies(func_def),
            "side_effects": self._detect_side_effects(func_def),
            "confidence": 0.85
        }
    
    def _analyze_function_call_semantics(self, func_call: FunctionCall, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze semantic meaning of function call"""
        callee_name = func_call.callee.value if hasattr(func_call.callee, 'value') else str(func_call.callee)
        
        # Detect intent from function being called
        primary_intent = self._detect_intent_from_name(callee_name)
        
        # Analyze argument semantics
        argument_semantics = []
        for arg in func_call.args:
            arg_semantic = self._analyze_expression_semantic(arg)
            argument_semantics.append(arg_semantic)
        
        return {
            "primary_intent": primary_intent,
            "secondary_intents": [],
            "semantic_role": "operation_execution",
            "data_flow": [{"from": "arguments", "to": callee_name, "type": "parameter_passing"}],
            "dependencies": [callee_name],
            "side_effects": self._predict_call_side_effects(callee_name),
            "confidence": 0.75
        }
    
    def _analyze_variable_semantics(self, let_stmt: LetStatement, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze semantic meaning of variable declaration"""
        var_name = let_stmt.name.value if hasattr(let_stmt.name, 'value') else str(let_stmt.name)
        
        # Detect semantic role from variable name
        semantic_role = self._determine_variable_role(var_name)
        
        # Analyze initialization expression
        init_semantic = self._analyze_expression_semantic(let_stmt.value_expr) if let_stmt.value_expr else {}
        
        return {
            "primary_intent": "data_storage",
            "secondary_intents": [],
            "semantic_role": semantic_role,
            "data_flow": [{"from": "initialization", "to": var_name, "type": "assignment"}],
            "dependencies": init_semantic.get("dependencies", []),
            "side_effects": [],
            "confidence": 0.8
        }
    
    def _analyze_operation_semantics(self, binary_op: BinaryOp, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze semantic meaning of binary operation"""
        operator = binary_op.operator
        
        # Determine operation type
        if operator in ["+", "-", "*", "/", "%"]:
            operation_type = "arithmetic"
            primary_intent = "computation"
        elif operator in ["&&", "||", "!"]:
            operation_type = "logical"
            primary_intent = "logical_evaluation"
        elif operator in ["<", ">", "<=", ">=", "==", "!="]:
            operation_type = "comparison"
            primary_intent = "comparison"
        else:
            operation_type = "unknown"
            primary_intent = "operation"
        
        # Analyze operand semantics
        left_semantic = self._analyze_expression_semantic(binary_op.left)
        right_semantic = self._analyze_expression_semantic(binary_op.right)
        
        return {
            "primary_intent": primary_intent,
            "secondary_intents": [],
            "semantic_role": operation_type,
            "data_flow": [
                {"from": "left_operand", "to": "operation", "type": "input"},
                {"from": "right_operand", "to": "operation", "type": "input"}
            ],
            "dependencies": left_semantic.get("dependencies", []) + right_semantic.get("dependencies", []),
            "side_effects": [],
            "confidence": 0.9
        }
    
    def _analyze_conditional_semantics(self, if_stmt: IfStatement, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze semantic meaning of conditional statement"""
        condition_semantic = self._analyze_expression_semantic(if_stmt.condition)
        
        # Analyze branch semantics
        then_intents = self._extract_intents_from_block(if_stmt.then_branch) if if_stmt.then_branch else []
        else_intents = self._extract_intents_from_block(if_stmt.else_branch) if if_stmt.else_branch else []
        
        return {
            "primary_intent": "conditional_execution",
            "secondary_intents": then_intents + else_intents,
            "semantic_role": "control_flow_branching",
            "data_flow": [{"from": "condition", "to": "branch_selection", "type": "control"}],
            "dependencies": condition_semantic.get("dependencies", []),
            "side_effects": self._detect_conditional_side_effects(if_stmt),
            "confidence": 0.85
        }
    
    def _analyze_loop_semantics(self, loop_stmt: Union[ForStatement, WhileStatement], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze semantic meaning of loop statement"""
        if isinstance(loop_stmt, ForStatement):
            iterable_semantic = self._analyze_expression_semantic(loop_stmt.iterable)
            loop_type = "iteration"
        else:
            condition_semantic = self._analyze_expression_semantic(loop_stmt.condition)
            iterable_semantic = condition_semantic
            loop_type = "conditional_iteration"
        
        # Analyze body semantics
        body_intents = self._extract_intents_from_block(loop_stmt.body) if loop_stmt.body else []
        
        return {
            "primary_intent": "repeated_execution",
            "secondary_intents": body_intents,
            "semantic_role": loop_type,
            "data_flow": [{"from": "iterable", "to": "loop_body", "type": "iteration"}],
            "dependencies": iterable_semantic.get("dependencies", []),
            "side_effects": self._detect_loop_side_effects(loop_stmt),
            "confidence": 0.8
        }
    
    def _detect_intent_from_name(self, name: str) -> str:
        """Detect primary intent from identifier name"""
        name_lower = name.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, name_lower):
                    return intent
        
        return "general_operation"
    
    def _determine_function_role(self, func_name: str, func_def: FunctionDef) -> str:
        """Determine the semantic role of a function"""
        name_lower = func_name.lower()
        
        if any(word in name_lower for word in ["get", "fetch", "retrieve", "read"]):
            return "data_retrieval"
        elif any(word in name_lower for word in ["set", "update", "modify", "write"]):
            return "data_modification"
        elif any(word in name_lower for word in ["calc", "compute", "calculate", "evaluate"]):
            return "computation"
        elif any(word in name_lower for word in ["check", "validate", "verify", "test"]):
            return "validation"
        elif any(word in name_lower for word in ["process", "handle", "manage"]):
            return "data_processing"
        else:
            return "general_function"
    
    def _determine_variable_role(self, var_name: str) -> str:
        """Determine the semantic role of a variable"""
        name_lower = var_name.lower()
        
        if any(word in name_lower for word in ["count", "total", "sum", "num"]):
            return "counter"
        elif any(word in name_lower for word in ["index", "i", "j", "k"]):
            return "iterator"
        elif any(word in name_lower for word in ["flag", "is_", "has_", "should_"]):
            return "boolean_flag"
        elif any(word in name_lower for word in ["temp", "tmp", "buffer"]):
            return "temporary_storage"
        elif any(word in name_lower for word in ["result", "output", "return"]):
            return "result_holder"
        else:
            return "general_variable"
    
    def _analyze_parameter_semantic(self, param) -> Dict[str, Any]:
        """Analyze semantic meaning of function parameter"""
        param_name = param.value if hasattr(param, 'value') else str(param)
        return {
            "semantic_role": self._determine_variable_role(param_name),
            "expected_type": "unknown",
            "confidence": 0.7
        }
    
    def _analyze_expression_semantic(self, expr) -> Dict[str, Any]:
        """Analyze semantic meaning of expression"""
        if isinstance(expr, Identifier):
            return {
                "semantic_role": self._determine_variable_role(str(expr.value)),
                "dependencies": [str(expr.value)],
                "confidence": 0.8
            }
        elif isinstance(expr, Literal):
            return {
                "semantic_role": "constant_value",
                "dependencies": [],
                "confidence": 0.95
            }
        elif isinstance(expr, FunctionCall):
            return self._analyze_function_call_semantics(expr, {})
        elif isinstance(expr, BinaryOp):
            return self._analyze_operation_semantics(expr, {})
        else:
            return {
                "semantic_role": "complex_expression",
                "dependencies": [],
                "confidence": 0.5
            }
    
    def _extract_intents_from_block(self, block: Block) -> List[str]:
        """Extract intents from a block of statements"""
        intents = []
        if block and hasattr(block, 'statements'):
            for stmt in block.statements:
                meaning = self.extract_deep_meaning(stmt, {})
                if meaning.get("primary_intent"):
                    intents.append(meaning["primary_intent"])
                intents.extend(meaning.get("secondary_intents", []))
        return intents
    
    def _analyze_data_flow_in_function(self, func_def: FunctionDef) -> List[Dict[str, str]]:
        """Analyze data flow within a function"""
        data_flow = []
        # Simplified implementation - could be enhanced with full data flow analysis
        if hasattr(func_def, 'params') and func_def.params:
            for param in func_def.params:
                param_name = param.value if hasattr(param, 'value') else str(param)
                data_flow.append({"from": "parameter", "to": param_name, "type": "parameter_binding"})
        return data_flow
    
    def _extract_function_dependencies(self, func_def: FunctionDef) -> List[str]:
        """Extract function dependencies"""
        dependencies = []
        # Simplified implementation - could be enhanced with full dependency analysis
        if func_def.body:
            dependencies = self._extract_identifiers_from_ast(func_def.body)
        return dependencies
    
    def _detect_side_effects(self, func_def: FunctionDef) -> List[str]:
        """Detect potential side effects of a function"""
        side_effects = []
        # Simplified implementation - could be enhanced with full side effect analysis
        if func_def.body:
            body_str = str(func_def.body).lower()
            if any(word in body_str for word in ["print", "write", "save", "send"]):
                side_effects.append("io_operation")
            if any(word in body_str for word in ["modify", "change", "update"]):
                side_effects.append("state_mutation")
        return side_effects
    
    def _predict_call_side_effects(self, callee_name: str) -> List[str]:
        """Predict side effects based on function name"""
        name_lower = callee_name.lower()
        side_effects = []
        
        if any(word in name_lower for word in ["print", "log", "write", "save"]):
            side_effects.append("io_operation")
        if any(word in name_lower for word in ["set", "update", "modify", "delete"]):
            side_effects.append("state_mutation")
        if any(word in name_lower for word in ["send", "fetch", "request"]):
            side_effects.append("network_operation")
        
        return side_effects
    
    def _detect_conditional_side_effects(self, if_stmt: IfStatement) -> List[str]:
        """Detect side effects in conditional branches"""
        side_effects = []
        # Analyze both branches for side effects
        if if_stmt.then_branch:
            then_str = str(if_stmt.then_branch).lower()
            if any(word in then_str for word in ["print", "write", "modify"]):
                side_effects.append("branch_side_effect")
        if if_stmt.else_branch:
            else_str = str(if_stmt.else_branch).lower()
            if any(word in else_str for word in ["print", "write", "modify"]):
                side_effects.append("branch_side_effect")
        return side_effects
    
    def _detect_loop_side_effects(self, loop_stmt) -> List[str]:
        """Detect side effects in loop body"""
        side_effects = []
        if loop_stmt.body:
            body_str = str(loop_stmt.body).lower()
            if any(word in body_str for word in ["print", "write", "modify"]):
                side_effects.append("iteration_side_effect")
        return side_effects
    
    def _extract_identifiers_from_ast(self, ast_node: ASTNode) -> List[str]:
        """Extract all identifiers from AST node"""
        identifiers = []
        
        if isinstance(ast_node, Identifier):
            identifiers.append(str(ast_node.value))
        elif isinstance(ast_node, FunctionCall):
            identifiers.append(str(ast_node.callee.value) if hasattr(ast_node.callee, 'value') else str(ast_node.callee))
            for arg in ast_node.args:
                identifiers.extend(self._extract_identifiers_from_ast(arg))
        elif isinstance(ast_node, BinaryOp):
            identifiers.extend(self._extract_identifiers_from_ast(ast_node.left))
            identifiers.extend(self._extract_identifiers_from_ast(ast_node.right))
        
        return list(set(identifiers))  # Remove duplicates


class IntelligentSemanticAnalyzer:
    """
    Compiler-First Intelligent Semantic Analyzer
    Enhances traditional semantic analysis with deep understanding:
    - Deep semantic meaning extraction
    - Context-aware relationship detection
    - Pattern recognition in code semantics
    - Intent inference and validation
    - Security implication analysis
    - Optimization opportunity detection
    """
    
    def __init__(self, enable_deep_analysis: bool = True):
        self.deep_understanding = DeepSemanticUnderstanding() if enable_deep_analysis else None
        self.semantic_engine = SemanticEngine()
        self.enable_deep_analysis = enable_deep_analysis
        
        # Learning and adaptation
        self.semantic_patterns = defaultdict(int)
        self.analysis_cache = {}
        
    def analyze_ast(self, ast: ASTNode, context: Dict[str, Any] = None) -> SemanticAnalysisResult:
        """
        Perform comprehensive semantic analysis on AST
        Returns detailed semantic analysis result
        """
        context = context or {}
        
        # Generate cache key
        cache_key = self._generate_cache_key(ast, context)
        if cache_key in self.analysis_cache:
            return self.analysis_cache[cache_key]
        
        # Perform deep semantic analysis
        if self.enable_deep_analysis and self.deep_understanding:
            deep_meaning = self.deep_understanding.extract_deep_meaning(ast, context)
            
            # Build comprehensive analysis result
            result = SemanticAnalysisResult(
                is_valid=True,
                confidence=deep_meaning.get("confidence", 0.8),
                semantic_type=deep_meaning.get("semantic_role", "unknown"),
                meaning=self._generate_meaning_description(deep_meaning),
                context_understanding=self._analyze_context(ast, context),
                relationships=self._extract_relationships(ast, deep_meaning),
                patterns=self._detect_semantic_patterns(ast, deep_meaning),
                ai_insights=self._generate_ai_insights(deep_meaning),
                security_implications=self._analyze_security_implications(ast, deep_meaning),
                optimization_suggestions=self._suggest_optimizations(ast, deep_meaning)
            )
        else:
            # Fallback to basic semantic analysis
            result = self._perform_basic_semantic_analysis(ast, context)
        
        # Cache result
        self.analysis_cache[cache_key] = result
        
        # Learn from analysis
        self._learn_from_analysis(result)
        
        return result
    
    def _generate_cache_key(self, ast: ASTNode, context: Dict[str, Any]) -> str:
        """Generate cache key for analysis result"""
        ast_str = str(ast)
        context_str = str(sorted(context.items()))
        combined = f"{ast_str}:{context_str}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _generate_meaning_description(self, deep_meaning: Dict[str, Any]) -> str:
        """Generate human-readable meaning description"""
        primary_intent = deep_meaning.get("primary_intent", "unknown")
        semantic_role = deep_meaning.get("semantic_role", "unknown")
        
        description = f"This code performs {primary_intent} with a {semantic_role} role"
        
        if deep_meaning.get("dependencies"):
            deps = ", ".join(deep_meaning["dependencies"][:3])
            description += f". It depends on: {deps}"
        
        if deep_meaning.get("side_effects"):
            effects = ", ".join(deep_meaning["side_effects"])
            description += f". It may have side effects: {effects}"
        
        return description
    
    def _analyze_context(self, ast: ASTNode, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze context of the AST node"""
        return {
            "node_type": type(ast).__name__,
            "provided_context": context,
            "complexity_level": self._assess_complexity(ast),
            "nesting_depth": self._calculate_nesting_depth(ast)
        }
    
    def _extract_relationships(self, ast: ASTNode, deep_meaning: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract relationships between code elements"""
        relationships = []
        
        # Extract data flow relationships
        for flow in deep_meaning.get("data_flow", []):
            relationships.append({
                "type": "data_flow",
                "source": flow.get("from", "unknown"),
                "target": flow.get("to", "unknown"),
                "relationship": flow.get("type", "unknown")
            })
        
        # Extract dependency relationships
        for dep in deep_meaning.get("dependencies", []):
            relationships.append({
                "type": "dependency",
                "source": "current_node",
                "target": dep,
                "relationship": "depends_on"
            })
        
        return relationships
    
    def _detect_semantic_patterns(self, ast: ASTNode, deep_meaning: Dict[str, Any]) -> List[str]:
        """Detect semantic patterns in the code"""
        patterns = []
        
        # Add intent-based patterns
        primary_intent = deep_meaning.get("primary_intent", "")
        if primary_intent:
            patterns.append(f"intent_{primary_intent}")
        
        # Add role-based patterns
        semantic_role = deep_meaning.get("semantic_role", "")
        if semantic_role:
            patterns.append(f"role_{semantic_role}")
        
        # Add side effect patterns
        for effect in deep_meaning.get("side_effects", []):
            patterns.append(f"side_effect_{effect}")
        
        return patterns
    
    def _generate_ai_insights(self, deep_meaning: Dict[str, Any]) -> List[str]:
        """Generate AI-powered insights from semantic analysis"""
        insights = []
        
        primary_intent = deep_meaning.get("primary_intent", "")
        if primary_intent == "data_processing":
            insights.append("This code processes data - consider input validation and error handling")
        elif primary_intent == "io_operation":
            insights.append("This code performs I/O - consider resource management and error handling")
        elif primary_intent == "computation":
            insights.append("This code performs computations - consider performance optimization")
        
        side_effects = deep_meaning.get("side_effects", [])
        if "state_mutation" in side_effects:
            insights.append("This code mutates state - consider immutability patterns")
        if "io_operation" in side_effects:
            insights.append("This code performs I/O operations - consider async patterns")
        
        return insights
    
    def _analyze_security_implications(self, ast: ASTNode, deep_meaning: Dict[str, Any]) -> List[str]:
        """Analyze security implications of the code"""
        implications = []
        
        # Check for security-sensitive operations
        primary_intent = deep_meaning.get("primary_intent", "")
        if primary_intent in ["io_operation", "communication"]:
            implications.append("Review input validation and sanitization")
        
        # Check for data flow to external systems
        for flow in deep_meaning.get("data_flow", []):
            if flow.get("to") in ["file", "network", "database"]:
                implications.append(f"Data flows to {flow['to']} - ensure proper security controls")
        
        # Check for side effects that could be security-relevant
        for effect in deep_meaning.get("side_effects", []):
            if effect in ["state_mutation", "io_operation"]:
                implications.append(f"Side effect '{effect}' may have security implications")
        
        return implications
    
    def _suggest_optimizations(self, ast: ASTNode, deep_meaning: Dict[str, Any]) -> List[str]:
        """Suggest optimizations based on semantic analysis"""
        suggestions = []
        
        # Check for optimization opportunities
        primary_intent = deep_meaning.get("primary_intent", "")
        if primary_intent == "computation":
            suggestions.append("Consider memoization for repeated computations")
        elif primary_intent == "data_processing":
            suggestions.append("Consider lazy evaluation for data processing pipelines")
        
        # Check for loop optimizations
        if "iteration" in deep_meaning.get("semantic_role", ""):
            suggestions.append("Consider loop unrolling or vectorization for performance")
        
        # Check for data flow optimizations
        data_flow = deep_meaning.get("data_flow", [])
        if len(data_flow) > 3:
            suggestions.append("Complex data flow detected - consider restructuring for better cache locality")
        
        return suggestions
    
    def _perform_basic_semantic_analysis(self, ast: ASTNode, context: Dict[str, Any]) -> SemanticAnalysisResult:
        """Perform basic semantic analysis without deep understanding"""
        return SemanticAnalysisResult(
            is_valid=True,
            confidence=0.6,
            semantic_type=type(ast).__name__,
            meaning=f"Basic analysis of {type(ast).__name__}",
            context_understanding={"node_type": type(ast).__name__},
            relationships=[],
            patterns=[],
            ai_insights=["Deep analysis disabled - enable for better insights"],
            security_implications=[],
            optimization_suggestions=[]
        )
    
    def _assess_complexity(self, ast: ASTNode) -> str:
        """Assess complexity of AST node"""
        complexity_score = 0
        
        # Count child nodes
        if hasattr(ast, 'statements'):
            complexity_score += len(ast.statements)
        elif hasattr(ast, 'args'):
            complexity_score += len(ast.args)
        elif hasattr(ast, 'params'):
            complexity_score += len(ast.params)
        
        if complexity_score > 5:
            return "high"
        elif complexity_score > 2:
            return "medium"
        else:
            return "low"
    
    def _calculate_nesting_depth(self, ast: ASTNode) -> int:
        """Calculate nesting depth of AST node"""
        depth = 0
        current = ast
        
        while hasattr(current, 'parent'):
            depth += 1
            current = current.parent
        
        return depth
    
    def _learn_from_analysis(self, result: SemanticAnalysisResult):
        """Learn from semantic analysis for future improvements"""
        pattern_key = f"{result.semantic_type}_{result.semantic_role}"
        self.semantic_patterns[pattern_key] += 1
    
    def get_analysis_statistics(self) -> Dict[str, Any]:
        """Get statistics about semantic analysis"""
        return {
            "total_analyses": len(self.semantic_patterns),
            "pattern_frequencies": dict(self.semantic_patterns),
            "cache_size": len(self.analysis_cache),
            "deep_analysis_enabled": self.enable_deep_analysis
        }


class CompilerFirstSemanticAnalyzer:
    """
    Main entry point for compiler-first intelligent semantic analysis
    This represents the intelligent semantic analyzer level in the compiler-first architecture
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "enable_deep_analysis": True,
            "enable_security_analysis": True,
            "enable_optimization_suggestions": True,
            "confidence_threshold": 0.7
        }
        
        self.intelligent_analyzer = IntelligentSemanticAnalyzer(
            enable_deep_analysis=self.config["enable_deep_analysis"]
        )
        
    def analyze_program(self, ast: Program) -> Dict[str, Any]:
        """
        Perform comprehensive semantic analysis on entire program
        Returns complete semantic analysis
        """
        program_analysis = {
            "overall_semantic_type": "program",
            "statements_analysis": [],
            "global_patterns": [],
            "security_summary": {},
            "optimization_opportunities": [],
            "analysis_timestamp": self._get_timestamp()
        }
        
        # Analyze each statement
        for stmt in ast.statements:
            stmt_analysis = self.intelligent_analyzer.analyze_ast(stmt)
            program_analysis["statements_analysis"].append(stmt_analysis)
            
            # Collect patterns
            program_analysis["global_patterns"].extend(stmt_analysis.patterns)
            
            # Collect security implications
            if self.config["enable_security_analysis"]:
                program_analysis["security_summary"][type(stmt).__name__] = stmt_analysis.security_implications
            
            # Collect optimization suggestions
            if self.config["enable_optimization_suggestions"]:
                program_analysis["optimization_opportunities"].extend(stmt_analysis.optimization_suggestions)
        
        # Remove duplicates from patterns
        program_analysis["global_patterns"] = list(set(program_analysis["global_patterns"]))
        
        # Add analyzer statistics
        program_analysis["statistics"] = self.intelligent_analyzer.get_analysis_statistics()
        
        return program_analysis
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for analysis tracking"""
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_semantic_summary(self, ast: Program) -> str:
        """Get human-readable summary of semantic analysis"""
        analysis = self.analyze_program(ast)
        
        summary = f"""
Intelligent Semantic Analysis Summary
====================================
Overall Semantic Type: {analysis['overall_semantic_type']}
Total Statements Analyzed: {len(analysis['statements_analysis'])}
Deep Analysis: {'Enabled' if self.config['enable_deep_analysis'] else 'Disabled'}

Global Semantic Patterns:
{self._format_patterns(analysis['global_patterns'])}

Security Implications:
{self._format_security(analysis['security_summary'])}

Optimization Opportunities:
{self._format_optimizations(analysis['optimization_opportunities'])}

Analysis Statistics:
{self._format_statistics(analysis['statistics'])}
"""
        return summary
    
    def _format_patterns(self, patterns: List[str]) -> str:
        """Format semantic patterns for display"""
        if not patterns:
            return "  No significant patterns detected"
        return "\n".join([f"  - {pattern}" for pattern in patterns])
    
    def _format_security(self, security_summary: Dict[str, List[str]]) -> str:
        """Format security implications for display"""
        if not security_summary:
            return "  No security implications detected"
        
        formatted = []
        for stmt_type, implications in security_summary.items():
            if implications:
                formatted.append(f"  {stmt_type}:")
                for impl in implications:
                    formatted.append(f"    - {impl}")
        
        if not formatted:
            return "  No security implications detected"
        return "\n".join(formatted)
    
    def _format_optimizations(self, optimizations: List[str]) -> str:
        """Format optimization suggestions for display"""
        if not optimizations:
            return "  No optimization opportunities detected"
        
        # Remove duplicates
        unique_optimizations = list(set(optimizations))
        return "\n".join([f"  - {opt}" for opt in unique_optimizations])
    
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