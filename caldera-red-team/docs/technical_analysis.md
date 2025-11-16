# Caldera Operation Technical Analysis

## Operation Details
- **Operation Name**: Windows Security Assessment
- **Adversary Profile**: Discovery
- **Target Platform**: Windows
- **Agent**: Sandcat (GoLang)

## MITRE ATT&CK Techniques Tested

### T1087 - Account Discovery
- **Ability**: Enumerate local users
- **Command**: `Get-WmiObject -Class Win32_UserAccount`
- **Purpose**: Identify user accounts on the system

### T1057 - Process Discovery
- **Ability**: List running processes
- **Command**: `Get-Process | Select-Object ProcessName, Id, CPU`
- **Purpose**: Understand running applications and services

### T1018 - Remote System Discovery
- **Ability**: Network share enumeration
- **Command**: `net share`
- **Purpose**: Identify shared resources

### T1069 - Permission Groups Discovery
- **Ability**: Local group enumeration
- **Command**: `net localgroup`
- **Purpose**: Understand user privileges and groups

## Detection Evasion Techniques
- **Obfuscation**: Manual mode to avoid pattern detection
- **Execution Policy**: Bypassed for PowerShell execution
- **Persistence**: Agent runs with hidden window style

## Results Analysis
The operation successfully demonstrates:
1. Initial access and persistence capabilities
2. Privilege escalation detection
3. System reconnaissance techniques
4. Data collection methods
