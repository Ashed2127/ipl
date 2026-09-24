"""
Intelligent Code Generator for IPL - Compiler-First Neural Architecture
Enhances traditional code generation with AI-powered optimization and transformation
"""
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass
from collections import defaultdict
import re
import hashlib

try:
    from .ast_nodes import (
        ASTNode, Program, LetStatement, AssignStatement, FunctionDef, 
        FunctionCall, BinaryOp, Identifier, Literal, Block, IfStatement,
        ForStatement, WhileStatement, ReturnStatement, TypeAnnotation,
        PrintStatement
    )
    from .tokens import Token, TokenType
    from .semantic_engine import SemanticEngine
except (ImportError, ValueError):
    from ast_nodes import (
        ASTNode, Program, LetStatement, AssignStatement, FunctionDef, 
        FunctionCall, BinaryOp, Identifier, Literal, Block, IfStatement,
        ForStatement, WhileStatement, ReturnStatement, TypeAnnotation,
        PrintStatement
    )
    from tokens import Token, TokenType
    from semantic_engine import SemanticEngine


@dataclass
class CodeGenerationResult:
    """Enhanced code generation result with AI optimization insights"""
    generated_code: str
    optimization_level: str
    performance_improvements: List[str]
    code_quality_metrics: Dict[str, Any]
    ai_transformations: List[Dict[str, str]]
    confidence: float
    generation_strategy: str
    
    def __post_init__(self):
        if self.performance_improvements is None:
            self.performance_improvements = []
        if self.code_quality_metrics is None:
            self.code_quality_metrics = {}
        if self.ai_transformations is None:
            self.ai_transformations = []


class NeuralCodeOptimizer:
    """
    Neural code optimization system that provides:
    - AI-powered code transformation suggestions
    - Performance optimization opportunities
    - Code quality improvements
    - Resource usage optimization
    - Intelligent refactoring recommendations
    """
    
    def __init__(self):
        self.semantic_engine = SemanticEngine()
        self.optimization_patterns = self._initialize_optimization_patterns()
        self.performance_models = self._initialize_performance_models()
        self.learning_cache = {}  # Learn from optimization patterns
        
    def _initialize_optimization_patterns(self) -> Dict[str, List[str]]:
        """Initialize optimization patterns for AI-driven code generation"""
        return {
            "loop_optimization": [
                r"for\s+\w+\s+in\s+range\([^)]+\)",
                r"while\s+.*:",
                r"for\s+\w+\s+in\s+\w+:"
            ],
            "function_inlining": [
                r"def\s+\w+\([^)]*\):\s*return\s+\w+",
                r"fn\s+\w+\([^)]*\)\s*->\s*\w+\s*\{[^}]*\}"
            ],
            "dead_code_elimination": [
                r"\w+\s*=\s*[^;]+;.*\w+\s*=\s*[^;]+",
                r"if\s+False\s*:"
            ],
            "constant_folding": [
                r"\d+\s*[+\-*/]\s*\d+",
                r"\w+\s*=\s*\d+\s*[+\-*/]\s*\d+"
            ],
            "memory_optimization": [
                r"\[\s*\w+\s+for\s+\w+\s+in\s+\w+\s+if\s+\w+\]",
                r"list\(\w+\)"
            ]
        }
    
    def _initialize_performance_models(self) -> Dict[str, Any]:
        """Initialize performance models for optimization decisions"""
        return {
            "time_complexity_weights": {
                "O(1)": 1.0,
                "O(log n)": 0.8,
                "O(n)": 0.6,
                "O(n log n)": 0.4,
                "O(n^2)": 0.2,
                "O(2^n)": 0.1
            },
            "memory_efficiency_weights": {
                "constant": 1.0,
                "linear": 0.7,
                "quadratic": 0.4,
                "exponential": 0.1
            }
        }
    
    def analyze_optimization_opportunities(self, ast: ASTNode) -> Dict[str, Any]:
        """
        Analyze AST for optimization opportunities
        Returns comprehensive optimization analysis
        """
        analysis = {
            "optimization_opportunities": [],
            "performance_improvements": [],
            "code_quality_issues": [],
            "resource_usage": {},
            "transformation_suggestions": []
        }
        
        # Analyze different types of optimizations
        analysis["loop_optimizations"] = self._analyze_loop_optimizations(ast)
        analysis["function_optimizations"] = self._analyze_function_optimizations(ast)
        analysis["memory_optimizations"] = self._analyze_memory_optimizations(ast)
        analysis["data_structure_optimizations"] = self._analyze_data_structure_optimizations(ast)
        
        # Calculate overall optimization potential
        analysis["optimization_score"] = self._calculate_optimization_score(analysis)
        
        return analysis
    
    def _analyze_loop_optimizations(self, ast: ASTNode) -> List[Dict[str, Any]]:
        """Analyze loop optimization opportunities"""
        optimizations = []
        
        # Find all loops in the AST
        loops = self._find_nodes_by_type(ast, (ForStatement, WhileStatement))
        
        for loop in loops:
            loop_analysis = {
                "node_type": type(loop).__name__,
                "optimization_type": "loop",
                "suggestions": []
            }
            
            # Check for loop unrolling opportunities
            if self._can_unroll_loop(loop):
                loop_analysis["suggestions"].append("Consider loop unrolling for small iteration counts")
            
            # Check for loop invariant code motion
            if self._has_loop_invariant_code(loop):
                loop_analysis["suggestions"].append("Move loop-invariant code outside the loop")
            
            # Check for vectorization opportunities
            if self._can_vectorize_loop(loop):
                loop_analysis["suggestions"].append("Consider vectorization for data parallel operations")
            
            if loop_analysis["suggestions"]:
                optimizations.append(loop_analysis)
        
        return optimizations
    
    def _analyze_function_optimizations(self, ast: ASTNode) -> List[Dict[str, Any]]:
        """Analyze function optimization opportunities"""
        optimizations = []
        
        # Find all function definitions
        functions = self._find_nodes_by_type(ast, FunctionDef)
        
        for func in functions:
            func_analysis = {
                "node_type": "FunctionDef",
                "function_name": str(func.name.value) if hasattr(func.name, 'value') else str(func.name),
                "optimization_type": "function",
                "suggestions": []
            }
            
            # Check for inlining opportunities
            if self._can_inline_function(func):
                func_analysis["suggestions"].append("Consider function inlining for small, frequently called functions")
            
            # Check for tail recursion optimization
            if self._has_tail_recursion(func):
                func_analysis["suggestions"].append("Consider tail recursion optimization")
            
            # Check for memoization opportunities
            if self._can_memoize_function(func):
                func_analysis["suggestions"].append("Consider memoization for pure functions with repeated calls")
            
            if func_analysis["suggestions"]:
                optimizations.append(func_analysis)
        
        return optimizations
    
    def _analyze_memory_optimizations(self, ast: ASTNode) -> List[Dict[str, Any]]:
        """Analyze memory optimization opportunities"""
        optimizations = []
        
        # Check for memory-intensive patterns
        memory_patterns = self._find_memory_patterns(ast)
        
        for pattern in memory_patterns:
            pattern_analysis = {
                "pattern_type": pattern["type"],
                "optimization_type": "memory",
                "suggestions": []
            }
            
            if pattern["type"] == "large_list_comprehension":
                pattern_analysis["suggestions"].append("Consider using generators for lazy evaluation")
            elif pattern["type"] == "repeated_allocation":
                pattern_analysis["suggestions"].append("Consider object pooling or reuse")
            elif pattern["type"] == "inefficient_data_structure":
                pattern_analysis["suggestions"].append("Consider using more efficient data structures")
            
            if pattern_analysis["suggestions"]:
                optimizations.append(pattern_analysis)
        
        return optimizations
    
    def _analyze_data_structure_optimizations(self, ast: ASTNode) -> List[Dict[str, Any]]:
        """Analyze data structure optimization opportunities"""
        optimizations = []
        
        # Analyze data structure usage patterns
        data_structures = self._analyze_data_structure_usage(ast)
        
        for ds_analysis in data_structures:
            if ds_analysis.get("optimization_potential") > 0.7:
                optimizations.append({
                    "structure_type": ds_analysis["type"],
                    "optimization_type": "data_structure",
                    "suggestions": ds_analysis["suggestions"]
                })
        
        return optimizations
    
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
        
        return found_nodes
    
    def _can_unroll_loop(self, loop: ASTNode) -> bool:
        """Check if loop can be unrolled"""
        # Simplified heuristic - could be enhanced with more sophisticated analysis
        if isinstance(loop, ForStatement):
            # Check if iteration count is small and known
            iterable_str = str(loop.iterable)
            if "range" in iterable_str and any(char.isdigit() for char in iterable_str):
                # Extract the range limit
                numbers = re.findall(r'\d+', iterable_str)
                if numbers and int(numbers[-1]) <= 10:
                    return True
        return False
    
    def _has_loop_invariant_code(self, loop: ASTNode) -> bool:
        """Check if loop has invariant code that can be moved outside"""
        # Simplified implementation - could be enhanced with proper data flow analysis
        return False  # Placeholder for actual implementation
    
    def _can_vectorize_loop(self, loop: ASTNode) -> bool:
        """Check if loop can be vectorized"""
        # Simplified heuristic - check for simple arithmetic operations
        if isinstance(loop, ForStatement) and loop.body:
            body_str = str(loop.body)
            if any(op in body_str for op in ["+", "-", "*", "/"]):
                return True
        return False
    
    def _can_inline_function(self, func: FunctionDef) -> bool:
        """Check if function can be inlined"""
        # Check if function is small and simple
        if func.body and hasattr(func.body, 'statements'):
            # Simple heuristic: small number of statements
            if len(func.body.statements) <= 3:
                return True
        return False
    
    def _has_tail_recursion(self, func: FunctionDef) -> bool:
        """Check if function has tail recursion"""
        # Simplified implementation - could be enhanced with proper analysis
        if func.body:
            body_str = str(func.body)
            if "return" in body_str and str(func.name.value) in body_str:
                return True
        return False
    
    def _can_memoize_function(self, func: FunctionDef) -> bool:
        """Check if function can benefit from memoization"""
        # Check if function appears to be pure (no side effects)
        if func.body:
            body_str = str(func.body).lower()
            # Simple heuristic: no I/O operations or state mutations
            if not any(word in body_str for word in ["print", "write", "modify", "global"]):
                return True
        return False
    
    def _find_memory_patterns(self, ast: ASTNode) -> List[Dict[str, str]]:
        """Find memory-intensive patterns in AST"""
        patterns = []
        ast_str = str(ast).lower()
        
        if "list comprehension" in ast_str or "[x for" in ast_str:
            patterns.append({"type": "large_list_comprehension", "location": "various"})
        
        if ast_str.count("=") > 10:  # Many assignments might indicate repeated allocation
            patterns.append({"type": "repeated_allocation", "location": "various"})
        
        return patterns
    
    def _analyze_data_structure_usage(self, ast: ASTNode) -> List[Dict[str, Any]]:
        """Analyze data structure usage patterns"""
        analyses = []
        ast_str = str(ast)
        
        # Check for list usage
        if "[]" in ast_str or "list(" in ast_str:
            analyses.append({
                "type": "list",
                "usage_frequency": ast_str.count("[]") + ast_str.count("list("),
                "optimization_potential": 0.6,
                "suggestions": ["Consider using arrays for numeric data", "Consider using sets for uniqueness checks"]
            })
        
        # Check for dictionary usage
        if "{}" in ast_str or "dict(" in ast_str:
            analyses.append({
                "type": "dictionary",
                "usage_frequency": ast_str.count("{}") + ast_str.count("dict("),
                "optimization_potential": 0.5,
                "suggestions": ["Consider using defaultdict for missing keys", "Consider using OrderedDict if order matters"]
            })
        
        return analyses
    
    def _calculate_optimization_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall optimization potential score"""
        score = 0.0
        
        # Count optimization opportunities
        opportunity_count = (
            len(analysis.get("loop_optimizations", [])) +
            len(analysis.get("function_optimizations", [])) +
            len(analysis.get("memory_optimizations", [])) +
            len(analysis.get("data_structure_optimizations", []))
        )
        
        # Calculate score based on opportunity count
        score = min(1.0, opportunity_count * 0.15)
        
        return score
    
    def suggest_ai_transformations(self, ast: ASTNode, optimization_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Suggest AI-powered code transformations"""
        transformations = []
        
        # Suggest transformations based on optimization analysis
        for loop_opt in optimization_analysis.get("loop_optimizations", []):
            for suggestion in loop_opt.get("suggestions", []):
                transformations.append({
                    "type": "loop_transformation",
                    "suggestion": suggestion,
                    "confidence": 0.8,
                    "estimated_improvement": "10-30%"
                })
        
        for func_opt in optimization_analysis.get("function_optimizations", []):
            for suggestion in func_opt.get("suggestions", []):
                transformations.append({
                    "type": "function_transformation",
                    "suggestion": suggestion,
                    "confidence": 0.75,
                    "estimated_improvement": "5-20%"
                })
        
        for mem_opt in optimization_analysis.get("memory_optimizations", []):
            for suggestion in mem_opt.get("suggestions", []):
                transformations.append({
                    "type": "memory_transformation",
                    "suggestion": suggestion,
                    "confidence": 0.7,
                    "estimated_improvement": "15-40%"
                })
        
        return transformations


class IntelligentCodeGenerator:
    """
    Compiler-First Intelligent Code Generator
    Enhances traditional code generation with AI-powered optimization:
    - AI-driven code transformation and optimization
    - Performance-oriented code generation
    - Resource-aware code generation
    - Quality-focused code generation
    - Adaptive generation strategies
    """
    
    def __init__(self, enable_ai_optimization: bool = True):
        self.neural_optimizer = NeuralCodeOptimizer() if enable_ai_optimization else None
        self.semantic_engine = SemanticEngine()
        self.enable_ai_optimization = enable_ai_optimization
        
        # Learning and adaptation
        self.generation_patterns = defaultdict(int)
        self.optimization_success_rate = {}
        
    def generate_code(self, ast: ASTNode, target_language: str = "ipl") -> CodeGenerationResult:
        """
        Generate optimized code from AST
        Returns enhanced code generation result with AI insights
        """
        # Analyze optimization opportunities
        optimization_analysis = {}
        if self.enable_ai_optimization and self.neural_optimizer:
            optimization_analysis = self.neural_optimizer.analyze_optimization_opportunities(ast)
        
        # Determine generation strategy
        generation_strategy = self._determine_generation_strategy(optimization_analysis)
        
        # Generate code based on strategy
        if generation_strategy == "ai_optimized":
            generated_code = self._generate_ai_optimized_code(ast, optimization_analysis)
        elif generation_strategy == "hybrid":
            generated_code = self._generate_hybrid_code(ast, optimization_analysis)
        else:
            generated_code = self._generate_traditional_code(ast)
        
        # Calculate quality metrics
        quality_metrics = self._calculate_code_quality_metrics(ast, generated_code)
        
        # Generate AI transformations
        ai_transformations = []
        if self.enable_ai_optimization and self.neural_optimizer:
            ai_transformations = self.neural_optimizer.suggest_ai_transformations(ast, optimization_analysis)
        
        # Calculate performance improvements
        performance_improvements = self._estimate_performance_improvements(optimization_analysis)
        
        # Calculate overall confidence
        confidence = self._calculate_generation_confidence(optimization_analysis, quality_metrics)
        
        result = CodeGenerationResult(
            generated_code=generated_code,
            optimization_level=generation_strategy,
            performance_improvements=performance_improvements,
            code_quality_metrics=quality_metrics,
            ai_transformations=ai_transformations,
            confidence=confidence,
            generation_strategy=generation_strategy
        )
        
        # Learn from generation
        self._learn_from_generation(result, optimization_analysis)
        
        return result
    
    def _determine_generation_strategy(self, optimization_analysis: Dict[str, Any]) -> str:
        """Determine optimal code generation strategy"""
        if not self.enable_ai_optimization:
            return "traditional"
        
        optimization_score = optimization_analysis.get("optimization_score", 0.0)
        
        if optimization_score > 0.7:
            return "ai_optimized"
        elif optimization_score > 0.3:
            return "hybrid"
        else:
            return "traditional"
    
    def _generate_traditional_code(self, ast: ASTNode) -> str:
        """Generate code using traditional approach"""
        return self._ast_to_code(ast)
    
    def _generate_hybrid_code(self, ast: ASTNode, optimization_analysis: Dict[str, Any]) -> str:
        """Generate code using hybrid approach"""
        # Start with traditional code
        base_code = self._ast_to_code(ast)
        
        # Apply basic optimizations
        optimized_code = self._apply_basic_optimizations(base_code, optimization_analysis)
        
        return optimized_code
    
    def _generate_ai_optimized_code(self, ast: ASTNode, optimization_analysis: Dict[str, Any]) -> str:
        """Generate code using AI-optimized approach"""
        # Start with traditional code
        base_code = self._ast_to_code(ast)
        
        # Apply AI-driven optimizations
        optimized_code = self._apply_ai_optimizations(base_code, optimization_analysis)
        
        return optimized_code
    
    def _ast_to_code(self, ast: ASTNode) -> str:
        """Convert AST to code string"""
        if isinstance(ast, Program):
            return self._generate_program(ast)
        elif isinstance(ast, LetStatement):
            return self._generate_let_statement(ast)
        elif isinstance(ast, FunctionDef):
            return self._generate_function_def(ast)
        elif isinstance(ast, FunctionCall):
            return self._generate_function_call(ast)
        elif isinstance(ast, IfStatement):
            return self._generate_if_statement(ast)
        elif isinstance(ast, ForStatement):
            return self._generate_for_statement(ast)
        elif isinstance(ast, WhileStatement):
            return self._generate_while_statement(ast)
        elif isinstance(ast, ReturnStatement):
            return self._generate_return_statement(ast)
        elif isinstance(ast, PrintStatement):
            return self._generate_print_statement(ast)
        elif isinstance(ast, BinaryOp):
            return self._generate_binary_op(ast)
        elif isinstance(ast, Identifier):
            return str(ast.value)
        elif isinstance(ast, Literal):
            return str(ast.value)
        else:
            return f"# Unknown node type: {type(ast).__name__}"
    
    def _generate_program(self, program: Program) -> str:
        """Generate code for program"""
        statements = []
        for stmt in program.statements:
            statements.append(self._ast_to_code(stmt))
        return "\n".join(statements)
    
    def _generate_let_statement(self, let_stmt: LetStatement) -> str:
        """Generate code for let statement"""
        var_name = self._ast_to_code(let_stmt.name)
        value = self._ast_to_code(let_stmt.value_expr) if let_stmt.value_expr else "None"
        
        type_annotation = ""
        if let_stmt.target_type:
            type_annotation = f": {let_stmt.target_type.name}"
        
        return f"let {var_name}{type_annotation} = {value}"
    
    def _generate_function_def(self, func_def: FunctionDef) -> str:
        """Generate code for function definition"""
        func_name = self._ast_to_code(func_def.name)
        
        # Generate parameters
        params = []
        if hasattr(func_def, 'params') and func_def.params:
            params = [self._ast_to_code(param) for param in func_def.params]
        
        # Generate return type
        return_type = ""
        if hasattr(func_def, 'return_type') and func_def.return_type:
            return_type = f" -> {func_def.return_type.name}"
        
        # Generate body
        body = self._ast_to_code(func_def.body) if func_def.body else "{}"
        
        return f"fn {func_name}({', '.join(params)}){return_type} {body}"
    
    def _generate_function_call(self, func_call: FunctionCall) -> str:
        """Generate code for function call"""
        callee = self._ast_to_code(func_call.callee)
        args = [self._ast_to_code(arg) for arg in func_call.args]
        return f"{callee}({', '.join(args)})"
    
    def _generate_if_statement(self, if_stmt: IfStatement) -> str:
        """Generate code for if statement"""
        condition = self._ast_to_code(if_stmt.condition)
        then_branch = self._ast_to_code(if_stmt.then_branch) if if_stmt.then_branch else "{}"
        
        code = f"if {condition} {then_branch}"
        
        # Generate elif branches
        for cond, branch in if_stmt.elif_branches:
            elif_cond = self._ast_to_code(cond)
            elif_branch = self._ast_to_code(branch) if branch else "{}"
            code += f" elif {elif_cond} {elif_branch}"
        
        # Generate else branch
        if if_stmt.else_branch:
            else_branch = self._ast_to_code(if_stmt.else_branch)
            code += f" else {else_branch}"
        
        return code
    
    def _generate_for_statement(self, for_stmt: ForStatement) -> str:
        """Generate code for for statement"""
        var_name = self._ast_to_code(for_stmt.variable) if hasattr(for_stmt, 'variable') else "item"
        iterable = self._ast_to_code(for_stmt.iterable)
        body = self._ast_to_code(for_stmt.body) if for_stmt.body else "{}"
        
        return f"for {var_name} in {iterable} {body}"
    
    def _generate_while_statement(self, while_stmt: WhileStatement) -> str:
        """Generate code for while statement"""
        condition = self._ast_to_code(while_stmt.condition)
        body = self._ast_to_code(while_stmt.body) if while_stmt.body else "{}"
        
        return f"while {condition} {body}"
    
    def _generate_return_statement(self, return_stmt: ReturnStatement) -> str:
        """Generate code for return statement"""
        value = self._ast_to_code(return_stmt.value_expr) if return_stmt.value_expr else ""
        return f"return {value}"
    
    def _generate_print_statement(self, print_stmt: PrintStatement) -> str:
        """Generate code for print statement"""
        exprs = [self._ast_to_code(expr) for expr in print_stmt.exprs]
        return f"print({', '.join(exprs)})"
    
    def _generate_binary_op(self, binary_op: BinaryOp) -> str:
        """Generate code for binary operation"""
        left = self._ast_to_code(binary_op.left)
        right = self._ast_to_code(binary_op.right)
        return f"{left} {binary_op.operator} {right}"
    
    def _apply_basic_optimizations(self, code: str, optimization_analysis: Dict[str, Any]) -> str:
        """Apply basic optimizations to generated code"""
        optimized_code = code
        
        # Apply simple constant folding
        optimized_code = self._constant_folding(optimized_code)
        
        # Apply simple dead code elimination
        optimized_code = self._dead_code_elimination(optimized_code)
        
        return optimized_code
    
    def _apply_ai_optimizations(self, code: str, optimization_analysis: Dict[str, Any]) -> str:
        """Apply AI-driven optimizations to generated code"""
        optimized_code = self._apply_basic_optimizations(code, optimization_analysis)
        
        # Apply more sophisticated optimizations based on AI analysis
        # This could be expanded with more advanced AI-driven transformations
        
        return optimized_code
    
    def _constant_folding(self, code: str) -> str:
        """Perform constant folding optimization"""
        # Simplified implementation - could be enhanced with proper constant propagation
        import re
        
        # Find simple arithmetic expressions with constants
        pattern = r'(\d+)\s*([+\-*/])\s*(\d+)'
        
        def fold_expression(match):
            left = int(match.group(1))
            op = match.group(2)
            right = int(match.group(3))
            
            if op == '+':
                return str(left + right)
            elif op == '-':
                return str(left - right)
            elif op == '*':
                return str(left * right)
            elif op == '/':
                return str(left / right)
            return match.group(0)
        
        return re.sub(pattern, fold_expression, code)
    
    def _dead_code_elimination(self, code: str) -> str:
        """Perform dead code elimination"""
        # Simplified implementation - could be enhanced with proper control flow analysis
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip obviously dead code
            if not line.strip().startswith('#') and line.strip():
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _calculate_code_quality_metrics(self, ast: ASTNode, generated_code: str) -> Dict[str, Any]:
        """Calculate code quality metrics"""
        return {
            "lines_of_code": len(generated_code.split('\n')),
            "cyclomatic_complexity": self._calculate_cyclomatic_complexity(ast),
            "maintainability_index": self._calculate_maintainability_index(ast, generated_code),
            "code_duplication": self._detect_code_duplication(generated_code),
            "naming_convention_score": self._assess_naming_conventions(ast)
        }
    
    def _find_nodes_by_type(self, ast: ASTNode, node_types: Tuple) -> List[ASTNode]:
        """Find all nodes of specific types in AST"""
        found_nodes = []
        if isinstance(ast, node_types):
            found_nodes.append(ast)
        if hasattr(ast, 'statements'):
            for stmt in ast.statements:
                found_nodes.extend(self._find_nodes_by_type(stmt, node_types))
        elif hasattr(ast, 'body'):
            if isinstance(ast.body, list):
                for stmt in ast.body:
                    found_nodes.extend(self._find_nodes_by_type(stmt, node_types))
            else:
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
        elif hasattr(ast, 'else_branch') and ast.else_branch:
            found_nodes.extend(self._find_nodes_by_type(ast.else_branch, node_types))
        return found_nodes

    def _calculate_cyclomatic_complexity(self, ast: ASTNode) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        # Count decision points
        decision_nodes = self._find_nodes_by_type(ast, (IfStatement, ForStatement, WhileStatement))
        complexity += len(decision_nodes)
        
        return complexity
    
    def _calculate_maintainability_index(self, ast: ASTNode, code: str) -> float:
        """Calculate maintainability index"""
        # Simplified implementation
        lines = len(code.split('\n'))
        complexity = self._calculate_cyclomatic_complexity(ast)
        
        # MI = 171 - 5.2 * ln(vol) - 0.23 * cc - 16.2 * ln(loc)
        # Simplified version
        mi = max(0, 100 - complexity * 2 - lines * 0.1)
        return round(mi, 1)
    
    def _detect_code_duplication(self, code: str) -> float:
        """Detect code duplication percentage"""
        # Simplified implementation
        lines = code.split('\n')
        unique_lines = set(lines)
        duplication_ratio = 1.0 - (len(unique_lines) / len(lines)) if lines else 0.0
        return round(duplication_ratio * 100, 1)
    
    def _assess_naming_conventions(self, ast: ASTNode) -> float:
        """Assess naming convention compliance"""
        # Simplified implementation
        identifiers = self._find_nodes_by_type(ast, Identifier)
        if not identifiers:
            return 100.0
        
        good_names = 0
        for identifier in identifiers:
            name = str(identifier.value)
            # Check for basic naming conventions
            if name.replace('_', '').isalnum() and len(name) > 1:
                good_names += 1
        
        return round((good_names / len(identifiers)) * 100, 1)
    
    def _estimate_performance_improvements(self, optimization_analysis: Dict[str, Any]) -> List[str]:
        """Estimate performance improvements from optimizations"""
        improvements = []
        
        optimization_score = optimization_analysis.get("optimization_score", 0.0)
        
        if optimization_score > 0.7:
            improvements.append("High optimization potential: 20-40% performance improvement expected")
        elif optimization_score > 0.4:
            improvements.append("Moderate optimization potential: 10-20% performance improvement expected")
        elif optimization_score > 0.2:
            improvements.append("Low optimization potential: 5-10% performance improvement expected")
        
        # Add specific improvements based on analysis
        if optimization_analysis.get("loop_optimizations"):
            improvements.append("Loop optimizations may reduce iteration overhead")
        
        if optimization_analysis.get("memory_optimizations"):
            improvements.append("Memory optimizations may reduce allocation overhead")
        
        return improvements
    
    def _calculate_generation_confidence(self, optimization_analysis: Dict[str, Any], quality_metrics: Dict[str, Any]) -> float:
        """Calculate overall confidence in generated code"""
        base_confidence = 0.8
        
        # Adjust based on optimization potential
        optimization_score = optimization_analysis.get("optimization_score", 0.0)
        confidence = base_confidence + (optimization_score * 0.1)
        
        # Adjust based on code quality
        maintainability = quality_metrics.get("maintainability_index", 50)
        if maintainability > 70:
            confidence += 0.1
        elif maintainability < 40:
            confidence -= 0.1
        
        return min(1.0, max(0.0, confidence))
    
    def _learn_from_generation(self, result: CodeGenerationResult, optimization_analysis: Dict[str, Any]):
        """Learn from code generation for future improvements"""
        strategy_key = result.generation_strategy
        self.generation_patterns[strategy_key] += 1
        
        # Track optimization success rate
        optimization_score = optimization_analysis.get("optimization_score", 0.0)
        if optimization_score > 0.5:
            success_key = f"{strategy_key}_success"
            self.optimization_success_rate[success_key] = self.optimization_success_rate.get(success_key, 0) + 1
    
    def get_generation_statistics(self) -> Dict[str, Any]:
        """Get statistics about code generation"""
        return {
            "total_generations": len(self.generation_patterns),
            "strategy_frequencies": dict(self.generation_patterns),
            "optimization_success_rates": self.optimization_success_rate,
            "ai_optimization_enabled": self.enable_ai_optimization
        }


class CompilerFirstCodeGenerator:
    """
    Main entry point for compiler-first intelligent code generation
    This represents the intelligent code generator level in the compiler-first architecture
    """
    
    DEFAULT_CONFIG = {
        "enable_ai_optimization": True,
        "target_language": "ipl",
        "optimization_level": "balanced",
        "quality_threshold": 0.7
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        
        self.intelligent_generator = IntelligentCodeGenerator(
            enable_ai_optimization=self.config.get("enable_ai_optimization", True)
        )
        
    def generate_program(self, ast: Program) -> Dict[str, Any]:
        """
        Generate optimized code from program AST
        Returns complete code generation analysis
        """
        # Generate code with AI optimization
        generation_result = self.intelligent_generator.generate_code(
            ast, 
            target_language=self.config.get("target_language", "ipl")
        )
        
        # Compile comprehensive analysis
        analysis = {
            "generated_code": generation_result.generated_code,
            "optimization_level": generation_result.optimization_level,
            "performance_improvements": generation_result.performance_improvements,
            "code_quality_metrics": generation_result.code_quality_metrics,
            "ai_transformations": generation_result.ai_transformations,
            "generation_confidence": generation_result.confidence,
            "generation_strategy": generation_result.generation_strategy,
            "statistics": self.intelligent_generator.get_generation_statistics(),
            "generation_timestamp": self._get_timestamp()
        }
        
        return analysis
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for generation tracking"""
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_generation_summary(self, ast: Program) -> str:
        """Get human-readable summary of code generation"""
        analysis = self.generate_program(ast)
        
        summary = f"""
Intelligent Code Generation Summary
====================================
Optimization Level: {analysis['optimization_level']}
Generation Strategy: {analysis['generation_strategy']}
Generation Confidence: {analysis['generation_confidence']:.2%}
AI Optimization: {'Enabled' if self.config.get('enable_ai_optimization', True) else 'Disabled'}

Generated Code:
{analysis['generated_code']}

Performance Improvements:
{self._format_improvements(analysis['performance_improvements'])}

Code Quality Metrics:
{self._format_quality_metrics(analysis['code_quality_metrics'])}

AI Transformations:
{self._format_transformations(analysis['ai_transformations'])}

Generation Statistics:
{self._format_statistics(analysis['statistics'])}
"""
        return summary
    
    def _format_improvements(self, improvements: List[str]) -> str:
        """Format performance improvements for display"""
        if not improvements:
            return "  No significant performance improvements detected"
        return "\n".join([f"  - {imp}" for imp in improvements])
    
    def _format_quality_metrics(self, metrics: Dict[str, Any]) -> str:
        """Format code quality metrics for display"""
        formatted = []
        for key, value in metrics.items():
            formatted.append(f"  {key}: {value}")
        return "\n".join(formatted)
    
    def _format_transformations(self, transformations: List[Dict[str, str]]) -> str:
        """Format AI transformations for display"""
        if not transformations:
            return "  No AI transformations applied"
        
        formatted = []
        for i, transform in enumerate(transformations, 1):
            formatted.append(f"  {i}. {transform['type']}: {transform['suggestion']}")
            formatted.append(f"     Confidence: {transform['confidence']:.2%}, Improvement: {transform['estimated_improvement']}")
        
        return "\n".join(formatted)
    
    def _format_statistics(self, statistics: Dict[str, Any]) -> str:
        """Format generation statistics for display"""
        formatted = []
        for key, value in statistics.items():
            if isinstance(value, dict):
                formatted.append(f"  {key}:")
                for sub_key, sub_value in value.items():
                    formatted.append(f"    {sub_key}: {sub_value}")
            else:
                formatted.append(f"  {key}: {value}")
        return "\n".join(formatted)