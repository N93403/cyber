#!/usr/bin/env python3
"""
Script per testare la connettività di base nel laboratorio
"""

import socket
import subprocess
import sys

def ping_host(host):
    """Esegue un ping verso l'host specificato"""
    try:
        result = subprocess.run(
            ['ping', '-c', '3', host],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except:
        return False

def test_port(host, port):
    """Testa la connessione a una porta specifica"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)
            result = sock.connect_ex((host, port))
            return result == 0
    except:
        return False

def main():
    hosts = {
        'Kali Linux': '192.168.100.10',
        'Metasploitable': '192.168.100.20', 
        'Ubuntu Server': '192.168.100.30'
    }
    
    print("🔍 Test di connettività del laboratorio...")
    
    all_success = True
    
    for name, ip in hosts.items():
        print(f"\nTesting {name} ({ip})...")
        
        # Test ping
        if ping_host(ip):
            print(f"  ✅ Ping a {ip} - OK")
        else:
            print(f"  ❌ Ping a {ip} - FALLITO")
            all_success = False
            continue
        
        # Test porte comuni
        ports = [22, 80, 443, 8000]
        for port in ports:
            if test_port(ip, port):
                print(f"  ✅ Porta {port} - APERTA")
            else:
                print(f"  ❌ Porta {port} - CHIUSA")
    
    if all_success:
        print("\n🎉 Tutti i test sono passati! Il laboratorio è configurato correttamente.")
        return 0
    else:
        print("\n⚠️  Alcuni test sono falliti. Controlla la configurazione di rete.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
