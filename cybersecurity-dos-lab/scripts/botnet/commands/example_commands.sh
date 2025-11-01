#!/bin/bash

# Esempio di comandi che possono essere inviati ai bot
# Questo file mostra il tipo di comandi che il C2 può distribuire

# 1. Comando per raccogliere informazioni di sistema
echo "=== INFORMATIONSYSTEM BOT ==="
echo "Hostname: $(hostname)"
echo "OS: $(uname -a)"
echo "Uptime: $(uptime)"
echo "Current user: $(whoami)"

# 2. Comando per test di connettività
echo ""
echo "=== NETWORK TEST ==="
ping -c 2 192.168.100.20 || echo "Ping failed"

# 3. Comando per stress test limitato
echo ""
echo "=== STRESS TEST ==="
echo "Simulazione carico CPU per 10 secondi..."
timeout 10 stress-ng --cpu 1 --timeout 10 || echo "Stress-ng non installato"

# 4. Comando per raccolta informazioni di rete
echo ""
echo "=== NETWORK INFO ==="
ip addr show || ifconfig 2>/dev/null || echo "Network commands not available"
