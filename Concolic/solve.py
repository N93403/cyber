import angr
import sys

# Carica il binario 'simple'. 'auto_load_libs': False velocizza per binari piccoli.
project = angr.Project('simple', load_options={'auto_load_libs': False})
initial_state = project.factory.entry_state()
simulation = project.factory.simgr(initial_state)

# Funzione che definisce il successo
def is_successful(state):
    # Cerca la stringa 'Access Granted' nell'output standard del programma simulato
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Access Granted' in stdout_output

# Funzione che definisce il fallimento (da evitare)
def should_abort(state):
    # Cerca la stringa 'Access Denied' nell'output standard
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Access Denied' in stdout_output

# Inizia l'esplorazione simbolica
print("Inizio esplorazione...")
# find: il percorso da trovare; avoid: i percorsi da scartare per efficienza
simulation.explore(find=is_successful, avoid=should_abort)

# Estrai e stampa la soluzione
if simulation.found:
    solution_state = simulation.found[0]
    print("\n✅ Trovata la soluzione!")

    # Chiede ad Angr di concretizzare il valore simbolico che è stato fornito a stdin
    password_bytes = solution_state.posix.dumps(sys.stdin.fileno()).strip()
    
    try:
        # Tenta di decodificare e convertire in intero (il formato previsto)
        password = int(password_bytes.decode('utf-8').strip())
    except:
        password = f"Raw bytes: {password_bytes}"

    print(f"Password trovata: {password}")
else:
    print("\n❌ Impossibile trovare la password.")
    # Si raccomanda di verificare la corretta compilazione con -m32
    sys.exit(1)
