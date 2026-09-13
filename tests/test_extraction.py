from ipl_lang.semantic_engine import SemanticEngine

test_cases = [
    "the service costs ninety-nine bucks and 50 cents",
    "approx 8 dollars and 45 cents",
    "costs about $99.99",
    "twenty-five dollars",
    "around 450 euros",
    "£25.50",
    "about a dozen",
    "three hundred and forty"
]

for tc in test_cases:
    print(f"INPUT: '{tc}'")
    print("  Currency:", SemanticEngine.extract_currency(tc))
    print("  Number  :", SemanticEngine.extract_number(tc, as_float=True))
    print()
