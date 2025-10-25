#(Simulato per GitHub)
# 🔒 Ransomware-Hybrid-VM-Sim: Simulazione Crittografia Ibrida (AES/RSA) su 2 VM

Questo progetto è un esercizio pratico di cybersecurity per simulare il ciclo completo di un attacco ransomware ibrido e il successivo ripristino in un ambiente di rete distribuito (due Macchine Virtuali).

## ⚠️ Disclaimer Etico

**Questo codice è strettamente a scopo didattico. Non usarlo per scopi illeciti.**

## 🎯 Obiettivo del Progetto

Simulare lo scambio di chiavi asimmetrico (`RSA`) su una rete (`socket`) per sbloccare la crittografia simmetrica (`AES`) dei file, replicando un tipico schema di riscatto.

## 💻 Configurazione Lab (Due VM)

| Ruolo | VM | IP Esempio | File Eseguiti |
| :--- | :--- | :--- | :--- |
| **Aggressore/Server** | **VM 1** | `192.168.1.10` | `server_decrypt_key.py`, `utils.py`, **`keys/private_key.pem`** |
| **Vittima/Client** | **VM 2** | `192.168.1.11` | `ransomware_attack.py`, `client_send_key.py`, `decryptor.py` |

**NOTA:** Assicurati che le VM siano sulla stessa rete e che i firewall non blocchino la porta `8082`.

## 🚀 Istruzioni Passo-Passo

### Passo 0: Setup e Generazione Chiavi

1.  **Su entrambe le VM:** Installa le dipendenze: `pip install -r requirements.txt`.
2.  **Su VM 1 (Aggressore):** Genera la coppia di chiavi RSA.
    ```bash
    cd vm1_attacker_server
    python3 utils.py
    ```
3.  **Distribuzione Chiave:** Copia il file **`keys/public_key.pem`** da VM 1 alla cartella `keys/` di VM 2.

### Passo 1: L'Attacco (Su VM 2)

Esegui lo script del ransomware sulla vittima. Questo cifra `FileToEncrypt.txt` e crea `encryptedSymmertricKey.key`.

```bash
# Su VM 2 (Vittima)
cd vm2_victim_client
python3 ransomware_attack.py

Passo 2: Il Riscatto (Comunicazione Network)
Su VM 1 (Aggressore): Avvia il server in attesa del riscatto.

Bash

# Su VM 1 (Aggressore/Server)
cd vm1_attacker_server
python3 server_decrypt_key.py
Su VM 2 (Vittima): Modifica l'IP in client_send_key.py con l'IP di VM 1. Esegui il client per inviare la chiave cifrata.

Bash

# Su VM 2 (Vittima/Client)
cd vm2_victim_client
python3 client_send_key.py
Il server (VM 1) decifra la chiave AES con la sua chiave privata e la rispedisce al client (VM 2), che la salva in test_files/decrypted_key_from_server.key.

Passo 3: Il Ripristino (Su VM 2)
Esegui lo strumento di decrittazione (che simula il tool fornito dall'aggressore) per ripristinare i file.

Bash

# Su VM 2 (Vittima/Client)
cd vm2_victim_client
python3 decryptor.py
Il file FileToEncrypt.txt sarà ripristinato, confermando il successo dell'intero ciclo.
