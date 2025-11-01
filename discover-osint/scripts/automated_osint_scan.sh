#!/bin/bash
# Automated OSINT Scan Script for Discover Framework

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║           Automated OSINT Scan              ║"
    echo "║           Discover Framework                ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${GREEN}[→]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 <domain> [output_directory]"
    echo "Example: $0 techsolutions.local /home/student/results"
    exit 1
fi

DOMAIN=$1
OUTPUT_DIR=${2:-"/home/$(whoami)/osint_results"}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
SCAN_DIR="$OUTPUT_DIR/$DOMAIN/$TIMESTAMP"

print_header

# Create scan directory
mkdir -p "$SCAN_DIR"
cd "$SCAN_DIR"

print_step "Iniziando scansione OSINT per: $DOMAIN"
print_step "Directory risultati: $SCAN_DIR"

# 1. DNS Enumeration
print_step "1. Esecuzione DNS reconnaissance..."
dnsrecon -d "$DOMAIN" -t std > dns_recon.txt 2>&1
dnsrecon -d "$DOMAIN" -t axfr >> dns_recon.txt 2>&1
print_success "DNS reconnaissance completata"

# 2. Subdomain Discovery
print_step "2. Enumerazione sottodomini..."
{
    subfinder -d "$DOMAIN" -silent
    amass enum -passive -d "$DOMAIN" 2>/dev/null || echo "Amass not available"
} > subdomains.txt
print_success "Enumerazione sottodomini completata"

# 3. Email Harvesting
print_step "3. Raccolta indirizzi email..."
theharvester -d "$DOMAIN" -b google,bing -l 50 > email_harvesting.txt 2>&1
print_success "Email harvesting completato"

# 4. Network Scanning
print_step "4. Scansione servizi di rete..."
nmap -sS -A -T4 "$DOMAIN" > nmap_scan.txt 2>&1
print_success "Scansione network completata"

# 5. Web Fingerprinting
print_step "5. Fingerprinting servizi web..."
whatweb -v "http://$DOMAIN" > whatweb_scan.txt 2>&1
print_success "Web fingerprinting completato"

# 6. Generate comprehensive report
print_step "6. Generazione report consolidato..."

cat > OSINT_REPORT.md << EOF
# OSINT Report - $DOMAIN
## Scansione Eseguita: $(date)

### Informazioni Generali
- **Dominio Target**: $DOMAIN
- **Data Scansione**: $(date)
- **Tool Utilizzati**: Discover, DNSRecon, SubFinder, theHarvester, Nmap

### Executive Summary
Scansione OSINT passiva completata con successo. Scoperti \$(grep -c . subdomains.txt) sottodomini e \$(grep -c "open" nmap_scan.txt) servizi network.

### Risultati Dettagliati

#### Sottodomini Identificati
\`\`\`
$(cat subdomains.txt)
\`\`\`

#### Servizi Network
\`\`\`
$(grep "open" nmap_scan.txt | head -20)
\`\`\`

#### Record DNS
\`\`\`
$(grep -A 5 "Trying" dns_recon.txt | head -15)
\`\`\`

### Raccomandazioni
1. Verificare l'esposizione dei servizi identificati
2. Monitorare i sottodomini non autorizzati
3. Implementare controlli di sicurezza adeguati

---
*Report generato automaticamente con Discover OSINT Framework*
EOF

print_success "Report generato: $SCAN_DIR/OSINT_REPORT.md"

# 7. Create summary file
print_step "7. Creazione file di sintesi..."

cat > scan_summary.txt << EOF
=== SCAN SUMMARY ===
Domain: $DOMAIN
Timestamp: $TIMESTAMP
Scan Directory: $SCAN_DIR

Files Generated:
- dns_recon.txt (DNS information)
- subdomains.txt ($(grep -c . subdomains.txt) subdomains)
- email_harvesting.txt (Email addresses)
- nmap_scan.txt (Network services)
- whatweb_scan.txt (Web technologies)
- OSINT_REPORT.md (Comprehensive report)

Next Steps:
1. Review OSINT_REPORT.md for findings
2. Validate discovered subdomains
3. Check for exposed services
4. Conduct manual verification
EOF

print_success "Scansione completata!"
echo -e "${YELLOW}========================================${NC}"
echo -e "${GREEN}📁 Risultati salvati in: $SCAN_DIR${NC}"
echo -e "${YELLOW}📄 Report principale: OSINT_REPORT.md${NC}"
echo -e "${YELLOW}📋 Sintesi: scan_summary.txt${NC}"
echo -e "${YELLOW}========================================${NC}"

# Display quick findings
echo -e "\n${BLUE}=== QUICK FINDINGS ===${NC}"
echo -e "Sottodomini: $(grep -c . subdomains.txt)"
echo -e "Servizi aperti: $(grep -c "open" nmap_scan.txt)"
echo -e "Tecnologie web: $(grep -c "http" whatweb_scan.txt)"
