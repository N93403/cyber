# Ethical MITM Lab – Bettercap & HTTPS

Questo progetto è un laboratorio **didattico** per comprendere:
- Differenza tra HTTP e HTTPS
- Attacchi Man-in-the-Middle (MITM)
- Tecniche di ARP spoofing e SSL stripping
- Difese e mitigazioni

⚠️ **Disclaimer**: Questo progetto è destinato esclusivamente a scopi educativi in ambienti controllati (VM locali).  
Non deve essere usato su reti reali o senza autorizzazione.

---

## 🖥️ Scenario di rete
- **VM Vittima**: IP `10.0.2.15`, MAC `08:00:27:55:44:07`
- **VM Router**: IP `10.0.2.2`, MAC `52:54:00:12:35:02`
- **VM Attaccante**: IP `10.0.2.100`, MAC `00:11:22:33:44:55`

---

## 🚀 Avvio rapido
```bash
cd vagrant
vagrant up

vagrant ssh attacker
sudo bettercap --silent -iface eth0 -caplet ../scripts/bettercap_lab.cap

