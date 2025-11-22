# 🏁 Getting Started con Meterpreter

## Prerequisiti

### Ambiente di Laboratorio Richiesto
- ✅ VirtualBox/VMware
- ✅ Kali Linux (Attacker)
- ✅ Windows 10 VM (Target)
- ✅ Rete isolata (NAT Network)
- ✅ Autorizzazione scritta per il testing

### Conoscenze Base Richieste
- Concetti base di networking
- Familiarità con Linux command line
- Basi di Metasploit Framework

## 🛠️ Setup Ambiente di Testing

### 1. Configurazione Rete Isolata
```bash
# Creare una rete NAT isolata in VirtualBox
VBoxManage natnetwork add --netname RedTeamLab --network "192.168.100.0/24" --enable

# Assegnare le VM alla rete isolata
