"""
Intelligent Lexer for IPL (Intelligent Programming Language).
Implements semantic tokenization with AI-enhanced understanding.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import re
import json
import urllib.request
import urllib.error

try:
    from .tokens import Token, TokenType
    from .lexer import Lexer as TraditionalLexer
except (ImportError, ValueError):
    from tokens import Token, TokenType
    from lexer import Lexer as TraditionalLexer


class SemanticCategory(Enum):
    """Semantic categories for enhanced token understanding."""
    DECLARATION = "declaration"      # let, var, fn
    OPERATION = "operation"          # arithmetic, logical operations
    CONTROL_FLOW = "control_flow"    # if, for, while
    DATA_TYPE = "data_type"          # Int, String, Currency, etc.
    FUNCTION_CALL = "function_call"  # function invocations
    LITERAL = "literal"              # numbers, strings, booleans
    IDENTIFIER = "identifier"        # variable names
    SECURITY = "security"            # sanitize, secure, trusted
    UNKNOWN = "unknown"              # ambiguous tokens


@dataclass
class SemanticToken:
    """Enhanced token with semantic understanding."""
    token: Token                    # Original token
    semantic_category: SemanticCategory
    probable_type: Optional[str] = None  # Likely data type
    context_clues: List[str] = field(default_factory=list)
    confidence: float = 1.0         # Confidence in semantic classification
    ai_insights: List[str] = field(default_factory=list)
    
    def __repr__(self) -> str:
        return (f"SemanticToken({self.token.type.name}, {repr(self.token.value)}, "
                f"category={self.semantic_category.value}, type={self.probable_type}, "
                f"confidence={self.confidence:.2f})")


class AIEnhancedTokenizer:
    """AI-enhanced token classification for semantic understanding."""
    
    def __init__(self, ollama_endpoint: str = "http://localhost:11434", model: str = "qwen2.5-coder:0.5b"):
        self.ollama_endpoint = ollama_endpoint
        self.model = model
        self.cache: Dict[str, SemanticCategory] = {}
    
    def classify_token_semantic(self, token: Token, context: str) -> tuple[SemanticCategory, List[str]]:
        """Classify token semantic category using AI-enhanced analysis."""
        
        # Check cache first for performance
        cache_key = f"{token.type.name}_{token.value}"
        if cache_key in self.cache:
            return self.cache[cache_key], []
        
        # Rule-based classification for performance
        rule_based_category = self._rule_based_classification(token)
        
        # Use AI for ambiguous or complex cases
        if self._needs_ai_analysis(token, context):
            try:
                ai_category, ai_insights = self._ai_classify_token(token, context)
                self.cache[cache_key] = ai_category
                return ai_category, ai_insights
            except Exception as e:
                # Fallback to rule-based if AI fails
                return rule_based_category, [f"AI analysis failed: {str(e)}"]
        
        self.cache[cache_key] = rule_based_category
        return rule_based_category, []
    
    def _rule_based_classification(self, token: Token) -> SemanticCategory:
        """Fast rule-based semantic classification."""
        
        # Keywords
        if token.type in (TokenType.LET, TokenType.VAR):
            return SemanticCategory.DECLARATION
        if token.type == TokenType.FN:
            return SemanticCategory.DECLARATION
        if token.type in (TokenType.IF, TokenType.ELIF, TokenType.ELSE, 
                       TokenType.FOR, TokenType.WHILE, TokenType.BREAK, TokenType.CONTINUE):
            return SemanticCategory.CONTROL_FLOW
        if token.type in (TokenType.SANITIZE, TokenType.SECURE, TokenType.TRUSTED):
            return SemanticCategory.SECURITY
        
        # Literals
        if token.type in (TokenType.NUMBER, TokenType.STRING, TokenType.TRUE, TokenType.FALSE):
            return SemanticCategory.LITERAL
        
        # Operators
        if token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH,
                       TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.GT):
            return SemanticCategory.OPERATION
        
        # Identifiers (need context for better classification)
        if token.type == TokenType.IDENTIFIER:
            return SemanticCategory.IDENTIFIER
        
        return SemanticCategory.UNKNOWN
    
    def _needs_ai_analysis(self, token: Token, context: str) -> bool:
        """Determine if token needs AI analysis for better classification."""
        
        # Only use AI for identifiers where context matters
        if token.type != TokenType.IDENTIFIER:
            return False
        
        # Use AI for complex or ambiguous identifiers
        identifier = str(token.value)
        
        # Simple identifiers don't need AI
        if len(identifier) <= 3:
            return False
        
        # Identifiers with numbers or underscores might need AI
        if any(char.isdigit() or char == '_' for char in identifier):
            return True
        
        # Identifiers in complex contexts might need AI
        if len(context) > 100:  # Complex code context
            return True
        
        return False
    
    def _ai_classify_token(self, token: Token, context: str) -> tuple[SemanticCategory, List[str]]:
        """Use AI to classify token semantic category."""
        
        prompt = f"""You are a programming language expert. Classify this token:

Token: {token.value}
Token Type: {token.type.name}
Context: {context[:200]}...

Classify the semantic category:
- declaration (variable/function declaration)
- operation (arithmetic/logical operation)
- control_flow (if/for/while statements)
- data_type (type annotations)
- function_call (function invocation)
- literal (numbers, strings, booleans)
- identifier (variable names)
- security (sanitize, secure, trusted)

Respond with just the category name (one word)."""
        
        try:
            url = f"{self.ollama_endpoint}/api/generate"
            data = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "max_tokens": 10
                }
            }
            
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode('utf-8'))
                ai_response = result.get('response', '').strip().lower()
                
                # Map AI response to semantic category
                category_mapping = {
                    'declaration': SemanticCategory.DECLARATION,
                    'operation': SemanticCategory.OPERATION,
                    'control_flow': SemanticCategory.CONTROL_FLOW,
                    'data_type': SemanticCategory.DATA_TYPE,
                    'function_call': SemanticCategory.FUNCTION_CALL,
                    'literal': SemanticCategory.LITERAL,
                    'identifier': SemanticCategory.IDENTIFIER,
                    'security': SemanticCategory.SECURITY
                }
                
                category = category_mapping.get(ai_response, SemanticCategory.UNKNOWN)
                insights = [f"AI classified as: {ai_response}"]
                
                return category, insights
                
        except Exception as e:
            raise Exception(f"AI classification failed: {e}")


class IntelligentLexer:
    """Intelligent lexer with semantic tokenization and AI-enhanced understanding."""
    
    def __init__(self, source: str, enable_ai: bool = True, ollama_endpoint: str = "http://localhost:11434"):
        self.source = source
        self.enable_ai = enable_ai
        self.ollama_endpoint = ollama_endpoint
        
        # Initialize components
        self.traditional_lexer = TraditionalLexer(source)
        self.ai_tokenizer = AIEnhancedTokenizer(ollama_endpoint) if enable_ai else None
        
        # Performance tracking
        self.stats = {
            'total_tokens': 0,
            'ai_enhanced_tokens': 0,
            'rule_based_tokens': 0,
            'cache_hits': 0
        }
    
    def tokenize(self) -> List[SemanticToken]:
        """Perform intelligent tokenization with semantic understanding."""
        
        # Get traditional tokens first
        traditional_tokens = self.traditional_lexer.tokenize()
        
        # Enhance with semantic understanding
        semantic_tokens = []
        context = self.source
        
        for i, token in enumerate(traditional_tokens):
            self.stats['total_tokens'] += 1
            
            # Extract context around token for AI analysis
            token_context = self._extract_token_context(token, traditional_tokens, i)
            
            # Classify semantic category
            if self.enable_ai and self.ai_tokenizer:
                semantic_category, ai_insights = self.ai_tokenizer.classify_token_semantic(token, token_context)
                
                if ai_insights and "AI classified as" in str(ai_insights):
                    self.stats['ai_enhanced_tokens'] += 1
                else:
                    self.stats['rule_based_tokens'] += 1
            else:
                # Rule-based only
                semantic_category = self.ai_tokenizer._rule_based_classification(token) if self.ai_tokenizer else SemanticCategory.UNKNOWN
                self.stats['rule_based_tokens'] += 1
            
            # Infer probable type
            probable_type = self._infer_probable_type(token, semantic_category, token_context)
            
            # Create semantic token
            semantic_token = SemanticToken(
                token=token,
                semantic_category=semantic_category,
                probable_type=probable_type,
                context_clues=self._extract_context_clues(token, token_context),
                confidence=0.9 if semantic_category != SemanticCategory.UNKNOWN else 0.5,
                ai_insights=ai_insights if self.enable_ai and self.ai_tokenizer else []
            )
            
            semantic_tokens.append(semantic_token)
        
        return semantic_tokens
    
    def _extract_token_context(self, token: Token, all_tokens: List[Token], token_index: int) -> str:
        """Extract context around a token for AI analysis."""
        
        # Get tokens within a window (3 before, 3 after)
        window_size = 3
        start = max(0, token_index - window_size)
        end = min(len(all_tokens), token_index + window_size + 1)
        
        context_tokens = all_tokens[start:end]
        context = " ".join(str(t.value) for t in context_tokens if t.value is not None)
        
        return context
    
    def _infer_probable_type(self, token: Token, category: SemanticCategory, context: str) -> Optional[str]:
        """Infer probable data type based on token and context."""
        
        # Based on token type
        if token.type == TokenType.NUMBER:
            return "Int" if isinstance(token.value, int) else "Float"
        if token.type == TokenType.STRING:
            return "String"
        if token.type in (TokenType.TRUE, TokenType.FALSE):
            return "Boolean"
        
        # Based on semantic category
        if category == SemanticCategory.DATA_TYPE:
            return str(token.value).title()  # e.g., "Int", "String"
        
        # Based on context patterns
        if category == SemanticCategory.IDENTIFIER:
            # Look for type annotations
            if ":" in context:
                parts = context.split(":")
                if len(parts) > 1:
                    potential_type = parts[1].strip().split()[0]
                    if potential_type.isalpha():
                        return potential_type.capitalize()
        
        return None
    
    def _extract_context_clues(self, token: Token, context: str) -> List[str]:
        """Extract contextual clues about the token."""
        
        clues = []
        
        # Look for type annotations
        if ":" in context:
            clues.append("type_annotation_present")
        
        # Look for function patterns
        if "fn" in context or "function" in context:
            clues.append("function_context")
        
        # Look for control flow
        if any(keyword in context for keyword in ["if", "for", "while"]):
            clues.append("control_flow_context")
        
        # Look for security operations
        if any(keyword in context for keyword in ["sanitize", "secure", "trusted"]):
            clues.append("security_context")
        
        return clues
    
    def get_stats(self) -> Dict[str, Any]:
        """Get tokenization statistics."""
        ai_percentage = (self.stats['ai_enhanced_tokens'] / self.stats['total_tokens'] * 100) if self.stats['total_tokens'] > 0 else 0
        
        return {
            **self.stats,
            'ai_enhancement_percentage': ai_percentage,
            'intelligence_mode': 'ai_enhanced' if self.enable_ai else 'rule_based'
        }
    
    def print_stats(self):
        """Print tokenization statistics."""
        stats = self.get_stats()
        
        print("\n" + "="*60)
        print("INTELLIGENT LEXER STATISTICS")
        print("="*60)
        print(f"Total Tokens: {stats['total_tokens']}")
        print(f"AI-Enhanced Tokens: {stats['ai_enhanced_tokens']}")
        print(f"Rule-Based Tokens: {stats['rule_based_tokens']}")
        print(f"AI Enhancement: {stats['ai_enhancement_percentage']:.1f}%")
        print(f"Intelligence Mode: {stats['intelligence_mode']}")
        print("="*60)