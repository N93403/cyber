#Assunzione: Il file encrypted_data.txt (il tuo encrypted.txt) è stato cifrato con OpenSSL usando la chiave simmetrica derivata da DH.
#!/usr/bin/env python3
"""
Decifra il file encrypted_data.txt usando la chiave simmetrica AliceSharedSecret.bin.
Richiede OpenSSL (solitamente preinstallato su Linux MX).
"""
import subprocess
import os
import sys

# === CONFIGURAZIONE ===
ENCRYPTED_FILE = 'encrypted_data.txt'
SHARED_SECRET_FILE = 'AliceSharedSecret.bin'
DECRYPTED_FILE = 'decrypted_output.txt'

def decifra_dati():
    """Esegue la decifratura chiamando OpenSSL."""
    
    if not os.path.exists(ENCRYPTED_FILE) or not os.path.exists(SHARED_SECRET_FILE):
        print(f"ERRORE: File {ENCRYPTED_FILE} o {SHARED_SECRET_FILE} non trovati.")
        print("Assicurati che i file siano presenti e che il file DH contenga la chiave simmetrica.")
        sys.exit(1)

    print(f"Tentativo di decifrare {ENCRYPTED_FILE} usando la chiave da {SHARED_SECRET_FILE}...")
    
    try:
        # 1. Lettura della chiave binaria segreta (Shared Secret)
        with open(SHARED_SECRET_FILE, 'rb') as f:
            # La chiave DH viene usata come chiave/passphrase
            dh_key = f.read().hex()
            
        # 2. Chiamata a OpenSSL per decifrare
        # Verrà usato un algoritmo comune (es. AES-256-CBC)
        # La decifratura OpenSSL richiede l'opzione -K (per la chiave in esadecimale)
        command = [
            'openssl', 'enc', '-d', '-aes-256-cbc', 
            '-in', ENCRYPTED_FILE,
            '-out', DECRYPTED_FILE,
            '-K', dh_key, # Passa la chiave segreta (Shared Secret) in esadecimale
            '-base64'
        ]
        
        # Esecuzione del comando
        result = subprocess.run(command, check=True, capture_output=True)
        
        print(f"\n[ DEIFRATURA RIUSCITA ]")
        print(f"Dati decifrati salvati in {DECRYPTED_FILE}")
        
        # Stampa il contenuto per verifica
        with open(DECRYPTED_FILE, 'r') as f:
            print("\n--- Contenuto Decifrato ---")
            print(f.read().strip())
            print("--------------------------")

    except subprocess.CalledProcessError as e:
        print(f"ERRORE di Decifratura OpenSSL. Potrebbe essere necessario specificare un algoritmo differente o la chiave non è corretta.")
        print(f"Errore: {e.stderr.decode()}")
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == '__main__':
    decifra_dati()
