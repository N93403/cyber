import angr
import sys
import logging

# Disabilita i messaggi di log verobsi di Angr, mantenendo solo i critici
logging.getLogger('angr').setLevel(logging.ERROR)
logging.getLogger('claripy').setLevel(logging.ERROR)
logging.getLogger('simgr').setLevel(logging.ERROR)

# --- CONFIGURAZIONE ---
TARGET_BINARY = 'simple'
PASSWORD_LENGTH = 4 # Lunghezza della password (solo per info, non necessaria per un int)

try:
    # Carica il binario. 'auto_load_libs': False è per performance su binari semplici.
    project = angr.Project(TARGET_BINARY, load_options={'auto_load_libs': False})
except Exception as e:
    print(f"❌ Errore nel caricamento del binario '{TARGET_BINARY}'. Assicurati che esista e sia compilato (usa 'make').")
    print(f"Dettagli: {e}")
    sys.exit(1)


initial_state = project.factory.entry_state()
simulation = project.factory.simgr(initial_state)

# --- DEFINIZIONE DEI CRITERI DI ESPLORAZIONE ---

def is_successful(state):
    """Controlla se lo stato attuale ha raggiunto il percorso di successo."""
    # Controlla l'output standard per la stringa di successo.
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Access Granted' in stdout_output

def should_abort(state):
    """Controlla se lo stato attuale è in un percorso di fallimento."""
    # Controlla l'output standard per la stringa di fallimento.
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Access Denied' in stdout_output

# --- ESECUZIONE SIMBOLICA ---

print(f"Inizio esplorazione simbolica sul binario '{TARGET_BINARY}'...")
print(f"Cercando il percorso che genera l'output: 'Access Granted'")

# explore: esplora i percorsi. find: il criterio di successo. avoid: il criterio di fallimento (path pruning).
simulation.explore(find=is_successful, avoid=should_abort)

# --- ESTRAZIONE DELLA SOLUZIONE ---

if simulation.found:
    solution_state = simulation.found[0]
    print("\n" + "="*30)
    print("✅ Risoluzione completata con successo!")
    
    # Angr risolve il valore simbolico che è stato letto da stdin (file descriptor 0)
    password_bytes = solution_state.posix.dumps(sys.stdin.fileno()).strip()
    
    try:
        # Decodifica l'input (che dovrebbe essere un numero)
        password = password_bytes.decode('utf-8').strip()
        # Converti in intero per pulizia
        final_password = int(password)
        print(f"Password trovata (Concrete Value): {final_password}")
    except ValueError:
        print(f"Attenzione: Impossibile interpretare l'output come intero.")
        print(f"Raw Output (Bytes): {password_bytes}")

    print("="*30)
else:
    print("\n" + "="*30)
    print("❌ Esplorazione fallita. Impossibile trovare un percorso di successo.")
    print("Verifica i vincoli o la compilazione del binario (-m32).")
    print("="*30)
    sys.exit(1)
