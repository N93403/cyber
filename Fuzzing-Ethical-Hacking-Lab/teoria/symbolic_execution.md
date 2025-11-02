
### **9. `teoria/symbolic_execution.md`**
```markdown
# Symbolic Execution - Teoria

## Cos'è l'Esecuzione Simbolica?
Tecnica di analisi che esegue un programma usando variabili simboliche invece di valori concreti.

## Concetti Fondamentali

### Variabili Simboliche
- Rappresentano valori sconosciuti
- Esempio: α, β, γ invece di 1, 2, 3
- Permettono di rappresentare multiple esecuzioni

### Vincoli di Percorso (Path Constraints)
- Condizioni che devono essere vere per seguire un percorso
- Esempio: `α > 0 AND β < 5`

### Risolutori (SMT Solvers)
- Strumenti che risolvono vincoli matematici
- Esempi: Z3, CVC4, Boolector

## Implementazione Pratica

### Esempio con Z3 Python
```python
from z3 import *

def symbolic_example():
    # Crea variabili simboliche
    a = BitVec('a', 32)
    b = BitVec('b', 32)
    
    # Crea risolutore
    s = Solver()
    
    # Aggiungi vincoli
    s.add(a > 0)
    s.add(b < 10)
    s.add(a + b == 15)
    
    # Verifica soddisfacibilità
    if s.check() == sat:
        model = s.model()
        print(f"a = {model[a]}, b = {model[b]}")

Applicazioni in Sicurezza
Vulnerability Discovery
Trovare input che triggerano bug

Scoprire condizioni di overflow

Identificare percorsi non raggiungibili

Reverse Engineering
Analisi di binari senza esecuzione

Understanding complex conditions

Deobfuscation

Strumenti Popolari
Angr
Framework per analisi binaria

Supporta esecuzione simbolica

Usabile da Python

KLEE
Symbolic execution engine per C/C++

Basato su LLVM

S2E
Piattaforma di analisi simbolica

Supporta analisi whole-system

Vantaggi e Limiti
Vantaggi
Copertura completa del codice

Scopre vulnerabilità complesse

Non richiede esecuzione reale

Limiti
State explosion problem

Complessità computazionale

Difficile scalare a programmi grandi
