# Client (rsa-oaep-decryption-client)

Questo è il componente client del sistema. È responsabile della creazione (simulata) del dato cifrato e dell'invio al server tramite TCP.

## Contenuto

* `client.py`: Il client TCP che legge `cipher.bin` e lo invia al server.
* `plaintext_in.txt`: Un file di esempio contenente il messaggio da cifrare.
* `generate_cipher.sh`: Script per utilizzare OpenSSL per cifrare `plaintext_in.txt` in `cipher.bin` (simulando l'operazione di cifratura).
* `cipher.bin` (generato): Il file binario cifrato da inviare.
* `plainD_received.txt` (risultato): Il file generato dopo la ricezione della risposta decifrata dal server.

## Istruzioni per l'Esecuzione

1. **Assicurati che il Server sia Attivo:**
   Avvia `server/server.py` nella cartella server.

2. **Genera il File Cifrato:**
   Esegui lo script di generazione (necessita di OpenSSL e della chiave privata nella cartella `server`):
   ```bash
   chmod +x generate_cipher.sh
   ./generate_cipher.sh
