
### **10. `tools-setup/spike_setup.md`**
```markdown
# Spike Framework Setup

## Introduction
Spike è un framework per fuzzing di protocolli di rete sviluppato da Immunity Inc.

## Installation on Kali Linux

### Method 1: APT Package
```bash
sudo apt update
sudo apt install spike

Method 2: Manual Compilation
bash
# Install dependencies
sudo apt install git build-essential

# Clone and build
git clone https://github.com/guilhermeferreira/spike.git
cd spike
./configure
make
sudo make install
Verifica Installazione
bash
which generic_send_tcp
which generic_web_server_fuzz
Struttura di Spike
File SPK
Script che definiscono il protocollo da fuzzare:

s_string(): Stringa fissa

s_string_variable(): Campo da fuzzare

s_read(): Legge risposta

s_write(): Scrive dati

Tool Principali
generic_send_tcp: Fuzzer TCP generico

generic_web_server_fuzz: Fuzzer per protocolli web

generic_send_udp: Fuzzer UDP

Esempio di Utilizzo
SMTP Fuzzing
bash
generic_web_server_fuzz 192.168.1.100 25 smtp1.spk 0 0
HTTP Fuzzing
bash
generic_web_server_fuzz 192.168.1.100 80 http1.spk 0 0
Creazione Script Personalizzati
Template Base
spike
# Simple SPK template
s_read(); # Read banner
s_string("COMMAND ");
s_string_variable("input");
s_string("\r\n");
s_read(); # Read response
Esempio HTTP
spike
s_string("GET /");
s_string_variable("index.html");
s_string(" HTTP/1.1\r\n");
s_string("Host: ");
s_string_variable("localhost");
s_string("\r\n\r\n");
s_read();
Best Practices
1. Protocol Understanding
Studia il protocollo prima di fuzzare

Usa Wireshark per analizzare il traffico

Testa manualmente prima di automatizzare

2. Script Development
Inizia con comandi base

Aggiungi gradualmente complessità

Testa ogni modifica

3. Monitoring
Usa tcpdump per catturare il traffico

Monitora i log del server target

Salva i crash per analisi successiva

Troubleshooting
Common Issues
"Command not found": Verifica installazione e PATH

"Connection refused": Verifica target e porta

No crashes: Prova diversi script e parametri

Performance Tips
Usa skip_variables per riprendere sessioni lunghe

Monitora l'utilizzo di risorse

Salva periodicamente lo stato
