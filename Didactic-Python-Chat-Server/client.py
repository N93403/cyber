#!/usr/bin/env python3
# client.py - Client di connessione e invio messaggi didattico

import socket
import threading
import sys
import os

SERVER_IP = "127.0.0.1" 
SERVER_PORT = 8000

def receive_messages(sock):
    """Funzione che gira in un thread separato per ricevere messaggi dal server."""
    while True:
        try:
            # Riceve i dati dal socket
            data = sock.recv(1024)
            if not data:
                # Se non riceve dati, il server si è disconnesso
                print("\nDisconnesso dal server.")
                os._exit(0) 
            
            # Stampa il messaggio ricevuto e ripristina la richiesta di input
            print(f"\n{data.decode('utf-8')}\n> ", end="", flush=True) 
        except:
            # Interrompe il thread in caso di errore
            break

def start_client():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print(f"Tentativo di connessione a {SERVER_IP}:{SERVER_PORT}...")
            sock.connect((SERVER_IP, SERVER_PORT))
            print("Connessione stabilita. Digita 'exit' o premi Ctrl+C per uscire.")

            # Avvia il thread per la ricezione asincrona
            threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

            # Ciclo principale per l'invio dei messaggi (input utente)
            while True:
                user_input = input("> ")
                if user_input.lower() == 'exit':
                    break
                sock.sendall(user_input.encode('utf-8'))

    except ConnectionRefusedError:
        print(f"Errore: Connessione rifiutata. Il server non è in ascolto su {SERVER_IP}:{SERVER_PORT}.")
    except socket.gaierror:
        print(f"Errore: L'indirizzo IP '{SERVER_IP}' non è valido.")
    except KeyboardInterrupt:
        print("\nClient interrotto dall'utente.")
    finally:
        print("Client terminato.")

if __name__ == "__main__":
    start_client()
