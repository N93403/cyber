#!/usr/bin/env python3
"""
Script per test di stress limitato sul target Metasploitable
Utilizzare solo in ambienti controllati per scopi didattici
"""

import requests
import threading
import time
import logging

class LimitedStressTester:
    def __init__(self, target_url):
        self.target_url = target_url
        self.requests_sent = 0
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('StressTester')
    
    def make_request(self, thread_id):
        """Invia una singola richiesta HTTP"""
        try:
            response = requests.get(self.target_url, timeout=5)
            self.requests_sent += 1
            if self.requests_sent % 50 == 0:
                self.logger.info(f"Thread {thread_id}: {self.requests_sent} richieste inviate")
        except Exception as e:
            self.logger.error(f"Thread {thread_id}: Errore - {e}")
    
    def run_stress_test(self, duration=30, max_threads=10):
        """
        Esegue un test di stress limitato per scopi didattici
        
        Args:
            duration: Durata del test in secondi
            max_threads: Numero massimo di thread concorrenti
        """
        self.logger.info(f"🚀 Avvio stress test limitato su {self.target_url}")
        self.logger.info(f"⏱️  Durata: {duration} secondi")
        self.logger.info(f"🧵 Threads: {max_threads}")
        self.logger.info("⚠️  Questo è un test CONTROLLATO per scopi didattici!")
        
        stop_event = threading.Event()
        threads = []
        
        def worker(thread_id):
            while not stop_event.is_set():
                self.make_request(thread_id)
                time.sleep(0.1)  # Limita il rate
        
        # Avvia i thread
        for i in range(max_threads):
            t = threading.Thread(target=worker, args=(i,))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Avvia il timer
        start_time = time.time()
        try:
            while time.time() - start_time < duration:
                elapsed = time.time() - start_time
                remaining = duration - elapsed
                self.logger.info(f"⏳ Tempo rimanente: {remaining:.1f}s - Richieste: {self.requests_sent}")
                time.sleep(2)
        except KeyboardInterrupt:
            self.logger.info("Test interrotto dall'utente")
        
        # Ferma i thread
        stop_event.set()
        for t in threads:
            t.join(timeout=1)
        
        self.logger.info(f"✅ Test completato")
        self.logger.info(f"📊 Totale richieste effettuate: {self.requests_sent}")
        self.logger.info(f"📈 Richieste al secondo: {self.requests_sent / duration:.1f}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Test di stress limitato')
    parser.add_argument('target', help='URL target (es: http://192.168.100.20)')
    parser.add_argument('-d', '--duration', type=int, default=30, 
                       help='Durata in secondi (default: 30)')
    parser.add_argument('-t', '--threads', type=int, default=10,
                       help='Numero di thread (default: 10)')
    
    args = parser.parse_args()
    
    print("⚠️  AVVISO: Questo tool è solo per scopi didattici!")
    print("⚠️  Usare solo in ambienti controllati con autorizzazione")
    print(f"🎯 Target: {args.target}")
    print(f"⏱️  Durata: {args.duration}s")
    print(f"🧵 Threads: {args.threads}")
    
    confirm = input("\nProcedere? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Operazione annullata.")
        return
    
    tester = LimitedStressTester(args.target)
    tester.run_stress_test(args.duration, args.threads)

if __name__ == "__main__":
    main()
