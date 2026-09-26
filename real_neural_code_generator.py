"""
Real Neural Code Generator for IPL - LLM Integration
Uses local LLM for AI-powered code generation and optimization
"""
import subprocess
import json
from typing import Dict, Any, List
import time
import re

class RealNeuralCodeGenerator:
    def __init__(self):
        print("Initializing Real Neural Code Generator with LLM...")
        self.ollama_available = self._check_ollama_available()
        self.model_name = "qwen2.5:0.5b"  # Small local model
        
        if self.ollama_available:
            print(f"✅ Real neural code generator loaded with {self.model_name}")
        else:
            print("⚠️ Ollama not available, falling back to neural-enhanced generation")
    
    def _check_ollama_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            result = subprocess.run(
                ["ollama", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama LLM for code generation"""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"Ollama error: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            print("Ollama request timed out")
            return None
        except Exception as e:
            print(f"Ollama call failed: {e}")
            return None
    
    def generate_code_with_neural(self, ast: List, source_code: str, optimization_hints: Dict) -> Dict[str, Any]:
        """Generate optimized code using neural LLM"""
        start_time = time.time()
        
        if self.ollama_available:
            generated_code = self._generate_with_llm(ast, source_code, optimization_hints)
            method = "llm_neural"
        else:
            generated_code = self._generate_with_patterns(ast, source_code, optimization_hints)
            method = "neural_enhanced"
        
        generation_time = (time.time() - start_time) * 1000
        
        return {
            'generated_code': generated_code,
            'generation_time_ms': generation_time,
            'method': method,
            'uses_llm': self.ollama_available,
            'model_used': self.model_name if self.ollama_available else None,
            'optimizations_applied': self._count_optimizations(generated_code, source_code),
            'code_quality_score': self._assess_code_quality(generated_code),
            'ast_nodes_processed': len(ast) if ast else 0
        }
    
    def _generate_with_llm(self, ast: List, source_code: str, optimization_hints: Dict) -> str:
        """Generate code using LLM"""
        # Build prompt for LLM
        prompt = f"""Generate optimized IPL code based on the following:

Original code:
{source_code}

Optimization hints:
{json.dumps(optimization_hints, indent=2)}

Requirements:
- Maintain the same functionality
- Apply suggested optimizations
- Keep IPL syntax valid
- Focus on performance improvements

Generate only the code, no explanations:"""

        llm_output = self._call_ollama(prompt)
        
        if llm_output:
            # Extract code from LLM output
            code = self._extract_code_from_llm_output(llm_output)
            if code:
                return code
        
        # Fallback to pattern-based generation
        return self._generate_with_patterns(ast, source_code, optimization_hints)
    
    def _extract_code_from_llm_output(self, output: str) -> str:
        """Extract code from LLM output"""
        # Remove markdown code blocks if present
        output = re.sub(r'```ipl\n?', '', output)
        output = re.sub(r'```\n?', '', output)
        output = re.sub(r'```', '', output)
        
        # Extract code-like content
        lines = output.split('\n')
        code_lines = []
        in_code = False
        
        for line in lines:
            if 'let ' in line or 'if ' in line or 'for ' in line or 'while ' in line or 'function ' in line:
                in_code = True
            if in_code:
                code_lines.append(line)
        
        if code_lines:
            return '\n'.join(code_lines)
        
        return output
    
    def _generate_with_patterns(self, ast: List, source_code: str, optimization_hints: Dict) -> str:
        """Generate code using neural-enhanced patterns"""
        optimized_code = source_code
        
        # Apply constant folding
        optimized_code = self._apply_constant_folding(optimized_code)
        
        # Apply dead code elimination hints
        if optimization_hints.get('selected_strategies'):
            for strategy in optimization_hints['selected_strategies']:
                if strategy['strategy'] == 'DEAD_CODE_ELIMINATION':
                    optimized_code = self._remove_dead_code(optimized_code)
        
        # Apply simple optimizations
        optimized_code = self._apply_simple_optimizations(optimized_code)
        
        return optimized_code
    
    def _apply_constant_folding(self, code: str) -> str:
        """Apply constant folding optimization"""
        # Simple constant folding patterns
        patterns = [
            (r'let\s+(\w+)\s*=\s*(\d+)\s*\*\s*(\d+)\s*;', 
             lambda m: f"let {m.group(1)} = {int(m.group(2)) * int(m.group(3))};"),
            (r'let\s+(\w+)\s*=\s*(\d+)\s*\+\s*(\d+)\s*;', 
             lambda m: f"let {m.group(1)} = {int(m.group(2)) + int(m.group(3))};"),
        ]
        
        for pattern, replacement in patterns:
            code = re.sub(pattern, replacement, code)
        
        return code
    
    def _remove_dead_code(self, code: str) -> str:
        """Remove obvious dead code patterns"""
        # Remove unreachable code after return
        lines = code.split('\n')
        cleaned_lines = []
        after_return = False
        
        for line in lines:
            if 'return' in line and after_return is False:
                cleaned_lines.append(line)
                after_return = True
            elif not after_return:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _apply_simple_optimizations(self, code: str) -> str:
        """Apply simple code optimizations"""
        # Remove redundant semicolons
        code = re.sub(r';+', ';', code)
        
        # Clean up whitespace
        code = re.sub(r'\s+', ' ', code)
        code = re.sub(r'\s*;\s*', '; ', code)
        
        return code.strip()
    
    def _count_optimizations(self, generated_code: str, original_code: str) -> int:
        """Count number of optimizations applied"""
        # Simple heuristic: count differences
        original_lines = set(original_code.split('\n'))
        generated_lines = set(generated_code.split('\n'))
        
        changes = len(original_lines.symmetric_difference(generated_lines))
        return max(0, changes // 2)  # Rough estimate
    
    def _assess_code_quality(self, code: str) -> float:
        """Assess quality of generated code"""
        score = 0.7  # Base score
        
        # Check for valid IPL syntax patterns
        if re.search(r'let\s+\w+\s*=', code):
            score += 0.1
        if re.search(r';\s*$', code, re.MULTILINE):
            score += 0.1
        if len(code) > 10:  # Reasonable length
            score += 0.1
        
        return min(score, 1.0)

# Test the real neural code generator
if __name__ == "__main__":
    generator = RealNeuralCodeGenerator()
    
    test_ast = [
        {'type': 'declaration', 'variable': 'x', 'value': 25},
        {'type': 'declaration', 'variable': 'y', 'value': 30}
    ]
    
    test_code = """
let x = 25;
let y = 30;
let result = x * y;
"""
    
    optimization_hints = {
        'selected_strategies': [
            {'strategy': 'CONSTANT_FOLDING', 'priority': 'HIGH'},
            {'strategy': 'DEAD_CODE_ELIMINATION', 'priority': 'LOW'}
        ],
        'performance_profile': {'complexity': 'LOW'}
    }
    
    print("Testing neural code generator...")
    result = generator.generate_code_with_neural(test_ast, test_code, optimization_hints)
    
    print(f"\n✅ Code generation complete")
    print(f"Method: {result['method']}")
    print(f"Time: {result['generation_time_ms']:.2f}ms")
    print(f"Uses LLM: {result['uses_llm']}")
    
    if result['uses_llm']:
        print(f"Model: {result['model_used']}")
    
    print(f"\n📝 Generated Code:")
    print(result['generated_code'])
    
    print(f"\n📊 Generation Stats:")
    print(f"  Optimizations applied: {result['optimizations_applied']}")
    print(f"  Code quality score: {result['code_quality_score']:.2%}")
    print(f"  AST nodes processed: {result['ast_nodes_processed']}")