# Caldera Red Team Setup Guide

## Prerequisites
- Kali Linux (Attacker)
- Windows 10/11 or Server 2019 (Target)
- Network connectivity between machines

## Step 1: Caldera Installation
```bash
chmod +x scripts/install_caldera.sh
./scripts/install_caldera.sh

Step 2: Start Caldera
bash
cd caldera
source venv/bin/activate
python3 server.py --insecure
Step 3: Access Web Interface
Navigate to: http://localhost:8888

Login: red / admin

Step 4: Deploy Agent on Windows Target
Open PowerShell as Administrator

Run the deploy script:

powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
.\deploy_agent.ps1 -KaliIP "192.168.1.100"
Step 5: Execute Operation
In Caldera: Navigate to "Operations"

Create new operation:

Name: "Windows Security Test"

Adversary: "Discovery"

Group: "red"

Start operation and monitor results

Expected Outcomes
Agent appears in Caldera interface

Operation executes discovery techniques

Results show system information and vulnerabilities

text

### 5. README.md Principale

```markdown
# Caldera Red Team Operation Demonstration

![Caldera Logo](https://github.com/mitre/caldera/raw/master/static/images/caldera-logo.png)

## 🎯 Project Overview

This project demonstrates practical red team operations using MITRE Caldera, showcasing adversary emulation capabilities and security assessment techniques.

## ✨ Features Demonstrated

- ✅ Caldera installation and configuration
- ✅ Agent deployment on Windows targets
- ✅ Adversary emulation using MITRE ATT&CK framework
- ✅ Discovery operations and system reconnaissance
- ✅ Results analysis and reporting

## 🛠️ Technical Skills Demonstrated

- **Red Teaming**: Adversary emulation and attack simulation
- **Tool Proficiency**: MITRE Caldera platform expertise
- **Scripting**: PowerShell and Bash automation
- **Security Assessment**: Vulnerability identification and analysis
- **Documentation**: Professional reporting and technical writing

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/yourusername/caldera-red-team-demo.git
cd caldera-red-team-demo/scripts
chmod +x install_caldera.sh
./install_caldera.sh
Operation Execution
Start Caldera: cd caldera && source venv/bin/activate && python3 server.py --insecure

Access: http://localhost:8888 (red/admin)

Deploy agent on Windows target using provided PowerShell script

Execute discovery operation through Caldera interface
