#!/bin/bash

# Script di configurazione rete per laboratorio cybersecurity
# Configura una rete NAT isolata per le VM

echo "🔧 Configurazione Laboratorio Sicurezza"
echo "⚠️  Eseguire solo su host machine con VirtualBox/VMware"

NETWORK_NAME="CybersecurityLab"
SUBNET="192.168.100.0/24"

create_virtual_network() {
    echo "Creazione rete virtuale..."
    
    # Crea host-only network (VirtualBox)
    if command -v VBoxManage &> /dev/null; then
        VBoxManage hostonlyif create
        VBoxManage hostonlyif ipconfig vboxnet0 --ip 192.168.100.1 --netmask 255.255.255.0
        echo "Rete VirtualBox configurata: 192.168.100.0/24"
    fi
    
    # Configurazione per VMware
    if command -v vmnet-cli &> /dev/null; then
        echo "Configura VMware Network Editor per la subnet $SUBNET"
    fi
}

setup_firewall_rules() {
    echo "Configurazione firewall per isolamento..."
    
    # Esempio regole iptables per isolamento
    iptables -A FORWARD -s $SUBNET -d 0.0.0.0/0 -j DROP
    iptables -A FORWARD -d $SUBNET -s 0.0.0.0/0 -j DROP
    
    echo "Rete isolata configurata: $SUBNET"
}

display_vm_configs() {
    echo ""
    echo "🎯 Configurazione VM consigliata:"
    echo "   Kali Linux:      192.168.100.10"
    echo "   Metasploitable:  192.168.100.20"
    echo "   Ubuntu Server:   192.168.100.30"
    echo ""
    echo "📝 Assicurarsi che:"
    echo "   - Tutte le VM siano nella stessa rete NAT"
    echo "   - Il traffico sia isolato da internet"
    echo "   - Snapshot siano creati prima dei test"
}

main() {
    echo "Iniziando configurazione..."
    create_virtual_network
    setup_firewall_rules
    display_vm_configs
    echo "✅ Configurazione completata!"
}

main
