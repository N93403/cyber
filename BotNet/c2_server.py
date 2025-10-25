#Questo file funge da Server di Comando e Controllo, gestendo le connessioni dei bot in modo multi-threaded.
#Il Server C2
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Moduli necessari per la gestione di server TCP con threading
import socketserver 
import threading

# Classe Handler: Gestisce la comunicazione con un singolo client (Bot) in un thread separato
class BotRequestHandler(socketserver.BaseRequestHandler):
    
    # Il metodo handle() viene eseguito all'avvio di ogni nuova connessione
    def handle(self):
        # Ottiene l'IP del client per il logging
        client_ip = self.client_address[0]
        thread_name = threading.current_thread().name
        print(f"[{thread_name}] Connessione ricevuta da: {client_ip} (NUOVO BOT)")
        
        try:
            # Ciclo principale di comunicazione: riceve comandi e invia risposte
            while True:
                # Tenta di ricevere fino a 1024 byte di dati dal client
                data_bytes = self.request.recv(1024)
                
                # Se non si ricevono dati, significa che il client ha chiuso la connessione
                if not data_bytes:
                    break

                # DECODIFICA: Trasforma i byte ricevuti in una stringa UTF-8 e rimuove spazi/newline
                received_message = data_bytes.decode('utf-8').strip()
                print(f"[{thread_name}] Comandato da {client_ip}: '{received_message}'")

                # LOGICA DI CONTROLLO: Simula l'elaborazione di un comando.
                # In questo caso, invia una risposta ECHO in MAIUSCOLO.
                response_message = received_message.upper()

                # CODIFICA: Invia la risposta codificata in byte al client
                self.request.sendall(response_message.encode('utf-8'))

        except ConnectionResetError:
            # Gestisce disconnessioni forzate (es. reset del socket)
            print(f"[{thread_name}] Connessione con {client_ip} interrotta bruscamente.")
        except Exception as e:
            # Gestisce altri errori generici
            print(f"[{thread_name}] Errore di comunicazione con {client_ip}: {e}")
        finally:
            # Chiude la connessione e logga l'evento
            print(f"[{thread_name}] Disconnessione Bot: {client_ip}")


def main():
    # Configurazione di rete del C2 Server
    HOST, PORT = "0.0.0.0", 8000
    # Permette il riutilizzo immediato della porta dopo l'arresto (utile in fase di sviluppo)
    socketserver.ThreadingTCPServer.allow_reuse_address = True

    try:
        # Crea e avvia il server multi-threaded. La clausola 'with' gestisce la chiusura automatica.
        with socketserver.ThreadingTCPServer((HOST, PORT), BotRequestHandler) as server:
            print(f"C2 Server in ascolto su {HOST}:{PORT}")
            print("Server pronto per ricevere connessioni di Bot. Premi CTRL+C per arrestare.")
            # serve_forever() tiene il server attivo in ascolto continuo
            server.serve_forever()
    except KeyboardInterrupt:
        # Gestisce l'interruzione da tastiera (CTRL+C)
        print("\n[C2] Arresto del server richiesto.")
    finally:
        print("[C2] Server terminato.")

if __name__ == "__main__":
    main()
