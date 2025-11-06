# 🔐 Analisi Encoder 

## Descrizione
Progetto dimostrativo per l'analisi delle tecniche di encoding in cybersecurity. Questo repository mostra come diversi encoder modificano la firma dei payload mantenendone la funzionalità.

## Struttura del Progetto
Encoder Analizzati
Base64: Encoding semplice per evasion basica

Shikata Ga Nai: Encoder polimorfico avanzato

Multi-Encoding: Combinazione di più encoder

XOR Custom: Encoder personalizzato dimostrativo

## Quick Start
```bash
# Clona il repository
git clone https://github.com/your-username/encoder-analysis-example.git
cd encoder-analysis-example

# Esegui il setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# Genera i payload
./scripts/generate_payloads.sh

# Esegui l'analisi
python3 scripts/analysis_tool.py
