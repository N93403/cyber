# bot_client.py - Versione Python 3
# Stabilisce la connessione con il C2 Server e funge da "Bot"


import socket
import sys

# Dimensione massima della risposta attesa per evitare overflow
MAX_RESPONSE_SIZE = 4096 

def connect_to_server(server_ip, server_port):
    """Gestisce la connessione e il ciclo di invio/ricezione dei comandi."""
    try:
        # Crea un socket TCP/IP standard
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server_ip, server_port)

        print(f"[BOT] Tentativo di connessione a C2 {server_ip}:{server_port}")
        # Connessione al server
        sock.connect(server_address)
        print("[BOT] Connessione al C2 stabilita.")

        try:
            while True:
                # Richiede all'utente (simulando l'input del Botmaster) il comando
                message = input("INVIA COMANDO: ")

                if message.lower() == 'exit':
                    print("[BOT] Richiesta di chiusura connessione.")
                    break 

                # CODIFICA: Trasforma la stringa (comando) in byte prima di inviare
                sock.sendall(message.encode('utf-8'))

                # RICEZIONE: Si aspetta una singola risposta dal server C2
                data_bytes = sock.recv(MAX_RESPONSE_SIZE)

                # Se non ci sono dati, il C2 ha chiuso la connessione
                if not data_bytes:
                    print("[BOT] Connessione chiusa dal C2 Server.")
                    break 

                # DECODIFICA: I byte ricevuti vengono trasformati in stringa per la visualizzazione
                response_message = data_bytes.decode('utf-8').strip()
                print(f"RISPOSTA C2: {response_message}")

        finally:
            # Assicura che il socket venga chiuso, sia in caso di successo che di errore
            sock.close()
            print("[BOT] Connessione terminata.")

    except Exception as e:
        # Cattura e gestisce gli errori di connessione (es. C2 non raggiungibile)
        print(f"[BOT] Errore critico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Verifica che l'IP del server C2 e la PORTA siano passati come argomenti
    if len(sys.argv) != 3:
        print("Uso: python3 bot_client.py [IP_C2_SERVER] [PORTA]")
        sys.exit(1)

    try:
        # Legge gli argomenti e converte la porta in intero
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
    except ValueError:
        print("Errore: La porta deve essere un numero intero valido.")
        sys.exit(1)

    connect_to_server(server_ip, server_port)
