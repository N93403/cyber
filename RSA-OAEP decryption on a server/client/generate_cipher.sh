#!/bin/bash
# Script per generare il file cifrato necessario per testare il server.
# Simula l'operazione di cifratura che il client farebbe in un ambiente reale (usando la chiave pubblica).

# --- PREREQUISITI ---
# Per eseguire questo script, devi copiare la chiave privata nella cartella client
# in modo che OpenSSL possa estrarre la chiave pubblica necessaria per cifrare.
# Rimuovi la chiave privata dopo l'esecuzione per mantenere la sicurezza.

PRIVATE_KEY="../server/pub_priv_pair.key" # Assumiamo che la chiave sia nella cartella server
PUBLIC_KEY="public_key.pem"
INPUT_FILE="plaintext_in.txt"
OUTPUT_FILE="cipher.bin"

if [ ! -f "$PRIVATE_KEY" ]; then
    echo "ERRORE: Chiave privata non trovata nel percorso atteso: $PRIVATE_KEY"
    echo "Assicurati di avviare il progetto dalla cartella principale o di copiare il file."
    exit 1
fi

echo "--- Generazione del file cifrato RSA-OAEP ---"

# 1. Estrae la chiave pubblica (che sarebbe l'unica posseduta dal mittente in un contesto reale)
echo "1. Estrazione della chiave pubblica in $PUBLIC_KEY..."
openssl rsa -in "$PRIVATE_KEY" -pubout -out "$PUBLIC_KEY"

# 2. Cifra il file di input con la chiave pubblica, usando padding OAEP
echo "2. Cifratura di '$INPUT_FILE' in '$OUTPUT_FILE' (Padding: OAEP)..."
openssl pkeyutl -encrypt \
    -in "$INPUT_FILE" \
    -pubin \
    -inkey "$PUBLIC_KEY" \
    -out "$OUTPUT_FILE" \
    -pkeyopt rsa_padding_mode:oaep

if [ $? -eq 0 ]; then
    echo "SUCCESSO: File cifrato '$OUTPUT_FILE' creato. Pronto per l'invio."
    # Pulizia: rimuovi la chiave pubblica estratta
    rm "$PUBLIC_KEY"
else
    echo "ERRORE: Cifratura fallita. Controlla l'installazione di OpenSSL e i permessi."
fi
