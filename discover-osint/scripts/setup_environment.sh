#!/bin/bash
# Discover OSINT - Environment Setup Script

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════╗"
echo "║           Discover OSINT Setup              ║"
echo "║         Environment Configuration           ║"
echo "╚══════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if running as normal user
if [ "$EUID" -eq 0 ]; then
    print_warning "Non eseguire come root. Usa un utente normale."
    exit 1
fi

# Parse arguments
ROLE=""
DOMAIN=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --role)
            ROLE="$2"
            shift 2
            ;;
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        *)
            print_error "Parametro sconosciuto: $1"
            exit 1
            ;;
    esac
done

# Main setup function
setup_attacker() {
    print_status "Configurazione VM Attaccante..."
    
    # Update system
    print_status "Aggiornamento sistema..."
    sudo apt update && sudo apt upgrade -y
    
    # Install dependencies
    print_status "Installazione dipendenze..."
    sudo apt install -y git python3 python3-pip curl wget
    
    # Clone Discover
    if [ ! -d "discover" ]; then
        print_status "Download Discover..."
        git clone https://github.com/leebaird/discover
    else
        print_status "Discover già presente, aggiornamento..."
        cd discover && git pull && cd ..
    fi
    
    # Setup permissions
    print_status "Configurazione permessi..."
    chmod +x discover/*.sh
    chmod +x discover/scripts/*.sh
    
    # Create results directory
    mkdir -p ~/penetration-test-results
    
    print_status "VM Attaccante configurata!"
}

setup_target() {
    print_status "Configurazione VM Target..."
    
    if [ -z "$DOMAIN" ]; then
        print_error "Specifica un dominio con --domain"
        exit 1
    fi
    
    # Install services
    print_status "Installazione servizi..."
    sudo apt update
    sudo apt install -y apache2 openssh-server
    
    # Configure domain
    print_status "Configurazione dominio: $DOMAIN"
    echo "127.0.0.1 $DOMAIN" | sudo tee -a /etc/hosts
    echo "127.0.0.1 www.$DOMAIN" | sudo tee -a /etc/hosts
    echo "127.0.0.1 admin.$DOMAIN" | sudo tee -a /etc/hosts
    
    # Create web content
    print_status "Creazione contenuto web..."
    sudo mkdir -p /var/www/html/{admin,blog,api,test}
    
    # Basic index page
    sudo tee /var/www/html/index.html > /dev/null << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Test Company - Penetration Testing Target</title>
</head>
<body>
    <h1>Test Company</h1>
    <p>This is a test environment for penetration testing exercises.</p>
    <p>Contact: info@$DOMAIN</p>
</body>
</html>
EOF

    # Admin page
    sudo tee /var/www/html/admin/index.html > /dev/null << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Admin Area - Test Company</title>
</head>
<body>
    <h1>Administrative Panel</h1>
    <p>Restricted access area for administrators.</p>
</body>
</html>
EOF

    # Start services
    print_status "Avvio servizi..."
    sudo systemctl enable apache2 ssh
    sudo systemctl start apache2 ssh
    
    # Create test files
    print_status "Creazione file di test..."
    echo "User-agent: *" | sudo tee /var/www/html/robots.txt
    echo "Disallow: /admin/" | sudo tee -a /var/www/html/robots.txt
    
    sudo tee /var/www/html/sitemap.xml > /dev/null << EOF
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>http://$DOMAIN/</loc>
    </url>
    <url>
        <loc>http://$DOMAIN/admin/</loc>
    </url>
</urlset>
EOF

    print_status "VM Target configurata con dominio: $DOMAIN"
}

# Main execution
case $ROLE in
    "attacker")
        setup_attacker
        ;;
    "target")
        setup_target
        ;;
    *)
        print_error "Specifica --role attacker o --role target"
        echo "Usage: $0 --role [attacker|target] --domain example.com (for target)"
        exit 1
        ;;
esac

print_status "Setup completato! 🎉"
echo -e "${YELLOW}Prossimi passi:${NC}"
echo "1. Verifica connettività di rete"
echo "2. Esegui gli esercizi nella cartella /exercises"
echo "3. Consulta la documentazione in /docs"
