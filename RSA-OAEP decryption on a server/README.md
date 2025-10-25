# rsa-oaep-client (Cifratore e Mittente)

Questo progetto implementa un client TCP robusto in Python 3 per inviare dati crittografati RSA-OAEP a un server decifratore.

## Contenuto del Repository

* `client.py`: Il codice client, migliorato con timeout di connessione e gestione errori robusta.
* `plaintext_in.txt`: File di esempio da crittografare.
* `generate_cipher.sh`: Script helper per cifrare `plaintext_in.txt` in `cipher.bin` (simulazione lato client).
* `cipher.bin` (generato): Il file binario cifrato da inviare al server.
* `plainD_received.txt` (risultato): Il file che conterrà il messaggio decifrato ricevuto dal server.

## Istruzioni per il Test

1. **Preparazione Chiave Pubblica:**
   Per simulare l'operazione di cifratura lato client, avrai bisogno di un file di chiave privata per estrarre la pubblica. **Copia `pub_priv_pair.key`** dal repository del server in questa directory.

2. **Generazione del Cipher:**
   Esegui lo script bash per cifrare il file di input.
   ```bash
   chmod +x generate_cipher.sh
   ./generate_cipher.sh
