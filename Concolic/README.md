# Angr Simple Crackme: Esecuzione Simbolica



Questo progetto dimostra l'uso del framework di analisi binaria **Angr** per risolvere un semplice "crackme" (un programma binario che richiede una password).

Il codice C (`simple.c`) contiene una password hardcoded e lo script Python (`solve.py`) utilizza l'esecuzione simbolica per trovare la password automaticamente, senza eseguire il programma concretamente.

---

## ⚙️ Prerequisiti

Per eseguire questo progetto è necessario avere installato:

1.  **GCC:** Il compilatore C.
2.  **Python 3:** L'ambiente di esecuzione Python.
3.  **Angr:** Il framework di esecuzione simbolica.

Per installare Angr e le sue dipendenze:

```bash
pip install angr
