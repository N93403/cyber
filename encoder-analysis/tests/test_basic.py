#!/usr/bin/env python3
"""
TEST BASE PER PROGETTO ENCODER
Verifica funzionalità fondamentali
"""

import unittest
import os
import subprocess
from pathlib import Path

class TestEncoderProject(unittest.TestCase):
    
    def setUp(self):
        """Setup prima di ogni test"""
        self.project_root = Path(__file__).parent.parent
        self.payloads_dir = self.project_root / 'payloads'
        self.scripts_dir = self.project_root / 'scripts'
        self.results_dir = self.project_root / 'results'
    
    def test_directory_structure(self):
        """Test struttura directory progetto"""
        required_dirs = ['payloads', 'scripts', 'docs', 'tests', 'results']
        
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            self.assertTrue(dir_path.exists(), f"Directory {dir_name} mancante")
            self.assertTrue(dir_path.is_dir(), f"{dir_name} non è una directory")
    
    def test_essential_scripts(self):
        """Test script essenziali"""
        essential_scripts = [
            'generate_payloads.sh',
            'custom_xor_encoder.py',
            'analysis_tool.py'
        ]
        
        for script in essential_scripts:
            script_path = self.scripts_dir / script
            self.assertTrue(script_path.exists(), f"Script {script} mancante")
            self.assertTrue(os.access(script_path, os.X_OK), f"Script {script} non eseguibile")
    
    def test_payload_generation(self):
        """Test generazione payload base"""
        # Esegui script di generazione
        gen_script = self.scripts_dir / 'generate_payloads.sh'
        
        if gen_script.exists():
            result = subprocess.run(
                ['bash', str(gen_script)], 
                capture_output=True, 
                text=True,
                cwd=self.scripts_dir
            )
            
            # Verifica che lo script sia eseguito
            self.assertEqual(result.returncode, 0, 
                           f"Script generazione fallito: {result.stderr}")
            
            # Verifica che alcuni file siano stati creati
            expected_files = ['original.elf', 'base64_encoded.elf']
            for file in expected_files:
                file_path = self.payloads_dir / file
                if result.returncode == 0:  # Solo se lo script ha successo
                    self.assertTrue(file_path.exists(), f"File {file} non generato")
    
    def test_python_dependencies(self):
        """Test dipendenze Python"""
        try:
            import hashlib
            import argparse
            import json
            from collections import Counter
            from pathlib import Path
            
            # Se arriviamo qui, le dipendenze sono OK
            self.assertTrue(True)
            
        except ImportError as e:
            self.fail(f"Dipendenza Python mancante: {e}")
    
    def test_analysis_tool(self):
        """Test strumento di analisi"""
        analysis_script = self.scripts_dir / 'analysis_tool.py'
        
        if analysis_script.exists():
            # Test che lo script possa essere importato
            try:
                # Aggiungi directory scripts al path
                import sys
                sys.path.append(str(self.scripts_dir))
                
                # Importa il modulo
                from analysis_tool import PayloadAnalyzer
                
                # Test creazione istanza
                analyzer = PayloadAnalyzer()
                self.assertIsNotNone(analyzer)
                
            except ImportError as e:
                self.fail(f"Impossibile importare analysis_tool: {e}")
    
    def test_custom_encoder(self):
        """Test encoder personalizzato"""
        encoder_script = self.scripts_dir / 'custom_xor_encoder.py'
        
        if encoder_script.exists():
            try:
                import sys
                sys.path.append(str(self.scripts_dir))
                
                from custom_xor_encoder import XOREncoder
                
                # Test creazione encoder
                encoder = XOREncoder(key=0xAA)
                self.assertIsNotNone(encoder)
                self.assertEqual(encoder.key, 0xAA)
                
            except ImportError as e:
                self.fail(f"Impossibile importare custom_xor_encoder: {e}")

class TestSecurityMeasures(unittest.TestCase):
    """Test misure di sicurezza"""
    
    def test_no_hardcoded_credentials(self):
        """Test che non ci siano credenziali hardcoded"""
        project_root = Path(__file__).parent.parent
        
        # Cerca pattern sospetti
        suspicious_patterns = [
            'password=',
            'passwd=',
            'pwd=',
            'key=',
            'secret=',
            'token='
        ]
        
        for pattern in suspicious_patterns:
            # Cerca in file Python e shell
            for file_path in project_root.rglob('*.py'):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    self.assertNotIn(pattern, content.lower(), 
                                   f"Pattern sospetto in {file_path}")
            
            for file_path in project_root.rglob('*.sh'):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    self.assertNotIn(pattern, content.lower(),
                                   f"Pattern sospetto in {file_path}")

if __name__ == '__main__':
    # Crea directory necessarie per i test
    test_project_root = Path(__file__).parent.parent
    (test_project_root / 'payloads').mkdir(exist_ok=True)
    (test_project_root / 'results').mkdir(exist_ok=True)
    
    # Esegui test
    unittest.main(verbosity=2)
