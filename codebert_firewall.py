"""
CodeBERT-based Intelligent Firewall for IPL
Uses pretrained CodeBERT model for code understanding and security analysis
"""
import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer
from typing import Dict, Any, Tuple, List
import os

# Set fixed seed for reproducibility
torch.manual_seed(42)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(42)


class CodeBERTSecurityModel(nn.Module):
    """CodeBERT-based security classifier"""
    
    def __init__(self, model_name="microsoft/codebert-base"):
        super().__init__()
        self.codebert = AutoModel.from_pretrained(model_name)
        self.classifier = nn.Linear(768, 2)  # 768 is CodeBERT output dimension
        self.dropout = nn.Dropout(0.1)
    
    def forward(self, input_ids, attention_mask):
        # Get CodeBERT embeddings
        outputs = self.codebert(input_ids=input_ids, attention_mask=attention_mask)
        # Use [CLS] token embedding (first token)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        # Apply dropout
        cls_embedding = self.dropout(cls_embedding)
        # Classify
        logits = self.classifier(cls_embedding)
        return logits


class IntelligentFirewall:
    """
    Intelligent Firewall using CodeBERT for code understanding
    Replaces the simple neural network with pretrained code model
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize CodeBERT-based firewall
        
        Args:
            model_path: Path to trained model (if None, uses pretrained without fine-tuning)
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"CodeBERT Firewall initialized on device: {self.device}")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        
        # Load model
        if model_path and os.path.exists(model_path):
            # Load fine-tuned model
            self.model = CodeBERTSecurityModel()
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            print(f"Loaded fine-tuned model from: {model_path}")
        else:
            # Use pretrained model (no fine-tuning yet)
            self.model = CodeBERTSecurityModel()
            print("Using pretrained CodeBERT (not fine-tuned on vulnerabilities yet)")
        
        self.model.to(self.device)
        self.model.eval()
    
    def ast_to_string(self, node) -> str:
        """
        Convert AST node to code string for CodeBERT analysis
        This is a simplified version - in production, use proper AST to code conversion
        """
        # Simple string representation for now
        if hasattr(node, 'value'):
            return str(node.value)
        elif hasattr(node, 'name'):
            return node.name
        elif hasattr(node, 'intent_prompt'):
            return node.intent_prompt
        else:
            return str(type(node).__name__)
    
    def check_code(self, code_snippet: str) -> Tuple[bool, float, str]:
        """
        Check if code snippet is safe using CodeBERT
        
        Args:
            code_snippet: Code string to analyze
            
        Returns:
            (is_safe, confidence, reasoning)
        """
        # Tokenize
        inputs = self.tokenizer(
            code_snippet,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        # Move to device
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)
        
        # Get prediction
        with torch.no_grad():
            logits = self.model(input_ids, attention_mask)
            probs = torch.softmax(logits, dim=1)
            safe_prob = probs[0][1].item()  # Index 1 = safe
            is_safe = safe_prob > 0.5
            confidence = max(safe_prob, 1 - safe_prob)
        
        reasoning = f"CodeBERT analysis: safe probability = {safe_prob:.3f}"
        
        return is_safe, confidence, reasoning
    
    def verify_ast_node(self, node, context: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
        """
        Verify AST node using CodeBERT
        
        Args:
            node: AST node to verify
            context: Additional context (unused in CodeBERT approach)
            
        Returns:
            (is_valid, list_of_violations)
        """
        if context is None:
            context = {}
        
        violations = []
        
        # Convert AST to code string
        code_snippet = self.ast_to_string(node)
        
        # Check with CodeBERT
        is_safe, confidence, reasoning = self.check_code(code_snippet)
        
        # If unsafe and confident, flag as violation
        if not is_safe and confidence > 0.6:
            violations.append(
                f"CodeBERT decision: {type(node).__name__} flagged as potentially unsafe. "
                f"{reasoning}. "
                f"Confidence: {confidence:.2f}."
            )
        
        return len(violations) == 0, violations


# Test function
def test_codebert_firewall():
    """Test the CodeBERT firewall with sample code"""
    print("=" * 70)
    print("Testing CodeBERT Intelligent Firewall")
    print("=" * 70)
    
    firewall = IntelligentFirewall()
    
    # Test cases
    test_cases = [
        ("SELECT * FROM users WHERE id = " + "' OR 1=1 --", "SQL Injection"),
        ("SELECT * FROM users WHERE id = ?", "Safe Parameterized Query"),
        ("<script>alert('XSS')</script>", "XSS Attack"),
        ("<div>Safe content</div>", "Safe HTML"),
    ]
    
    for code, description in test_cases:
        is_safe, confidence, reasoning = firewall.check_code(code)
        status = "✅ SAFE" if is_safe else "❌ UNSAFE"
        print(f"\n{description}:")
        print(f"  Code: {code[:50]}...")
        print(f"  Status: {status}")
        print(f"  Confidence: {confidence:.2f}")
        print(f"  Reasoning: {reasoning}")
    
    print("\n" + "=" * 70)
    print("Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    test_codebert_firewall()
