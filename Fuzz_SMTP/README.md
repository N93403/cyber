# 📧 Progetto: SMTP Fuzzing con Spike

Questo repository contiene uno script di fuzzing (test di robustezza) per il protocollo **SMTP (Simple Mail Transfer Protocol)**, utilizzando il framework **Spike**. Lo scopo è identificare potenziali vulnerabilità di gestione dell'input (come buffer overflow o crash) nel software di un server di posta.

**⚠️ Disclaimer Legale:** L'uso di strumenti di fuzzing e penetration testing è legale solo contro sistemi di cui si è proprietari o per i quali si ha un'esplicita autorizzazione scritta. L'uso non autorizzato contro sistemi esterni è illegale e non etico.

---

## 1. 📄 Script di Fuzzing (`scripts/smtp1.spk`)

Lo script `smtp1.spk` definisce la sequenza di comunicazione SMTP standard e identifica i punti specifici in cui il fuzzer Spike deve iniettare i suoi payload mutati.

**Contenuto completo in `scripts/smtp1.spk`.**

```c
// smtp1.spk - esempio didattico (non reale, adattalo se necessario)

/* Connessione: Spike apre la connessione TCP e attende il banner SMTP */
s_read(); // legge il banner del server (220 ...)

/* Invia HELO/EHLO: qui definiamo un campo stringa fuzzabile */
s_write("EHLO ");
STR("HOSTNAME"); // <--- Punto di Fuzzing #1: Nome Host
s_write("\r\n");
s_read(); // legge la risposta del server

/* MAIL FROM: campo email - altro punto di fuzzing */
s_write("MAIL FROM:<");
STR("<attacker@example.com>"); // <--- Punto di Fuzzing #2: Indirizzo Mittente
s_write(">\r\n");
s_read();

/* RCPT TO: */
s_write("RCPT TO:<");
STR("victim@example.com"); // <--- Punto di Fuzzing #3: Indirizzo Destinatario
s_write(">\r\n");
s_read();

/* DATA: invia body, possibile fuzzing di payload multilinea */
s_write("DATA\r\n");
s_read();
s_write("Subject: Test\r\n\r\n");
STR("Corpo del messaggio con possibili payload di fuzzing...\r\n"); // <--- Punto di Fuzzing #4: Corpo Messaggio
s_write("\r\n.\r\n");
s_read();

/* QUIT e chiusura */
s_write("QUIT\r\n");
s_close();
