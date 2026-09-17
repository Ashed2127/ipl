#!/usr/bin/env python3
"""
Demonstration of IPL's embedded intelligence without Ollama
This shows what IPL can do purely with its built-in semantic engine
"""

from semantic_engine import SemanticEngine

print("=" * 60)
print("IPL EMBEDDED INTELLIGENCE DEMONSTRATION (No Ollama)")
print("=" * 60)

# Test 1: Currency Extraction
print("\n1. CURRENCY EXTRACTION")
print("-" * 40)
test_currency = "the service costs ninety-nine bucks and 50 cents"
result = SemanticEngine.extract_currency(test_currency)
print(f"Input:  '{test_currency}'")
print(f"Output: {result['formatted']} (confidence: {result['confidence']:.0%})")

# Test 2: Sentiment Analysis
print("\n2. SENTIMENT ANALYSIS")
print("-" * 40)
test_sentiment = "absolutely fantastic build quality"
result = SemanticEngine.extract_sentiment(test_sentiment)
print(f"Input:  '{test_sentiment}'")
print(f"Output: {result['label']} (score: {result['score']:+.2f}, confidence: {result['confidence']:.0%})")

# Test 3: Number Words to Numbers
print("\n3. NUMBER WORDS TO NUMBERS")
print("-" * 40)
test_numbers = "twenty-five"
result = SemanticEngine.parse_words_to_number(test_numbers)
print(f"Input:  '{test_numbers}'")
print(f"Output: {result}")

# Test 4: Date Parsing
print("\n4. DATE PARSING")
print("-" * 40)
test_date = "tomorrow at 3pm"
result = SemanticEngine.extract_date(test_date)
print(f"Input:  '{test_date}'")
print(f"Output: {result}")

# Test 5: Intent Classification
print("\n5. INTENT CLASSIFICATION")
print("-" * 40)
test_intent = "someone used my stolen credit card for unauthorized transactions"
result = SemanticEngine.extract_intent(test_intent)
print(f"Input:  '{test_intent}'")
print(f"Output: Intent: {result['intent']} (confidence: {result['confidence']:.0%})")

print("\n" + "=" * 60)
print("All of this works WITHOUT Ollama or any external AI!")
print("It's pure Python with regex and pattern matching.")
print("=" * 60)