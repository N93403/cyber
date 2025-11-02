# 🧠 Teoria della Vulnerabilità Heartbleed (CVE-2014-0160)

## Cos'è Heartbleed?

**Heartbleed** è una vulnerabilità critica scoperta nel 2014 che affliggeva l'implementazione del protocollo Heartbeat in OpenSSL. Questa falla di sicurezza permette a un attaccante di leggere la memoria del server senza autenticazione, potenzialmente esponendo informazioni sensibili.

### Dati Chiave
- **CVE**: CVE-2014-0160
- **Data Scoperta**: Aprile 2014
- **Versioni Affette**: OpenSSL 1.0.1 - 1.0.1f
- **Tipo**: Buffer Over-read
- **Impatto**: Lettura memoria del server

## Il Protocollo Heartbeat

### Scopo Legittimo
Il protocollo Heartbeat è parte dello standard TLS/SSL e serve per:
- ✅ **Mantenere connessioni attive** durante periodi di inattività
- ✅ **Verificare che il peer sia online** senza dover rinegoziare la connessione
- ✅ **Prevenire timeout** in connessioni di lunga durata

### Funzionamento Normale
