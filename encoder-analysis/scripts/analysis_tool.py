#!/usr/bin/env python3
"""
STRUMENTO DI ANALISI ENCODER
Analizza e confronta payload originali e codificati
"""

import os
import hashlib
import math
import json
from collections import Counter
from pathlib import Path

class PayloadAnalyzer:
    def __init__(self):
        self.results = {}
        
    def calculate_entropy(self, data):
        """Calcola l'entropia di Shannon"""
        if len(data) == 0:
            return 0.0
            
        counter = Counter(data)
        entropy = 0.0
        
        for count in counter.values():
            p_x = count / len(data)
            if p_x > 0:
                entropy += -p_x * math.log2(p_x)
                
        return entropy
    
    def calculate_compression_ratio(self, original_size, encoded_size):
        """Calcola rapporto di compressione (negativo per aumento)"""
        return ((encoded_size - original_size) / original_size) * 100
    
    def analyze_file(self, filepath):
        """Analizza un singolo file"""
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            filename = Path(filepath).name
            analysis = {
                'filename': filename,
                'size': len(data),
                'md5': hashlib.md5(data).hexdigest(),
                'sha256': hashlib.sha256(data).hexdigest(),
                'entropy': self.calculate_entropy(data),
                'byte_distribution': self._get_byte_distribution(data)
            }
            
            return analysis
            
        except Exception as e:
            print(f"❌ Errore analisi {filepath}: {e}")
            return None
    
    def _get_byte_distribution(self, data):
        """Ottiene distribuzione bytes per categoria"""
        if len(data) == 0:
            return {}
            
        categories = {
            'null_bytes': sum(1 for b in data if b == 0),
            'printable_ascii': sum(1 for b in data if 32 <= b <= 126),
            'control_chars': sum(1 for b in data if b < 32 and b != 0),
            'high_bytes': sum(1 for b in data if b > 126)
        }
        
        total = len(data)
        for key in categories:
            categories[key] = (categories[key] / total) * 100
            
        return categories
    
    def compare_payloads(self, base_analysis, encoded_analysis):
        """Confronta due analisi"""
        comparison = {
            'size_difference': encoded_analysis['size'] - base_analysis['size'],
            'size_ratio_percent': self.calculate_compression_ratio(
                base_analysis['size'], encoded_analysis['size']),
            'entropy_difference': encoded_analysis['entropy'] - base_analysis['entropy'],
            'entropy_ratio_percent': ((encoded_analysis['entropy'] - base_analysis['entropy']) / base_analysis['entropy']) * 100,
            'hash_changed': base_analysis['md5'] != encoded_analysis['md5']
        }
        
        return comparison
    
    def analyze_directory(self, directory_path):
        """Analizza tutti i file in una directory"""
        payload_files = list(Path(directory_path).glob('*.elf'))
        
        if not payload_files:
            print(f"❌ Nessun file .elf trovato in {directory_path}")
            return {}
        
        print(f"🔍 Analisi {len(payload_files)} file in {directory_path}")
        
        analyses = {}
        for filepath in payload_files:
            analysis = self.analyze_file(filepath)
            if analysis:
                analyses[analysis['filename']] = analysis
        
        return analyses
    
    def generate_report(self, analyses, output_file):
        """Genera report completo"""
        if not analyses:
            print("❌ Nessuna analisi da reportare")
            return
        
        # Trova file originale per confronti
        original_analysis = None
        for name, analysis in analyses.items():
            if 'original' in name.lower():
                original_analysis = analysis
                break
        
        report = {
            'metadata': {
                'generated_at': str(os.path.dirname(os.path.abspath(__file__))),
                'total_files_analyzed': len(analyses),
                'original_file': original_analysis['filename'] if original_analysis else None
            },
            'analyses': analyses,
            'comparisons': {}
        }
        
        # Calcola confronti se abbiamo originale
        if original_analysis:
            for name, analysis in analyses.items():
                if name != original_analysis['filename']:
                    report['comparisons'][name] = self.compare_payloads(
                        original_analysis, analysis)
        
        # Salva report JSON
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Genera report leggibile
        self._generate_human_report(report, output_file.replace('.json', '.txt'))
        
        return report
    
    def _generate_human_report(self, report, output_file):
        """Genera report in formato leggibile"""
        with open(output_file, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("           RAPPORTO ANALISI ENCODER\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("METADATA:\n")
            f.write(f"- File analizzati: {report['metadata']['total_files_analyzed']}\n")
            f.write(f"- File originale: {report['metadata']['original_file']}\n\n")
            
            f.write("ANALISI INDIVIDUALI:\n")
            f.write("-" * 40 + "\n")
            
            for name, analysis in report['analyses'].items():
                f.write(f"\n📁 {name}:\n")
                f.write(f"  Size: {analysis['size']} bytes\n")
                f.write(f"  MD5: {analysis['md5']}\n")
                f.write(f"  Entropy: {analysis['entropy']:.4f}\n")
                f.write(f"  SHA256: {analysis['sha256'][:32]}...\n")
            
            if report['comparisons']:
                f.write("\n" + "=" * 60 + "\n")
                f.write("CONFRONTI CON ORIGINALE:\n")
                f.write("=" * 60 + "\n")
                
                for name, comparison in report['comparisons'].items():
                    f.write(f"\n🔄 {name} vs Originale:\n")
                    f.write(f"  📏 Size change: {comparison['size_difference']:+d} bytes ")
                    f.write(f"({comparison['size_ratio_percent']:+.2f}%)\n")
                    f.write(f"  🎲 Entropy change: {comparison['entropy_difference']:+.4f} ")
                    f.write(f"({comparison['entropy_ratio_percent']:+.2f}%)\n")
                    f.write(f"  🔐 Hash changed: {comparison['hash_changed']}\n")
        
        print(f"✅ Report generato: {output_file}")

def main():
    analyzer = PayloadAnalyzer()
    
    # Configurazione paths
    payloads_dir = Path('../payloads')
    results_dir = Path('../results')
    results_dir.mkdir(exist_ok=True)
    
    print("🔍 STRUMENTO DI ANALISI ENCODER")
    print("=" * 50)
    
    # Verifica esistenza payloads
    if not payloads_dir.exists():
        print(f"❌ Directory payloads non trovata: {payloads_dir}")
        return
    
    # Analizza tutti i file
    analyses = analyzer.analyze_directory(payloads_dir)
    
    if not analyses:
        print("❌ Nessun file valido da analizzare")
        return
    
    # Genera report
    json_report = results_dir / 'analysis_report.json'
    txt_report = results_dir / 'analysis_report.txt'
    
    report = analyzer.generate_report(analyses, json_report)
    
    if report:
        print(f"\n📊 ANALISI COMPLETATA!")
        print(f"📁 File analizzati: {len(analyses)}")
        print(f"📄 Report JSON: {json_report}")
        print(f"📄 Report testo: {txt_report}")
        
        # Mostra riepilogo a schermo
        if 'comparisons' in report and report['comparisons']:
            print(f"\n🎯 ENCODER PIÙ EFFICACE:")
            best_encoder = max(report['comparisons'].items(), 
                             key=lambda x: x[1]['entropy_difference'])
            print(f"   {best_encoder[0]}: Δ entropy = {best_encoder[1]['entropy_difference']:+.4f}")

if __name__ == "__main__":
    main()
