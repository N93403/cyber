#!/usr/bin/env python3
"""
Client mTLS (Autenticazione Mutua TLS) per il progetto CyberLab.
Si connette alla VM Vittima (10.0.2.15), presenta il proprio certificato e verifica il server.
"""
import socket
import ssl
import sys
import os

# === CONFIGURAZIONE ===
PORT = 4433
BUFFER_SIZE = 1024

# Percorsi ai file chiave e certificati (relativi alla cartella CLIENT-LINUX-MX)
CA_CERT_FILE = 'client_keys/ca_cert.pem'
CLIENT_CERT_FILE = 'client_keys/client_cert.pem'
CLIENT_KEY_FILE = 'client_keys/client_key.pem'

def avvia_client(server_host):
    """Avvia il client, esegue l'handshake mTLS e comunica con il server."""
    print(f"Connessione al Server mTLS su {server_host}:{PORT}...")

    # 1. Creazione del Contesto SSL
    # ssl.PROTOCOL_TLS_CLIENT è appropriato per il client.
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

    # Carica la propria chiave e certificato (da presentare al server)
    try:
        context.load_cert_chain(certfile=CLIENT_CERT_FILE, keyfile=CLIENT_KEY_FILE)
    except FileNotFoundError as e:
        print(f"ERRORE: File chiave/certificato non trovato. Dettaglio: {e}")
        sys.exit(1)
    
    # Carica il certificato della CA per verificare il certificato del server
    context.load_verify_locations(cafile=CA_CERT_FILE)
    
    # 2. Verifica del Server (già impostata di default, ma esplicitata)
    context.verify_mode = ssl.CERT_REQUIRED
    
    # Configurazioni di sicurezza aggiuntive
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

    # 3. Avvio della Connessione
    try:
        # socket.create_connection tenta la connessione TCP
        with socket.create_connection((server_host, PORT)) as sock:
            # Wrap del socket con il contesto SSL (avvia l'handshake)
            with context.wrap_socket(sock, server_side=False, server_hostname=server_host) as ssock:
                print(f"Connessione TLS stabilita. Versione: {ssock.version()}")
                
                # A questo punto, sia il Server che il Client si sono autenticati (mTLS)

                # Logica di comunicazione
                message = "Hello Server from Client Linux MX!"
                print(f"Invio: '{message}'")
                ssock.sendall(message.encode())
                
                # Ricezione della risposta
                data = ssock.recv(BUFFER_SIZE)
                print(f"Ricevuto dal Server: {data.decode()}")

    except ssl.SSLError as e:
        # Gestisce errori di handshake (es. server con certificato non valido o non richiesto)
        print(f"ERRORE SSL (Connessione Rifiutata): Impossibile stabilire mTLS. Dettaglio: {e}")
    except ConnectionRefusedError:
        print(f"Connessione rifiutata. Server non attivo o firewall.")
    except Exception as e:
        print(f"Errore generico: {e}")


if __name__ == '__main__':
    # Nello scenario, l'host del server è 10.0.2.15
    server_ip = '10.0.2.15'
    if len(sys.argv) > 1:
        # Permette di specificare l'IP del server da riga di comando
        server_ip = sys.argv[1] 
    
    avvia_client(server_ip)
