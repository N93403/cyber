# SMTP Fuzzing con Spike - Istruzioni

## Prerequisiti
- Kali Linux o distribuzione con Spike installato
- Server SMTP target (es. Metasploitable)
- Connessione di rete tra attaccante e target

## Installazione Spike
```bash
sudo apt update
sudo apt install spike

## Configurazione Target
Verifica connessione:

bash
ping <target_ip>
nmap -p 25 <target_ip>
Test manuale SMTP:

bash
telnet <target_ip> 25
EHLO test
QUIT
## Esecuzione Fuzzing
Metodo 1: Script Python
bash
python fuzzer_spike.py 192.168.1.100 25 0 0
Metodo 2: Comando diretto
bash
generic_web_server_fuzz 192.168.1.100 25 smtp1.spk 0 0
Parametri
skip_variables: Salta le prime N variabili (utile per riprendere sessioni)

skip_strings: Salta le prime N stringhe di mutazione

## Monitoraggio
Traffico di rete:

bash
tcpdump -i eth0 host <target_ip> -w smtp_fuzz.pcap
Log del server (sul target):

bash
tail -f /var/log/mail.log
Analisi Crash
I crash vengono salvati nella directory crashes/

## Riprodurre manualmente con:

bash
nc <target_ip> 25 < crashes/crash_001.txt
Troubleshooting
"Connection refused": Verifica che il servizio SMTP sia attivo

Spike non trovato: Reinstalla spike o verifica il PATH

Nessun crash: Prova a variare i parametri skip_variables/skip_strings
