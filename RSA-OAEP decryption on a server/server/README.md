# Server (rsa-oaep-decryption-server)

Questo è il componente server del sistema di decifratura. Utilizza un server TCP multithreaded in Python e l'utility OpenSSL per decifrare in modo sicuro dati crittografati con lo schema RSA-OAEP.

## Prerequisiti

1. **Python 3.x**
2. **OpenSSL** (Installato e accessibile)

## Contenuto

* `server.py`: Il server multithreaded che gestisce la ricezione e la decifratura.
* `pub_priv_pair.key`: La chiave privata RSA (da mantenere segreta) utilizzata per l'operazione di decifratura.

## Istruzioni per l'Avvio

1. **Sicurezza della Chiave:**
   Assicurati di impostare permessi restrittivi sulla chiave privata (essenziale per la sicurezza):
   ```bash
   chmod 600 pub_priv_pair.key
Esecuzione: Avvia il server. Sarà in ascolto sulla porta 8082.

Bash

python3 server.py
Test: Avviare il client nella cartella client per inviare i dati cifrati.


---

## 2. Cartella `client`

Contiene il client per l'invio dei dati e gli script di supporto per la cifratura.

### 📄 `client/client.py`

Il client potenziato con timeout di connessione e gestione robusta degli errori di rete.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket       # API di rete
import sys          # Argomenti da riga di comando

def get_server_address():
    """
    Richiede all'utente IP e porta del server e valida l'input.
    """
    while True:
        try:
            ip = input("Enter the server IP address (e.g., 127.0.0.1): ").strip()
            if not ip: continue
            
            port_input = input("Enter the server port number (default 8082): ").strip()
            if not port_input.isdigit(): 
                print("Port must be a number.")
                continue

            port = int(port_input)
            if not (0 < port < 65536):
                print("Port must be in range 1–65535.")
                continue

            return (ip, port)

        except KeyboardInterrupt:
            print("\nUser interrupted input. Exiting.")
            sys.exit(1)


def main():
    # --- 1) Determinazione indirizzo server e configurazione ---
    TIMEOUT_SECONDS = 5
    
    if len(sys.argv) == 3:
        server_ip = sys.argv[1]
        try:
            server_port = int(sys.argv[2])
            if not (0 < server_port < 65536): raise ValueError
            server_address = (server_ip, server_port)
        except ValueError:
            print("Invalid port number in arguments. Using interactive mode.")
            server_address = get_server_address()
    else:
        server_address = get_server_address()

    # --- 2) Caricamento del file cifrato da inviare ---
    CIPHER_FILE = "cipher.bin"
    try:
        with open(CIPHER_FILE, "rb") as f:
            encrypted_data = f.read()
    except FileNotFoundError:
        print(f"Error: '{CIPHER_FILE}' not found.")
        print("Run './generate_cipher.sh' first to create the encrypted file.")
        return
    
    # --- 3) Connessione e Invio ---
    try:
        # Crea connessione con timeout
        with socket.create_connection(server_address, timeout=TIMEOUT_SECONDS) as sock:
            print(f"Connected to server {server_address[0]}:{server_address[1]}")

            sock.sendall(encrypted_data)
            print(f"File '{CIPHER_FILE}' sent to the server (len={len(encrypted_data)} bytes).")

            # --- 4) Ricezione del plaintext dal server ---
            decrypted_data = b""
            while True:
                part = sock.recv(4096)
                if not part:
                    # EOF TCP: il server ha chiuso la connessione.
                    break
                decrypted_data += part

            print("Decrypted file received from the server.")

            # --- 5) Persistenza su disco del risultato ---
            DECRYPTED_OUT = "plainD_received.txt" 
            with open(DECRYPTED_OUT, "wb") as f:
                f.write(decrypted_data)
            print(f"File '{DECRYPTED_OUT}' saved locally. ({len(decrypted_data)} bytes)")

    # --- Gestione delle eccezioni di rete ---
    except ConnectionRefusedError:
        print("Error: Connection refused. Is the server running on the specified port?")
    except TimeoutError:
        print(f"Error: Connection timed out after {TIMEOUT_SECONDS}s. Check server availability.")
    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
    except Exception as e:
        print(f"Error during connection or data transfer: {e}")


if __name__ == "__main__":
    main()
