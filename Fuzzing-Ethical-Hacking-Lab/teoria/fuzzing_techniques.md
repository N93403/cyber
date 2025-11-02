# Fuzzing Techniques

## 1. Random Fuzzing
- Generazione casuale di input
- Semplice ma inefficiente per spazi di input grandi

## 2. Mutation-based Fuzzing
- Modifica di input esistenti
- Utilizzato da AFL e Spike

## 3. Generation-based Fuzzing
- Creazione di input da specifiche del protocollo
- Più efficace ma complesso da implementare

## 4. Symbolic Execution
- Analisi statica del codice
- Scopre percorsi di esecuzione senza eseguire il programma
