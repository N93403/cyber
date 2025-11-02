
### 📄 **tools/memory_analyzer.py**
```python
#!/usr/bin/env python3
"""
Memory Analyzer for Heartbleed Dumps
Advanced analysis of extracted memory data
"""

import re
import json
import argparse
from typing import Dict, List, Any
from pathlib import Path

class MemoryAnalyzer:
    """Advanced memory dump analyzer for Heartbleed data"""
    
    def __init__(self):
        self.patterns = {
            'credentials': [
                rb'admin:([^\s&]+)',
                rb'username=([^&\s]+)',
                rb'password=([^&\s]+)',
                rb'login=([^&\s]+)',
                rb'pass=([^&\s]+)',
            ],
            'sessions': [
                rb'session=([A-Za-z0-9+/=]{16,})',
                rb'session_id=([A-Za-z0-9+/=]{16,})',
                rb'PHPSESSID=([A-Za-z0-9+/=]{16,})',
                rb'token=([A-Za-z0-9+/=]{16,})',
            ],
            'keys': [
                rb'-----BEGIN RSA PRIVATE KEY-----',
                rb'-----BEGIN DSA PRIVATE KEY-----',
                rb'-----BEGIN EC PRIVATE KEY-----',
                rb'ssh-rsa AAAA[0-9A-Za-z+/]+',
            ],
            'emails': [
                rb'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            ],
            'urls': [
                rb'https?://[^\s<>"]+',
                rb'www\.[^\s<>"]+\.[a-z]{2,}',
            ]
        }
    
    def load_dump(self, file_path: str) -> bytes:
        """Load memory dump from file"""
        with open(file_path, 'rb') as f:
            return f.read()
    
    def analyze_dump(self, data: bytes) -> Dict[str, Any]:
        """Comprehensive analysis of memory dump"""
        results = {
            'file_info': {},
            'patterns_found': {},
            'statistics': {},
            'interesting_strings': [],
            'risk_assessment': {}
        }
        
        # Basic file info
        results['file_info'] = {
            'size_bytes': len(data),
            'size_kb': len(data) / 1024,
            'size_mb': len(data) / (1024 * 1024)
        }
        
        # Pattern matching
        for category, pattern_list in self.patterns.items():
            category_results = []
            for pattern in pattern_list:
                matches = re.findall(pattern, data, re.IGNORECASE)
                for match in matches:
                    try:
                        decoded = match.decode('utf-8', errors='ignore') if isinstance(match, bytes) else match
                        category_results.append({
                            'pattern': pattern.decode('utf-8', errors='ignore'),
                            'match': decoded,
                            'context': self.get_context(data, match)
                        })
                    except:
                        continue
            
            if category_results:
                results['patterns_found'][category] = category_results
        
        # Statistics
        results['statistics'] = self.calculate_statistics(data)
        
        # Interesting strings (long, high entropy)
        results['interesting_strings'] = self.find_interesting_strings(data)
        
        # Risk assessment
        results['risk_assessment'] = self.assess_risk(results)
        
        return results
    
    def get_context(self, data: bytes, match: bytes, context_size: int = 50) -> str:
        """Get context around a match"""
        if isinstance(match, bytes):
            pos = data.find(match)
            if pos == -1:
                return ""
            
            start = max(0, pos - context_size)
            end = min(len(data), pos + len(match) + context_size)
            context = data[start:end]
            
            try:
                return context.decode('utf-8', errors='ignore')
            except:
                return str(context)
        return ""
    
    def calculate_statistics(self, data: bytes) -> Dict[str, Any]:
        """Calculate various statistics about the dump"""
        stats = {}
        
        # Basic character counts
        stats['total_bytes'] = len(data)
        stats['null_bytes'] = sum(b == 0 for b in data)
        stats['printable'] = sum(32 <= b <= 126 for b in data)
        stats['whitespace'] = sum(b in [9, 10, 13, 32] for b in data)
        stats['control_chars'] = sum(b < 32 and b not in [9, 10, 13] for b in data)
        stats['high_bytes'] = sum(b > 127 for b in data)
        
        # Percentages
        stats['printable_percent'] = (stats['printable'] / stats['total_bytes']) * 100
        stats['null_percent'] = (stats['null_bytes'] / stats['total_bytes']) * 100
        
        # Entropy estimation
        stats['entropy'] = self.calculate_entropy(data)
        
        return stats
    
    def calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy of the data"""
        if not data:
            return 0
        
        entropy = 0
        for x in range(256):
            p_x = data.count(x) / len(data)
            if p_x > 0:
                entropy += - p_x * (p_x and (p_x * p_x).log() or 0)
        
        return entropy
    
    def find_interesting_strings(self, data: bytes, min_length: int = 20) -> List[Dict]:
        """Find potentially interesting strings in the dump"""
        interesting = []
        
        # Extract all strings of minimum length
        strings = self.extract_strings(data, min_length)
        
        for string in strings:
            # Score string based on various characteristics
            score = self.score_string(string)
            
            if score > 0.7: 
