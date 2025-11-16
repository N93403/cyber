#!/bin/bash
# Caldera Installation Script
# Tested on Kali Linux 2024

echo "[*] Starting Caldera Installation..."

# Remove any existing installations
sudo apt purge caldera -y 2>/dev/null
sudo apt autoremove --purge -y
sudo rm -rf /usr/share/caldera /var/lib/caldera /etc/caldera

# Install dependencies
echo "[*] Installing dependencies..."
sudo apt update
sudo apt install -y python3-venv python3-full git nodejs npm

# Clone Caldera repository
echo "[*] Cloning Caldera repository..."
git clone https://github.com/mitre/caldera.git
cd caldera

# Initialize submodules
echo "[*] Initializing submodules..."
git submodule update --init --recursive

# Create virtual environment
echo "[*] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Fix requirements.txt for lxml
echo "[*] Updating requirements.txt..."
sed -i 's/lxml~=4.9.1/lxml>=5.2,<6/' requirements.txt

# Install Python dependencies
echo "[*] Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Build Caldera
echo "[*] Building Caldera..."
python3 server.py --build

echo "[*] Installation complete!"
echo "[*] Start Caldera with: cd caldera && source venv/bin/activate && python3 server.py --insecure"
echo "[*] Access at: http://localhost:8888"
echo "[*] Credentials: red/admin"
