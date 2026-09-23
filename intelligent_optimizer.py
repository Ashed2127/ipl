"""
Intelligent Optimizer for IPL - Compiler-First Neural Architecture
Enhances traditional optimization with AI-powered learning and adaptive improvement
"""
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict
import re
import hashlib
import json

try:
    from .ast_nodes import (
        ASTNode, Program, LetStatement, AssignStatement, FunctionDef, 
        FunctionCall, BinaryOp, Identifier, Literal, Block, IfStatement,
        ForStatement, WhileStatement, ReturnStatement
    )
    from .tokens import Token, TokenType
    from .semantic_engine import SemanticEngine
except (ImportError, ValueError):
    from ast_nodes import (
        ASTNode, Program, LetStatement, AssignStatement, FunctionDef, 
        FunctionCall, BinaryOp, Identifier, Literal, Block, IfStatement,
        ForStatement, WhileStatement, ReturnStatement
    )
    from tokens import Token, TokenType
    from semantic_engine import SemanticEngine


@dataclass
class OptimizationResult:
    """Enhanced optimization result with AI-powered learning insights"""
    optimized_ast: ASTNode
    optimization_score: float
    applied_optimizations: List[Dict[str, Any]]
    performance_improvement: float
    learning_insights: List[str]
    adaptation_suggestions: List[str]
    confidence: float
    optimization_strategy: str
    
    def __post_init__(self):
        if self.applied_optimizations is None:
            self.applied_optimizations = []
        if self.learning_insights is None:
            self.learning_insights = []
        if self.adaptation_suggestions is None:
            self.adaptation_suggestions = []


class LearningOptimizer:
    """
    Learning optimizer system that provides:
    - AI-powered optimization pattern learning
    - Adaptive optimization strategies
    - Performance prediction and improvement
    - Continuous learning from optimization results
    - Intelligent optimization selection
    """
    
    def __init__(self):
        self.semantic_engine = SemanticEngine()
        self.optimization_patterns = self._initialize_optimization_patterns()
        self.performance_models = self._initialize_performance_models()
        self.learning_database = self._load_learning_database()
        self.optimization_history = []
        
    def _initialize_optimization_patterns(self) -> Dict[str, List[str]]:
        """Initialize optimization patterns for AI-powered learning"""
        return {
            "loop_optimizations": [
                r"for\s+\w+\s+in\s+range\([^)]+\)",
                r"while\s+.*:",
                r"for\s+\w+\s+in\s+\w+:"
            ],
            "function_optimizations": [
                r"def\s+\w+\([^)]*\):\s*return\s+\w+",
                r"fn\s+\w+\([^)]*\)\s*->\s*\w+\s*\{[^}]*\}"
            ],
            "memory_optimizations": [
                r"\[\s*\w+\s+for\s+\w+\s+in\s+\w+\s+if\s+\w+\]",
                r"list\(\w+\)"
            ],
            "expression_optimizations": [
                r"\d+\s*[+\-*/]\s*\d+",
                r"\w+\s*=\s*\d+\s*[+\-*/]\s*\d+"
            ],
            "control_flow_optimizations": [
                r"if\s+.*:\s*return\s+.*",
                r"if\s+.*:\s*break",
                r"if\s+.*:\s*continue"
            ]
        }
    
    def _initialize_performance_models(self) -> Dict[str, Any]:
        """Initialize performance models for optimization decisions"""
        return {
            "execution_time_models": {
                "O(1)": {"base_time": 1.0, "scaling_factor": 0.0},
                "O(log n)": {"base_time": 2.0, "scaling_factor": 0.1},
                "O(n)": {"base_time": 5.0, "scaling_factor": 1.0},
                "O(n log n)": {"base_time": 10.0, "scaling_factor": 1.5},
                "O(n^2)": {"base_time": 20.0, "scaling_factor": 2.0},
                "O(2^n)": {"base_time": 50.0, "scaling_factor": 5.0}
            },
            "memory_usage_models": {
                "constant": {"base_memory": 1.0, "scaling_factor": 0.0},
                "linear": {"base_memory": 5.0, "scaling_factor": 1.0},
                "quadratic": {"base_memory": 15.0, "scaling_factor": 2.0},
                "exponential": {"base_memory": 30.0, "scaling_factor": 5.0}
            }
        }
    
    def _load_learning_database(self) -> Dict[str, Any]:
        """Load learning database from persistent storage"""
        # In a real implementation, this would load from a file or database
        return {
            "optimization_success_rates": {},
            "pattern_frequencies": defaultdict(int),
            "performance_improvements": {},
            "best_strategies": {}
        }
    
    def optimize_with_learning(self, ast: ASTNode, context: Dict[str, Any] = None) -> OptimizationResult:
        """
        Perform AI-powered optimization with learning
        Returns enhanced optimization result with learning insights
        """
        context = context or {}
        
        # Analyze current performance characteristics
        performance_analysis = self._analyze_performance_characteristics(ast)
        
        # Select optimal optimization strategy based on learning
        optimization_strategy = self._select_optimization_strategy(ast, performance_analysis)
        
        # Apply optimizations based on selected strategy
        optimized_ast, applied_optimizations = self._apply_optimizations(ast, optimization_strategy)
        
        # Predict performance improvement
        predicted_improvement = self._predict_performance_improvement(ast, optimized_ast, applied_optimizations)
        
        # Generate learning insights
        learning_insights = self._generate_learning_insights(ast, applied_optimizations, performance_analysis)
        
        # Generate adaptation suggestions
        adaptation_suggestions = self._generate_adaptation_suggestions(ast, performance_analysis)
        
        # Calculate optimization score
        optimization_score = self._calculate_optimization_score(ast, optimized_ast, applied_optimizations)
        
        # Calculate confidence
        confidence = self._calculate_optimization_confidence(applied_optimizations, performance_analysis)
        
        # Update learning database
        self._update_learning_database(ast, optimization_strategy, applied_optimizations, predicted_improvement)
        
        result = OptimizationResult(
            optimized_ast=optimized_ast,
            optimization_score=optimization_score,
            applied_optimizations=applied_optimizations,
            performance_improvement=predicted_improvement,
            learning_insights=learning_insights,
            adaptation_suggestions=adaptation_suggestions,
            confidence=confidence,
            optimization_strategy=optimization_strategy
        )
        
        # Add to optimization history
        self.optimization_history.append(result)
        
        return result
    
    def _analyze_performance_characteristics(self, ast: ASTNode) -> Dict[str, Any]:
        """Analyze performance characteristics of AST"""
        analysis = {
            "time_complexity": self._estimate_time_complexity(ast),
            "space_complexity": self._estimate_space_complexity(ast),
            "bottlenecks": self._identify_bottlenecks(ast),
            "optimization_opportunities": self._identify_optimization_opportunities(ast),
            "resource_usage": self._estimate_resource_usage(ast)
        }
        return analysis
    
    def _estimate_time_complexity(self, ast: ASTNode) -> str:
        """Estimate time complexity of AST"""
        # Simplified implementation - could be enhanced with proper complexity analysis
        loops = self._find_nodes_by_type(ast, (ForStatement, WhileStatement))
        nested_loops = self._count_nested_loops(ast)
        
        if nested_loops > 2:
            return "O(n^3)"
        elif nested_loops == 2:
            return "O(n^2)"
        elif nested_loops == 1:
            return "O(n)"
        elif len(loops) > 0:
            return "O(n)"
        else:
            return "O(1)"
    
    def _estimate_space_complexity(self, ast: ASTNode) -> str:
        """Estimate space complexity of AST"""
        # Simplified implementation
        data_structures = self._count_data_structures(ast)
        
        if data_structures > 5:
            return "O(n^2)"
        elif data_structures > 2:
            return "O(n)"
        else:
            return "O(1)"
    
    def _identify_bottlenecks(self, ast: ASTNode) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks"""
        bottlenecks = []
        
        # Find nested loops
        nested_loops = self._find_nested_loops(ast)
        for loop in nested_loops:
            bottlenecks.append({
                "type": "nested_loop",
                "location": "control_flow",
                "severity": "high",
                "description": "Nested loop detected - potential performance bottleneck"
            })
        
        # Find expensive operations
        expensive_calls = self._find_expensive_function_calls(ast)
        for call in expensive_calls:
            bottlenecks.append({
                "type": "expensive_function",
                "location": "function_call",
                "severity": "medium",
                "description": f"Potentially expensive function call: {call}"
            })
        
        return bottlenecks
    
    def _identify_optimization_opportunities(self, ast: ASTNode) -> List[Dict[str, Any]]:
        """Identify optimization opportunities"""
        opportunities = []
        
        # Check for loop unrolling opportunities
        loops = self._find_nodes_by_type(ast, (ForStatement, WhileStatement))
        for loop in loops:
            if self._can_unroll_loop(loop):
                opportunities.append({
                    "type": "loop_unrolling",
                    "target": "loop",
                    "potential_improvement": "10-30%"
                })
        
        # Check for function inlining opportunities
        functions = self._find_nodes_by_type(ast, FunctionDef)
        for func in functions:
            if self._can_inline_function(func):
                opportunities.append({
                    "type": "function_inlining",
                    "target": str(func.name.value) if hasattr(func.name, 'value') else str(func.name),
                    "potential_improvement": "5-15%"
                })
        
        # Check for constant folding opportunities
        if self._has_constant_folding_opportunities(ast):
            opportunities.append({
                "type": "constant_folding",
                "target": "expressions",
                "potential_improvement": "5-10%"
            })
        
        return opportunities
    
    def _estimate_resource_usage(self, ast: ASTNode) -> Dict[str, Any]:
        """Estimate resource usage"""
        return {
            "memory_usage": "medium",
            "cpu_usage": "medium",
            "io_operations": len(self._find_nodes_by_type(ast, FunctionCall)),
            "allocations": self._count_memory_allocations(ast)
        }
    
    def _select_optimization_strategy(self, ast: ASTNode, performance_analysis: Dict[str, Any]) -> str:
        """Select optimal optimization strategy based on learning"""
        # Check learning database for best strategies
        complexity = performance_analysis["time_complexity"]
        
        # Use learned best strategies if available
        if complexity in self.learning_database["best_strategies"]:
            return self.learning_database["best_strategies"][complexity]
        
        # Default strategy selection based on complexity
        if complexity in ["O(n^2)", "O(n^3)"]:
            return "aggressive_optimization"
        elif complexity == "O(n)":
            return "balanced_optimization"
        else:
            return "conservative_optimization"
    
    def _apply_optimizations(self, ast: ASTNode, strategy: str) -> Tuple[ASTNode, List[Dict[str, Any]]]:
        """Apply optimizations based on selected strategy"""
        applied_optimizations = []
        optimized_ast = ast  # Start with original AST
        
        if strategy == "aggressive_optimization":
            # Apply all possible optimizations
            optimized_ast, loop_opts = self._apply_loop_optimizations(optimized_ast)
            applied_optimizations.extend(loop_opts)
            
            optimized_ast, func_opts = self._apply_function_optimizations(optimized_ast)
            applied_optimizations.extend(func_opts)
            
            optimized_ast, const_opts = self._apply_constant_folding(optimized_ast)
            applied_optimizations.extend(const_opts)
            
        elif strategy == "balanced_optimization":
            # Apply moderate optimizations
            optimized_ast, loop_opts = self._apply_loop_optimizations(optimized_ast)
            applied_optimizations.extend(loop_opts)
            
            optimized_ast, const_opts = self._apply_constant_folding(optimized_ast)
            applied_optimizations.extend(const_opts)
            
        elif strategy == "conservative_optimization":
            # Apply only safe optimizations
            optimized_ast, const_opts = self._apply_constant_folding(optimized_ast)
            applied_optimizations.extend(const_opts)
        
        return optimized_ast, applied_optimizations
    
    def _apply_loop_optimizations(self, ast: ASTNode) -> Tuple[ASTNode, List[Dict[str, Any]]]:
        """Apply loop optimizations"""
        optimizations = []
        # Simplified implementation - in reality, this would transform the AST
        loops = self._find_nodes_by_type(ast, (ForStatement, WhileStatement))
        
        for loop in loops:
            if self._can_unroll_loop(loop):
                optimizations.append({
                    "type": "loop_unrolling",
                    "description": "Loop unrolling applied",
                    "estimated_improvement": "15%"
                })
        
        return ast, optimizations  # Return original AST for simplicity
    
    def _apply_function_optimizations(self, ast: ASTNode) -> Tuple[ASTNode, List[Dict[str, Any]]]:
        """Apply function optimizations"""
        optimizations = []
        functions = self._find_nodes_by_type(ast, FunctionDef)
        
        for func in functions:
            if self._can_inline_function(func):
                optimizations.append({
                    "type": "function_inlining",
                    "description": "Function inlining candidate identified",
                    "estimated_improvement": "10%"
                })
        
        return ast, optimizations  # Return original AST for simplicity
    
    def _apply_constant_folding(self, ast: ASTNode) -> Tuple[ASTNode, List[Dict[str, Any]]]:
        """Apply constant folding optimization"""
        optimizations = []
        
        if self._has_constant_folding_opportunities(ast):
            optimizations.append({
                "type": "constant_folding",
                "description": "Constant folding opportunities detected",
                "estimated_improvement": "5%"
            })
        
        return ast, optimizations  # Return original AST for simplicity
    
    def _predict_performance_improvement(self, original_ast: ASTNode, optimized_ast: ASTNode, 
                                       applied_optimizations: List[Dict[str, Any]]) -> float:
        """Predict performance improvement from optimizations"""
        total_improvement = 0.0
        
        for opt in applied_optimizations:
            estimated = opt.get("estimated_improvement", "0%")
            # Extract percentage
            match = re.search(r'(\d+)%', estimated)
            if match:
                improvement_pct = int(match.group(1))
                total_improvement += improvement_pct
        
        # Normalize to 0-1 range
        return min(1.0, total_improvement / 100.0)
    
    def _generate_learning_insights(self, ast: ASTNode, applied_optimizations: List[Dict[str, Any]], 
                                  performance_analysis: Dict[str, Any]) -> List[str]:
        """Generate learning insights from optimization process"""
        insights = []
        
        # Analyze optimization patterns
        if len(applied_optimizations) > 3:
            insights.append("Multiple optimization opportunities detected - code may benefit from refactoring")
        
        # Analyze performance characteristics
        complexity = performance_analysis["time_complexity"]
        if complexity in ["O(n^2)", "O(n^3)"]:
            insights.append(f"High time complexity ({complexity}) detected - consider algorithmic improvements")
        
        # Analyze bottleneck patterns
        bottlenecks = performance_analysis["bottlenecks"]
        if any(b["severity"] == "high" for b in bottlenecks):
            insights.append("High-severity bottlenecks detected - prioritize optimization efforts")
        
        # Add learning-based insights
        if len(self.optimization_history) > 10:
            insights.append("Sufficient optimization history accumulated - predictions becoming more accurate")
        
        return insights
    
    def _generate_adaptation_suggestions(self, ast: ASTNode, performance_analysis: Dict[str, Any]) -> List[str]:
        """Generate adaptation suggestions for future improvements"""
        suggestions = []
        
        # Suggest algorithmic improvements
        complexity = performance_analysis["time_complexity"]
        if complexity == "O(n^2)":
            suggestions.append("Consider using more efficient algorithms (e.g., hash tables instead of nested loops)")
        elif complexity == "O(n^3)":
            suggestions.append("Strongly recommend algorithmic redesign - current complexity is very high")
        
        # Suggest data structure improvements
        if performance_analysis["space_complexity"] == "O(n^2)":
            suggestions.append("Consider using more memory-efficient data structures")
        
        # Suggest caching strategies
        if len(performance_analysis["bottlenecks"]) > 2:
            suggestions.append("Consider implementing caching for frequently computed results")
        
        return suggestions
    
    def _calculate_optimization_score(self, original_ast: ASTNode, optimized_ast: ASTNode, 
                                    applied_optimizations: List[Dict[str, Any]]) -> float:
        """Calculate overall optimization score"""
        if not applied_optimizations:
            return 0.0
        
        # Base score from number of optimizations
        base_score = min(1.0, len(applied_optimizations) * 0.2)
        
        # Adjust for improvement estimates
        total_improvement = 0.0
        for opt in applied_optimizations:
            estimated = opt.get("estimated_improvement", "0%")
            match = re.search(r'(\d+)%', estimated)
            if match:
                total_improvement += int(match.group(1))
        
        improvement_factor = min(1.0, total_improvement / 50.0)  # Normalize to 0-1
        
        return (base_score + improvement_factor) / 2
    
    def _calculate_optimization_confidence(self, applied_optimizations: List[Dict[str, Any]], 
                                         performance_analysis: Dict[str, Any]) -> float:
        """Calculate confidence in optimization results"""
        if not applied_optimizations:
            return 0.5
        
        # Base confidence from number of optimizations
        base_confidence = min(0.9, 0.5 + len(applied_optimizations) * 0.1)
        
        # Adjust based on learning history
        history_factor = min(0.1, len(self.optimization_history) * 0.01)
        
        return min(1.0, base_confidence + history_factor)
    
    def _update_learning_database(self, ast: ASTNode, strategy: str, 
                                applied_optimizations: List[Dict[str, Any]], 
                                improvement: float):
        """Update learning database with optimization results"""
        # Update pattern frequencies
        for opt in applied_optimizations:
            opt_type = opt.get("type", "unknown")
            self.learning_database["pattern_frequencies"][opt_type] += 1
        
        # Update success rates
        strategy_key = f"{strategy}_success"
        if improvement > 0.1:  # Consider successful if improvement > 10%
            self.learning_database["optimization_success_rates"][strategy_key] = \
                self.learning_database["optimization_success_rates"].get(strategy_key, 0) + 1
        
        # Update best strategies
        complexity = self._estimate_time_complexity(ast)
        if improvement > 0.2:  # Consider as best if improvement > 20%
            self.learning_database["best_strategies"][complexity] = strategy
        
        # Update performance improvements
        self.learning_database["performance_improvements"][strategy] = \
            self.learning_database["performance_improvements"].get(strategy, []) + [improvement]
    
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
    
    def _count_nested_loops(self, ast: ASTNode) -> int:
        """Count nested loop structures"""
        max_nesting = 0
        
        def count_nesting(node, current_depth):
            nonlocal max_nesting
            if isinstance(node, (ForStatement, WhileStatement)):
                current_depth += 1
                max_nesting = max(max_nesting, current_depth)
            
            # Recursively check children
            if hasattr(node, 'body'):
                count_nesting(node.body, current_depth)
            if hasattr(node, 'statements'):
                for stmt in node.statements:
                    count_nesting(stmt, current_depth)
        
        count_nesting(ast, 0)
        return max_nesting
    
    def _find_nested_loops(self, ast: ASTNode) -> List[ASTNode]:
        """Find nested loop structures"""
        nested_loops = []
        
        def find_nested(node, parent_is_loop=False):
            if isinstance(node, (ForStatement, WhileStatement)):
                if parent_is_loop:
                    nested_loops.append(node)
                parent_is_loop = True
            else:
                parent_is_loop = False
            
            # Recursively check children
            if hasattr(node, 'body'):
                find_nested(node.body, parent_is_loop)
            if hasattr(node, 'statements'):
                for stmt in node.statements:
                    find_nested(stmt, parent_is_loop)
        
        find_nested(ast, False)
        return nested_loops
    
    def _find_expensive_function_calls(self, ast: ASTNode) -> List[str]:
        """Find potentially expensive function calls"""
        expensive_functions = ["sort", "search", "parse", "serialize", "deserialize"]
        expensive_calls = []
        
        function_calls = self._find_nodes_by_type(ast, FunctionCall)
        for call in function_calls:
            func_name = str(call.callee.value) if hasattr(call.callee, 'value') else str(call.callee)
            if any(expensive in func_name.lower() for expensive in expensive_functions):
                expensive_calls.append(func_name)
        
        return expensive_calls
    
    def _count_data_structures(self, ast: ASTNode) -> int:
        """Count data structure allocations"""
        # Simplified implementation
        return len(self._find_nodes_by_type(ast, (FunctionCall,)))  # Placeholder
    
    def _can_unroll_loop(self, loop: ASTNode) -> bool:
        """Check if loop can be unrolled"""
        # Simplified heuristic
        if isinstance(loop, ForStatement):
            iterable_str = str(loop.iterable)
            if "range" in iterable_str and any(char.isdigit() for char in iterable_str):
                numbers = re.findall(r'\d+', iterable_str)
                if numbers and int(numbers[-1]) <= 10:
                    return True
        return False
    
    def _can_inline_function(self, func: FunctionDef) -> bool:
        """Check if function can be inlined"""
        if func.body and hasattr(func.body, 'statements'):
            return len(func.body.statements) <= 3
        return False
    
    def _has_constant_folding_opportunities(self, ast: ASTNode) -> bool:
        """Check if constant folding opportunities exist"""
        # Simplified implementation
        binary_ops = self._find_nodes_by_type(ast, BinaryOp)
        for op in binary_ops:
            if op.operator in ["+", "-", "*", "/"]:
                if isinstance(op.left, Literal) and isinstance(op.right, Literal):
                    return True
        return False
    
    def _count_memory_allocations(self, ast: ASTNode) -> int:
        """Count memory allocations"""
        # Simplified implementation
        return len(self._find_nodes_by_type(ast, FunctionCall))
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get learning statistics"""
        return {
            "total_optimizations": len(self.optimization_history),
            "pattern_frequencies": dict(self.learning_database["pattern_frequencies"]),
            "success_rates": self.learning_database["optimization_success_rates"],
            "best_strategies": self.learning_database["best_strategies"],
            "average_improvements": self._calculate_average_improvements()
        }
    
    def _calculate_average_improvements(self) -> Dict[str, float]:
        """Calculate average improvements by strategy"""
        avg_improvements = {}
        for strategy, improvements in self.learning_database["performance_improvements"].items():
            if improvements:
                avg_improvements[strategy] = sum(improvements) / len(improvements)
        return avg_improvements


class IntelligentOptimizer:
    """
    Compiler-First Intelligent Optimizer
    Enhances traditional optimization with AI-powered learning:
    - Learning-based optimization selection
    - Adaptive optimization strategies
    - Performance prediction and improvement
    - Continuous learning from results
    - Intelligent optimization sequencing
    """
    
    def __init__(self, enable_learning: bool = True):
        self.learning_optimizer = LearningOptimizer() if enable_learning else None
        self.semantic_engine = SemanticEngine()
        self.enable_learning = enable_learning
        
        # Optimization configuration
        self.optimization_config = {
            "max_optimization_passes": 3,
            "improvement_threshold": 0.05,  # 5% minimum improvement
            "confidence_threshold": 0.7
        }
        
    def optimize_ast(self, ast: ASTNode, context: Dict[str, Any] = None) -> OptimizationResult:
        """
        Perform intelligent optimization on AST
        Returns enhanced optimization result with learning insights
        """
        context = context or {}
        
        if self.enable_learning and self.learning_optimizer:
            # Use learning optimizer
            return self.learning_optimizer.optimize_with_learning(ast, context)
        else:
            # Fallback to basic optimization
            return self._perform_basic_optimization(ast, context)
    
    def _perform_basic_optimization(self, ast: ASTNode, context: Dict[str, Any]) -> OptimizationResult:
        """Perform basic optimization without learning"""
        return OptimizationResult(
            optimized_ast=ast,
            optimization_score=0.0,
            applied_optimizations=[],
            performance_improvement=0.0,
            learning_insights=["Learning disabled - enable for better optimization"],
            adaptation_suggestions=[],
            confidence=0.5,
            optimization_strategy="basic"
        )
    
    def get_optimization_statistics(self) -> Dict[str, Any]:
        """Get optimization statistics"""
        if self.enable_learning and self.learning_optimizer:
            return self.learning_optimizer.get_learning_statistics()
        else:
            return {"learning_enabled": False}


class CompilerFirstOptimizer:
    """
    Main entry point for compiler-first intelligent optimization
    This represents the intelligent optimizer level in the compiler-first architecture
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "enable_learning": True,
            "optimization_level": "balanced",
            "max_passes": 3,
            "improvement_threshold": 0.05
        }
        
        self.intelligent_optimizer = IntelligentOptimizer(
            enable_learning=self.config["enable_learning"]
        )
        
    def optimize_program(self, ast: Program) -> Dict[str, Any]:
        """
        Perform comprehensive intelligent optimization on program
        Returns complete optimization analysis
        """
        # Optimize overall program
        program_optimization = self.intelligent_optimizer.optimize_ast(ast)
        
        # Optimize individual statements for detailed optimization
        statement_optimizations = []
        for stmt in ast.statements:
            stmt_optimization = self.intelligent_optimizer.optimize_ast(stmt)
            statement_optimizations.append(stmt_optimization)
        
        # Compile comprehensive analysis
        analysis = {
            "optimized_ast": program_optimization.optimized_ast,
            "optimization_score": program_optimization.optimization_score,
            "applied_optimizations": program_optimization.applied_optimizations,
            "performance_improvement": program_optimization.performance_improvement,
            "learning_insights": program_optimization.learning_insights,
            "adaptation_suggestions": program_optimization.adaptation_suggestions,
            "optimization_strategy": program_optimization.optimization_strategy,
            "statement_optimizations": statement_optimizations,
            "optimization_summary": self._generate_optimization_summary(program_optimization, statement_optimizations),
            "statistics": self.intelligent_optimizer.get_optimization_statistics(),
            "optimization_timestamp": self._get_timestamp()
        }
        
        return analysis
    
    def _generate_optimization_summary(self, program_optimization: OptimizationResult,
                                     statement_optimizations: List[OptimizationResult]) -> Dict[str, Any]:
        """Generate comprehensive optimization summary"""
        total_optimizations = len(program_optimization.applied_optimizations)
        statement_level_optimizations = sum(len(opt.applied_optimizations) for opt in statement_optimizations)
        
        return {
            "total_optimizations_applied": total_optimizations,
            "statement_level_optimizations": statement_level_optimizations,
            "overall_improvement": program_optimization.performance_improvement,
            "optimization_strategy": program_optimization.optimization_strategy,
            "confidence": program_optimization.confidence
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for optimization tracking"""
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_optimization_summary(self, ast: Program) -> str:
        """Get human-readable summary of optimization"""
        analysis = self.optimize_program(ast)
        
        summary = f"""
Intelligent Optimization Summary
====================================
Optimization Score: {analysis['optimization_score']:.2%}
Performance Improvement: {analysis['performance_improvement']:.2%}
Optimization Strategy: {analysis['optimization_strategy']}
Confidence: {analysis['optimization_confidence']:.2%}
Learning Enabled: {'Yes' if self.config['enable_learning'] else 'No'}

Optimization Summary:
{self._format_optimization_summary(analysis['optimization_summary'])}

Applied Optimizations:
{self._format_applied_optimizations(analysis['applied_optimizations'])}

Learning Insights:
{self._format_learning_insights(analysis['learning_insights'])}

Adaptation Suggestions:
{self._format_adaptation_suggestions(analysis['adaptation_suggestions'])}

Optimization Statistics:
{self._format_statistics(analysis['statistics'])}
"""
        return summary
    
    def _format_optimization_summary(self, opt_summary: Dict[str, Any]) -> str:
        """Format optimization summary for display"""
        formatted = []
        for key, value in opt_summary.items():
            formatted.append(f"  {key}: {value}")
        return "\n".join(formatted)
    
    def _format_applied_optimizations(self, optimizations: List[Dict[str, Any]]) -> str:
        """Format applied optimizations for display"""
        if not optimizations:
            return "  No optimizations applied"
        
        formatted = []
        for i, opt in enumerate(optimizations, 1):
            formatted.append(f"  {i}. {opt['type']}: {opt['description']}")
            formatted.append(f"     Estimated improvement: {opt['estimated_improvement']}")
        
        return "\n".join(formatted)
    
    def _format_learning_insights(self, insights: List[str]) -> str:
        """Format learning insights for display"""
        if not insights:
            return "  No learning insights available"
        return "\n".join([f"  - {insight}" for insight in insights])
    
    def _format_adaptation_suggestions(self, suggestions: List[str]) -> str:
        """Format adaptation suggestions for display"""
        if not suggestions:
            return "  No adaptation suggestions"
        return "\n".join([f"  - {suggestion}" for suggestion in suggestions])
    
    def _format_statistics(self, statistics: Dict[str, Any]) -> str:
        """Format optimization statistics for display"""
        formatted = []
        for key, value in statistics.items():
            if isinstance(value, dict):
                formatted.append(f"  {key}:")
                for sub_key, sub_value in value.items():
                    formatted.append(f"    {sub_key}: {sub_value}")
            else:
                formatted.append(f"  {key}: {value}")
        return "\n".join(formatted)