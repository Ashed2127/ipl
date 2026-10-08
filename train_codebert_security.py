#!/usr/bin/env python3
"""
Fine-tune CodeBERT on vulnerability data for security classification
"""
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModel, AutoTokenizer, get_linear_schedule_with_warmup
from torch.optim import AdamW
from codebert_firewall import CodeBERTSecurityModel
import json
import os
from typing import List, Tuple

class SecurityDataset(Dataset):
    """Dataset for security classification (safe vs unsafe code)"""
    
    def __init__(self, data: List[Tuple[str, int]], tokenizer, max_length=512):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        code, label = self.data[idx]
        
        encoding = self.tokenizer(
            code,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

def prepare_training_data():
    """Prepare training data from various sources"""
    training_data = []
    
    # Unsafe code examples (vulnerabilities)
    unsafe_examples = [
        # SQL Injection
        ("SELECT * FROM users WHERE id = '" + "' OR '1'='1", 0),
        ("SELECT * FROM users WHERE id = admin'--", 0),
        ("SELECT * FROM users WHERE id = ' OR 1=1#", 0),
        ("' OR '1'='1' --", 0),
        ("admin' OR '1'='1", 0),
        
        # Command Injection
        ("rm -rf /", 0),
        ("; cat /etc/passwd", 0),
        ("| ls -la", 0),
        ("&& whoami", 0),
        ("execute command: rm -rf /", 0),
        
        # Path Traversal
        ("../../../etc/passwd", 0),
        ("..\\..\\..\\windows\\system32", 0),
        ("/etc/passwd", 0),
        ("read file: ../../../etc/passwd", 0),
        
        # XSS
        ("<script>alert('XSS')</script>", 0),
        ("<img src=x onerror=alert('XSS')>", 0),
        ("<svg onload=alert('XSS')>", 0),
        ("javascript:alert('XSS')", 0),
        
        # Other dangerous patterns
        ("eval(malicious_code)", 0),
        ("exec(user_input)", 0),
        ("system(user_command)", 0),
    ]
    
    # Safe code examples
    safe_examples = [
        # Safe SQL
        ("SELECT * FROM users WHERE id = ?", 1),
        ("SELECT * FROM users WHERE id = :id", 1),
        ("SELECT * FROM users WHERE id = $1", 1),
        
        # Safe file operations
        ("read_file(user_data.txt)", 1),
        ("open('./data.json', 'r')", 1),
        
        # Safe strings
        ("Hello World", 1),
        ("user age is 25", 1),
        ("twenty-five", 1),
        
        # Safe HTML
        ("<div>Safe content</div>", 1),
        ("<p>Paragraph</p>", 1),
        
        # Safe code
        ("def calculate(x, y): return x + y", 1),
        ("print('Hello')", 1),
        ("x = 5", 1),
    ]
    
    training_data = unsafe_examples + safe_examples
    
    # Balance the dataset
    print(f"Training data: {len(unsafe_examples)} unsafe, {len(safe_examples)} safe")
    
    return training_data

def train_codebert(
    model_path: str = ".ipl_data/codebert_security_model.pt",
    epochs: int = 1,  # Reduced from 3 to 1 for faster training
    batch_size: int = 4,
    learning_rate: float = 2e-5
):
    """Fine-tune CodeBERT on security data"""
    
    print("="*70)
    print("TRAINING CODEBERT FOR SECURITY CLASSIFICATION")
    print("="*70)
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    
    # Prepare data
    training_data = prepare_training_data()
    dataset = SecurityDataset(training_data, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # Initialize model
    model = CodeBERTSecurityModel()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    # Optimizer
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    
    # Scheduler
    total_steps = len(dataloader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=total_steps
    )
    
    # Training loop
    print(f"\nTraining for {epochs} epochs...")
    print(f"Device: {device}")
    print(f"Batch size: {batch_size}")
    print(f"Total steps: {total_steps}")
    
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for batch_idx, batch in enumerate(dataloader):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)
            
            # Forward pass
            outputs = model(input_ids, attention_mask)
            loss = nn.CrossEntropyLoss()(outputs, labels)
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            scheduler.step()
            
            total_loss += loss.item()
            
            if batch_idx % 5 == 0:
                print(f"Epoch {epoch+1}/{epochs}, Batch {batch_idx}/{len(dataloader)}, Loss: {loss.item():.4f}")
        
        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch+1} completed. Average loss: {avg_loss:.4f}")
    
    # Save model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    torch.save(model.state_dict(), model_path)
    print(f"\n✅ Model saved to: {model_path}")
    
    return model_path

if __name__ == "__main__":
    model_path = train_codebert()
    print(f"\n✅ Training complete!")
    print(f"Model saved: {model_path}")
    print(f"\nTo use the trained model:")
    print(f"  firewall = IntelligentFirewall(model_path='{model_path}')")
