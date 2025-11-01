#!/usr/bin/env python3
"""
Monitor di sistema per laboratorio didattico
Monitora CPU, memoria, rete e processi
"""

import psutil
import time
import logging
import json
from datetime import datetime

class SystemMonitor:
    def __init__(self, log_file='system_monitor.log'):
        self.log_file = log_file
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('SystemMonitor')
    
    def get_system_stats(self):
        """Raccoglie statistiche di sistema"""
        stats = {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'cores': psutil.cpu_count(),
                'load_avg': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else 'N/A'
            },
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent,
                'used': psutil.virtual_memory().used
            },
            'network': {
                'bytes_sent': psutil.net_io_counters().bytes_sent,
                'bytes_recv': psutil.net_io_counters().bytes_recv,
                'packets_sent': psutil.net_io_counters().packets_sent,
                'packets_recv': psutil.net_io_counters().packets_recv
            },
            'processes': len(psutil.pids())
        }
        return stats
    
    def format_stats(self, stats):
        """Formatta le statistiche per la visualizzazione"""
        return (
            f"🖥️  CPU: {stats['cpu']['percent']}% | "
            f"🧠 MEM: {stats['memory']['percent']}% | "
            f"📨 NET: ↓{stats['network']['bytes_recv']} ↑{stats['network']['bytes_sent']} | "
            f"🔢 PROCESSI: {stats['processes']}"
        )
    
    def save_stats_json(self, stats):
        """Salva le statistiche in formato JSON"""
        with open('system_stats.json', 'a') as f:
            json.dump(stats, f)
            f.write('\n')
    
    def monitor_loop(self, interval=5):
        """Loop principale di monitoraggio"""
        self.logger.info(f"Inizio monitoraggio sistema (intervallo: {interval}s")
        
        try:
            while True:
                stats = self.get_system_stats()
                
                # Log delle statistiche
                self.logger.info(self.format_stats(stats))
                
                # Salva in JSON
                self.save_stats_json(stats)
                
                # Allerta se l'uso della CPU o memoria è troppo alto
                if stats['cpu']['percent'] > 80:
                    self.logger.warning(f"⚠️  Utilizzo CPU elevato: {stats['cpu']['percent']}%")
                
                if stats['memory']['percent'] > 80:
                    self.logger.warning(f"⚠️  Utilizzo memoria elevato: {stats['memory']['percent']}%")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.logger.info("Monitoraggio interrotto dall'utente")

def main():
    print("📊 System Monitor Avviato")
    print("⚠️  Monitoraggio risorse di sistema...")
    
    monitor = SystemMonitor()
    monitor.monitor_loop()

if __name__ == "__main__":
    main()
