#!/usr/bin/env python3
"""
SMTP Fuzzer using Spike framework
Educational purposes only
"""

import subprocess
import sys
import time
from pathlib import Path

class SMTPFuzzer:
    def __init__(self, target_ip, target_port=25):
        self.target_ip = target_ip
        self.target_port = target_port
        self.spike_script = "smtp1.spk"
        self.results_dir = Path("analysis_results")
        self.results_dir.mkdir(exist_ok=True)
    
    def check_target(self):
        """Verify target is reachable and SMTP port is open"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.target_ip, self.target_port))
            sock.close()
            return result == 0
        except Exception as e:
            print(f"Error checking target: {e}")
            return False
    
    def start_fuzzing(self, skip_variables=0, skip_strings=0):
        """Start SMTP fuzzing with Spike"""
        if not self.check_target():
            print(f"Target {self.target_ip}:{self.target_port} is not reachable")
            return False
        
        print(f"Starting SMTP fuzzing on {self.target_ip}:{self.target_port}")
        print(f"Spike script: {self.spike_script}")
        
        try:
            # Build command for generic_web_server_fuzz
            cmd = [
                "generic_web_server_fuzz",
                self.target_ip,
                str(self.target_port),
                self.spike_script,
                str(skip_variables),
                str(skip_strings)
            ]
            
            print(f"Executing: {' '.join(cmd)}")
            
            # Start fuzzing process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Monitor output
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                
                time.sleep(0.1)
            
            return True
            
        except FileNotFoundError:
            print("Error: generic_web_server_fuzz not found. Is Spike installed?")
            return False
        except Exception as e:
            print(f"Fuzzing error: {e}")
            return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python fuzzer_spike.py <target_ip> [port] [skip_vars] [skip_strings]")
        print("Example: python fuzzer_spike.py 192.168.1.100 25 0 0")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    skip_vars = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    skip_strings = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    
    fuzzer = SMTPFuzzer(target_ip, port)
    fuzzer.start_fuzzing(skip_vars, skip_strings)

if __name__ == "__main__":
    main()
