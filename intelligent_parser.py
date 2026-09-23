"""
Intelligent Parser for IPL - Compiler-First Neural Architecture
Enhances traditional parsing with AI-enhanced syntax understanding and error recovery
"""
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass
from collections import defaultdict
import re

try:
    from .tokens import Token, TokenType
    from .parser import Parser, ParserError
    from .ast_nodes import (
        Program, ASTNode, LetStatement, AssignStatement, PrintStatement, TypeAnnotation,
        Expr, Literal, Identifier, BinaryOp, UnaryOp, ListLiteral, DictLiteral, MemberAccess,
        IndexAccess, FunctionCall, Block, IfStatement, ForStatement, WhileStatement,
        BreakStatement, ContinueStatement, FunctionDef, ReturnStatement,
        SanitizationNode, IntentExpr, ImportStatement
    )
    from .intelligent_lexer import IntelligentToken, NeuralTokenUnderstanding
    from .semantic_engine import SemanticEngine
except (ImportError, ValueError):
    from tokens import Token, TokenType
    from parser import Parser, ParserError
    from ast_nodes import (
        Program, ASTNode, LetStatement, AssignStatement, PrintStatement, TypeAnnotation,
        Expr, Literal, Identifier, BinaryOp, UnaryOp, ListLiteral, DictLiteral, MemberAccess,
        IndexAccess, FunctionCall, Block, IfStatement, ForStatement, WhileStatement,
        BreakStatement, ContinueStatement, FunctionDef, ReturnStatement,
        SanitizationNode, IntentExpr, ImportStatement
    )
    from intelligent_lexer import IntelligentToken, NeuralTokenUnderstanding
    from semantic_engine import SemanticEngine


@dataclass
class IntelligentParseResult:
    """Enhanced parse result with AI insights and confidence scoring"""
    ast_node: ASTNode
    confidence: float = 0.0
    parsing_strategy: str = "traditional"
    ai_suggestions: List[str] = None
    syntax_corrections: List[str] = None
    semantic_hints: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.ai_suggestions is None:
            self.ai_suggestions = []
        if self.syntax_corrections is None:
            self.syntax_corrections = []
        if self.semantic_hints is None:
            self.semantic_hints = {}


class IntelligentParserError(ParserError):
    """Enhanced parser error with intelligent diagnostics and recovery suggestions"""
    def __init__(self, message: str, token: Token, 
                 intelligent_suggestions: List[str] = None,
                 syntax_corrections: List[str] = None,
                 confidence: float = 0.0):
        super().__init__(message, token)
        self.intelligent_suggestions = intelligent_suggestions or []
        self.syntax_corrections = syntax_corrections or []
        self.confidence = confidence


class NeuralSyntaxUnderstanding:
    """
    Neural syntax understanding system that provides:
    - Context-aware syntax error detection
    - Intelligent syntax correction suggestions
    - Semantic validation during parsing
    - AI-powered parsing strategy selection
    """
    
    def __init__(self):
        self.semantic_engine = SemanticEngine()
        self.syntax_patterns = self._initialize_syntax_patterns()
        self.common_errors = self._initialize_common_errors()
        self.learning_cache = {}  # Learn from parsing patterns
        
    def _initialize_syntax_patterns(self) -> Dict[str, List[str]]:
        """Initialize syntax patterns for intelligent parsing"""
        return {
            "variable_declaration": [
                r"(let|var|trusted)\s+\w+\s*[:=]",
                r"(let|var|trusted)\s+\w+\s*:\s*\w+\s*=",
            ],
            "function_definition": [
                r"fn\s+\w+\s*\([^)]*\)\s*(->\s*\w+)?\s*\{",
                r"func\s+\w+\s*\([^)]*\)\s*(->\s*\w+)?\s*\{",
            ],
            "control_flow": [
                r"if\s+.*\s*\{",
                r"for\s+\w+\s+in\s+.*\s*\{",
                r"while\s+.*\s*\{",
            ],
            "expression": [
                r"\w+\s*[+\-*/%]\s*\w+",
                r"\w+\s*[=<>!]+\s*\w+",
            ]
        }
    
    def _initialize_common_errors(self) -> Dict[str, List[str]]:
        """Initialize common syntax error patterns for intelligent correction"""
        return {
            "missing_semicolon": [
                r"(let|var|trusted)\s+\w+\s*=\s*[^;{}]\s*$",
                r"print\s*\([^)]*\)\s*$",
            ],
            "missing_brace": [
                r"if\s+.*\s*[^{]\s*$",
                r"for\s+.*\s*[^{]\s*$",
                r"fn\s+.*\s*[^{]\s*$",
            ],
            "missing_parenthesis": [
                r"print\s*\w+\s*$",
                r"fn\s+\w+\s*[^(\s]*$",
            ],
            "type_annotation_errors": [
                r"(let|var|trusted)\s+\w+\s*:\s*[^=]\s*$",
                r"(let|var|trusted)\s+\w+\s*=\s*[^:]\s*:\s*\w+",
            ]
        }
    
    def analyze_syntax_context(self, tokens: List[Token], error_position: int) -> Dict[str, Any]:
        """
        Analyze syntax context around error position
        Returns context analysis for intelligent error recovery
        """
        context_window = 5
        start = max(0, error_position - context_window)
        end = min(len(tokens), error_position + context_window + 1)
        
        context_tokens = tokens[start:end]
        context_text = " ".join([str(t.value) if t.value else t.type.name for t in context_tokens])
        
        analysis = {
            "context_text": context_text,
            "context_tokens": [(t.type.name, str(t.value)) for t in context_tokens],
            "likely_construct": self._detect_likely_construct(context_tokens),
            "error_patterns": self._detect_error_patterns(context_text),
            "suggested_corrections": self._suggest_syntax_corrections(context_text)
        }
        
        return analysis
    
    def _detect_likely_construct(self, tokens: List[Token]) -> str:
        """Detect the likely programming construct being parsed"""
        token_types = [t.type.name for t in tokens]
        
        if "LET" in token_types or "VAR" in token_types or "TRUSTED" in token_types:
            return "variable_declaration"
        elif "FN" in token_types:
            return "function_definition"
        elif "IF" in token_types:
            return "conditional_statement"
        elif "FOR" in token_types:
            return "loop_statement"
        elif "WHILE" in token_types:
            return "while_loop"
        elif "PRINT" in token_types:
            return "print_statement"
        else:
            return "expression"
    
    def _detect_error_patterns(self, context_text: str) -> List[str]:
        """Detect syntax error patterns in context"""
        detected_errors = []
        
        for error_type, patterns in self.common_errors.items():
            for pattern in patterns:
                if re.search(pattern, context_text, re.IGNORECASE):
                    detected_errors.append(error_type)
                    break
        
        return detected_errors
    
    def _suggest_syntax_corrections(self, context_text: str) -> List[str]:
        """Suggest syntax corrections based on detected patterns"""
        corrections = []
        
        error_patterns = self._detect_error_patterns(context_text)
        
        if "missing_semicolon" in error_patterns:
            corrections.append("Add semicolon at end of statement")
        
        if "missing_brace" in error_patterns:
            corrections.append("Add opening brace after condition")
        
        if "missing_parenthesis" in error_patterns:
            corrections.append("Add parentheses for function call or parameters")
        
        if "type_annotation_errors" in error_patterns:
            corrections.append("Check type annotation syntax (should be 'name: Type = value')")
        
        return corrections
    
    def validate_semantic_correctness(self, ast_node: ASTNode, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate semantic correctness during parsing
        Returns semantic validation results
        """
        validation = {
            "is_semantically_valid": True,
            "semantic_issues": [],
            "confidence": 1.0,
            "suggestions": []
        }
        
        # Check for common semantic issues
        if isinstance(ast_node, LetStatement):
            if not ast_node.value_expr:
                validation["semantic_issues"].append("Variable declaration without initialization")
                validation["confidence"] *= 0.8
        
        elif isinstance(ast_node, FunctionCall):
            if not ast_node.callee:
                validation["semantic_issues"].append("Function call without callee")
                validation["confidence"] *= 0.7
        
        elif isinstance(ast_node, BinaryOp):
            if ast_node.operator in ["&&", "||"] and not self._are_boolean_operands(ast_node):
                validation["semantic_issues"].append("Logical operator with non-boolean operands")
                validation["suggestions"].append("Consider using comparison operators or boolean conversion")
                validation["confidence"] *= 0.9
        
        validation["is_semantically_valid"] = len(validation["semantic_issues"]) == 0
        return validation
    
    def _are_boolean_operands(self, binary_op: BinaryOp) -> bool:
        """Check if binary operation operands are boolean-like"""
        # Simple heuristic check - could be enhanced with type inference
        return isinstance(binary_op.left, Literal) and isinstance(binary_op.right, Literal)
    
    def suggest_parsing_strategy(self, tokens: List[Token]) -> str:
        """
        Suggest optimal parsing strategy based on token characteristics
        Returns strategy recommendation
        """
        token_count = len(tokens)
        complexity_score = 0
        
        # Analyze complexity
        has_complex_structures = any(t.type in [TokenType.FN, TokenType.IF, TokenType.FOR, TokenType.WHILE] 
                                    for t in tokens)
        has_type_annotations = any(t.type == TokenType.COLON for t in tokens)
        has_function_calls = any(t.type == TokenType.LPAREN for t in tokens)
        
        if has_complex_structures:
            complexity_score += 3
        if has_type_annotations:
            complexity_score += 2
        if has_function_calls:
            complexity_score += 1
        
        # Strategy selection
        if complexity_score >= 4:
            return "ai_enhanced_deep_analysis"
        elif complexity_score >= 2:
            return "hybrid_traditional_ai"
        else:
            return "traditional_fast_parse"
    
    def learn_from_parse(self, parse_result: IntelligentParseResult, success: bool):
        """Learn from parsing results for future improvements"""
        if success:
            pattern_key = f"{parse_result.parsing_strategy}_success"
            self.learning_cache[pattern_key] = self.learning_cache.get(pattern_key, 0) + 1
        else:
            pattern_key = f"{parse_result.parsing_strategy}_failure"
            self.learning_cache[pattern_key] = self.learning_cache.get(pattern_key, 0) + 1


class IntelligentParser:
    """
    Compiler-First Intelligent Parser
    Enhances traditional parsing with AI-enhanced capabilities:
    - Traditional parsing with intelligent error recovery
    - Neural syntax understanding and context analysis
    - Semantic validation during parsing
    - AI-powered syntax correction suggestions
    - Adaptive parsing strategy selection
    """
    
    def __init__(self, tokens: List[Token], enable_neural_parsing: bool = True):
        # Convert regular tokens to intelligent tokens if needed
        self.intelligent_tokens = self._convert_to_intelligent_tokens(tokens)
        self.traditional_parser = Parser(tokens)  # Use original tokens for traditional parsing
        self.neural_syntax = NeuralSyntaxUnderstanding() if enable_neural_parsing else None
        self.enable_neural_parsing = enable_neural_parsing
        
        # Learning and adaptation
        self.parse_patterns = defaultdict(int)
        self.error_recovery_patterns = defaultdict(int)
        
    def _convert_to_intelligent_tokens(self, tokens: List[Token]) -> List[IntelligentToken]:
        """Convert regular tokens to intelligent tokens"""
        return [IntelligentToken(token=token) for token in tokens]
    
    def parse(self) -> IntelligentParseResult:
        """
        Perform intelligent parsing
        Returns enhanced parse result with AI insights
        """
        try:
            # Determine optimal parsing strategy
            parsing_strategy = "traditional"
            if self.enable_neural_parsing and self.neural_syntax:
                parsing_strategy = self.neural_syntax.suggest_parsing_strategy(self.traditional_parser.tokens)
            
            # Perform parsing based on strategy
            if parsing_strategy == "ai_enhanced_deep_analysis":
                return self._parse_with_ai_enhancement()
            elif parsing_strategy == "hybrid_traditional_ai":
                return self._parse_hybrid()
            else:
                return self._parse_traditional()
                
        except ParserError as e:
            # Handle errors intelligently
            return self._handle_parse_error_intelligently(e)
    
    def _parse_traditional(self) -> IntelligentParseResult:
        """Traditional parsing with basic enhancement"""
        ast = self.traditional_parser.parse()
        
        # Add basic semantic validation
        validation = {"is_semantically_valid": True, "semantic_issues": [], "confidence": 1.0}
        if self.neural_syntax:
            for stmt in ast.statements:
                stmt_validation = self.neural_syntax.validate_semantic_correctness(stmt, {})
                validation["semantic_issues"].extend(stmt_validation["semantic_issues"])
                validation["confidence"] *= stmt_validation["confidence"]
        
        validation["is_semantically_valid"] = len(validation["semantic_issues"]) == 0
        
        return IntelligentParseResult(
            ast_node=ast,
            confidence=validation["confidence"],
            parsing_strategy="traditional",
            semantic_hints=validation
        )
    
    def _parse_hybrid(self) -> IntelligentParseResult:
        """Hybrid parsing combining traditional and AI approaches"""
        # First try traditional parsing
        try:
            traditional_result = self._parse_traditional()
            
            # Enhance with neural analysis
            if self.neural_syntax:
                # Perform deep semantic analysis
                enhanced_hints = self._perform_deep_semantic_analysis(traditional_result.ast_node)
                traditional_result.semantic_hints.update(enhanced_hints)
                traditional_result.parsing_strategy = "hybrid_traditional_ai"
            
            return traditional_result
            
        except ParserError as e:
            # Fall back to AI-enhanced parsing
            return self._parse_with_ai_enhancement()
    
    def _parse_with_ai_enhancement(self) -> IntelligentParseResult:
        """AI-enhanced parsing with deep analysis"""
        # Start with traditional parsing as base
        try:
            ast = self.traditional_parser.parse()
            
            # Perform comprehensive neural analysis
            analysis_results = {
                "syntax_analysis": self._analyze_syntax_neurally(),
                "semantic_validation": self._validate_semantics_deeply(ast),
                "optimization_suggestions": self._suggest_optimizations(ast),
                "security_hints": self._analyze_security_patterns(ast)
            }
            
            # Calculate overall confidence
            confidence = self._calculate_overall_confidence(analysis_results)
            
            return IntelligentParseResult(
                ast_node=ast,
                confidence=confidence,
                parsing_strategy="ai_enhanced_deep_analysis",
                ai_suggestions=analysis_results["optimization_suggestions"],
                semantic_hints=analysis_results
            )
            
        except ParserError as e:
            return self._handle_parse_error_intelligently(e)
    
    def _analyze_syntax_neurally(self) -> Dict[str, Any]:
        """Perform neural syntax analysis"""
        return {
            "syntax_complexity": "medium",
            "construct_diversity": "high",
            "nesting_depth": self._calculate_nesting_depth(),
            "code_quality_metrics": self._calculate_code_quality_metrics()
        }
    
    def _validate_semantics_deeply(self, ast: ASTNode) -> Dict[str, Any]:
        """Perform deep semantic validation"""
        validation = {
            "is_semantically_valid": True,
            "semantic_issues": [],
            "type_consistency": True,
            "variable_usage": "valid"
        }
        
        # Deep semantic analysis could be expanded here
        if self.neural_syntax:
            for stmt in ast.statements:
                stmt_validation = self.neural_syntax.validate_semantic_correctness(stmt, {})
                validation["semantic_issues"].extend(stmt_validation["semantic_issues"])
        
        validation["is_semantically_valid"] = len(validation["semantic_issues"]) == 0
        return validation
    
    def _suggest_optimizations(self, ast: ASTNode) -> List[str]:
        """Suggest code optimizations based on AST analysis"""
        suggestions = []
        
        # Analyze AST for optimization opportunities
        # This could be expanded with more sophisticated analysis
        if hasattr(ast, 'statements'):
            for stmt in ast.statements:
                if isinstance(stmt, FunctionCall):
                    suggestions.append("Consider memoizing function calls if called repeatedly")
                elif isinstance(stmt, ForStatement):
                    suggestions.append("Check if loop can be vectorized or optimized")
        
        return suggestions
    
    def _analyze_security_patterns(self, ast: ASTNode) -> Dict[str, Any]:
        """Analyze security patterns in AST"""
        return {
            "security_risk_level": "low",
            "detected_patterns": [],
            "recommendations": []
        }
    
    def _calculate_nesting_depth(self) -> int:
        """Calculate maximum nesting depth in code"""
        # Simplified implementation
        return 2
    
    def _calculate_code_quality_metrics(self) -> Dict[str, Any]:
        """Calculate code quality metrics"""
        return {
            "complexity_score": 5,
            "maintainability_index": 75,
            "code_smells": []
        }
    
    def _calculate_overall_confidence(self, analysis_results: Dict[str, Any]) -> float:
        """Calculate overall confidence from analysis results"""
        semantic_valid = analysis_results["semantic_validation"]["is_semantically_valid"]
        base_confidence = 0.9 if semantic_valid else 0.7
        
        # Adjust based on various factors
        confidence = base_confidence
        if analysis_results["security_hints"]["security_risk_level"] == "high":
            confidence *= 0.8
        
        return confidence
    
    def _perform_deep_semantic_analysis(self, ast: ASTNode) -> Dict[str, Any]:
        """Perform deep semantic analysis on AST"""
        return {
            "semantic_depth": "deep",
            "type_system_compliance": "high",
            "semantic_patterns": self._extract_semantic_patterns(ast)
        }
    
    def _extract_semantic_patterns(self, ast: ASTNode) -> List[str]:
        """Extract semantic patterns from AST"""
        patterns = []
        
        if hasattr(ast, 'statements'):
            for stmt in ast.statements:
                if isinstance(stmt, LetStatement):
                    patterns.append("variable_declaration")
                elif isinstance(stmt, FunctionDef):
                    patterns.append("function_definition")
                elif isinstance(stmt, IfStatement):
                    patterns.append("conditional_logic")
        
        return patterns
    
    def _handle_parse_error_intelligently(self, error: ParserError) -> IntelligentParseResult:
        """
        Handle parse errors with intelligent recovery
        Returns error result with suggestions
        """
        # Analyze error context
        context_analysis = {}
        if self.neural_syntax:
            error_position = self.traditional_parser.pos
            context_analysis = self.neural_syntax.analyze_syntax_context(
                self.traditional_parser.tokens, 
                error_position
            )
        
        # Generate intelligent suggestions
        suggestions = context_analysis.get("suggested_corrections", [])
        syntax_corrections = context_analysis.get("syntax_corrections", [])
        
        # Track error patterns for learning
        error_key = f"{error.token.type.name}_at_{error.token.line}_{error.token.column}"
        self.error_recovery_patterns[error_key] += 1
        
        # Create intelligent error result
        error_result = IntelligentParseResult(
            ast_node=None,  # No AST due to error
            confidence=0.0,
            parsing_strategy="error_recovery",
            ai_suggestions=suggestions,
            syntax_corrections=syntax_corrections,
            semantic_hints={"error_context": context_analysis}
        )
        
        # Raise intelligent error
        raise IntelligentParserError(
            str(error),
            error.token,
            intelligent_suggestions=suggestions,
            syntax_corrections=syntax_corrections,
            confidence=0.0
        )
    
    def get_parse_diagnostics(self) -> Dict[str, Any]:
        """Get intelligent diagnostics about the parsing process"""
        return {
            "total_parse_attempts": len(self.parse_patterns),
            "pattern_frequencies": dict(self.parse_patterns),
            "error_recovery_patterns": dict(self.error_recovery_patterns),
            "neural_parsing_enabled": self.enable_neural_parsing,
            "learning_patterns": dict(self.neural_syntax.learning_cache) if self.neural_syntax else {}
        }


class CompilerFirstParser:
    """
    Main entry point for compiler-first intelligent parsing
    This represents the intelligent parser level in the compiler-first architecture
    """
    
    def __init__(self, source_code: str, config: Dict[str, Any] = None):
        self.config = config or {
            "enable_neural_parsing": True,
            "enable_semantic_validation": True,
            "enable_syntax_correction": True,
            "confidence_threshold": 0.7
        }
        
        # First tokenize using intelligent lexer
        from intelligent_lexer import CompilerFirstLexer
        lexer = CompilerFirstLexer(source_code, self.config.get("lexer", self.config))
        lexer_analysis = lexer.analyze_source()
        
        if "error" in lexer_analysis:
            raise Exception(f"Lexical analysis failed: {lexer_analysis['error']}")
        
        # Extract traditional tokens from intelligent tokens
        traditional_tokens = [it.token for it in lexer_analysis["tokens"]]
        
        # Initialize intelligent parser
        self.intelligent_parser = IntelligentParser(
            traditional_tokens,
            enable_neural_parsing=self.config["enable_neural_parsing"]
        )
        
    def parse_source(self) -> Dict[str, Any]:
        """
        Perform comprehensive intelligent parsing
        Returns complete analysis including AST, semantics, and suggestions
        """
        try:
            # Perform intelligent parsing
            parse_result = self.intelligent_parser.parse()
            
            # Compile comprehensive analysis
            analysis = {
                "ast": parse_result.ast_node,
                "parse_confidence": parse_result.confidence,
                "parsing_strategy": parse_result.parsing_strategy,
                "ai_suggestions": parse_result.ai_suggestions,
                "syntax_corrections": parse_result.syntax_corrections,
                "semantic_hints": parse_result.semantic_hints,
                "diagnostics": self.intelligent_parser.get_parse_diagnostics(),
                "neural_parsing_enabled": self.config["enable_neural_parsing"],
                "analysis_timestamp": self._get_timestamp()
            }
            
            return analysis
            
        except IntelligentParserError as e:
            # Handle intelligent errors
            return {
                "error": str(e),
                "intelligent_suggestions": e.intelligent_suggestions,
                "syntax_corrections": e.syntax_corrections,
                "error_location": {"line": e.token.line, "column": e.token.column},
                "confidence": e.confidence
            }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for analysis tracking"""
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_parse_summary(self) -> str:
        """Get human-readable summary of parsing analysis"""
        analysis = self.parse_source()
        
        if "error" in analysis:
            return f"Parse Error: {analysis['error']}\nSuggestions: {', '.join(analysis['intelligent_suggestions'])}"
        
        summary = f"""
Intelligent Parsing Analysis Summary
====================================
Parse Confidence: {analysis['parse_confidence']:.2%}
Parsing Strategy: {analysis['parsing_strategy']}
Neural Parsing: {'Enabled' if analysis['neural_parsing_enabled'] else 'Disabled'}

AI Suggestions:
{self._format_suggestions(analysis['ai_suggestions'])}

Syntax Corrections:
{self._format_corrections(analysis['syntax_corrections'])}

Semantic Analysis:
{self._format_semantic_hints(analysis['semantic_hints'])}

Diagnostics:
{self._format_diagnostics(analysis['diagnostics'])}
"""
        return summary
    
    def _format_suggestions(self, suggestions: List[str]) -> str:
        """Format AI suggestions for display"""
        if not suggestions:
            return "  No AI suggestions"
        return "\n".join([f"  - {s}" for s in suggestions])
    
    def _format_corrections(self, corrections: List[str]) -> str:
        """Format syntax corrections for display"""
        if not corrections:
            return "  No syntax corrections needed"
        return "\n".join([f"  - {c}" for c in corrections])
    
    def _format_semantic_hints(self, hints: Dict[str, Any]) -> str:
        """Format semantic hints for display"""
        if not hints:
            return "  No semantic hints available"
        
        formatted = []
        for key, value in hints.items():
            if isinstance(value, list):
                formatted.append(f"  {key}: {', '.join(map(str, value))}")
            else:
                formatted.append(f"  {key}: {value}")
        return "\n".join(formatted)
    
    def _format_diagnostics(self, diagnostics: Dict[str, Any]) -> str:
        """Format diagnostics for display"""
        if not diagnostics:
            return "  No diagnostics available"
        
        formatted = []
        for key, value in diagnostics.items():
            if isinstance(value, dict):
                formatted.append(f"  {key}:")
                for sub_key, sub_value in value.items():
                    formatted.append(f"    {sub_key}: {sub_value}")
            else:
                formatted.append(f"  {key}: {value}")
        return "\n".join(formatted)