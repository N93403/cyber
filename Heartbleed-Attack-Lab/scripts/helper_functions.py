#!/usr/bin/env python3
"""
Helper functions for Heartbleed Attack Lab
Utility functions for analysis and reporting
"""

import re
import struct
from typing import List, Dict, Any

def analyze_memory_patterns(data: bytes) -> Dict[str, Any]:
    """
    Analyze memory dump for common patterns
    
    Args:
        data: Memory dump bytes
        
    Returns:
        Dict with analysis results
    """
    results = {
        'total_bytes': len(data),
        'patterns_found': {},
        'statistics': {},
        'potential_secrets': []
    }
    
    # Common patterns to search for
    patterns = {
        'email': rb'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'url': rb'https?://[^\s<>"]+|www\.[^\s<>"]+',
        'ip_address': rb'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        'private_key': rb'-----BEGIN (?:RSA|DSA|EC) PRIVATE KEY-----',
        'session_id': rb'session(?:_id)?=[A-Za-z0-9+/=]{16,}',
        'password_field': rb'password[=:\s][^&\s]{3,50}',
        'username_field': rb'username[=:\s][^&\s]{3,50}',
    }
    
    # Search for patterns
    for pattern_name, pattern in patterns.items():
        matches = re.findall(pattern, data, re.IGNORECASE)
        if matches:
            results['patterns_found'][pattern_name] = [
                match.decode('utf-8', errors='ignore') for match in matches[:5]  # Limit to 5 matches
            ]
    
    # Calculate statistics
    results['statistics'] = {
        'printable_chars': sum(32 <= b <= 126 for b in data),
        'null_bytes': sum(b == 0 for b in data),
        'whitespace_chars': sum(b in [9, 10, 13, 32] for b in data),
        'high_bytes': sum(b > 127 for b in data),
    }
    
    # Look for potential secrets (long random-looking strings)
    secret_pattern = rb'[A-Za-z0-9+/=]{20,}'
    potential_secrets = re.findall(secret_pattern, data)
    
    for secret in potential_secrets[:10]:  # Limit to 10
        secret_str = secret.decode('utf-8', errors='ignore')
        if looks_like_secret(secret_str):
            results['potential_secrets'].append(secret_str)
    
    return results

def looks_like_secret(string: str) -> bool:
    """
    Heuristic to determine if a string looks like a secret/key
    
    Args:
        string: String to analyze
        
    Returns:
        bool: True if it looks like a secret
    """
    if len(string) < 16:
        return False
    
    # Check character distribution (secrets often have good entropy)
    char_counts = {}
    for char in string:
        char_counts[char] = char_counts.get(char, 0) + 1
    
    # Calculate simple entropy
    entropy = 0
    for count in char_counts.values():
        p = count / len(string)
        entropy -= p * (p and (p * p).log() or 0)
    
    # Secrets typically have higher entropy than normal text
    return entropy > 2.5 and not string.isalpha()

def format_hex_dump(data: bytes, width: int = 16, start_addr: int = 0) -> List[str]:
    """
    Format bytes as hex dump lines
    
    Args:
        data: Bytes to format
        width: Bytes per line
        start_addr: Starting address
        
    Returns:
        List of formatted lines
    """
    lines = []
    for i in range(0, len(data), width):
        # Address
        line = f'{start_addr + i:08x}: '
        
        # Hex bytes
        hex_part = ''
        for j in range(width):
            if i + j < len(data):
                hex_part += f'{data[i + j]:02x} '
            else:
                hex_part += '   '
            
            if j == width // 2 - 1:  # Space in middle
                hex_part += ' '
        
        # ASCII
        ascii_part = ''
        for j in range(width):
            if i + j < len(data):
                b = data[i + j]
                if 32 <= b <= 126:
                    ascii_part += chr(b)
                else:
                    ascii_part += '.'
            else:
                ascii_part += ' '
        
        lines.append(line + hex_part + ' ' + ascii_part)
    
    return lines

def extract_strings(data: bytes, min_length: int = 4) -> List[str]:
    """
    Extract readable strings from binary data
    
    Args:
        data: Binary data to scan
        min_length: Minimum string length
        
    Returns:
        List of extracted strings
    """
    strings = []
    current_string = []
    
    for byte in data:
        if 32 <= byte <= 126:  # Printable ASCII
            current_string.append(chr(byte))
        else:
            if len(current_string) >= min_length:
                strings.append(''.join(current_string))
            current_string = []
    
    # Don't forget the last string
    if len(current_string) >= min_length:
        strings.append(''.join(current_string))
    
    return strings

def create_report(analysis_results: Dict[str, Any], target: str) -> str:
    """
    Create a formatted report from analysis results
    
    Args:
        analysis_results: Results from analyze_memory_patterns
        target: Target hostname
        
    Returns:
        Formatted report string
    """
    report = []
    report.append("HEARTBLEED ATTACK ANALYSIS REPORT")
    report.append("=" * 50)
    report.append(f"Target: {target}")
    report.append(f"Total bytes analyzed: {analysis_results['total_bytes']}")
    report.append("")
    
    # Patterns found
    if analysis_results['patterns_found']:
        report.append("PATTERNS FOUND:")
        report.append("-" * 20)
        for pattern, matches in analysis_results['patterns_found'].items():
            report.append(f"{pattern}: {len(matches)} matches")
            for match in matches[:3]:  # Show first 3 matches
                report.append(f"  - {match}")
        report.append("")
    else:
        report.append("No significant patterns found")
        report.append("")
    
    # Statistics
    stats = analysis_results['statistics']
    report.append("MEMORY STATISTICS:")
    report.append("-" * 20)
    report.append(f"Printable characters: {stats['printable_chars']} ({stats['printable_chars']/analysis_results['total_bytes']*100:.1f}%)")
    report.append(f"Null bytes: {stats['null_bytes']} ({stats['null_bytes']/analysis_results['total_bytes']*100:.1f}%)")
    report.append(f"Whitespace: {stats['whitespace_chars']} ({stats['whitespace_chars']/analysis_results['total_bytes']*100:.1f}%)")
    report.append(f"High bytes (>127): {stats['high_bytes']} ({stats['high_bytes']/analysis_results['total_bytes']*100:.1f}%)")
    report.append("")
    
    # Potential secrets
    if analysis_results['potential_secrets']:
        report.append("POTENTIAL SECRETS FOUND:")
        report.append("-" * 25)
        for secret in analysis_results['potential_secrets'][:5]:
            report.append(f"  - {secret}")
    else:
        report.append("No potential secrets identified")
    
    return '\n'.join(report)

if __name__ == '__main__':
    # Example usage
    test_data = b"Hello World! admin:password123 https://example.com session_id=abc123def456"
    results = analyze_memory_patterns(test_data)
    print(create_report(results, "test.example.com"))
