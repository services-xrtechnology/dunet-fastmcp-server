#!/usr/bin/env python3
"""
Deploy completo en Linode para producción
Crea servidor, instala Docker, despliega FastMCP
"""
import requests
import paramiko
import time
import json

LINODE_TOKEN = "9645efc4b8c3512ff4ace4aae95beaf40f936c33db0f42aaf9ce72440524d7d0"
ROOT_PASSWORD = "Santodomingo2828."
ODOO_URL = "https://robust-briefly-mink.ngrok-free.app"
ODOO_DB = "doonet"
ODOO_USER = "xavier@xrtechnology.com.do"
ODOO_PASS = "Santodomingo2828."

headers = {"Authorization": f"Bearer {LINODE_TOKEN}", "Content-Type": "application/json"}

print("="*70)
print("🚀 DEPLOY PRODUCCIÓN COMPLETO - DUNET FASTMCP")
print("="*70)

# PASO 1: Crear servidor
print("\n📍 PASO 1: Creando servidor Linode...")
payload = {
    "type": "g6-nanode-1",
    "region": "us-southeast",
    "image": "linode/ubuntu22.04",
    "root_pass": ROOT_PASSWORD,
    "label": "dunet-fastmcp-production",
    "tags": ["fastmcp", "production", "dunet"],
    "booted": True
}

r = requests.post("https://api.linode.com/v4/linode/instances", headers=headers, json=payload)

if r.status_code == 200:
    data = r.json()
    server_id = data['id']
    print(f"✅ Servidor creado (ID: {server_id})")
    print(f"⏳ Esperando IP...")

    # Esperar IP
    for i in range(30):
        time.sleep(5)
        status = requests.get(f"https://api.linode.com/v4/linode/instances/{server_id}", headers=headers).json()
        if status['status'] == 'running' and status.get('ipv4'):
            ip = status['ipv4'][0]
            print(f"✅ IP asignada: {ip}")
            break
    else:
        print("❌ Timeout esperando IP")
        exit(1)
else:
    print(f"❌ Error: {r.status_code} - {r.text}")
    exit(1)

# PASO 2: Configurar servidor
print(f"\n⚙️  PASO 2: Configurando servidor {ip}...")
print("⏳ Esperando SSH (puede tardar 2-3 minutos)...")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for i in range(30):
    try:
        ssh.connect(ip, username='root', password=ROOT_PASSWORD, timeout=10)
        print("✅ Conectado por SSH")
        break
    except:
        time.sleep(10)
        print(f"   Reintentando... ({i+1}/30)")
else:
    print("❌ No se pudo conectar")
    exit(1)

# PASO 3: Instalar Docker y configurar
print("\n🐳 PASO 3: Instalando Docker...")

install_script = f"""#!/bin/bash
set -e

echo "Actualizando sistema..."
apt-get update -y
apt-get upgrade -y

echo "Instalando Docker..."
apt-get install -y docker.io docker-compose git curl python3-pip

echo "Habilitando Docker..."
systemctl enable docker
systemctl start docker

echo "Creando directorio..."
mkdir -p /opt/dunet-fastmcp
cd /opt/dunet-fastmcp

echo "Clonando repositorio..."
git clone https://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@github.com/services-xrtechnology/dunet-fastmcp-server.git .

echo "Configurando .env..."
cat > .env << 'ENVEOF'
ODOO_URL={ODOO_URL}
ODOO_DB={ODOO_DB}
ODOO_USERNAME={ODOO_USER}
ODOO_PASSWORD={ODOO_PASS}
ENVEOF

echo "Instalando dependencias Python..."
pip3 install -r requirements.txt

echo "Creando servicio systemd..."
cat > /etc/systemd/system/dunet-fastmcp.service << 'SERVICEEOF'
[Unit]
Description=Dunet FastMCP Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/dunet-fastmcp
EnvironmentFile=/opt/dunet-fastmcp/.env
ExecStart=/usr/bin/python3 /opt/dunet-fastmcp/simple_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEEOF

systemctl daemon-reload
systemctl enable dunet-fastmcp
systemctl start dunet-fastmcp

echo "Configurando firewall..."
ufw allow 22/tcp
ufw allow 8070/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo "✅ INSTALACIÓN COMPLETADA"
"""

stdin, stdout, stderr = ssh.exec_command(install_script, get_pty=True)

print("📦 Instalando (esto toma 3-5 minutos)...")
for line in stdout:
    line_clean = line.strip()
    if line_clean:
        print(f"   {line_clean}")

ssh.close()

print("\n" + "="*70)
print("✅ DEPLOY COMPLETADO - SERVIDOR LISTO PARA PRODUCCIÓN")
print("="*70)
print(f"\n🌐 IP del servidor: {ip}")
print(f"🔌 FastMCP Server: http://{ip}:8070")
print(f"🛠️  Herramientas MCP: http://{ip}:8070/mcp")
print(f"\n📝 Conectar ElevenLabs a: http://{ip}:8070/mcp")
print(f"\n🔐 Acceso SSH: ssh root@{ip}")
print(f"   Password: {ROOT_PASSWORD}")
print(f"\n📊 Ver estado:")
print(f"   ssh root@{ip}")
print(f"   systemctl status dunet-fastmcp")
print(f"\n✅ Servidor corriendo 24/7 con systemd")
