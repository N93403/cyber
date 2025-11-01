# 🛡️ Angr Simple Crackme: Esecuzione Simbolica (Analisi Concolica)



Questo progetto funge da dimostrazione pratica dell'uso del framework di analisi binaria **Angr** per risolvere un semplice problema di reverse engineering noto come **"crackme."**

L'obiettivo è trovare automaticamente la password (`7857`) analizzando il binario compilato, un processo noto come **Esecuzione Simbolica** (o **Analisi Concolica**).

---

## 💡 Principi di Sicurezza e Analisi

L'analisi con Angr non si basa sul *brute force*, ma sulla **matematica dei vincoli**. Quando lo script `solve.py` esegue il binario, il processo si articola come segue:

* **Input Simbolico:** Angr tratta l'input utente (`x`) come una **variabile simbolica** $X$, non un numero concreto.
* **Generazione di Vincoli:** L'istruzione di controllo `if(x == 7857)` nel codice C viene convertita in un vincolo matematico per il solutore SMT: $X = 7857$.
* **Esplorazione del Percorso (Path Exploration):** Angr utilizza le funzioni `is_successful` e `should_abort` per dirigere l'esplorazione verso l'unico percorso che soddisfa il vincolo e stampa **"Access Granted."**
* **Risoluzione (Constraint Solving):** Il **Solutore SMT (Satisfiability Modulo Theories)** calcola il valore di $X$ che soddisfa il vincolo, rivelando la password: **7857**.

> Questo dimostra che *hardcoding* valori di sicurezza in un binario è una tecnica inefficace, poiché la logica del programma può essere invertita con strumenti di analisi binaria avanzati.

---

## ⚙️ Prerequisiti

Per clonare, compilare ed eseguire questo progetto, sono necessari i seguenti strumenti nel tuo ambiente Linux o macOS:

| Strumento | Scopo | Installazione (Esempio Debian/Ubuntu) |
| :--- | :--- | :--- |
| **Git** | Clonare la repository | `sudo apt install git` |
| **GCC** | Compilatore C | `sudo apt install build-essential` |
| **Python 3** | Eseguire lo script Angr | Generalmente preinstallato |
| **Angr** | Framework di Esecuzione Simbolica | `pip install angr` |

⚠️ **Nota sulla Compilazione (Architettura a 32 bit):** Il `Makefile` utilizza l'opzione `-m32`. Se si verificano errori di compilazione relativi a librerie mancanti (ad esempio, `cannot find -lc`), potrebbe essere necessario installare le librerie a 32-bit: `sudo apt install libc6-dev-i386`.

---

## 🚀 Istruzioni Dettagliate per l'Esecuzione

Esegui tutti i passaggi all'interno della directory del progetto.

### Passo 1: Compilazione del Binario (`make`)

Il `Makefile` compila il sorgente C (`simple.c`) nell'eseguibile **`simple`**, impostando i flag corretti per l'analisi a 32 bit.

```bash
make
Output Atteso:

Compilazione di simple... 
gcc simple.c -o simple -Wall -m32 
Compilazione completata. Binario: simple
Passo 2: Risoluzione con Angr
Esegui lo script Python per avviare l'analisi simbolica. Questo processo risolve il binario e stampa la password risolta.

Bash

python3 solve.py
Output Finale di Successo:

L'output di Angr includerà diversi log di esplorazione, culminando nel risultato finale:

... (Angr log e messaggi di esplorazione) ...

============================== 
✅ Risoluzione completata con successo! 
Password trovata (Concrete Value): 7857
==============================
Passo 3: Pulizia (Facoltativo)
Rimuovi il binario eseguibile simple e i file oggetto generati dalla compilazione.

Bash

make clean


