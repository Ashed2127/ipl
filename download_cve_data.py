"""
Download CVE data from NVD API and convert to IPL training format
"""
import requests
import json
import time
from typing import List, Dict


def download_cves(keyword: str, limit: int = 20) -> List[Dict]:
    """Download CVEs from NVD API matching a keyword"""
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    
    params = {
        'resultsPerPage': limit,
        'startIndex': 0
    }
    
    if keyword:
        params['keywordSearch'] = keyword
    
    print(f"Downloading CVEs for keyword: {keyword}")
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        cves = data.get('vulnerabilities', [])
        print(f"  ✓ Downloaded {len(cves)} CVEs")
        return cves
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return []


def extract_code_from_description(description: str) -> List[str]:
    """Extract potential code patterns from CVE description"""
    code_samples = []
    
    # Look for common injection patterns
    injection_keywords = [
        "' OR '1'='1",
        "SELECT",
        "UNION",
        "<script>",
        "alert(",
        "eval(",
        "document.cookie",
        "../",
        "; rm",
        "&&",
        "||",
        "$(",
        "`",
    ]
    
    desc_lower = description.lower()
    for keyword in injection_keywords:
        if keyword.lower() in desc_lower:
            code_samples.append(keyword)
    
    return code_samples


def cve_to_training_sample(cve: Dict, attack_type: str) -> Dict:
    """Convert CVE record to IPL training sample"""
    cve_data = cve.get('cve', {})
    descriptions = cve_data.get('descriptions', [])
    
    # Get English description
    description = ""
    for desc in descriptions:
        if desc.get('lang') == 'en':
            description = desc.get('value', '')
            break
    
    # Extract potential code patterns
    code_samples = extract_code_from_description(description)
    
    # Determine if dangerous (all CVEs are by definition vulnerabilities)
    is_dangerous = True
    
    # Generate features based on attack type
    if attack_type == 'sql_injection':
        features = {
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': 3,
            'num_nodes': 15,
            'num_edges': 25,
            'avg_degree': 3.3,
            'execution_count': 50,
            'avg_execution_time_ms': 10.0,
            'sql_sink_count': 1,
            'html_sink_count': 0,
            'shell_sink_count': 0,
            'file_sink_count': 0,
            'sql_injection_score': 0.8,
            'xss_score': 0.0,
            'command_injection_score': 0.0,
            'path_traversal_score': 0.0,
        }
    elif attack_type == 'xss':
        features = {
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': 2,
            'num_nodes': 12,
            'num_edges': 18,
            'avg_degree': 3.0,
            'execution_count': 40,
            'avg_execution_time_ms': 8.0,
            'sql_sink_count': 0,
            'html_sink_count': 1,
            'shell_sink_count': 0,
            'file_sink_count': 0,
            'sql_injection_score': 0.0,
            'xss_score': 0.8,
            'command_injection_score': 0.0,
            'path_traversal_score': 0.0,
        }
    elif attack_type == 'command_injection':
        features = {
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': 2,
            'num_nodes': 10,
            'num_edges': 15,
            'avg_degree': 3.0,
            'execution_count': 30,
            'avg_execution_time_ms': 6.0,
            'sql_sink_count': 0,
            'html_sink_count': 0,
            'shell_sink_count': 1,
            'file_sink_count': 0,
            'sql_injection_score': 0.0,
            'xss_score': 0.0,
            'command_injection_score': 0.8,
            'path_traversal_score': 0.0,
        }
    else:  # general vulnerability
        features = {
            'has_untrusted_data': True,
            'has_sanitization': False,
            'taint_propagation_steps': 2,
            'num_nodes': 12,
            'num_edges': 18,
            'avg_degree': 3.0,
            'execution_count': 35,
            'avg_execution_time_ms': 7.0,
            'sql_sink_count': 0,
            'html_sink_count': 0,
            'shell_sink_count': 0,
            'file_sink_count': 0,
            'sql_injection_score': 0.0,
            'xss_score': 0.0,
            'command_injection_score': 0.0,
            'path_traversal_score': 0.0,
        }
    
    return {
        'id': cve_data.get('id', 'unknown'),
        'attack_type': attack_type,
        'description': description[:200],  # Truncate description
        'features': features,
        'label': 1 if is_dangerous else 0,
        'expected_safe': not is_dangerous,
        'source': 'CVE'
    }


def main():
    """Download CVE data and convert to training format"""
    print("=" * 70)
    print("DOWNLOADING CVE DATA FROM NVD")
    print("=" * 70)
    
    start_time = time.time()
    
    # Download CVEs for different attack types
    all_samples = []
    
    # SQL Injection
    sql_cves = download_cves('sql injection', limit=15)
    for cve in sql_cves:
        sample = cve_to_training_sample(cve, 'sql_injection')
        all_samples.append(sample)
    
    # XSS
    xss_cves = download_cves('cross-site scripting', limit=15)
    for cve in xss_cves:
        sample = cve_to_training_sample(cve, 'xss')
        all_samples.append(sample)
    
    # Command Injection
    cmd_cves = download_cves('command injection', limit=10)
    for cve in cmd_cves:
        sample = cve_to_training_sample(cve, 'command_injection')
        all_samples.append(sample)
    
    # Path Traversal
    path_cves = download_cves('path traversal', limit=10)
    for cve in path_cves:
        sample = cve_to_training_sample(cve, 'path_traversal')
        all_samples.append(sample)
    
    # General vulnerabilities
    general_cves = download_cves('injection', limit=20)
    for cve in general_cves:
        sample = cve_to_training_sample(cve, 'injection')
        all_samples.append(sample)
    
    print(f"\nTotal CVE samples collected: {len(all_samples)}")
    
    # Save to JSON
    output_file = '.ipl_data/cve_training_data.json'
    with open(output_file, 'w') as f:
        json.dump(all_samples, f, indent=2)
    
    print(f"✓ Saved to {output_file}")
    print(f"Time: {time.time() - start_time:.2f}s")
    
    # Print summary
    attack_types = {}
    for sample in all_samples:
        atype = sample['attack_type']
        attack_types[atype] = attack_types.get(atype, 0) + 1
    
    print("\nAttack type distribution:")
    for atype, count in attack_types.items():
        print(f"  {atype}: {count}")
    
    return all_samples


if __name__ == "__main__":
    main()
