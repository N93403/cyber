#Questo file utilizza socketserver.ThreadingTCPServer per gestire più client in modo concorrente.
#!/usr/bin/env python3
# server.py - Server di ascolto e gestione connessioni didattico

import socketserver
import threading
import sys

# Lista globale per tenere traccia dei socket dei client connessi per il broadcast
client_list = []

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        """Metodo eseguito quando un nuovo client si connette."""
        client_ip = self.client_address[0]
        thread_name = threading.current_thread().name
        print(f"[{thread_name}] Connessione da: {client_ip}")
        # Aggiunge il socket del client alla lista globale
        client_list.append(self.request) 

        try:
            # Ciclo di ricezione continua
            while True:
                data = self.request.recv(1024)
                if not data:
                    break
                
                message = data.decode('utf-8')
                full_message = f"[{client_ip}] dice: {message}"
                print(full_message)
                
                # Invia il messaggio a tutti gli altri client
                self.broadcast(full_message, self.request)

        except ConnectionResetError:
            print(f"[{thread_name}] Connessione interrotta bruscamente da {client_ip}.")
        except Exception as e:
            # Gestisce altri errori di socket
            print(f"[{thread_name}] Errore imprevisto: {e}")
        finally:
            # Assicura la pulizia all'uscita
            if self.request in client_list:
                client_list.remove(self.request)
            print(f"[{thread_name}] Connessione chiusa con: {client_ip}")

    def broadcast(self, message: str, sender_socket):
        """Invia un messaggio a tutti i client tranne il mittente."""
        encoded_message = message.encode('utf-8')
        # Si usa una copia della lista per evitare problemi di concorrenza
        for client_socket in list(client_list):
            if client_socket is not sender_socket:
                try:
                    client_socket.sendall(encoded_message)
                except:
                    # Rimuove i socket che non rispondono (client disconnessi)
                    if client_socket in client_list:
                        client_list.remove(client_socket)

def main():
    HOST, PORT = "0.0.0.0", 8000
    # Permette il riutilizzo dell'indirizzo e porta subito dopo la chiusura
    socketserver.ThreadingTCPServer.allow_reuse_address = True

    try:
        # Crea il server in ascolto
        with socketserver.ThreadingTCPServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
            print(f"Server di Chat Didattica in ascolto su {HOST}:{PORT}")
            print("Premi CTRL+C per terminare il server.")
            # Avvia il server, gestendo ogni client in un thread separato
            server.serve_forever() 
    except KeyboardInterrupt:
        print("\nInterruzione richiesta. Server arrestato.")
    except Exception as e:
        print(f"Errore critico all'avvio: {e}")

if __name__ == "__main__":
    main()
