#!/usr/bin/env python3
"""
Script per la generazione dell'Infrastruttura a Chiave Pubblica (PKI) self-signed.
Crea la CA, il Server e il Client Certificate/Key per l'Autenticazione Mutua (mTLS).
"""
import os
import sys
import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

# === CONFIGURAZIONE CERTIFICATI ===
# Nomi dei file
CA_CERT_FILE = 'ca_cert.pem'
CA_KEY_FILE = 'ca_key.pem'
SERVER_CERT_FILE = 'server_cert.pem'
SERVER_KEY_FILE = 'server_key.pem'
CLIENT_CERT_FILE = 'client_cert.pem'
CLIENT_KEY_FILE = 'client_key.pem'

# Informazioni Identità (Subject)
CA_INFO = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"IT"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Italy"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Rome"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My CA"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"myca.example.com"),
])

SERVER_INFO = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"IT"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Italy"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Milan"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Server Org"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"server.example.com"),
])

CLIENT_INFO = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"IT"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Italy"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Turin"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Client Device"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"client.example.com"),
])


def genera_chiave_privata():
    """Genera una chiave privata RSA."""
    print("  -> Generazione chiave privata RSA...")
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

def scrivi_file(nome_file, contenuto, serializzazione_formato=serialization.Encoding.PEM):
    """Scrive il contenuto (chiave o certificato) su un file."""
    with open(nome_file, "wb") as f:
        f.write(contenuto)
    print(f"  -> Creato: {nome_file}")

def crea_certificato_ca(key):
    """Crea il certificato root self-signed della CA."""
    print("  -> Creazione Certificato CA...")
    return x509.CertificateBuilder().subject_name(
        CA_INFO
    ).issuer_name( # La CA è self-signed, quindi Issuer = Subject
        CA_INFO
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=3650) # Valido per 10 anni
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True
    ).sign(key, hashes.SHA256(), default_backend())

def crea_certificato_firmato(subject_info, ca_cert, ca_key, key, usage_extension, filename):
    """Crea un certificato per server/client e lo firma con la CA."""
    print(f"  -> Creazione Certificato {filename.split('_')[0]}...")

    # Estensione per l'uso (Server Authentication o Client Authentication)
    extended_key_usage = x509.ExtendedKeyUsage([usage_extension])

    # Creazione del Certificato
    cert = x509.CertificateBuilder().subject_name(
        subject_info
    ).issuer_name(
        ca_cert.subject # L'issuer è la CA
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365) # Valido per 1 anno
    ).add_extension(
        extended_key_usage, critical=True # Aggiunge EKU (essenziale per mTLS)
    ).sign(ca_key, hashes.SHA256(), default_backend())

    return cert


def genera_tutti_certificati():
    """Genera l'intera PKI: CA, Server e Client."""
    print("\n[ INIZIO GENERAZIONE PKI ]")

    # 1. Generazione Chiave e Certificato CA
    ca_key = genera_chiave_privata()
    scrivi_file(CA_KEY_FILE, ca_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))
    ca_cert = crea_certificato_ca(ca_key)
    scrivi_file(CA_CERT_FILE, ca_cert.public_bytes(serialization.Encoding.PEM))

    # 2. Generazione Chiave e Certificato Server
    server_key = genera_chiave_privata()
    scrivi_file(SERVER_KEY_FILE, server_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))
    server_cert = crea_certificato_firmato(
        SERVER_INFO, ca_cert, ca_key, server_key,
        x509.ExtendedKeyUsageOID.SERVER_AUTH, SERVER_CERT_FILE
    )
    scrivi_file(SERVER_CERT_FILE, server_cert.public_bytes(serialization.Encoding.PEM))

    # 3. Generazione Chiave e Certificato Client
    client_key = genera_chiave_privata()
    scrivi_file(CLIENT_KEY_FILE, client_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))
    client_cert = crea_certificato_firmato(
        CLIENT_INFO, ca_cert, ca_key, client_key,
        x509.ExtendedKeyUsageOID.CLIENT_AUTH, CLIENT_CERT_FILE
    )
    scrivi_file(CLIENT_CERT_FILE, client_cert.public_bytes(serialization.Encoding.PEM))
    
    print("\n[ GENERAZIONE PKI COMPLETATA ]")
    print("\nRicorda di spostare i file chiave (.key.pem) nelle rispettive cartelle SERVER-VICTIM e CLIENT-LINUX-MX.")


if __name__ == '__main__':
    # Esegue solo la generazione (NON il server/client)
    genera_tutti_certificati()
