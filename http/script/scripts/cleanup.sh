#!/bin/bash
echo "[*] Ripristino rete..."
sudo iptables -F
sudo systemctl restart networking
echo "[*] Pulizia completata."
