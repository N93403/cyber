#Questo script automatizza l'esecuzione di py-afl-fuzz, inclusa la variabile d'ambiente cruciale per trattare le eccezioni Python come crash.
#!/bin/bash
# Script per avviare il fuzzer AFL

# Variabile essenziale: dice a python-afl di convertire le eccezioni Python
# (come ZeroDivisionError, IndexError, ecc.) in un segnale che AFL riconosca
# come un crash (SIGUSR1 è il default di py-afl-fuzz).
export PYTHON_AFL_SIGNAL=SIGUSR1

# Rimuovi l'output precedente per un nuovo run pulito (OPZIONALE)
# rm -rf Results/*

echo "Avvio di py-afl-fuzz (Persistent Mode)..."
echo "Controlla la directory Results/ per i risultati (crashes, hangs, queue)."

# Comando per l'avvio del fuzzer:
# -i TestInput/: Directory degli input iniziali (seed corpus)
# -o Results/: Directory di output
# -- : Separatore tra opzioni di AFL e il comando da eseguire
# python3 App/fuzzer_harness.py : Il tuo script Python
py-afl-fuzz -i TestInput/ -o Results/ -- python3 App/fuzzer_harness.py
