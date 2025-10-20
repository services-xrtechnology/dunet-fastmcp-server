#!/bin/bash
#
# SCRIPT MAESTRO DE INSTALACIÓN PROFESIONAL
# Dunet FastMCP Server - Arquitectura Completa
#
# Instala:
# - FastMCP Server (puerto 8070)
# - Portal de Administración (puerto 8000)
# - PostgreSQL
# - Nginx con SSL
# - Todo con systemd
#

set -e  # Detener si hay error

echo "======================================================================"
echo "🚀 INSTALACIÓN PROFESIONAL - DUNET FASTMCP"
echo "======================================================================"
echo ""
echo "Esta instalación creará:"
echo "  ✅ FastMCP Server (puerto 8070)"
echo "  ✅ Portal Admin (puerto 8000)"
echo "  ✅ PostgreSQL Database"
echo "  ✅ Nginx Reverse Proxy"
echo "  ✅ Servicios systemd"
echo ""
echo "Tiempo estimado: 10-15 minutos"
echo "======================================================================"
echo ""

# Variables
GITHUB_REPO="https://github.com/services-xrtechnology/dunet-fastmcp-server.git"
ODOO_URL="https://robust-briefly-mink.ngrok-free.app"
ODOO_DB="doonet"
ODOO_USER="xavier@xrtechnology.com.do"
ODOO_PASS="Santodomingo2828."

# ====================================================================
# PASO 1: Actualizar sistema
# ====================================================================
echo "📦 PASO 1/8: Actualizando sistema..."
apt update
apt upgrade -y

# ====================================================================
# PASO 2: Instalar dependencias base
# ====================================================================
echo ""
echo "📦 PASO 2/8: Instalando dependencias..."
apt install -y \
    python3-pip \
    python3-venv \
    python3-full \
    git \
    nginx \
    postgresql \
    postgresql-contrib \
    certbot \
    python3-certbot-nginx

# ====================================================================
# PASO 3: Configurar PostgreSQL
# ====================================================================
echo ""
echo "🗄️  PASO 3/8: Configurando PostgreSQL..."

# Crear usuario y base de datos
sudo -u postgres psql -c "CREATE USER dunet_admin WITH PASSWORD 'Santodomingo2828.';" || true
sudo -u postgres psql -c "CREATE DATABASE dunet_fastmcp OWNER dunet_admin;" || true

# Crear tablas
sudo -u postgres psql -d dunet_fastmcp << 'SQL'
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    odoo_url VARCHAR(500) NOT NULL,
    odoo_db VARCHAR(100) NOT NULL,
    odoo_username VARCHAR(255) NOT NULL,
    odoo_password_encrypted TEXT NOT NULL,
    api_token VARCHAR(255) UNIQUE NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tool_usage (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    tool_name VARCHAR(100),
    timestamp TIMESTAMP DEFAULT NOW(),
    success BOOLEAN,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS configs (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);
SQL

echo "✅ PostgreSQL configurado"

# ====================================================================
# PASO 4: Instalar FastMCP Server
# ====================================================================
echo ""
echo "⚡ PASO 4/8: Instalando FastMCP Server..."

mkdir -p /opt/dunet-fastmcp
cd /opt/dunet-fastmcp

# Clonar repo
git clone $GITHUB_REPO .

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear .env
cat > .env << EOF
ODOO_URL=$ODOO_URL
ODOO_DB=$ODOO_DB
ODOO_USERNAME=$ODOO_USER
ODOO_PASSWORD=$ODOO_PASS
DATABASE_URL=postgresql://dunet_admin:Santodomingo2828.@localhost/dunet_fastmcp
EOF

# Crear servicio systemd para FastMCP
cat > /etc/systemd/system/dunet-fastmcp.service << 'SVCEOF'
[Unit]
Description=Dunet FastMCP Server
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/dunet-fastmcp
EnvironmentFile=/opt/dunet-fastmcp/.env
ExecStart=/opt/dunet-fastmcp/venv/bin/python3 -m fastmcp run simple_server.py:mcp --transport sse --port 8070 --host 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SVCEOF

echo "✅ FastMCP Server configurado"

# ====================================================================
# PASO 5: Crear Portal de Administración
# ====================================================================
echo ""
echo "🎛️  PASO 5/8: Creando Portal de Administración..."

mkdir -p /opt/dunet-admin
cd /opt/dunet-admin

# TODO: Aquí iría el código del portal admin
# Por ahora, placeholder
echo "ℹ️  Portal admin se configurará en siguiente fase"

# ====================================================================
# PASO 6: Configurar Nginx
# ====================================================================
echo ""
echo "🌐 PASO 6/8: Configurando Nginx..."

cat > /etc/nginx/sites-available/dunet-fastmcp << 'NGINX'
server {
    listen 80;
    server_name _;

    # FastMCP Server
    location /mcp {
        proxy_pass http://localhost:8070;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    # Portal Admin (futuro)
    location /admin {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Health check
    location /health {
        return 200 "OK";
        add_header Content-Type text/plain;
    }
}
NGINX

# Habilitar sitio
ln -sf /etc/nginx/sites-available/dunet-fastmcp /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Testear configuración
nginx -t

# Reiniciar Nginx
systemctl restart nginx
systemctl enable nginx

echo "✅ Nginx configurado"

# ====================================================================
# PASO 7: Configurar Firewall
# ====================================================================
echo ""
echo "🔒 PASO 7/8: Configurando Firewall..."

ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw allow 8070/tcp # FastMCP (temporal, luego cerrar)
ufw --force enable

echo "✅ Firewall configurado"

# ====================================================================
# PASO 8: Iniciar servicios
# ====================================================================
echo ""
echo "🚀 PASO 8/8: Iniciando servicios..."

systemctl daemon-reload
systemctl enable dunet-fastmcp
systemctl start dunet-fastmcp

echo "✅ Servicios iniciados"

# ====================================================================
# RESUMEN FINAL
# ====================================================================
echo ""
echo "======================================================================"
echo "✅ INSTALACIÓN COMPLETADA"
echo "======================================================================"
echo ""
echo "🌐 URLs de acceso:"
echo "   FastMCP (directo): http://$(hostname -I | awk '{print $1}'):8070/mcp"
echo "   FastMCP (nginx):   http://$(hostname -I | awk '{print $1}')/mcp"
echo ""
echo "📊 Verificar servicios:"
echo "   systemctl status dunet-fastmcp"
echo "   systemctl status nginx"
echo "   systemctl status postgresql"
echo ""
echo "📋 Ver logs:"
echo "   journalctl -u dunet-fastmcp -f"
echo ""
echo "🔌 Conectar ElevenLabs a:"
echo "   http://$(hostname -I | awk '{print $1}')/mcp"
echo ""
echo "======================================================================"
