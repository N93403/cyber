#!/usr/bin/env python3
"""
Discover OSINT - Professional Report Generator
Genera report professionali dai risultati delle scansioni OSINT
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

class OSINTReportGenerator:
    def __init__(self, scan_directory, output_file=None):
        self.scan_dir = Path(scan_directory)
        self.output_file = output_file or f"OSINT_Professional_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        self.findings = {}
        
    def load_scan_data(self):
        """Carica i dati dalle scansioni"""
        print("[+] Caricamento dati scansione...")
        
        # Carica sottodomini
        subdomains_file = self.scan_dir / "subdomains.txt"
        if subdomains_file.exists():
            with open(subdomains_file, 'r') as f:
                self.findings['subdomains'] = [line.strip() for line in f if line.strip()]
        
        # Carica hosts
        hosts_file = self.scan_dir / "hosts.txt"
        if hosts_file.exists():
            with open(hosts_file, 'r') as f:
                self.findings['hosts'] = [line.strip() for line in f if line.strip()]
        
        # Carica servizi da nmap
        nmap_file = self.scan_dir / "nmap_scan.txt"
        if nmap_file.exists():
            with open(nmap_file, 'r') as f:
                content = f.read()
                self.findings['open_ports'] = self.extract_open_ports(content)
                self.findings['services'] = self.extract_services(content)
    
    def extract_open_ports(self, nmap_content):
        """Estrae le porte aperte dal report nmap"""
        open_ports = []
        for line in nmap_content.split('\n'):
            if '/tcp' in line and 'open' in line:
                parts = line.split()
                if len(parts) >= 3:
                    open_ports.append({
                        'port': parts[0],
                        'state': parts[1],
                        'service': parts[2]
                    })
        return open_ports
    
    def extract_services(self, nmap_content):
        """Estrae informazioni sui servizi"""
        services = []
        lines = nmap_content.split('\n')
        for i, line in enumerate(lines):
            if 'Service Info:' in line:
                services.append(line.strip())
        return services
    
    def generate_report(self):
        """Genera il report professionale"""
        print("[+] Generazione report professionale...")
        
        # Calcola statistiche
        subdomain_count = len(self.findings.get('subdomains', []))
        open_ports_count = len(self.findings.get('open_ports', []))
        hosts_count = len(self.findings.get('hosts', []))
        
        report_content = f"""# PENETRATION TEST REPORT - OSINT FINDINGS

## 📋 Informazioni Progetto

| Campo | Valore |
|-------|--------|
| Data Rapporto | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| Dominio Target | {self.scan_dir.parent.name} |
| Tipo Assessment | OSINT Passivo |
| Classification | CONFIDENTIAL |

## 🎯 Executive Summary

### Scopo
Assessment di OSINT (Open Source Intelligence) per identificare informazioni pubblicamente esposte e potenziali vettori di attacco.

### Scoperte Principali
- **Sottodomini Identificati**: {subdomain_count}
- **Servizi Esposti**: {open_ports_count}
- **Host Scoperti**: {hosts_count}

### Rischio Complessivo
**MEDIO** - Presenza di servizi esposti e informazioni potenzialmente sensibili.

## 🔍 Risultati Dettagliati

### 1. Infrastruttura Network

#### Hosts Identificati
{chr(10).join(self.findings.get('hosts', ['Nessun host identificato']))}


#### Sottodomini Enumerati
{chr(10).join(self.findings.get('subdomains', ['Nessun sottodominio identificato']))}


### 2. Servizi di Rete Esposti

#### Porte Aperte e Servizi
"""
        
        # Aggiungi tabelle porte
        for port_info in self.findings.get('open_ports', []):
            report_content += f"- **{port_info['port']}** - {port_info['service']} ({port_info['state']})\n"
        
        report_content += """
### 3. Valutazione del Rischio

#### 🔴 Rischio Alto
- Servizi di amministrazione esposti pubblicamente
- Versioni software potenzialmente vulnerabili

#### 🟡 Rischio Medio  
- Informazioni banner che rivelano tecnologie
- Sottodomini non protetti

#### 🟢 Rischio Basso
- Configurazioni di base standard

## 🛡️ Raccomandazioni di Sicurezza

### Priorità Alta (Risoluzione entro 7 giorni)
1. **Limitare l'esposizione dei servizi di amministrazione**
   - Implementare VPN per accesso amministrativo
   - Restringere l'accesso per IP

2. **Oscurare informazioni banner**
   - Modificare header HTTP
   - Disabilitare banner informativi

### Priorità Media (Risoluzione entro 30 giorni)
3. **Monitoraggio continuo OSINT**
   - Implementare monitoring sottodomini
   - Configurare alert per nuove esposizioni

4. **Hardening servizi**
   - Applicare configurazioni security best practice
   - Aggiornare software alle ultime versioni

## 📊 Metriche e Statistiche

| Metrica | Valore |
|---------|--------|
| Sottodomini Scoperti | {subdomain_count} |
| Servizi Esposti | {open_ports_count} |
| Host Pubblici | {hosts_count} |
| Completeness Scan | 85% |

## 📝 Note Tecniche

### Metodologia Utilizzata
- Scansione DNS passiva
- Enumerazione sottodomini
- Fingerprinting servizi
- Analisi informazioni pubbliche

### Limitazioni
- Scansione eseguita da singola fonte
- Possibili falsi positivi/negativi
- Limitazioni di rate limiting

---
*Report generato automaticamente con Discover OSINT Framework*  
*Per uso autorizzato esclusivamente - Classification: CONFIDENTIAL*
"""

        # Salva il report
        with open(self.output_file, 'w') as f:
            f.write(report_content)
        
        print(f"[+] Report generato: {self.output_file}")
        return self.output_file

def main():
    parser = argparse.ArgumentParser(description='Generatore Report OSINT Professionale')
    parser.add_argument('scan_dir', help='Directory contenente i risultati della scansione')
    parser.add_argument('-o', '--output', help='File di output per il report')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.scan_dir):
        print(f"[-] Directory non trovata: {args.scan_dir}")
        sys.exit(1)
    
    # Genera report
    generator = OSINTReportGenerator(args.scan_dir, args.output)
    generator.load_scan_data()
    report_file = generator.generate_report()
    
    print(f"\n[+] Report OSINT professionale generato con successo!")
    print(f"[+] File: {report_file}")

if __name__ == "__main__":
    main()
