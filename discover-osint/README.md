# Discover OSINT 

Una dimostrazione completa dell'utilizzo del framework Discover per operazioni OSINT (Open Source Intelligence) nella penetration testing.

## 📋 Descrizione

Questo progetto dimostra l'uso di Discover per:
- Scansione OSINT passiva di domini
- Enumerazione di sottodomini
- Raccolta di informazioni da fonti pubbliche
- Generazione di report automatizzati



# Esegui lo script di setup
chmod +x scripts/setup.sh
./scripts/setup.sh

VM1 (Attacker) ────┐
                   ├── Network Lab ───► Internet (Opzionale)
VM2 (Target) ─────┘


Step 2: Configura VM Attaccante
bash# Esegui lo script di setup
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh --role attacker

# Verifica installazione
cd discover
./discover.sh
Step 3: Configura VM Target
bash# Sulla VM target
./scripts/setup_environment.sh --role target --domain techsolutions.local

# Verifica servizi
sudo systemctl status apache2
curl http://techsolutions.local
Step 4: Configurazione Avanzata (Opzionale)
API Keys per Migliori Risultati
bash# Copia il template
cp config/api-keys-template.yaml ~/.theHarvester/api-keys.yaml

# Modifica con le tue API keys
nano ~/.theHarvester/api-keys.yaml
Configurazione Discover Personalizzata
bashcp config/discover-config.example ~/discover/local-config.sh
nano ~/discover/local-config.sh
🔧 Verifica Installazione
Test Completamento
bash# Verifica strumenti installati
which dnsrecon
which theharvester
which subfinder
which nmap

# Verifica Discover
cd discover
./discover.sh --help
Troubleshooting Comune
Problema: Script non eseguibile
bashchmod +x scripts/*.sh
Problema: Dipendenze mancanti
bashsudo apt update
sudo apt install git python3 python3-pip
Problema: Permessi insufficienti
bash# Non eseguire come root
exit
# Ricollegati come utente normale
🎯 Configurazione di Rete
Scenario Raccomandato
textVM Attaccante (192.168.1.100) ↔ VM Target (192.168.1.101)
Verifica Connettività
bash# Dalla VM attaccante
ping -c 3 192.168.1.101
nmap -sn 192.168.1.0/24
📊 Post-Installazione
Struttura Directory Creata
text~/discover/                    # Framework principale
~/penetration-test-results/    # Risultati scansioni
~/.theHarvester/              # Configurazione theHarvester
