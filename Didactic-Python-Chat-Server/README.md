# 💬 Didactic-Python-Chat-Server

Un progetto didattico in Python per dimostrare la programmazione di rete (socket TCP/IP) e l'uso del **Threading** per gestire la concorrenza in un'applicazione di chat multi-utente.

## 🌟 Concetti Esplorati

* **Socketserver:** Utilizzo di `socketserver.ThreadingTCPServer` per un server altamente concorrente.
* **Networking TCP:** Implementazione di un protocollo base per l'invio e la ricezione di messaggi su TCP.
* **Threading:** Il client usa un thread separato per la ricezione dei dati per evitare il blocco dell'interfaccia utente durante l'attesa di input (il server usa thread per ogni connessione).
* **Broadcast:** Implementazione di una logica base per inviare i messaggi di un utente a tutti gli altri utenti connessi.

## 🚀 Istruzioni per l'Esecuzione

### Prerequisiti

* Python 3.x

### Esecuzione

Per avviare la chat, seguire i seguenti passi:

1.  **Avvia il Server:** Apri un terminale nella directory del progetto ed esegui:
    ```bash
    python3 server.py
    ```
    Il server si metterà in ascolto sulla porta `8000`.

2.  **Avvia i Client:** Apri una o più altre finestre di terminale ed esegui il client in ciascuna:
    ```bash
    python3 client.py
    ```
    I client si connetteranno a `127.0.0.1:8000`.

Ora puoi digitare messaggi in un client e vederli apparire in tutti gli altri! Digita `exit` o premi `Ctrl+C` per disconnettere un client.
