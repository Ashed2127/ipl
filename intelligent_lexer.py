"""
Intelligent Lexer for IPL - Compiler-First Neural Architecture
Enhances traditional lexical analysis with neural token understanding
"""
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

try:
    from .tokens import Token, TokenType
    from .lexer import Lexer, LexerError
    from .semantic_engine import SemanticEngine
except (ImportError, ValueError):
    from tokens import Token, TokenType
    from lexer import Lexer, LexerError
    from semantic_engine import SemanticEngine


@dataclass
class IntelligentToken:
    """Enhanced token with neural understanding and context"""
    token: Token
    semantic_type: Optional[str] = None
    confidence: float = 0.0
    context_hints: Dict[str, Any] = None
    security_flags: List[str] = None
    
    def __post_init__(self):
        if self.context_hints is None:
            self.context_hints = {}
        if self.security_flags is None:
            self.security_flags = []


class IntelligentLexerError(LexerError):
    """Enhanced lexer error with intelligent diagnostics"""
    def __init__(self, message: str, line: int, column: int, 
                 intelligent_suggestions: List[str] = None):
        super().__init__(message, line, column)
        self.intelligent_suggestions = intelligent_suggestions or []


class NeuralTokenUnderstanding:
    """
    Neural token understanding system that provides:
    - Semantic classification of tokens
    - Context-aware token interpretation
    - Security pattern detection in tokens
    - Intelligent error recovery suggestions
    """
    
    def __init__(self):
        self.semantic_engine = SemanticEngine()
        self.security_patterns = self._initialize_security_patterns()
        self.semantic_patterns = self._initialize_semantic_patterns()
        self.learning_cache = {}  # Learn from token patterns
        
    def _initialize_security_patterns(self) -> Dict[str, List[str]]:
        """Initialize security threat patterns for token analysis"""
        return {
            "sql_injection": [
                r"(\bunion\b.*\bselect\b)",
                r"(\bor\b.*=.*\bor\b)",
                r"(\bexec\b.*\bxp_\w+)",
                r"('\s*;\s*\bdrop\b)",
                r"('\s*;\s*\bdelete\b)",
                r"('\s*;\s*\btruncate\b)"
            ],
            "command_injection": [
                r"(\|\s*\w+)",
                r"(;\s*\w+)",
                r"(`.*`)",
                r"(\$\([^)]*\))",
                r"(\beval\s*\()",
                r"(\bsystem\s*\()"
            ],
            "xss_patterns": [
                r"(<script[^>]*>)",
                r"(javascript:)",
                r"(on\w+\s*=)",
                r"(<iframe[^>]*>)",
                r"(data:text/html)"
            ],
            "path_traversal": [
                r"(\.\./)",
                r"(\.\.\\\\)",
                r"(%2e%2e/)",
                r"(\.\.[\\])"
            ]
        }
    
    def _initialize_semantic_patterns(self) -> Dict[str, List[str]]:
        """Initialize semantic patterns for intelligent token classification"""
        return {
            "numeric": [
                r"\b\d+\b",
                r"\b\d+\.\d+\b",
                r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\b"
            ],
            "currency": [
                r"\$\s*\d+\.?\d*",
                r"€\s*\d+\.?\d*",
                r"£\s*\d+\.?\d*",
                r"\d+\.?\d*\s*(USD|EUR|GBP|dollars?|euros?|pounds?)"
            ],
            "temporal": [
                r"\b\d{1,2}:\d{2}\b",
                r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
                r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b",
                r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b"
            ],
            "sentiment_keywords": [
                r"\b(good|great|excellent|amazing|wonderful|fantastic)\b",
                r"\b(bad|terrible|awful|horrible|poor|disappointing)\b",
                r"\b(happy|sad|angry|excited|disappointed|satisfied)\b"
            ]
        }
    
    def analyze_token_semantics(self, token: Token, context: str = "") -> Dict[str, Any]:
        """
        Perform neural semantic analysis on a token
        Returns semantic classification, confidence, and context hints
        """
        analysis = {
            "semantic_type": None,
            "confidence": 0.0,
            "context_hints": {},
            "security_flags": []
        }
        
        if token.type == TokenType.IDENTIFIER:
            analysis.update(self._analyze_identifier(token.value, context))
        elif token.type == TokenType.STRING:
            analysis.update(self._analyze_string_literal(token.value, context))
        elif token.type == TokenType.NUMBER:
            analysis.update(self._analyze_number_literal(token.value, context))
        
        return analysis
    
    def _analyze_identifier(self, identifier: str, context: str) -> Dict[str, Any]:
        """Intelligent analysis of identifier tokens"""
        analysis = {"semantic_type": None, "confidence": 0.0, "context_hints": {}, "security_flags": []}
        
        # Check for security-sensitive identifiers
        if identifier.lower() in ["password", "secret", "token", "key", "auth"]:
            analysis["semantic_type"] = "security_sensitive"
            analysis["confidence"] = 0.9
            analysis["context_hints"]["security_implication"] = "requires_special_handling"
            analysis["security_flags"].append("sensitive_identifier")
        
        # Check for database-related identifiers
        elif any(db_word in identifier.lower() for db_word in ["query", "sql", "database", "table", "column"]):
            analysis["semantic_type"] = "database_operation"
            analysis["confidence"] = 0.8
            analysis["context_hints"]["operation_type"] = "database_access"
        
        # Check for I/O operations
        elif any(io_word in identifier.lower() for io_word in ["read", "write", "file", "input", "output"]):
            analysis["semantic_type"] = "io_operation"
            analysis["confidence"] = 0.7
            analysis["context_hints"]["operation_type"] = "file_io"
        
        # Check for function-like patterns
        elif identifier.endswith("_") or identifier.startswith("_"):
            analysis["semantic_type"] = "special_identifier"
            analysis["confidence"] = 0.6
            analysis["context_hints"]["naming_convention"] = "internal"
        
        return analysis
    
    def _analyze_string_literal(self, string_value: str, context: str) -> Dict[str, Any]:
        """Intelligent analysis of string literal tokens"""
        analysis = {"semantic_type": None, "confidence": 0.0, "context_hints": {}, "security_flags": []}
        
        # Security analysis
        for threat_type, patterns in self.security_patterns.items():
            for pattern in patterns:
                if re.search(pattern, string_value, re.IGNORECASE):
                    analysis["security_flags"].append(threat_type)
                    analysis["confidence"] = max(analysis["confidence"], 0.8)
        
        # Semantic analysis
        if analysis["security_flags"]:
            analysis["semantic_type"] = "potentially_malicious"
        elif re.search(r"\$\d+\.?\d*", string_value):
            analysis["semantic_type"] = "currency_value"
            analysis["confidence"] = 0.85
            analysis["context_hints"]["currency_type"] = "likely_monetary"
        elif re.search(r"\b\d{1,2}:\d{2}\b", string_value):
            analysis["semantic_type"] = "time_value"
            analysis["confidence"] = 0.75
            analysis["context_hints"]["temporal_type"] = "time"
        elif any(sentiment in string_value.lower() for sentiment in ["good", "bad", "excellent", "terrible"]):
            analysis["semantic_type"] = "sentiment_expression"
            analysis["confidence"] = 0.7
            analysis["context_hints"]["sentiment_category"] = "opinion"
        else:
            analysis["semantic_type"] = "generic_string"
            analysis["confidence"] = 0.5
        
        return analysis
    
    def _analyze_number_literal(self, number_value: Any, context: str) -> Dict[str, Any]:
        """Intelligent analysis of numeric literal tokens"""
        analysis = {"semantic_type": None, "confidence": 0.0, "context_hints": {}, "security_flags": []}
        
        if isinstance(number_value, float):
            analysis["semantic_type"] = "floating_point_number"
            analysis["confidence"] = 0.95
            analysis["context_hints"]["precision"] = "decimal"
        elif isinstance(number_value, int):
            # Try to infer semantic meaning from magnitude
            if number_value > 1000000:
                analysis["semantic_type"] = "large_number"
                analysis["confidence"] = 0.8
                analysis["context_hints"]["magnitude"] = "large_scale"
            elif number_value < 0:
                analysis["semantic_type"] = "negative_number"
                analysis["confidence"] = 0.9
                analysis["context_hints"]["sign"] = "negative"
            elif 0 <= number_value <= 100:
                analysis["semantic_type"] = "percentage_or_score"
                analysis["confidence"] = 0.6
                analysis["context_hints"]["likely_range"] = "percentage"
            else:
                analysis["semantic_type"] = "integer_number"
                analysis["confidence"] = 0.85
                analysis["context_hints"]["precision"] = "exact"
        
        return analysis
    
    def detect_security_threats(self, token: Token) -> List[str]:
        """Detect security threats in token using neural pattern recognition"""
        threats = []
        
        if token.type == TokenType.STRING:
            string_value = str(token.value)
            for threat_type, patterns in self.security_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, string_value, re.IGNORECASE):
                        threats.append(threat_type)
        
        elif token.type == TokenType.IDENTIFIER:
            identifier = str(token.value).lower()
            dangerous_keywords = ["eval", "exec", "system", "shell", "cmd", "command"]
            if any(keyword in identifier for keyword in dangerous_keywords):
                threats.append("dangerous_function_call")
        
        return threats
    
    def provide_intelligent_suggestions(self, error_token: Token, context: str) -> List[str]:
        """Provide intelligent suggestions for token-level error recovery"""
        suggestions = []
        
        if error_token.type == TokenType.IDENTIFIER:
            identifier = str(error_token.value)
            
            # Suggest keyword corrections
            similar_keywords = self._find_similar_keywords(identifier)
            if similar_keywords:
                suggestions.extend([f"Did you mean '{keyword}'?" for keyword in similar_keywords])
            
            # Suggest camelCase conversion
            if "_" in identifier:
                camel_case = identifier.replace("_", " ").title().replace(" ", "")
                suggestions.append(f"Consider using camelCase: '{camel_case}'")
        
        elif error_token.type == TokenType.STRING:
            string_value = str(error_token.value)
            if self.detect_security_threats(error_token):
                suggestions.append("Security warning: This string contains potentially dangerous patterns")
                suggestions.append("Consider using parameterized queries instead of string concatenation")
        
        return suggestions
    
    def _find_similar_keywords(self, identifier: str) -> List[str]:
        """Find similar keywords using simple similarity matching"""
        keywords = ["let", "var", "print", "where", "for", "if", "else", "while", "fn", "return", "true", "false"]
        similar = []
        
        for keyword in keywords:
            # Simple similarity: contains same letters in similar order
            if self._simple_similarity(identifier.lower(), keyword) > 0.5:
                similar.append(keyword)
        
        return similar
    
    def _simple_similarity(self, str1: str, str2: str) -> float:
        """Simple similarity metric for suggestion matching"""
        if not str1 or not str2:
            return 0.0
        
        # Check if one is substring of the other
        if str1 in str2 or str2 in str1:
            return 0.8
        
        # Check for common prefix
        common_prefix = 0
        for c1, c2 in zip(str1, str2):
            if c1 == c2:
                common_prefix += 1
            else:
                break
        
        return common_prefix / max(len(str1), len(str2))


class IntelligentLexer:
    """
    Compiler-First Intelligent Lexer
    Enhances traditional lexical analysis with neural understanding:
    - Traditional tokenization with enhanced error reporting
    - Neural semantic analysis of each token
    - Security threat detection at token level
    - Intelligent error recovery suggestions
    - Context-aware token interpretation
    """
    
    def __init__(self, source: str, enable_neural_analysis: bool = True):
        self.source = source
        self.traditional_lexer = Lexer(source)
        self.neural_understanding = NeuralTokenUnderstanding() if enable_neural_analysis else None
        self.enable_neural_analysis = enable_neural_analysis
        
        # Learning and adaptation
        self.token_patterns = defaultdict(int)
        self.error_patterns = defaultdict(int)
        
    def tokenize(self) -> List[IntelligentToken]:
        """
        Perform intelligent tokenization
        Returns list of IntelligentToken with neural understanding
        """
        traditional_tokens = self.traditional_lexer.tokenize()
        intelligent_tokens = []
        
        for token in traditional_tokens:
            if self.enable_neural_analysis and self.neural_understanding:
                # Perform neural analysis
                context = self._get_token_context(token, traditional_tokens)
                analysis = self.neural_understanding.analyze_token_semantics(token, context)
                
                # Create intelligent token
                intelligent_token = IntelligentToken(
                    token=token,
                    semantic_type=analysis["semantic_type"],
                    confidence=analysis["confidence"],
                    context_hints=analysis["context_hints"],
                    security_flags=analysis["security_flags"]
                )
                
                # Learn from token patterns
                self._learn_from_token(intelligent_token)
                
            else:
                # Fallback to traditional token
                intelligent_token = IntelligentToken(token=token)
            
            intelligent_tokens.append(intelligent_token)
        
        return intelligent_tokens
    
    def _get_token_context(self, token: Token, all_tokens: List[Token]) -> str:
        """Extract context around a token for neural analysis"""
        token_index = all_tokens.index(token) if token in all_tokens else 0
        
        # Get window of tokens around current token
        window_size = 3
        start = max(0, token_index - window_size)
        end = min(len(all_tokens), token_index + window_size + 1)
        
        context_tokens = all_tokens[start:end]
        context = " ".join([str(t.value) if t.value else t.type.name for t in context_tokens])
        
        return context
    
    def _learn_from_token(self, intelligent_token: IntelligentToken):
        """Learn from token patterns for future improvements"""
        token_key = f"{intelligent_token.token.type.name}:{intelligent_token.semantic_type}"
        self.token_patterns[token_key] += 1
    
    def get_intelligent_diagnostics(self) -> Dict[str, Any]:
        """Get intelligent diagnostics about the tokenization process"""
        return {
            "total_tokens": len(self.token_patterns),
            "pattern_frequencies": dict(self.token_patterns),
            "neural_analysis_enabled": self.enable_neural_analysis,
            "learning_patterns": dict(self.token_patterns)
        }
    
    def get_security_summary(self) -> Dict[str, Any]:
        """Get security analysis summary from tokenization"""
        if not self.enable_neural_analysis:
            return {"security_analysis": "disabled"}
        
        security_threats = defaultdict(int)
        for pattern_key, count in self.token_patterns.items():
            if "malicious" in pattern_key or any(threat in pattern_key for threat in 
                ["sql_injection", "command_injection", "xss", "path_traversal"]):
                security_threats[pattern_key] = count
        
        return {
            "total_security_flags": sum(security_threats.values()),
            "threat_distribution": dict(security_threats),
            "security_analysis": "enabled"
        }
    
    def handle_lexical_error_intelligently(self, error: LexerError) -> IntelligentLexerError:
        """
        Provide intelligent handling of lexical errors
        Returns enhanced error with suggestions
        """
        # Try to extract the problematic character/token
        error_context = self._extract_error_context(error.line, error.column)
        
        # Generate intelligent suggestions
        suggestions = []
        if self.neural_understanding and error_context:
            mock_token = Token(TokenType.IDENTIFIER, error_context, error.line, error.column)
            suggestions = self.neural_understanding.provide_intelligent_suggestions(mock_token, "")
        
        # Track error patterns for learning
        error_key = f"line_{error.line}:col_{error.column}"
        self.error_patterns[error_key] += 1
        
        return IntelligentLexerError(
            str(error),
            error.line,
            error.column,
            intelligent_suggestions=suggestions
        )
    
    def _extract_error_context(self, line: int, column: int) -> str:
        """Extract context around error location"""
        lines = self.source.split('\n')
        if 0 <= line - 1 < len(lines):
            error_line = lines[line - 1]
            # Extract character around error column
            start = max(0, column - 5)
            end = min(len(error_line), column + 5)
            return error_line[start:end]
        return ""


class CompilerFirstLexer:
    """
    Main entry point for compiler-first intelligent lexical analysis
    This represents the intelligent lexer level in the compiler-first architecture
    """
    
    def __init__(self, source: str, config: Dict[str, Any] = None):
        self.config = config or {
            "enable_neural_analysis": True,
            "enable_security_analysis": True,
            "enable_learning": True,
            "confidence_threshold": 0.7
        }
        
        self.intelligent_lexer = IntelligentLexer(
            source, 
            enable_neural_analysis=self.config.get("enable_neural_analysis", True)
        )
        
    def analyze_source(self) -> Dict[str, Any]:
        """
        Perform comprehensive intelligent lexical analysis
        Returns complete analysis including tokens, semantics, and security
        """
        try:
            # Perform intelligent tokenization
            intelligent_tokens = self.intelligent_lexer.tokenize()
            
            # Compile comprehensive analysis
            analysis = {
                "tokens": intelligent_tokens,
                "token_count": len(intelligent_tokens),
                "diagnostics": self.intelligent_lexer.get_intelligent_diagnostics(),
                "security_summary": self.intelligent_lexer.get_security_summary() if self.config["enable_security_analysis"] else {},
                "neural_analysis_enabled": self.config["enable_neural_analysis"],
                "analysis_timestamp": self._get_timestamp()
            }
            
            return analysis
            
        except LexerError as e:
            # Handle errors intelligently
            intelligent_error = self.intelligent_lexer.handle_lexical_error_intelligently(e)
            return {
                "error": str(intelligent_error),
                "suggestions": intelligent_error.intelligent_suggestions,
                "error_location": {"line": e.line, "column": e.column}
            }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for analysis tracking"""
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_analysis_summary(self) -> str:
        """Get human-readable summary of lexical analysis"""
        analysis = self.analyze_source()
        
        if "error" in analysis:
            return f"Lexical Error: {analysis['error']}\nSuggestions: {', '.join(analysis['suggestions'])}"
        
        summary = f"""
Intelligent Lexical Analysis Summary
====================================
Total Tokens: {analysis['token_count']}
Neural Analysis: {'Enabled' if analysis['neural_analysis_enabled'] else 'Disabled'}
Security Analysis: {analysis['security_summary'].get('security_analysis', 'N/A')}

Token Patterns Found:
{self._format_patterns(analysis['diagnostics']['pattern_frequencies'])}

Security Summary:
{self._format_security(analysis['security_summary'])}
"""
        return summary
    
    def _format_patterns(self, patterns: Dict[str, int]) -> str:
        """Format pattern frequencies for display"""
        if not patterns:
            return "  No significant patterns detected"
        
        formatted = []
        for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
            formatted.append(f"  {pattern}: {count}")
        return "\n".join(formatted)
    
    def _format_security(self, security_summary: Dict[str, Any]) -> str:
        """Format security summary for display"""
        if security_summary.get('security_analysis') == 'disabled':
            return "  Security analysis disabled"
        
        if security_summary.get('total_security_flags', 0) == 0:
            return "  No security threats detected"
        
        formatted = [f"  Total Security Flags: {security_summary['total_security_flags']}"]
        for threat, count in security_summary.get('threat_distribution', {}).items():
            formatted.append(f"  {threat}: {count}")
        return "\n".join(formatted)