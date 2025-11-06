# 🎓 Guida Tecnica - Analisi Encoder

## Panoramica Tecnica

### Architettura del Sistema

Input Payload → Encoder → Payload Codificato → Decoder → Esecuzione


### Metriche di Analisi

#### 1. Entropia di Shannon
- **Formula**: H(X) = -Σ p(x) log₂ p(x)
- **Scopo**: Misura la casualità dei dati
- **Interpretazione**:
  - Entropia alta → Dati casuali → Buon encoding
  - Entropia bassa → Pattern riconoscibili → Encoding debole

#### 2. Distribuzione Byte
- **Byte nulli (0x00)**: Comuni in padding
- **ASCII stampabile**: Text-based encoding
- **Byte di controllo**: Headers e metadata
- **Byte alti**: Dati binari/compressi

#### 3. Efficacia Encoding

Efficacia = ΔEntropia / ΔDimensioni


## Encoder Implementati

### Base64 Encoding
```python
# Esempio implementativo
import base64

def base64_encode(data):
    return base64.b64encode(data)

Shikata Ga Nai
Tipo: Polimorfico

Tecnica: XOR + ADD/SUB

Iterazioni: 1-5 raccomandate

XOR Personalizzato

def xor_encode(data, key):
    return bytes(b ^ key for b in data)

Strumenti di Analisi
Comandi Utili

# Analisi esadecimale
xxd payload.elf | head -20

# Tipo file
file payload.elf

# Entropia
ent payload.elf

# Hash
sha256sum payload.elf

Interpretazione Risultati
Scenario Ideale
ΔEntropia: > 0.5

ΔDimensioni: < 50%

Distribuzione: Uniforme

Scenario Critico
ΔEntropia: < 0.1

ΔDimensioni: > 100%

Distribuzione: Picchi anomali

Esempi Pratici
1. Analisi Comparativa

# Genera payload
./scripts/generate_payloads.sh

# Analizza
python3 scripts/analysis_tool.py

# Visualizza risultati
cat results/analysis_report.txt

2. Encoder Personalizzato

python3 scripts/custom_xor_encoder.py \
  -i payloads/original.elf \
  -o payloads/custom.elf \
  -k 0x42 \
  --generate-decoder

Troubleshooting
Problemi Comuni
Payload non generati
Verifica installazione Metasploit

Controlla permessi esecuzione

Verifica spazio disco

Errori Python
Installa dipendenze: pip3 install -r requirements.txt

Verifica versione Python (≥ 3.6)

Analisi fallita
Verifica esistenza file .elf

Controlla permessi lettura

Verifica formato file

Risorse Aggiuntive
Documentazione
Metasploit Encoders

Entropia in Cybersecurity

Strumenti Correlati
PEiD: Rilevamento packer

Detect It Easy: Analisi file

Binwalk: Analisi firmware

Best Practices
Sviluppo
Commenta sempre il codice

Gestisci eccezioni

Logga le operazioni

Testa edge cases

Sicurezza
Usa ambienti isolati

Non condividere payload reali

Respecta le licenze

Solo uso educativo


### **8. examples/quick_demo.py**
```python
#!/usr/bin/env python3
"""
DEMO RAPIDA - ANALISI ENCODER
Esempio minimale per dimostrazione concetti base
"""

import os
import hashlib
from collections import Counter
import math

def simple_entropy(data):
    """Calcola entropia semplice"""
    if not data:
        return 0
    
    counter = Counter(data)
    entropy = 0
    
    for count in counter.values():
        p = count / len(data)
        entropy -= p * math.log2(p)
    
    return entropy

def xor_encoder(data, key=0xAA):
    """Encoder XOR semplice"""
    return bytes(b ^ key for b in data)

def analyze_sample():
    """Analizza esempio semplice"""
    print("🎯 DEMO RAPIDA - CONCETTI BASE ENCODER")
    print("=" * 50)
    
    # Dati di esempio
    original_data = b"A" * 100  # Dati con bassa entropia
    key = 0x42
    
    print("📊 DATI ORIGINALI:")
    print(f"   Dimensione: {len(original_data)} bytes")
    print(f"   Entropia: {simple_entropy(original_data):.4f}")
    print(f"   Anteprima: {original_data[:20].hex()}")
    
    # Codifica
    encoded_data = xor_encoder(original_data, key)
    
    print("\n🔒 DATI CODIFICATI:")
    print(f"   Dimensione: {len(encoded_data)} bytes")
    print(f"   Entropia: {simple_entropy(encoded_data):.4f}") 
    print(f"   Anteprima: {encoded_data[:20].hex()}")
    
    print(f"\n📈 RISULTATI:")
    print(f"   Δ Entropia: {simple_entropy(encoded_data) - simple_entropy(original_data):+.4f}")
    print(f"   Δ Dimensioni: {len(encoded_data) - len(original_data):+d} bytes")
    
    # Verifica decodifica
    decoded_data = xor_encoder(encoded_data, key)
    print(f"   Decodifica corretta: {original_data == decoded_data}")

if __name__ == "__main__":
    analyze_sample()
