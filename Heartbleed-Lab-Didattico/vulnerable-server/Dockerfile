#Questo file Docker specifica l'installazione di una versione di OpenSSL *vulnerabile*.
```dockerfile
# Usa una distribuzione Linux di base nota per essere compatibile con le vecchie versioni
FROM ubuntu:14.04

# Istruzioni per installare OpenSSL 1.0.1f (La versione più vulnerabile)
# L'implementazione esatta può richiedere la compilazione manuale da sorgenti d'archivio,
# ma questo Dockerfile serve come segnaposto concettuale per un ambiente di laboratorio.
RUN apt-get update && apt-get install -y openssl apache2

# Esporre la porta HTTPS standard
EXPOSE 443

# Comandi per la configurazione del servizio (omessi per brevità)
# CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
