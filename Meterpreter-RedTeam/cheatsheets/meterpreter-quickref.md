
## 📄 FILE 5: cheatsheets/meterpreter-quickref.md

```markdown
# 📋 Meterpreter Quick Reference Cheatsheet

## 🚀 Comandi Essenziali per Session Management

### Session Basics
```bash
# Info sessione
getuid           # Current user
sysinfo          # System information
background       # Background session
sessions -i <ID> # Resume session

# Shell management
shell            # System shell
execute -f cmd   # Execute command
