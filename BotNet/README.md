# C2-Shell-Reverse-Echo: Simulazione di Rete Comando e Controllo (C2) 💻🤖

## 📌 Panoramica del Progetto

Questo progetto didattico implementa un'architettura Client/Server TCP multi-threaded per simulare la comunicazione in una rete di **Comando e Controllo (C2)**, tipica delle Botnet, a scopo di studio.

Il **C2 Server** gestisce le connessioni di più **Bot (Client)** contemporaneamente, eseguendo una semplice funzione di *echo in maiuscolo* come dimostrazione di un comando remoto.

**Tecnologie:** Python 3 (SocketServer, Socket, Threading).

## 💡 Miglioramenti e Caratteristiche

Il codice è stato sviluppato basandosi su un'analisi di script preesistenti, con un focus sull'uniformità e la robustezza:

1.  **Uniformità Python 3:** Entrambi i componenti (`c2_server.py` e `bot_client.py`) sono stati standardizzati in Python 3.
2.  **Gestione Concorrente:** Il server utilizza `ThreadingTCPServer` per accettare e gestire più connessioni di bot in parallelo.
3.  **Comunicazione Affidabile:** Viene gestito l'**encoding** e il **decoding** esplicito (`utf-8`) del traffico per garantire l'integrità dei dati.
4.  **Commenti Dettagliati:** Entrambi i file di codice sono ampiamente commentati per spiegare ogni sezione logica, rendendo il progetto ideale per la dimostrazione di competenze.

## 🛠️ Istruzioni di Esecuzione (Simulazione VM)

Per eseguire il progetto, sono necessarie due Macchine Virtuali (VM) sulla stessa rete.

### 1. Configurazione della Rete (Esempio)

| Ruolo Logico | VM Assegnata | Indirizzo IP | File Eseguito |
| :--- | :--- | :--- | :--- |
| **C2 Server** | VM Router/Gateway | `10.0.2.2` | `c2_server.py` |
| **Bot (Client)** | VM Vittima | `10.0.2.15` | `bot_client.py` |

### 2. Avvio del C2 Server

Sulla VM destinata al server (`10.0.2.2`), avviare lo script.

```bash
python3 c2_server.py
# Output atteso: C2 Server in ascolto su 0.0.0.0:8000
