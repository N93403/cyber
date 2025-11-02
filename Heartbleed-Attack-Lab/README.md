# 🔓 Heartbleed Attack Lab (CVE-2014-0160)

![Heartbleed Logo](images/heartbleed_visualization.png)
![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-green.svg)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-orange.svg)

**Laboratorio educativo per comprendere e testare la vulnerabilità Heartbleed in ambiente controllato**

## 📋 Panoramica

Questo repository contiene un laboratorio pratico per studiare la famosa vulnerabilità Heartbleed (CVE-2014-0160) che ha afflitto OpenSSL. Il lab è progettato per scopi educativi e deve essere utilizzato solo in ambienti controllati.

### 🎯 Obiettivi di Apprendimento

- Comprendere il protocollo TLS Heartbeat
- Analizzare la vulnerabilità Buffer Over-read
- Sviluppare e testare un exploit Heartbleed
- Estrarre dati dalla memoria del server
- Implementare contromisure e patch

## ⚡ Quick Start

### Prerequisiti
- 2 VM SEED Ubuntu 12.04
- VirtualBox/VMware
- Python 3.x

### Setup Rapido
```bash
git clone https://github.com/tuo-username/heartbleed-attack-lab.git
cd heartbleed-attack-lab

# Configura le VM
./scripts/setup_vms.sh

# Esegui l'attacco di base
python3 scripts/heartbleed_simple.py www.heartbleedlabelgg.com
