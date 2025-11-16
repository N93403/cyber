# Windows Security Settings for Red Team Lab
# TEMPORARY settings for educational purposes only

Write-Host "🔧 Configuring Windows VM for Red Team Lab..." -ForegroundColor Yellow

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Please run as Administrator!" -ForegroundColor Red
    exit 1
}

Write-Host "[1] Temporarily disabling Windows Defender..." -ForegroundColor Cyan
Set-MpPreference -DisableRealtimeMonitoring $true
Set-MpPreference -DisableBehaviorMonitoring $true
Set-MpPreference -DisableBlockAtFirstSeen $true

Write-Host "[2] Configuring Windows Firewall for lab network..." -ForegroundColor Cyan
New-NetFirewallRule -DisplayName "Caldera Lab" -Direction Inbound -LocalPort 8888 -Protocol TCP -Action Allow -Profile Private

Write-Host "[3] Setting execution policy for current session..." -ForegroundColor Cyan
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

Write-Host "[4] Enabling necessary services..." -ForegroundColor Cyan
Get-Service -Name WinRM | Set-Service -StartupType Automatic
Start-Service WinRM

Write-Host "[5] Creating lab network profile..." -ForegroundColor Cyan
Set-NetConnectionProfile -InterfaceAlias "Ethernet" -NetworkCategory Private

Write-Host "✅ Windows VM configuration complete!" -ForegroundColor Green
Write-Host "⚠️  Remember to re-enable security features after lab exercises!" -ForegroundColor Yellow

# Display current security status
Write-Host "`n🔒 Current Security Status:" -ForegroundColor Cyan
Get-MpComputerStatus | Select-Object AntivirusEnabled, AntispywareEnabled, RealTimeProtectionEnabled
