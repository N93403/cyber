# 🏗️ Esercizio 1: Configurazione Ambiente Base

## Obiettivi di Apprendimento
- Configurare due VM Kali Linux per testing
- Stabilire connettività di rete
- Verifica ambiente di lavoro

## 📋 Scenario
Sei un penetration tester che deve preparare l'ambiente per un assessment OSINT. Hai due VM Kali Linux da configurare come Attaccante e Target.

## 🛠️ Attività Richieste

### Task 1: Configurazione VM Attaccante
```bash
# 1. Aggiorna il sistema
sudo apt update && sudo apt upgrade -y

# 2. Installa dipendenze base
sudo apt install -y git curl wget python3 python3-pip

# 3. Clona il repository
git clone https://github.com/tuo-username/discover-osint-penetration-test.git
cd discover-osint-penetration-test

# 4. Esegui setup automatico
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh --role attacker
