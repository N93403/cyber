# 🛡️ Heartbleed: Laboratorio Didattico di Sicurezza Difensiva (CVE-2014-0160)

Questo progetto è inteso esclusivamente a scopo **didattico e di laboratorio universitario** per comprendere la vulnerabilità Heartbleed e implementare contromisure. **L'esecuzione di test di vulnerabilità su sistemi non di proprietà è illegale ed eticamente inaccettabile.**

## 🎯 Obiettivo del Laboratorio

L'obiettivo è dimostrare i principi di un attacco di tipo **Buffer Over-Read** e la sua risoluzione attraverso l'analisi di due ambienti:
1.  Un server **vulnerabile** (con OpenSSL 1.0.1f).
2.  Un server **patchato** (con OpenSSL 1.0.1g o superiore).

## 🪓 Analisi della Vulnerabilità (CVE-2014-0160)

Heartbleed è un difetto di divulgazione di memoria nell'estensione **TLS/DTLS Heartbeat** di OpenSSL.

### Il Meccanismo dell'Attacco

Quando un client invia una richiesta Heartbeat, il pacchetto contiene due valori critici:
1.  **Lunghezza del Payload Dichiarata:** Il numero di byte che il server dovrebbe restituire.
2.  **Payload Effettivo (il "ping"):** La stringa di dati inviata.

**Il Difetto:** Il server vulnerabile **non verificava** se la lunghezza dichiarata corrisponesse alla dimensione del payload effettivo. Se la lunghezza dichiarata è **maggiore** del payload inviato (ad esempio, 16384 byte dichiarati, 3 byte inviati), il server alloca un buffer di 16384 byte e lo riempie con:
* Il payload di 3 byte.
* **I successivi 16381 byte di memoria del server.**

Questa porzione di memoria non correlata è la "sanguinazione" (bleed) che può contenere chiavi private, credenziali di sessione o dati utente.

## 🛠️ Istruzioni per il Setup (Docker)

### Fase 1: Server Vulnerabile

Naviga in `vulnerable-server/` e costruisci l'immagine. Questa configurazione simula un server OpenSSL non patchato.

```bash
cd vulnerable-server
docker build -t heartbleed-vulnerable .
docker run -d -p 8443:443 --name vulnerable heartbleed-vulnerable


### Fase 2: Server Patchato
Naviga in patched-server/ e costruisci l'immagine. Questa configurazione utilizza una versione di OpenSSL che include la patch.

cd patched-server
docker build -t heartbleed-patched .
docker run -d -p 8444:443 --name patched heartbleed-patched


🔬 Attività di Laboratorio
Test di Verifica: Utilizzare uno strumento di verifica della vulnerabilità su localhost:8443 e localhost:8444.

Analisi Forense di Rete: Utilizzare Wireshark o tcpdump per catturare il traffico durante il test di verifica.


Identificare la Heartbeat Request: Notare il campo di lunghezza (ad esempio, 0x4000 o 16384) nell'intestazione del pacchetto Heartbeat.

Confronto delle Risposte:

Server vulnerabile: Risponde con un pacchetto Heartbeat Response (Tipo 24) contenente una grande quantità di dati inutili.

Server patchato: Risponde con un Alert (Tipo 21) o chiude la connessione, rifiutando la richiesta malformata.

Analisi del Memory Dump: In caso di esecuzione riuscita, analizzare i dati estratti (ad esempio, un file come dump.bin o l'output grezzo) per identificare frammenti di informazioni sensibili, come:

Chiavi di sessione TLS.

Header HTTP/SOAP (es. la richiesta per /etc/passwd visibile nel dump di memoria ).
