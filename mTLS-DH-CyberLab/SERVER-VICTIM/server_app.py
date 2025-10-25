#!/usr/bin/env python3
"""
Server mTLS (Autenticazione Mutua TLS) per il progetto CyberLab.
Ascolta sull'IP della VM Vittima (10.0.2.15) e richiede il certificato del Client.
"""
import socket
import ssl
import sys
import os

# === CONFIGURAZIONE ===
PORT = 4433
BUFFER_SIZE = 1024

# Percorsi ai file chiave e certificati (relativi alla cartella SERVER-VICTIM)
CA_CERT_FILE = 'server_keys/ca_cert.pem'
SERVER_CERT_FILE = 'server_keys/server_cert.pem'
SERVER_KEY_FILE = 'server_keys/server_key.pem'

def avvia_server(server_host):
    """Avvia il server e gestisce l'handshake mTLS e la comunicazione."""
    print(f"Server mTLS in ascolto su {server_host}:{PORT}...")

    # 1. Creazione del Contesto SSL
    # ssl.Purpose.CLIENT_AUTH specifica che il server deve verificare l'identità del client.
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    # Carica la propria chiave e certificato
    try:
        context.load_cert_chain(certfile=SERVER_CERT_FILE, keyfile=SERVER_KEY_FILE)
    except FileNotFoundError as e:
        print(f"ERRORE: File chiave/certificato non trovato. Esegui 'generate_certs.py'. Dettaglio: {e}")
        sys.exit(1)
        
    # Carica il certificato della CA per verificare il certificato del client
    context.load_verify_locations(cafile=CA_CERT_FILE)
    
    # 2. Abilitazione dell'Autenticazione Mutua (mTLS)
    # RICHIESTO: Il server terminerà l'handshake se il client non presenta un certificato valido.
    context.verify_mode = ssl.CERT_REQUIRED
    
    # Configurazioni di sicurezza aggiuntive (opzionale ma raccomandato)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

    # 3. Avvio del Socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((server_host, PORT))
        sock.listen(5)
        
        while True:
            try:
                # Accetta la connessione TCP
                conn, addr = sock.accept()
                print(f"Connessione TCP da: {addr}")
                
                # Wrap del socket con il contesto SSL
                with context.wrap_socket(conn, server_side=True) as ssock:
                    print("Handshake mTLS completato con successo.")
                    
                    # Verifica l'identità del client dal suo certificato
                    client_cert = ssock.getpeercert()
                    if client_cert:
                        subject = dict(x[0] for x in client_cert['subject'])
                        common_name = subject.get('commonName')
                        print(f"CLIENT AUTENTICATO (CN): {common_name}")
                    
                    # Logica di comunicazione
                    data = ssock.recv(BUFFER_SIZE)
                    if data:
                        message = data.decode()
                        print(f"Ricevuto dal Client: {message}")
                        
                        # Risposta
                        response = f"SERVER OK: Messaggio '{message.upper()}' ricevuto e autenticato."
                        ssock.sendall(response.encode())
                        
            except ssl.SSLError as e:
                # Gestisce errori di handshake (es. client senza certificato)
                print(f"ERRORE SSL (Connessione Rifiutata per mTLS): {e}")
            except Exception as e:
                print(f"Errore generico durante la comunicazione: {e}")


if __name__ == '__main__':
    # Nello scenario, l'host del server è 10.0.2.15
    host = '10.0.2.15' 
    if len(sys.argv) > 1:
        # Permette di sovrascrivere l'IP dalla riga di comando
        host = sys.argv[1] 
    
    avvia_server(host)
