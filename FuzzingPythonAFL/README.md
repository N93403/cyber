# 🐍 Fuzzing di Applicazioni Python con python-afl (American Fuzzy Lop)

Questo progetto dimostra come configurare e utilizzare la libreria `python-afl` per eseguire il fuzzing guidato da copertura (coverage-guided fuzzing) sul codice Python, utilizzando l'efficace motore AFL (American Fuzzy Lop).

Il file `fuzzer_harness.py` è configurato per utilizzare la **Modalità Persistente (Persistent Mode)**, che riduce drasticamente l'overhead di avvio del processo per ogni input, aumentando significativamente la velocità di esecuzione (execs/sec).

## 🚀 Setup e Lancio del Fuzzer

### 1. Prerequisiti

Assicurati di avere `python3` e `python3-venv` installati sul tuo sistema Linux (AFL funziona meglio su Linux).

```bash
sudo apt update
sudo apt install python3-venv python3-dev
