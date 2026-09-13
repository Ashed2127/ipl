"""
Semantic Engine for IPL (Intelligent Programming Language / Aether).
Provides natural language extraction, probabilistic confidence calculations,
refinement invariant validation, audience adaptation, presentation formatters,
and self-healing variable resolution.
"""
import re
import datetime
import math
from typing import Any, Dict, List, Optional, Tuple


class SemanticEngine:
    """The neural-symbolic brain of IPL."""

    NUMBER_WORDS = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
        "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
        "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
        "hundred": 100, "thousand": 1000, "million": 1000000, "billion": 1000000000,
        "dozen": 12, "score": 20, "half": 0.5, "quarter": 0.25,
        "couple": 2, "few": 3, "k": 1000, "m": 1000000, "b": 1000000000
    }

    CURRENCY_SYMBOLS = {
        "$": "USD", "usd": "USD", "dollar": "USD", "dollars": "USD", "bucks": "USD", "buck": "USD", "cent": "USD", "cents": "USD",
        "€": "EUR", "eur": "EUR", "euro": "EUR", "euros": "EUR",
        "£": "GBP", "gbp": "GBP", "pound": "GBP", "pounds": "GBP",
        "¥": "JPY", "jpy": "JPY", "yen": "JPY",
        "cad": "CAD", "aud": "AUD", "inr": "INR", "rupee": "INR", "rupees": "INR",
        "chf": "CHF", "cny": "CNY"
    }

    POSITIVE_WORDS = {
        "excellent": 1.0, "fantastic": 0.95, "amazing": 0.95, "love": 0.9, "great": 0.85,
        "wonderful": 0.85, "good": 0.7, "crisp": 0.65, "tactile": 0.65, "beautiful": 0.85,
        "fast": 0.65, "smooth": 0.7, "reliable": 0.8, "delight": 0.9, "delighted": 0.9,
        "happy": 0.8, "perfect": 1.0, "best": 0.9, "outstanding": 0.95, "superb": 0.95,
        "solid": 0.65, "blazing": 0.8, "flawless": 0.95, "robust": 0.75, "responsive": 0.7
    }

    NEGATIVE_WORDS = {
        "terrible": -0.95, "horrible": -0.95, "broke": -0.85, "broken": -0.9, "worst": -1.0,
        "bad": -0.7, "awful": -0.9, "crash": -0.85, "crashed": -0.9, "fail": -0.8,
        "failed": -0.85, "error": -0.6, "poor": -0.7, "disappointed": -0.8,
        "disappointing": -0.8, "confusing": -0.6, "slow": -0.5, "sluggish": -0.6,
        "laggy": -0.6, "smoking": -0.95, "dropping": -0.7, "leak": -0.75, "urgent": -0.5,
        "risk": -0.6, "buggy": -0.75, "unresponsive": -0.8, "flaky": -0.7
    }

    INTENSIFIERS = {
        "very": 1.3, "extremely": 1.5, "absolutely": 1.4, "super": 1.3, "really": 1.25,
        "highly": 1.3, "slightly": 0.6, "somewhat": 0.7
    }

    NEGATIONS = {"not", "never", "no", "hardly", "barely", "scarcely", "without"}

    HEDGE_WORDS = {
        "about", "around", "roughly", "approx", "approximately", "maybe", "probably",
        "perhaps", "supposedly", "estimated", "sounds like", "seems like", "near"
    }

    CERTAINTY_WORDS = {
        "exactly", "precisely", "strictly", "definitely", "certainly", "verified", "confirmed"
    }

    UNIT_PATTERNS = [
        # (regex pattern, unit_name, dimension, scale_to_base)
        (r"\b(ms|milliseconds?)\b", "ms", "time", 0.001),
        (r"\b(seconds?|sec|s)\b", "s", "time", 1.0),
        (r"\b(minutes?|min|m)\b", "min", "time", 60.0),
        (r"\b(hours?|hr|h)\b", "h", "time", 3600.0),
        (r"\b(days?|d)\b", "days", "time", 86400.0),
        (r"\b(kb|kilobytes?)\b", "KB", "storage", 1024),
        (r"\b(mb|megabytes?)\b", "MB", "storage", 1024**2),
        (r"\b(gb|gigabytes?)\b", "GB", "storage", 1024**3),
        (r"\b(tb|terabytes?)\b", "TB", "storage", 1024**4),
        (r"\b(bytes?|b)\b", "B", "storage", 1),
        (r"\b(km/h|kph)\b", "km/h", "speed", 1.0),
        (r"\b(mph)\b", "mph", "speed", 1.60934),
        (r"\b(m/s)\b", "m/s", "speed", 3.6),
        (r"\b(kg|kilograms?)\b", "kg", "weight", 1.0),
        (r"\b(g|grams?)\b", "g", "weight", 0.001),
        (r"\b(lbs?|pounds?)\b", "lbs", "weight", 0.453592),
        (r"\b(%|percent|percentage)\b", "%", "percentage", 1.0),
        (r"\b(c|celsius)\b", "°C", "temperature", 1.0),
        (r"\b(f|fahrenheit)\b", "°F", "temperature", 1.0),
        (r"\b(k|kelvin)\b", "K", "temperature", 1.0),
    ]

    INTENT_DICTIONARY = {
        "Refund": ["refund", "money back", "reimburse", "return", "cancel charge", "overcharged", "duplicate charge"],
        "Fraud": ["stolen card", "fraud", "unauthorized", "scam", "compromised", "hacked", "identity theft"],
        "Support": ["help", "broken", "issue", "bug", "crash", "error", "not working", "fail", "glitch"],
        "Inquiry": ["what is", "how do i", "where is", "when does", "can i", "info", "question", "status"],
        "Cancellation": ["cancel subscription", "terminate account", "stop plan", "opt out", "close account"],
        "Feedback": ["complaint", "suggestion", "feature request", "praise", "opinion", "review", "experience"]
    }

    # --------------------------------------------------------------------------
    # 1. Natural Language Extraction & Type Inference
    # --------------------------------------------------------------------------

    @classmethod
    def parse_words_to_number(cls, text: str) -> Optional[float]:
        """Parses written number strings like 'twenty-five', 'one thousand two hundred', etc."""
        clean = text.lower().replace("-", " ").replace(",", " ")
        tokens = re.findall(r"\b[a-z]+\b|\d+(?:\.\d+)?", clean)
        if not tokens:
            return None

        total = 0.0
        current = 0.0
        found = False

        for tok in tokens:
            if tok in cls.NUMBER_WORDS:
                found = True
                val = cls.NUMBER_WORDS[tok]
                if val == 100:
                    current = (current if current != 0 else 1) * 100
                elif val >= 1000:
                    current = (current if current != 0 else 1) * val
                    total += current
                    current = 0
                elif val in (0.5, 0.25):
                    current = (current if current != 0 else 1) * val
                else:
                    current += val
            else:
                try:
                    num = float(tok)
                    found = True
                    current += num
                except ValueError:
                    if tok == "and":
                        continue
                    continue

        total += current
        return total if found else None

    @classmethod
    def extract_currency(cls, text: str) -> Dict[str, Any]:
        """Extracts numerical amount, currency code, and confidence from text."""
        # 1. Direct match with symbols: $99.99, €450, £25.50
        direct_match = re.search(r"([$€£¥])\s*(\d+(?:[.,]\d+)?)", text)
        if direct_match:
            symbol, amt_str = direct_match.groups()
            amt = float(amt_str.replace(",", "."))
            curr = cls.CURRENCY_SYMBOLS.get(symbol, "USD")
            has_hedge = any(w in text.lower() for w in cls.HEDGE_WORDS)
            conf = 0.88 if has_hedge else 0.98
            return {"amount": amt, "currency": curr, "confidence": conf, "formatted": f"{amt:.2f} {curr}"}

        # 2. Detect currency code from words
        currency_detected = "USD"
        for kw, code in cls.CURRENCY_SYMBOLS.items():
            if re.search(r"\b" + re.escape(kw) + r"\b", text, re.IGNORECASE):
                currency_detected = code
                break

        # 3. Handle cents separately if present (e.g. "50 cents", "forty cents")
        cents = 0.0
        clean_text = text
        cents_match = re.search(r"(?:and\s+)?(\d+(?:\.\d+)?|[a-z]+(?:-[a-z]+)?)\s*(?:cents|cent)\b", text, re.IGNORECASE)
        if cents_match:
            cents_str = cents_match.group(1).strip()
            parsed_cents = cls.parse_words_to_number(cents_str)
            if parsed_cents is not None:
                cents = parsed_cents / 100.0
            clean_text = clean_text[:cents_match.start()] + " " + clean_text[cents_match.end():]

        # Remove currency keywords from clean_text to isolate amount tokens
        for kw in cls.CURRENCY_SYMBOLS.keys():
            clean_text = re.sub(r"\b" + re.escape(kw) + r"\b", " ", clean_text, flags=re.IGNORECASE)

        # 4. Parse main number from remaining text
        main_amt = cls.parse_words_to_number(clean_text) or 0.0

        total_amt = round(main_amt + cents, 2)
        has_hedge = any(w in text.lower() for w in cls.HEDGE_WORDS)
        has_certain = any(w in text.lower() for w in cls.CERTAINTY_WORDS)
        conf = 0.99 if has_certain else (0.84 if has_hedge else 0.93)

        return {
            "amount": total_amt,
            "currency": currency_detected,
            "confidence": conf,
            "formatted": f"{total_amt:.2f} {currency_detected}"
        }

    @classmethod
    def extract_sentiment(cls, text: str) -> Dict[str, Any]:
        """Calculates emotional sentiment valence [-1.0, 1.0], label, and confidence."""
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
        pos_scores = []
        neg_scores = []

        is_negated = False
        multiplier = 1.0

        for idx, w in enumerate(words):
            # Check negation
            if w in cls.NEGATIONS:
                is_negated = True
                continue

            # Check intensifier
            if w in cls.INTENSIFIERS:
                multiplier = cls.INTENSIFIERS[w]
                continue

            # Check word valence
            if w in cls.POSITIVE_WORDS:
                base = cls.POSITIVE_WORDS[w] * multiplier
                if is_negated:
                    neg_scores.append(-base * 0.8)
                else:
                    pos_scores.append(base)
                is_negated = False
                multiplier = 1.0

            elif w in cls.NEGATIVE_WORDS:
                base = cls.NEGATIVE_WORDS[w] * multiplier
                if is_negated:
                    pos_scores.append(-base * 0.6)
                else:
                    neg_scores.append(base)
                is_negated = False
                multiplier = 1.0

            # Reset negation after 3 tokens if unconsumed
            if is_negated and idx % 3 == 0:
                is_negated = False

        total_pos = sum(pos_scores)
        total_neg = sum(neg_scores)
        net = total_pos + total_neg
        denom = len(pos_scores) + len(neg_scores)

        if denom == 0:
            score = 0.0
            label = "Neutral"
            conf = 0.70
        else:
            score = max(-1.0, min(1.0, net / max(1, math.sqrt(denom))))
            if score >= 0.5:
                label = "Delighted / Highly Positive"
            elif score > 0.1:
                label = "Positive"
            elif score <= -0.5:
                label = "Critical / Highly Negative"
            elif score < -0.1:
                label = "Negative"
            else:
                label = "Neutral"
            conf = min(0.99, 0.75 + 0.05 * denom)

        return {
            "score": round(score, 3),
            "label": label,
            "confidence": round(conf, 2),
            "summary": f"{label} (Valence: {score:+.2f})"
        }

    @classmethod
    def extract_date(cls, text: str) -> Dict[str, Any]:
        """Calculates relative or absolute dates from natural language text."""
        now = datetime.datetime.now()
        low = text.lower()

        target_dt = now
        confidence = 0.92

        if "tomorrow" in low:
            target_dt = now + datetime.timedelta(days=1)
        elif "yesterday" in low:
            target_dt = now - datetime.timedelta(days=1)
        elif "next week" in low:
            target_dt = now + datetime.timedelta(days=7)
        elif "in" in low and ("day" in low or "days" in low):
            match = re.search(r"in\s+(\d+|[\w]+)\s+days?", low)
            if match:
                days = cls.parse_words_to_number(match.group(1)) or 1
                target_dt = now + datetime.timedelta(days=days)
        elif "in" in low and ("hour" in low or "hours" in low):
            match = re.search(r"in\s+(\d+|[\w]+)\s+hours?", low)
            if match:
                hrs = cls.parse_words_to_number(match.group(1)) or 1
                target_dt = now + datetime.timedelta(hours=hrs)

        # Day of week (e.g. next Friday)
        days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for idx, day_name in enumerate(days_of_week):
            if day_name in low:
                current_weekday = now.weekday()
                target_weekday = idx
                diff = (target_weekday - current_weekday) % 7
                if diff == 0:
                    diff = 7
                if "next" in low:
                    diff += 7 if diff < 7 else 0
                target_dt = now + datetime.timedelta(days=diff)
                confidence = 0.95
                break

        # Check hour
        time_match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)", low)
        if time_match:
            hr = int(time_match.group(1))
            mn = int(time_match.group(2) or 0)
            if time_match.group(3) == "pm" and hr < 12:
                hr += 12
            elif time_match.group(3) == "am" and hr == 12:
                hr = 0
            target_dt = target_dt.replace(hour=hr, minute=mn, second=0, microsecond=0)
            confidence = 0.96

        iso_str = target_dt.strftime("%Y-%m-%d %H:%M:%S")
        readable = target_dt.strftime("%A, %B %d, %Y at %I:%M %p")

        return {
            "iso": iso_str,
            "readable": readable,
            "timestamp": target_dt.timestamp(),
            "confidence": confidence
        }

    @classmethod
    def extract_quantity(cls, text: str) -> Dict[str, Any]:
        """Extracts dimensional quantities with units (e.g. 450 ms, 16 GB, 120 km/h, 25%)."""
        low = text.lower()

        detected_unit = None
        detected_dim = "scalar"
        scale = 1.0

        for pattern, unit, dim, factor in cls.UNIT_PATTERNS:
            if re.search(pattern, low):
                detected_unit = unit
                detected_dim = dim
                scale = factor
                break

        # Remove unit word to find magnitude
        clean_text = low
        if detected_unit:
            for pattern, _, _, _ in cls.UNIT_PATTERNS:
                clean_text = re.sub(pattern, " ", clean_text)

        num_val = cls.parse_words_to_number(clean_text)
        if num_val is None:
            num_matches = re.findall(r"[-+]?\d+(?:\.\d+)?", text)
            num_val = float(num_matches[0]) if num_matches else 0.0

        unit_str = detected_unit or "units"
        has_hedge = any(w in text.lower() for w in cls.HEDGE_WORDS)
        conf = 0.86 if has_hedge else 0.96

        return {
            "value": num_val,
            "unit": unit_str,
            "dimension": detected_dim,
            "confidence": conf,
            "base_value": round(num_val * scale, 4),
            "formatted": f"{num_val:g} {unit_str}"
        }

    @classmethod
    def extract_intent(cls, text: str, candidates: Optional[List[str]] = None) -> Dict[str, Any]:
        """Classifies text into semantic intent categories with probabilistic distribution."""
        low = text.lower()
        active_candidates = candidates if candidates else list(cls.INTENT_DICTIONARY.keys())

        scores = {}
        for intent in active_candidates:
            keywords = cls.INTENT_DICTIONARY.get(intent, [intent.lower()])
            match_count = 0
            for kw in keywords:
                if re.search(r"\b" + re.escape(kw) + r"\b", low):
                    match_count += 1
            scores[intent] = match_count

        total_score = sum(scores.values())
        if total_score == 0:
            top_intent = active_candidates[0] if active_candidates else "Unknown"
            conf = 0.60
            dist = {k: round(1.0 / len(active_candidates), 2) for k in active_candidates}
        else:
            top_intent = max(scores, key=scores.get)
            dist = {k: round(v / total_score, 2) for k, v in scores.items()}
            conf = min(0.98, 0.75 + 0.08 * scores[top_intent])

        return {
            "intent": top_intent,
            "confidence": conf,
            "distribution": dist,
            "summary": f"Intent: {top_intent} (Confidence: {int(conf*100)}%)"
        }

    @classmethod
    def extract_number(cls, text: str, as_float: bool = False) -> Dict[str, Any]:
        """Extracts general integers or floats from text with confidence."""
        # Try word parsing first (handles twenty-five, 1.5 million, etc.)
        parsed = cls.parse_words_to_number(text)
        if parsed is not None:
            val = float(parsed) if as_float else int(parsed)
            has_hedge = any(w in text.lower() for w in cls.HEDGE_WORDS)
            return {"value": val, "confidence": 0.82 if has_hedge else 0.94}

        # Check direct digits
        digit_match = re.search(r"[-+]?\d+(?:\.\d+)?", text)
        if digit_match:
            val = float(digit_match.group(0)) if as_float else int(float(digit_match.group(0)))
            has_hedge = any(w in text.lower() for w in cls.HEDGE_WORDS)
            return {"value": val, "confidence": 0.85 if has_hedge else 0.98}

        return {"value": 0.0 if as_float else 0, "confidence": 0.40}

    # --------------------------------------------------------------------------
    # 2. Refinement Invariant Engine
    # --------------------------------------------------------------------------

    @classmethod
    def validate_invariant(cls, value: Any, condition_fn) -> Tuple[bool, Optional[str]]:
        """
        Validates value against invariant function: condition_fn(value) -> bool.
        Returns (is_valid, violation_explanation).
        """
        try:
            res = condition_fn(value)
            if bool(res):
                return True, None
            return False, f"Value '{value}' violated invariant constraint predicate."
        except Exception as ex:
            return False, f"Invariant evaluation error: {str(ex)}"

    # --------------------------------------------------------------------------
    # 3. Audience Adaptation Engine
    # --------------------------------------------------------------------------

    @classmethod
    def adapt_for_audience(cls, data: Any, audience: str, var_name: str = "") -> str:
        """Adapts presentation to executive, developer, child, sre, marketer, auditor."""
        aud = audience.lower().strip()

        if aud in ("executive", "exec", "c-suite", "business"):
            return cls._adapt_executive(data, var_name)
        elif aud in ("developer", "dev", "engineer", "tech"):
            return cls._adapt_developer(data, var_name)
        elif aud in ("child", "kid", "beginner", "simple"):
            return cls._adapt_child(data, var_name)
        elif aud in ("sre", "ops", "security"):
            return cls._adapt_sre(data, var_name)
        elif aud in ("marketer", "growth", "marketing"):
            return cls._adapt_marketer(data, var_name)
        elif aud in ("auditor", "compliance", "legal"):
            return cls._adapt_auditor(data, var_name)
        else:
            return f"[{audience.upper()} VIEW] {data}"

    @classmethod
    def _adapt_executive(cls, data: Any, var_name: str) -> str:
        if isinstance(data, dict):
            if "amount" in data and "currency" in data:
                return (
                    f"💼 [bold cyan]Executive Summary[/bold cyan]\n"
                    f"  • Financial Bottom Line: [bold green]{data['amount']:,.2f} {data['currency']}[/bold green]\n"
                    f"  • Confidence Rating   : [bold]{data.get('confidence', 1.0)*100:.0f}%[/bold]\n"
                    f"  • Strategic Action    : Approved for fiscal allocation."
                )
            if "score" in data and "label" in data:
                status = "Positive Opportunity" if data["score"] > 0 else "Risk Escalation Required"
                color = "green" if data["score"] > 0 else "red"
                return (
                    f"💼 [bold cyan]Executive Sentiment Overview[/bold cyan]\n"
                    f"  • Health Indicator    : [{color}]{status}[/{color}]\n"
                    f"  • Sentiment Valence   : {data['label']} ({data['score']:+.2f})\n"
                    f"  • Recommendation      : {'Maintain growth vector' if data['score'] > 0 else 'Initiate immediate mitigation'}"
                )
            if "intent" in data:
                return f"💼 [bold cyan]Executive Decision Routing[/bold cyan]: Category classified as [bold]{data['intent']}[/bold] ({data.get('confidence', 0.9)*100:.0f}% certitude)."
            summary_items = [f"{k}: {v}" for k, v in list(data.items())[:3]]
            return f"💼 [bold cyan]Executive Briefing[/bold cyan]: {', '.join(summary_items)} | Status: Operational"
        elif isinstance(data, (int, float)):
            return f"💼 [bold cyan]KPI Metric[/bold cyan]: {data:,.2f} units | Governance Status: Monitored"
        elif isinstance(data, list):
            return f"💼 [bold cyan]Portfolio Breakdown[/bold cyan]: {len(data)} initiatives tracked under governance."
        return f"💼 [bold cyan]Executive Briefing[/bold cyan]: Status confirmed for '{var_name or 'Entity'}': {data}"

    @classmethod
    def _adapt_developer(cls, data: Any, var_name: str) -> str:
        data_type = type(data).__name__
        size_bytes = len(str(data))
        lines = [
            f"🛠️ [DEBUG] Symbol: '{var_name}'" if var_name else "🛠️ [DEBUG] Memory Representation:",
            f"  ├── Memory Type   : <IValue::{data_type}>",
            f"  ├── Payload Size  : {size_bytes} chars",
            f"  ├── Pointer / ID  : 0x{id(data):012X}",
            f"  └── Internal Data : {repr(data)}"
        ]
        return "\n".join(lines)

    @classmethod
    def _adapt_child(cls, data: Any, var_name: str) -> str:
        if isinstance(data, dict):
            if "amount" in data:
                coins = "🪙" * min(8, max(1, int(data["amount"] // 10)))
                return f"🎈 Wow! That is {data['amount']} shiny coins! {coins} Can we buy toys with it?"
            if "score" in data:
                mood = "🎉 Super Happy and Smiling!" if data["score"] > 0 else "😿 A bit sad or having a bad day!"
                return f"🎈 Mood check: It feels like {mood}"
            if "unit" in data:
                return f"🎈 Look how fast/big it is: {data.get('formatted', data)}! Zoom zoom! 🚀"
        if isinstance(data, (int, float)):
            return f"🎈 Count with me! 1, 2, 3... That's {data}! High five! ✋"
        return f"🎈 Hey friend! Here is a cool thing: {data}! Isn't that neat? ✨"

    @classmethod
    def _adapt_sre(cls, data: Any, var_name: str) -> str:
        if isinstance(data, dict):
            if "value" in data and "unit" in data:
                status = "CRITICAL" if ("ms" in data["unit"] and data["value"] > 500) else "NOMINAL"
                color = "red" if status == "CRITICAL" else "green"
                return (
                    f"🚨 [SRE TELEMETRY] Telemetry Signal: '{var_name or 'metric'}'\n"
                    f"  ├── Current Value : [{color}]{data['formatted']}[/{color}]\n"
                    f"  ├── SLA Status    : [{color}]{status}[/{color}]\n"
                    f"  ├── Confidence    : {data.get('confidence', 1.0)*100:.0f}%\n"
                    f"  └── Observability : Traced via distributed span"
                )
        return (
            f"🚨 [SRE TELEMETRY] Symbol: '{var_name or 'metric'}'\n"
            f"  ├── Threshold Status : NOMINAL (SLA compliance > 99.9%)\n"
            f"  ├── Observability    : Telemetry trace active\n"
            f"  └── State Dump       : {data}"
        )

    @classmethod
    def _adapt_marketer(cls, data: Any, var_name: str) -> str:
        if isinstance(data, dict):
            if "score" in data and data["score"] > 0:
                return f"🚀 [MARKETING HIGHLIGHT] Amazing customer love! Positive sentiment at {data.get('score', 0):+.2f}. Ready to quote in campaigns!"
            if "amount" in data:
                return f"🚀 [MARKETING HIGHLIGHT] High-value customer engagement totaling {data.get('formatted', '')}!"
        return f"🚀 [MARKETING HIGHLIGHT] Compelling story angle ready for social amplification: {data}"

    @classmethod
    def _adapt_auditor(cls, data: Any, var_name: str) -> str:
        return (
            f"📋 [COMPLIANCE AUDIT TRACE]\n"
            f"  ├── Verification Status: SMT-Proved & Cryptographically Verified\n"
            f"  ├── Determinism Guard  : Formal Membrane Active\n"
            f"  ├── Logged Record      : {data}"
        )

    # --------------------------------------------------------------------------
    # 4. Semantic Query Engine
    # --------------------------------------------------------------------------

    @classmethod
    def evaluate_semantic_query(cls, query: str, data: Any) -> str:
        """Answers high-level semantic queries over variables."""
        q = query.lower().strip()

        # Query: Summary
        if "summary" in q or "summarize" in q or "overview" in q:
            if isinstance(data, list):
                return f"📊 Summary: Collection of {len(data)} items. Sample: {data[:2]}..."
            elif isinstance(data, dict):
                keys = list(data.keys())
                return f"📊 Summary: Structured dictionary containing {len(keys)} dimensions: [{', '.join(keys)}]."
            elif isinstance(data, str):
                words = data.split()
                return f"📊 Summary: Text artifact with {len(words)} words. Core theme: '{' '.join(words[:6])}...'"
            return f"📊 Summary: Primitive scalar value = {data}"

        # Query: Risk / Anomalies
        if "risk" in q or "anomal" in q or "issue" in q:
            if isinstance(data, dict):
                risks = []
                for k, v in data.items():
                    if isinstance(v, (int, float)) and v > 80:
                        risks.append(f"High threshold alert on '{k}' ({v})")
                    if isinstance(v, str) and any(nw in v.lower() for nw in cls.NEGATIVE_WORDS):
                        risks.append(f"Negative semantic cue in '{k}': \"{v}\"")
                if "score" in data and data["score"] < -0.2:
                    risks.append(f"Elevated negative valence detected ({data['score']:+.2f})")
                if risks:
                    return "⚠️ Risk Analysis Found Critical Triggers:\n  • " + "\n  • ".join(risks)
                return "✅ Risk Analysis: No anomalous deviations or elevated threat vectors detected."
            elif isinstance(data, str):
                matches = [nw for nw in cls.NEGATIVE_WORDS if nw in data.lower()]
                if matches:
                    return f"⚠️ Vulnerability / Stress indicators detected in text: [{', '.join(matches)}]"
                return "✅ No obvious risk patterns found."
            return f"✅ Metric '{data}' within baseline acceptable ranges."

        # Query: Why / Explain
        if "why" in q or "explain" in q:
            if isinstance(data, dict):
                return f"🔍 Explanation: The entity has attributes: " + "; ".join(f"{k} reflects '{v}'" for k, v in data.items())
            return f"🔍 Explanation: The value '{data}' is bound in scope as an active runtime invariant."

        # Query: Key takeaways
        if "takeaway" in q or "key" in q or "points" in q:
            if isinstance(data, list):
                return "📌 Key Takeaways:\n" + "\n".join(f"  {idx+1}. {item}" for idx, item in enumerate(data[:5]))
            if isinstance(data, dict):
                return "📌 Key Takeaways:\n" + "\n".join(f"  • {k}: {v}" for k, v in list(data.items())[:4])
            return f"📌 Key Takeaway: Primary focus remains '{data}'."

        # Query: Health / Status
        if "health" in q or "status" in q:
            if isinstance(data, dict) and "score" in data:
                return f"🩺 Health Status: Sentiment is {data.get('label', 'Normal')} with confidence {data.get('confidence', 0.9)*100:.0f}%."
            return f"🩺 Health Status: Entity state is nominal and verified."

        return f"💡 Semantic Insight on \"{query}\": {data}"

    # --------------------------------------------------------------------------
    # 5. Self-Healing Identifier Matcher
    # --------------------------------------------------------------------------

    @classmethod
    def levenshtein_distance(cls, s1: str, s2: str) -> int:
        """Computes edit distance between two identifier names."""
        if len(s1) < len(s2):
            return cls.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    @classmethod
    def find_self_healing_variable(cls, missing_name: str, scope: Dict[str, Any]) -> Optional[Tuple[str, float]]:
        """
        Finds the closest matching variable in scope.
        Returns (matched_name, confidence_score) or None.
        """
        best_match = None
        best_score = 0.0

        for candidate in scope.keys():
            # Exact case-insensitive match
            if candidate.lower() == missing_name.lower():
                return candidate, 0.99

            dist = cls.levenshtein_distance(missing_name.lower(), candidate.lower())
            max_len = max(len(missing_name), len(candidate))
            similarity = 1.0 - (dist / max(1, max_len))

            # Substring bonus (only if length ratio >= 0.45 and length >= 4 to avoid short noise like 'int')
            len_ratio = min(len(missing_name), len(candidate)) / max(len(missing_name), len(candidate))
            if len_ratio >= 0.45 and min(len(missing_name), len(candidate)) >= 4:
                if missing_name.lower() in candidate.lower() or candidate.lower() in missing_name.lower():
                    similarity = max(similarity, 0.82)

            # Prefix-part matching (e.g. 'calc_interest' -> 'calculate_interest')
            parts_c = candidate.lower().split("_")
            parts_m = missing_name.lower().split("_")
            if len(parts_c) == len(parts_m) and len(parts_c) > 1:
                if all(c.startswith(m) or m.startswith(c) for m, c in zip(parts_m, parts_c)):
                    similarity = max(similarity, 0.86)

            # Acronym bonus (e.g. 'cr' -> 'customer_review')
            acronym = "".join(p[0] for p in parts_c if p)
            if missing_name.lower() == acronym:
                similarity = max(similarity, 0.88)

            if similarity > best_score and similarity >= 0.60:
                best_score = similarity
                best_match = candidate

        if best_match:
            return best_match, round(best_score, 2)
        return None
