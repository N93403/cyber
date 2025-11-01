#Questo file Docker specifica l'installazione di una versione di OpenSSL patchata (generalmente la più recente supportata dalla distribuzione).
# Usa una distribuzione moderna e aggiornata
FROM ubuntu:24.04

# Installazione di OpenSSL e Apache2. La versione di OpenSSL installata sarà aggiornata e sicura.
RUN apt-get update && apt-get install -y openssl apache2

# Esporre la porta HTTPS standard
EXPOSE 443

# Comandi per la configurazione del servizio (omessi per brevità)
# CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
