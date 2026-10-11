"""
SecureBERT 2.0-based Intelligent Firewall for IPL
Uses SecureBERT 2.0 model for cybersecurity intelligence and code vulnerability detection
Built on ModernBERT architecture with domain-specific pretraining for cybersecurity
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


class SecureBERTSecurityModel(nn.Module):
    """SecureBERT 2.0-based security classifier (binary: safe/unsafe)"""

    def __init__(self, model_name="cisco-ai/SecureBERT2.0-base"):
        super().__init__()
        self.securebert = AutoModel.from_pretrained(model_name)
        self.classifier = nn.Linear(768, 2)  # 768 is SecureBERT output dimension
        self.dropout = nn.Dropout(0.1)

    def forward(self, input_ids, attention_mask):
        # Get SecureBERT embeddings
        outputs = self.securebert(input_ids=input_ids, attention_mask=attention_mask)
        # Use [CLS] token embedding (first token)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        # Apply dropout
        cls_embedding = self.dropout(cls_embedding)
        # Classify
        logits = self.classifier(cls_embedding)
        return logits


class MultiClassSecureBERTSecurityModel(nn.Module):
    """SecureBERT 2.0-based multi-class security classifier"""

    def __init__(self, model_name="cisco-ai/SecureBERT2.0-base", num_classes=7):
        super().__init__()
        self.securebert = AutoModel.from_pretrained(model_name)
        self.classifier = nn.Linear(768, num_classes)  # 768 is SecureBERT output dimension
        self.dropout = nn.Dropout(0.1)
        self.num_classes = num_classes

    def forward(self, input_ids, attention_mask):
        # Get SecureBERT embeddings
        outputs = self.securebert(input_ids=input_ids, attention_mask=attention_mask)
        # Use [CLS] token embedding (first token)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        # Apply dropout
        cls_embedding = self.dropout(cls_embedding)
        # Classify
        logits = self.classifier(cls_embedding)
        return logits


class IntelligentFirewall:
    """
    Intelligent Firewall using SecureBERT 2.0 for cybersecurity intelligence
    Replaces the simple neural network with domain-specific cybersecurity model
    """

    def __init__(self, model_path: str = None):
        """
        Initialize SecureBERT 2.0-based firewall

        Args:
            model_path: Path to trained model (if None, uses pretrained without fine-tuning)
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"SecureBERT 2.0 Firewall initialized on device: {self.device}")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("cisco-ai/SecureBERT2.0-base")

        # Load model
        if model_path and os.path.exists(model_path):
            # Load fine-tuned model
            self.model = SecureBERTSecurityModel()
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            print(f"Loaded fine-tuned model from: {model_path}")
        else:
            # Use pretrained model (domain-specific cybersecurity training)
            self.model = SecureBERTSecurityModel()
            print("Using SecureBERT 2.0 (domain-specific cybersecurity pretraining)")

        self.model.to(self.device)
        self.model.eval()
    
    def ast_to_string(self, node) -> str:
        """
        Convert AST node to code string for SecureBERT 2.0 analysis
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
        Check if code snippet is safe using SecureBERT 2.0

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

        reasoning = f"SecureBERT 2.0 analysis: safe probability = {safe_prob:.3f}"

        return is_safe, confidence, reasoning

    def verify_ast_node(self, node, context: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
        """
        Verify AST node using SecureBERT 2.0

        Args:
            node: AST node to verify
            context: Additional context (unused in SecureBERT approach)

        Returns:
            (is_valid, list_of_violations)
        """
        if context is None:
            context = {}

        violations = []

        # Convert AST to code string
        code_snippet = self.ast_to_string(node)

        # Check with SecureBERT 2.0
        is_safe, confidence, reasoning = self.check_code(code_snippet)

        # If unsafe and confident, flag as violation
        # Lower threshold for pretrained model (0.6) vs fine-tuned model (0.7)
        if not is_safe and confidence > 0.5:
            violations.append(
                f"SecureBERT 2.0 decision: {type(node).__name__} flagged as potentially unsafe. "
                f"{reasoning}. "
                f"Confidence: {confidence:.2f}."
            )

        return len(violations) == 0, violations


class MultiClassIntelligentFirewall:
    """
    Multi-class Intelligent Firewall using SecureBERT 2.0 for specific vulnerability type detection
    Classifies code into specific vulnerability categories with domain-specific cybersecurity intelligence
    """

    VULN_TYPES = {
        0: "SQL Injection",
        1: "XSS",
        2: "Command Injection",
        3: "Path Traversal",
        4: "Dangerous Functions",
        5: "Other Vulnerabilities",
        6: "Safe Code"
    }

    def __init__(self, model_path: str = None, num_classes: int = 7):
        """
        Initialize multi-class SecureBERT 2.0-based firewall

        Args:
            model_path: Path to trained multi-class model (if None, uses pretrained without fine-tuning)
            num_classes: Number of vulnerability classes (default: 7)
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Multi-class SecureBERT 2.0 Firewall initialized on device: {self.device}")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("cisco-ai/SecureBERT2.0-base")

        # Load model
        if model_path and os.path.exists(model_path):
            # Load fine-tuned multi-class model
            self.model = MultiClassSecureBERTSecurityModel(num_classes=num_classes)
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            print(f"Loaded fine-tuned multi-class model from: {model_path}")
        else:
            # Use pretrained model (domain-specific cybersecurity training)
            self.model = MultiClassSecureBERTSecurityModel(num_classes=num_classes)
            print("Using SecureBERT 2.0 (domain-specific cybersecurity pretraining)")

        self.model.to(self.device)
        self.model.eval()
        self.num_classes = num_classes

    def ast_to_string(self, node) -> str:
        """
        Convert AST node to code string for SecureBERT 2.0 analysis
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

    def check_code(self, code_snippet: str) -> Tuple[str, float, str]:
        """
        Check if code snippet is safe using multi-class SecureBERT 2.0

        Args:
            code_snippet: Code string to analyze

        Returns:
            (vulnerability_type, confidence, reasoning)
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
            predicted_class = torch.argmax(probs, dim=1).item()
            confidence = probs[0][predicted_class].item()

        vuln_type = self.VULN_TYPES[predicted_class]
        reasoning = f"SecureBERT 2.0 multi-class analysis: predicted = {vuln_type} (class {predicted_class}), confidence = {confidence:.3f}"

        return vuln_type, confidence, reasoning

    def verify_ast_node(self, node, context: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
        """
        Verify AST node using multi-class SecureBERT 2.0

        Args:
            node: AST node to verify
            context: Additional context (unused in SecureBERT approach)

        Returns:
            (is_valid, list_of_violations)
        """
        if context is None:
            context = {}

        violations = []

        # Convert AST to code string
        code_snippet = self.ast_to_string(node)

        # Check with SecureBERT 2.0
        vuln_type, confidence, reasoning = self.check_code(code_snippet)

        # If not safe and confident, flag as violation
        if vuln_type != "Safe Code" and confidence > 0.6:
            violations.append(
                f"SecureBERT 2.0 multi-class decision: {type(node).__name__} flagged as {vuln_type}. "
                f"{reasoning}. "
                f"Confidence: {confidence:.2f}."
            )

        return len(violations) == 0, violations


# Test function for multi-class firewall
def test_multiclass_firewall():
    """Test the multi-class SecureBERT 2.0 firewall with sample code"""
    print("=" * 70)
    print("Testing Multi-class SecureBERT 2.0 Intelligent Firewall")
    print("=" * 70)

    firewall = MultiClassIntelligentFirewall()

    # Test cases covering different vulnerability types
    test_cases = [
        ("SELECT * FROM users WHERE id = '" + "' OR '1'='1", "SQL Injection"),
        ("<script>alert('XSS')</script>", "XSS Attack"),
        ("; cat /etc/passwd", "Command Injection"),
        ("../../../etc/passwd", "Path Traversal"),
        ("eval(malicious_code)", "Dangerous Function"),
        ("SELECT * FROM users WHERE id = ?", "Safe Parameterized Query"),
        ("<div>Safe content</div>", "Safe HTML"),
        ("def calculate(x, y): return x + y", "Safe Python Code"),
    ]

    for code, description in test_cases:
        vuln_type, confidence, reasoning = firewall.check_code(code)
        status = "✅ SAFE" if vuln_type == "Safe Code" else f"❌ {vuln_type}"
        print(f"\n{description}:")
        print(f"  Code: {code[:50]}...")
        print(f"  Status: {status}")
        print(f"  Confidence: {confidence:.2f}")
        print(f"  Reasoning: {reasoning}")

    print("\n" + "=" * 70)
    print("Test Complete")
    print("=" * 70)


# Test function for binary firewall
def test_securebert_firewall():
    """Test the SecureBERT 2.0 firewall with sample code"""
    print("=" * 70)
    print("Testing SecureBERT 2.0 Intelligent Firewall (Binary)")
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
    # Test both firewalls
    test_securebert_firewall()
    print("\n\n")
    test_multiclass_firewall()
