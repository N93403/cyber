# 🐍 Fuzzing di Applicazioni Python con python-afl (American Fuzzy Lop)

Questo progetto dimostra come configurare e utilizzare la libreria `python-afl` per eseguire il fuzzing guidato da copertura (coverage-guided fuzzing) sul codice Python, utilizzando l'efficace motore AFL (American Fuzzy Lop).

Il file `fuzzer_harness.py` è configurato per utilizzare la **Modalità Persistente (Persistent Mode)**, che riduce drasticamente l'overhead di avvio del processo per ogni input, aumentando significativamente la velocità di esecuzione (execs/sec).

## 🚀 Setup e Lancio del Fuzzer

### 1. Prerequisiti

Assicurati di avere `python3` e `python3-venv` installati sul tuo sistema Linux (AFL funziona meglio su Linux).

```bash
sudo apt update
sudo apt install python3-venv python3-dev

 ### 2. Creazione dell'Ambiente Virtuale

# Crea l'ambiente virtuale
python3 -m venv ~/afl-venv

# Attiva l'ambiente
source ~/afl-venv/bin/activate


### 3. Installazione di python-afl

#python-afl deve essere installato all'interno dell'ambiente virtuale.

# python-afl può richiedere cython
pip install cython

# Installa la libreria per il fork server di Python
pip install python-afl

### 4. Preparazione del Seed Corpus

#Il fuzzer ha bisogno di input iniziali validi (chiamati "seed") da mutare.
# Crea i file seed (già inclusi, ma utile saperlo)
# In TestInput/seed_01.txt, inserisci un input valido,
# ad esempio:
# 10 20 30


##5. Avvio del Fuzzing
#Utilizza lo script fuzz.sh per eseguire il fuzzer. Nota: Usiamo py-afl-fuzz fornito dalla libreria python-afl.
chmod +x fuzz.sh
./fuzz.sh

#Una volta avviato, vedrai la schermata di stato di AFL, dove potrai monitorare execs/sec e unique_crashes.
