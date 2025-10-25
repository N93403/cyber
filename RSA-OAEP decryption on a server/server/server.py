#Il server potenziato: gestisce la concorrenza (ThreadingTCPServer), corregge la logica di ricezione dati e usa tempfile per un I/O sicuro e pulito, eliminando il Base64 ridondante.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socketserver     # Framework per server (ThreadingTCPServer per la concorrenza)
import subprocess       # Esegue comandi esterni (openssl)
import os               # Operazioni sul filesystem
import tempfile         # Gestione sicura dei file temporanei

# Usiamo ThreadingTCPServer per gestire più client contemporaneamente.
class ClientHandler(socketserver.BaseRequestHandler):
    """
    Gestore per ogni singola connessione in arrivo (eseguito in un thread separato).
    """

    def handle(self):
        client_ip, client_port = self.client_address
        print(f"[{client_ip}:{client_port}] Nuova connessione iniziata.")
        
        # --- 1) Ricezione robusta dei dati cifrati dal client ---
        encrypted_data = b""
        try:
            # Leggiamo in un loop finché il client non chiude lo stream di scrittura (EOF)
            while True:
                part = self.request.recv(4096)
                if not part:
                    break
                encrypted_data += part
        except ConnectionResetError:
            print(f"[{client_ip}:{client_port}] Connessione interrotta dal client.")
            return

        print(f"[{client_ip}:{client_port}] Dati cifrati ricevuti (len={len(encrypted_data)} bytes).")

        if not encrypted_data:
             print(f"[{client_ip}:{client_port}] Nessun dato ricevuto. Interruzione.")
             return 

        # --- 2) Decifratura RSA-OAEP utilizzando openssl e file temporanei sicuri ---
        try:
            # Uso di tempfile.NamedTemporaryFile per creare file eliminati automaticamente.
            # Questo evita l'overhead di cleanup manuale e migliora la sicurezza I/O.
            with tempfile.NamedTemporaryFile(delete=True) as cipher_file, \
                 tempfile.NamedTemporaryFile(delete=True) as plain_file:
                
                # Scriviamo i dati cifrati nel file temporaneo di input
                cipher_file.write(encrypted_data)
                cipher_file.flush() # Forza la scrittura su disco
                
                # Comando openssl pkeyutl -decrypt (DIRETTO, senza Base64 intermedio)
                subprocess.run([
                    "openssl", "pkeyutl", "-decrypt",
                    "-inkey", "pub_priv_pair.key",         # La chiave privata
                    "-in", cipher_file.name,               # Input: file cifrato temporaneo
                    "-out", plain_file.name,               # Output: file in chiaro temporaneo
                    "-pkeyopt", "rsa_padding_mode:oaep"    # OBBLIGATORIO: Padding sicuro OAEP
                ], check=True, stderr=subprocess.PIPE, universal_newlines=True) 
                
                print(f"[{client_ip}:{client_port}] Decifratura riuscita. ")

                # --- 3) Lettura del plaintext e invio al client ---
                plain_file.seek(0) # Torna all'inizio del file
                decrypted_data = plain_file.read()
                
                self.request.sendall(decrypted_data)
                print(f"[{client_ip}:{client_port}] Plaintext inviato ({len(decrypted_data)} bytes).")

        except subprocess.CalledProcessError as e:
            # Errore di decifratura (e.g., dati corrotti, padding errato)
            print(f"[{client_ip}:{client_port}] Errore di decifratura OpenSSL (codice: {e.returncode}).")
            # print(f"Dettagli: {e.stderr}") # Abilitare per debugging openssl

        except Exception as e:
            # Errore generico
            print(f"[{client_ip}:{client_port}] Errore inatteso: {e}")
            
        finally:
            print(f"[{client_ip}:{client_port}] Connessione chiusa.")


if __name__ == "__main__":
    HOST, PORT = "", 8082 # Ascolta su tutte le interfacce sulla porta 8082
    
    # TCPServerThreaded per gestire la concorrenza
    with socketserver.ThreadingTCPServer((HOST, PORT), ClientHandler) as tcpServer:
        print("--- RSA-OAEP Decrypt Server ---")
        
        # Verifica l'esistenza della chiave privata
        if not os.path.exists("pub_priv_pair.key"):
            print("\nERRORE CRITICO: Chiave privata 'pub_priv_pair.key' non trovata.")
            print("Chiusura del server.")
            exit(1)
            
        print(f"Server in ascolto su {HOST}:{PORT}")
        
        try:
            tcpServer.serve_forever()
        except KeyboardInterrupt:
            print("\nServer interrotto dall'utente. Chiusura...")
        except Exception as e:
            print("Errore a livello server:", e)
        finally:
             tcpServer.server_close()
