"""
Neural Compiler for IPL - Compiler-First Architecture Integration
Unified neural compiler that integrates all intelligent components into a cohesive system
"""
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import hashlib
import time

try:
    from .ast_nodes import Program, ASTNode
    from .intelligent_lexer import CompilerFirstLexer
    from .intelligent_parser import CompilerFirstParser
    from .intelligent_semantic_analyzer import CompilerFirstSemanticAnalyzer
    from .intelligent_code_generator import CompilerFirstCodeGenerator
    from .intelligent_security_analyzer import CompilerFirstSecurityAnalyzer
    from .intelligent_type_system import CompilerFirstTypeSystem
    from .intelligent_optimizer import CompilerFirstOptimizer
    from .compiler import NeuroSymbolicCompiler, VerifiedAuditTrace
    from .rich.console import Console
except (ImportError, ValueError):
    from ast_nodes import Program, ASTNode
    from intelligent_lexer import CompilerFirstLexer
    from intelligent_parser import CompilerFirstParser
    from intelligent_semantic_analyzer import CompilerFirstSemanticAnalyzer
    from intelligent_code_generator import CompilerFirstCodeGenerator
    from intelligent_security_analyzer import CompilerFirstSecurityAnalyzer
    from intelligent_type_system import CompilerFirstTypeSystem
    from intelligent_optimizer import CompilerFirstOptimizer
    from compiler import NeuroSymbolicCompiler, VerifiedAuditTrace
    from rich.console import Console


@dataclass
class NeuralCompilationResult:
    """Complete neural compilation result with all intelligent analyses"""
    success: bool
    source_code: str
    ast: Optional[Program]
    lexical_analysis: Dict[str, Any]
    parsing_analysis: Dict[str, Any]
    semantic_analysis: Dict[str, Any]
    code_generation: Dict[str, Any]
    security_analysis: Dict[str, Any]
    type_analysis: Dict[str, Any]
    optimization_analysis: Dict[str, Any]
    generated_code: Optional[str]
    compilation_time: float
    overall_confidence: float
    intelligent_insights: List[str]
    warnings: List[str]
    errors: List[str]
    
    def __post_init__(self):
        if self.intelligent_insights is None:
            self.intelligent_insights = []
        if self.warnings is None:
            self.warnings = []
        if self.errors is None:
            self.errors = []


class NeuralCompiler:
    """
    Unified Neural Compiler - Compiler-First Architecture
    Integrates all intelligent components into a cohesive compilation pipeline:
    
    1. Intelligent Lexer - Neural token understanding and security detection
    2. Intelligent Parser - AI-enhanced parsing with error recovery
    3. Intelligent Semantic Analyzer - Deep semantic understanding
    4. Intelligent Type System - Advanced type inference
    5. Intelligent Security Analyzer - Neural threat detection
    6. Intelligent Code Generator - AI-powered optimization
    7. Intelligent Optimizer - Learning-based optimization
    
    This represents the culmination of the compiler-first architecture where
    intelligence is integrated at every level of the compilation process.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._default_config()
        self.console = Console()
        
        # Initialize all intelligent components
        self.intelligent_lexer = CompilerFirstLexer(
            "",  # Source will be provided during compilation
            self.config["lexer"]
        )
        
        self.intelligent_parser = CompilerFirstParser(
            "",  # Source will be provided during compilation
            self.config["parser"]
        )
        
        self.intelligent_semantic_analyzer = CompilerFirstSemanticAnalyzer(
            self.config["semantic_analyzer"]
        )
        
        self.intelligent_code_generator = CompilerFirstCodeGenerator(
            self.config["code_generator"]
        )
        
        self.intelligent_security_analyzer = CompilerFirstSecurityAnalyzer(
            self.config["security_analyzer"]
        )
        
        self.intelligent_type_system = CompilerFirstTypeSystem(
            self.config["type_system"]
        )
        
        self.intelligent_optimizer = CompilerFirstOptimizer(
            self.config["optimizer"]
        )
        
        # Traditional compiler for integration
        self.traditional_compiler = NeuroSymbolicCompiler(
            console=self.console,
            enable_expert_system=self.config.get("enable_expert_system", True)
        )
        
        # Compilation statistics
        self.compilation_history = []
        self.performance_metrics = defaultdict(list)
        
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for neural compiler"""
        return {
            "lexer": {
                "enable_neural_analysis": True,
                "enable_security_analysis": True,
                "enable_learning": True,
                "confidence_threshold": 0.7
            },
            "parser": {
                "enable_neural_parsing": True,
                "enable_semantic_validation": True,
                "enable_syntax_correction": True,
                "confidence_threshold": 0.7
            },
            "semantic_analyzer": {
                "enable_deep_analysis": True,
                "enable_security_analysis": True,
                "enable_optimization_suggestions": True,
                "confidence_threshold": 0.7
            },
            "code_generator": {
                "enable_ai_optimization": True,
                "target_language": "ipl",
                "optimization_level": "balanced",
                "quality_threshold": 0.7
            },
            "security_analyzer": {
                "enable_neural_detection": True,
                "enable_attack_vector_analysis": True,
                "enable_prevention_recommendations": True,
                "security_threshold": 0.7
            },
            "type_system": {
                "enable_neural_inference": True,
                "enable_semantic_types": True,
                "enable_type_suggestions": True,
                "consistency_threshold": 0.8
            },
            "optimizer": {
                "enable_learning": True,
                "optimization_level": "balanced",
                "max_passes": 3,
                "improvement_threshold": 0.05
            },
            "enable_expert_system": True,
            "enable_traditional_integration": True
        }
    
    def compile(self, source_code: str) -> NeuralCompilationResult:
        """
        Perform complete neural compilation
        Returns comprehensive compilation result with all intelligent analyses
        """
        start_time = time.time()
        
        try:
            # Step 1: Intelligent Lexical Analysis
            self.console.print("[cyan]🧠 Phase 1: Intelligent Lexical Analysis[/cyan]")
            lexical_analysis = self._perform_lexical_analysis(source_code)
            
            if "error" in lexical_analysis:
                return self._create_error_result(source_code, lexical_analysis, start_time)
            
            # Step 2: Intelligent Parsing
            self.console.print("[cyan]🧠 Phase 2: Intelligent Parsing[/cyan]")
            parsing_analysis = self._perform_parsing_analysis(source_code)
            
            if "error" in parsing_analysis:
                return self._create_error_result(source_code, parsing_analysis, start_time)
            
            ast = parsing_analysis["ast"]
            
            # Step 3: Intelligent Semantic Analysis
            self.console.print("[cyan]🧠 Phase 3: Intelligent Semantic Analysis[/cyan]")
            semantic_analysis = self._perform_semantic_analysis(ast)
            
            # Step 4: Intelligent Type Analysis
            self.console.print("[cyan]🧠 Phase 4: Intelligent Type Analysis[/cyan]")
            type_analysis = self._perform_type_analysis(ast)
            
            # Step 5: Intelligent Security Analysis
            self.console.print("[cyan]🧠 Phase 5: Intelligent Security Analysis[/cyan]")
            security_analysis = self._perform_security_analysis(ast)
            
            # Check if security analysis blocked compilation
            if not security_analysis["overall_security"].is_safe:
                return self._create_security_blocked_result(source_code, ast, security_analysis, start_time)
            
            # Step 6: Intelligent Optimization
            self.console.print("[cyan]🧠 Phase 6: Intelligent Optimization[/cyan]")
            optimization_analysis = self._perform_optimization_analysis(ast)
            
            # Step 7: Intelligent Code Generation
            self.console.print("[cyan]🧠 Phase 7: Intelligent Code Generation[/cyan]")
            code_generation = self._perform_code_generation(optimization_analysis["optimized_ast"])
            
            # Calculate compilation time
            compilation_time = time.time() - start_time
            
            # Calculate overall confidence
            overall_confidence = self._calculate_overall_confidence(
                lexical_analysis, parsing_analysis, semantic_analysis,
                type_analysis, security_analysis, optimization_analysis, code_generation
            )
            
            # Generate intelligent insights
            intelligent_insights = self._generate_intelligent_insights(
                lexical_analysis, parsing_analysis, semantic_analysis,
                type_analysis, security_analysis, optimization_analysis, code_generation
            )
            
            # Collect warnings
            warnings = self._collect_warnings(
                lexical_analysis, parsing_analysis, semantic_analysis,
                type_analysis, security_analysis, optimization_analysis
            )
            
            # Create successful result
            result = NeuralCompilationResult(
                success=True,
                source_code=source_code,
                ast=ast,
                lexical_analysis=lexical_analysis,
                parsing_analysis=parsing_analysis,
                semantic_analysis=semantic_analysis,
                code_generation=code_generation,
                security_analysis=security_analysis,
                type_analysis=type_analysis,
                optimization_analysis=optimization_analysis,
                generated_code=code_generation["generated_code"],
                compilation_time=compilation_time,
                overall_confidence=overall_confidence,
                intelligent_insights=intelligent_insights,
                warnings=warnings,
                errors=[]
            )
            
            # Add to compilation history
            self.compilation_history.append(result)
            
            # Update performance metrics
            self._update_performance_metrics(result)
            
            return result
            
        except Exception as e:
            # Handle unexpected errors
            return self._create_error_result(source_code, {"error": str(e)}, start_time)
    
    def _perform_lexical_analysis(self, source_code: str) -> Dict[str, Any]:
        """Perform intelligent lexical analysis"""
        # Reinitialize lexer with actual source code
        self.intelligent_lexer = CompilerFirstLexer(source_code, self.config["lexer"])
        return self.intelligent_lexer.analyze_source()
    
    def _perform_parsing_analysis(self, source_code: str) -> Dict[str, Any]:
        """Perform intelligent parsing analysis"""
        # Reinitialize parser with actual source code
        self.intelligent_parser = CompilerFirstParser(source_code, self.config["parser"])
        return self.intelligent_parser.parse_source()
    
    def _perform_semantic_analysis(self, ast: Program) -> Dict[str, Any]:
        """Perform intelligent semantic analysis"""
        return self.intelligent_semantic_analyzer.analyze_program(ast)
    
    def _perform_type_analysis(self, ast: Program) -> Dict[str, Any]:
        """Perform intelligent type analysis"""
        return self.intelligent_type_system.analyze_program_types(ast)
    
    def _perform_security_analysis(self, ast: Program) -> Dict[str, Any]:
        """Perform intelligent security analysis"""
        return self.intelligent_security_analyzer.analyze_program_security(ast)
    
    def _perform_optimization_analysis(self, ast: Program) -> Dict[str, Any]:
        """Perform intelligent optimization analysis"""
        return self.intelligent_optimizer.optimize_program(ast)
    
    def _perform_code_generation(self, ast: Program) -> Dict[str, Any]:
        """Perform intelligent code generation"""
        return self.intelligent_code_generator.generate_program(ast)
    
    def _calculate_overall_confidence(self, *analyses) -> float:
        """Calculate overall confidence from all analyses"""
        confidences = []
        
        for analysis in analyses:
            if isinstance(analysis, dict):
                # Extract confidence from various analysis types
                if "parse_confidence" in analysis:
                    confidences.append(analysis["parse_confidence"])
                elif "generation_confidence" in analysis:
                    confidences.append(analysis["generation_confidence"])
                elif "confidence" in analysis:
                    confidences.append(analysis["confidence"])
                elif "overall_security" in analysis:
                    confidences.append(analysis["overall_security"].confidence)
        
        if not confidences:
            return 0.5
        
        return sum(confidences) / len(confidences)
    
    def _generate_intelligent_insights(self, *analyses) -> List[str]:
        """Generate comprehensive intelligent insights"""
        insights = []
        
        for analysis in analyses:
            if isinstance(analysis, dict):
                # Extract insights from various analysis types
                if "ai_insights" in analysis:
                    insights.extend(analysis["ai_insights"])
                if "intelligent_insights" in analysis:
                    insights.extend(analysis["intelligent_insights"])
                if "learning_insights" in analysis:
                    insights.extend(analysis["learning_insights"])
                if "recommendations" in analysis:
                    insights.extend(analysis["recommendations"])
        
        # Add compiler-level insights
        if len(self.compilation_history) > 5:
            insights.append("Compiler has accumulated sufficient learning data for improved predictions")
        
        return list(set(insights))  # Remove duplicates
    
    def _collect_warnings(self, *analyses) -> List[str]:
        """Collect warnings from all analyses"""
        warnings = []
        
        for analysis in analyses:
            if isinstance(analysis, dict):
                # Extract warnings from various analysis types
                if "warnings" in analysis:
                    warnings.extend(analysis["warnings"])
                if "ai_suggestions" in analysis:
                    # Treat AI suggestions as warnings if they indicate potential issues
                    warnings.extend([s for s in analysis["ai_suggestions"] if "warning" in s.lower()])
        
        return warnings
    
    def _create_error_result(self, source_code: str, error_analysis: Dict[str, Any], 
                           start_time: float) -> NeuralCompilationResult:
        """Create error result"""
        return NeuralCompilationResult(
            success=False,
            source_code=source_code,
            ast=None,
            lexical_analysis={},
            parsing_analysis={},
            semantic_analysis={},
            code_generation={},
            security_analysis={},
            type_analysis={},
            optimization_analysis={},
            generated_code=None,
            compilation_time=time.time() - start_time,
            overall_confidence=0.0,
            intelligent_insights=[],
            warnings=[],
            errors=[error_analysis.get("error", "Unknown error")]
        )
    
    def _create_security_blocked_result(self, source_code: str, ast: Program, 
                                       security_analysis: Dict[str, Any], 
                                       start_time: float) -> NeuralCompilationResult:
        """Create security blocked result"""
        return NeuralCompilationResult(
            success=False,
            source_code=source_code,
            ast=ast,
            lexical_analysis={},
            parsing_analysis={},
            semantic_analysis={},
            code_generation={},
            security_analysis=security_analysis,
            type_analysis={},
            optimization_analysis={},
            generated_code=None,
            compilation_time=time.time() - start_time,
            overall_confidence=0.0,
            intelligent_insights=security_analysis["overall_security"].ai_insights,
            warnings=[],
            errors=[f"Security blocked: {security_analysis['overall_security'].threat_level} threat level detected"]
        )
    
    def _update_performance_metrics(self, result: NeuralCompilationResult):
        """Update performance metrics"""
        self.performance_metrics["compilation_time"].append(result.compilation_time)
        self.performance_metrics["confidence"].append(result.overall_confidence)
        self.performance_metrics["security_score"].append(
            result.security_analysis.get("overall_security", {}).security_score if result.security_analysis else 0.0
        )
    
    def get_compilation_statistics(self) -> Dict[str, Any]:
        """Get compilation statistics"""
        return {
            "total_compilations": len(self.compilation_history),
            "average_compilation_time": sum(self.performance_metrics["compilation_time"]) / len(self.performance_metrics["compilation_time"]) if self.performance_metrics["compilation_time"] else 0.0,
            "average_confidence": sum(self.performance_metrics["confidence"]) / len(self.performance_metrics["confidence"]) if self.performance_metrics["confidence"] else 0.0,
            "average_security_score": sum(self.performance_metrics["security_score"]) / len(self.performance_metrics["security_score"]) if self.performance_metrics["security_score"] else 0.0,
            "config": self.config
        }
    
    def get_compilation_summary(self, result: NeuralCompilationResult) -> str:
        """Get human-readable compilation summary"""
        if not result.success:
            return f"""
Neural Compilation Failed
=========================
Error: {result.errors[0] if result.errors else 'Unknown error'}
Compilation Time: {result.compilation_time:.3f}s
"""
        
        summary = f"""
Neural Compilation Summary
========================
Status: {'✅ SUCCESS' if result.success else '❌ FAILED'}
Compilation Time: {result.compilation_time:.3f}s
Overall Confidence: {result.overall_confidence:.2%}

Intelligent Components Status:
-----------------------------
Intelligent Lexer: {'✅ Enabled' if self.config['lexer']['enable_neural_analysis'] else '❌ Disabled'}
Intelligent Parser: {'✅ Enabled' if self.config['parser']['enable_neural_parsing'] else '❌ Disabled'}
Intelligent Semantic Analyzer: {'✅ Enabled' if self.config['semantic_analyzer']['enable_deep_analysis'] else '❌ Disabled'}
Intelligent Type System: {'✅ Enabled' if self.config['type_system']['enable_neural_inference'] else '❌ Disabled'}
Intelligent Security Analyzer: {'✅ Enabled' if self.config['security_analyzer']['enable_neural_detection'] else '❌ Disabled'}
Intelligent Code Generator: {'✅ Enabled' if self.config['code_generator']['enable_ai_optimization'] else '❌ Disabled'}
Intelligent Optimizer: {'✅ Enabled' if self.config['optimizer']['enable_learning'] else '❌ Disabled'}

Analysis Results:
---------------
Lexical Analysis: {len(result.lexical_analysis.get('tokens', []))} tokens
Parsing Confidence: {result.parsing_analysis.get('parse_confidence', 0):.2%}
Semantic Patterns: {len(result.semantic_analysis.get('global_patterns', []))} patterns
Type Consistency: {result.type_analysis.get('type_summary', {}).get('consistency_score', 0):.2%}
Security Score: {result.security_analysis.get('overall_security', {}).security_score if result.security_analysis else 0:.2%}
Optimization Score: {result.optimization_analysis.get('optimization_score', 0):.2%}
Code Generation Confidence: {result.code_generation.get('generation_confidence', 0):.2%}

Intelligent Insights:
--------------------
{self._format_insights(result.intelligent_insights)}

Warnings:
--------
{self._format_warnings(result.warnings)}

Generated Code:
--------------
{result.generated_code if result.generated_code else 'No code generated'}
"""
        return summary
    
    def _format_insights(self, insights: List[str]) -> str:
        """Format intelligent insights for display"""
        if not insights:
            return "  No insights available"
        return "\n".join([f"  - {insight}" for insight in insights])
    
    def _format_warnings(self, warnings: List[str]) -> str:
        """Format warnings for display"""
        if not warnings:
            return "  No warnings"
        return "\n".join([f"  - {warning}" for warning in warnings])


class CompilerFirstNeuralCompiler:
    """
    Main entry point for the Compiler-First Neural Compiler
    This represents the complete integration of all intelligent components
    into a unified neural compilation system.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.neural_compiler = NeuralCompiler(config)
        self.console = Console()
        
    def compile_source(self, source_code: str) -> Dict[str, Any]:
        """
        Compile source code using the complete neural compiler
        Returns comprehensive compilation analysis
        """
        # Perform neural compilation
        result = self.neural_compiler.compile(source_code)
        
        # Convert to dictionary for easy serialization
        compilation_dict = {
            "success": result.success,
            "source_code": result.source_code,
            "compilation_time": result.compilation_time,
            "overall_confidence": result.overall_confidence,
            "lexical_analysis": result.lexical_analysis,
            "parsing_analysis": result.parsing_analysis,
            "semantic_analysis": result.semantic_analysis,
            "type_analysis": result.type_analysis,
            "security_analysis": result.security_analysis,
            "optimization_analysis": result.optimization_analysis,
            "code_generation": result.code_generation,
            "generated_code": result.generated_code,
            "intelligent_insights": result.intelligent_insights,
            "warnings": result.warnings,
            "errors": result.errors,
            "statistics": self.neural_compiler.get_compilation_statistics(),
            "compilation_timestamp": self._get_timestamp()
        }
        
        return compilation_dict
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for compilation tracking"""
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def print_compilation_result(self, result: NeuralCompilationResult):
        """Print comprehensive compilation result"""
        self.console.print(self.neural_compiler.get_compilation_summary(result))
        
        if result.success:
            self.console.print("\n[green]✅ Neural Compilation Successful[/green]")
            
            # Print detailed analysis results
            self.console.print("\n[cyan]Detailed Analysis Results:[/cyan]")
            
            if result.lexical_analysis:
                self.console.print("\n[yellow]Lexical Analysis:[/yellow]")
                self.console.print(f"  Tokens: {len(result.lexical_analysis.get('tokens', []))}")
                self.console.print(f"  Security Flags: {result.lexical_analysis.get('security_summary', {}).get('total_security_flags', 0)}")
            
            if result.parsing_analysis:
                self.console.print("\n[yellow]Parsing Analysis:[/yellow]")
                self.console.print(f"  Confidence: {result.parsing_analysis.get('parse_confidence', 0):.2%}")
                self.console.print(f"  Strategy: {result.parsing_analysis.get('parsing_strategy', 'unknown')}")
            
            if result.semantic_analysis:
                self.console.print("\n[yellow]Semantic Analysis:[/yellow]")
                self.console.print(f"  Patterns: {len(result.semantic_analysis.get('global_patterns', []))}")
                self.console.print(f"  Security Implications: {len(result.semantic_analysis.get('security_summary', {}))}")
            
            if result.type_analysis:
                self.console.print("\n[yellow]Type Analysis:[/yellow]")
                type_summary = result.type_analysis.get('type_summary', {})
                self.console.print(f"  Consistency: {type_summary.get('consistency_score', 0):.2%}")
                self.console.print(f"  Conflicts: {type_summary.get('type_conflicts', 0)}")
            
            if result.security_analysis:
                self.console.print("\n[yellow]Security Analysis:[/yellow]")
                overall_security = result.security_analysis.get('overall_security', {})
                self.console.print(f"  Threat Level: {overall_security.threat_level if hasattr(overall_security, 'threat_level') else 'unknown'}")
                self.console.print(f"  Security Score: {overall_security.security_score if hasattr(overall_security, 'security_score') else 0:.2%}")
            
            if result.optimization_analysis:
                self.console.print("\n[yellow]Optimization Analysis:[/yellow]")
                self.console.print(f"  Optimization Score: {result.optimization_analysis.get('optimization_score', 0):.2%}")
                self.console.print(f"  Performance Improvement: {result.optimization_analysis.get('performance_improvement', 0):.2%}")
            
            if result.code_generation:
                self.console.print("\n[yellow]Code Generation:[/yellow]")
                self.console.print(f"  Confidence: {result.code_generation.get('generation_confidence', 0):.2%}")
                self.console.print(f"  Strategy: {result.code_generation.get('generation_strategy', 'unknown')}")
            
            if result.generated_code:
                self.console.print("\n[cyan]Generated Code:[/cyan]")
                self.console.print(result.generated_code)
            
            if result.intelligent_insights:
                self.console.print("\n[magenta]Intelligent Insights:[/magenta]")
                for insight in result.intelligent_insights:
                    self.console.print(f"  • {insight}")
            
            if result.warnings:
                self.console.print("\n[yellow]Warnings:[/yellow]")
                for warning in result.warnings:
                    self.console.print(f"  ⚠️  {warning}")
        else:
            self.console.print("\n[red]❌ Neural Compilation Failed[/red]")
            for error in result.errors:
                self.console.print(f"  Error: {error}")
    
    def get_compiler_info(self) -> Dict[str, Any]:
        """Get information about the neural compiler"""
        return {
            "compiler_type": "Compiler-First Neural Compiler",
            "version": "1.0.0",
            "architecture": "Neural-Symbolic Hybrid",
            "intelligent_components": [
                "Intelligent Lexer",
                "Intelligent Parser", 
                "Intelligent Semantic Analyzer",
                "Intelligent Type System",
                "Intelligent Security Analyzer",
                "Intelligent Code Generator",
                "Intelligent Optimizer"
            ],
            "capabilities": [
                "Neural token understanding",
                "AI-enhanced parsing with error recovery",
                "Deep semantic analysis",
                "Advanced type inference",
                "Neural threat detection",
                "AI-powered code optimization",
                "Learning-based optimization"
            ],
            "config": self.neural_compiler.config,
            "statistics": self.neural_compiler.get_compilation_statistics()
        }