# Introduzione
Internet agli albori trasmetteva dati in chiaro (HTTP).  
Con HTTPS, i dati sono cifrati e leggibili solo da client e server.  
Questo laboratorio mostra come un attaccante può inserirsi nel mezzo (MITM) e perché le difese moderne sono fondamentali.

# Setup del laboratorio
- Creare 3 VM con VirtualBox o Vagrant
- Configurare rete interna (NAT o Host-only)
- Installare:
  - Kali Linux (attaccante)
  - Windows/Linux minimale (vittima)
  - Linux minimale (router)

## Topologia di rete
[Victim 10.0.2.15] <---> [Attacker 10.0.2.100] <---> [Router 10.0.2.2] <---> Internet

# Flusso dell'attacco (simulazione)
1. Avvio di bettercap
2. net.probe, net.recon, net.sniff
3. ARP spoofing verso la vittima
4. Attivazione proxy HTTPS
5. SSL stripping
6. Osservazione pacchetti con Wireshark

# Difese e mitigazioni
- HTTPS ovunque
- HSTS
- Rilevamento ARP spoofing
- Certificati validi
- Awareness degli utenti
