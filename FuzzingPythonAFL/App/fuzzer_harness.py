#Questo file è l'harness di fuzzing. È stato modificato per utilizzare afl.loop() per il Persistent Mode, che è essenziale per massimizzare le prestazioni.
#!/usr/bin/env python3
"""
Harness di fuzzing per AFL (American Fuzzy Lop) e python-afl.
Implementa la modalità 'Persistent Fuzzing' per massime prestazioni.
"""
import sys
import os
import afl
from typing import List

# -------------------------------------------------------------
# 🎯 Funzione di Test (Il codice da fuzzare)
# -------------------------------------------------------------
# Sostituisci il corpo di questa funzione con il tuo codice reale.
# Una funzione ideale dovrebbe contenere la logica complessa e
# sollevare eccezioni in caso di bug/errore.
def test_target(values: List[int]) -> None:
    """
    Simula una funzione complessa che gestisce una lista di interi.
    Esempio di bug: Divisione per zero se il primo elemento è 0.
    """
    if not values:
        return

    # Esempio di logica con un potenziale bug:
    a = values[0]
    
    # 🚨 POTENZIALE CRASH/BUG: Accesso fuori bound se la lista è troppo corta
    # AFL troverà questo se genera un input con meno di 5 elementi.
    if len(values) < 5 and a > 100:
        # Questo solleverà un IndexError o TypeError se l'input non è come previsto.
        # Un IndexError è un crash che AFL rileverà.
        print(f"DEBUG: Elemento 5: {values[4]}") 

    # Esempio di eccezione:
    if a == 0:
        # Se AFL genera '0' come primo elemento, solleveremo un'eccezione
        # che simula un errore logico (Divisione per zero, in questo caso).
        # AFL registrerà questo come un "crash" grazie a PYTHON_AFL_SIGNAL.
        result = 1000 / a # Bug simulato

# -------------------------------------------------------------
# 🔄 Logica del Fuzzer (Persistent Mode)
# -------------------------------------------------------------
def main() -> None:
    # ⚠️ afl.init() non viene usato nel Persistent Mode. Usiamo afl.loop().
    
    # Ciclo persistente: processa N input (qui 1000) prima di riavviare
    # AFL utilizzerà questo ciclo per iniettare i nuovi input in modo efficiente.
    # N.B.: 1000 è un valore tipico, puoi aumentarlo o diminuirlo.
    while afl.loop(1000):
        try:
            # 1. Leggi l'input (il file generato da AFL)
            # Leggere in modo binario è spesso più robusto con python-afl
            in_bytes = sys.stdin.buffer.read()
            if not in_bytes:
                continue

            # 2. Decodifica e Parsing
            try:
                # Prova a decodificare l'input in stringa e splittare
                in_str = in_bytes.decode('utf-8', errors='ignore')
                tokens = in_str.strip().split()
            except Exception:
                # Gestisci problemi di decodifica
                continue

            # 3. Conversione (Parsing robusto per il fuzzing)
            values: List[int] = []
            for t in tokens:
                try:
                    # Tenta la conversione in intero
                    values.append(int(t))
                except ValueError:
                    # Ignora token non interi (utile per non far crashare il fuzzer
                    # con input malformati, ma farli passare alla funzione di test)
                    pass

            if not values:
                continue

            # 4. Chiama la funzione di test con l'input processato
            test_target(values)

        except Exception as e:
            # AFL tratterà le eccezioni Python non gestite (come ValueError, IndexError, 
            # ZeroDivisionError, ecc.) come crash, se l'ambiente è configurato correttamente.
            # Qui non facciamo nulla, lasciamo che AFL gestisca il segnale di crash.
            pass


if __name__ == "__main__":
    main()
    # Esci "pulitamente" per AFL
    os._exit(0)
