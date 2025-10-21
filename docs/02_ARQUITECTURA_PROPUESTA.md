# 🏗️ ARQUITECTURA PROPUESTA - FASTMCP MULTI-TENANT

**Versión:** 1.0
**Fecha:** 20 Octubre 2025

---

## 🎯 VISIÓN GENERAL

Sistema escalable de herramientas MCP para que múltiples clientes conecten sus agentes de IA a Odoo.

---

## 📊 ARQUITECTURA COMPLETA

```
┌──────────────────────────────────────────────────┐
│  INFRAESTRUCTURA (Linode/Digital Ocean)          │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌─────────────────────────────────────┐         │
│  │ PostgreSQL Database (Managed DB)    │         │
│  │ Puerto: 5432                        │         │
│  ├─────────────────────────────────────┤         │
│  │ Tables:                             │         │
│  │ - clients (configuraciones)         │         │
│  │ - api_tokens (autenticación)        │         │
│  │ - tool_usage (analytics)            │         │
│  │ - logs (auditoría)                  │         │
│  └──────────────┬──────────────────────┘         │
│                 │                                 │
│  ┌──────────────▼──────────────────────┐         │
│  │ Portal de Administración             │         │
│  │ FastAPI + Jinja2 Templates           │         │
│  │ Puerto: 8000 (interno)               │         │
│  ├──────────────────────────────────────┤         │
│  │ Funciones:                           │         │
│  │ - CRUD de clientes                   │         │
│  │ - Gestión de tokens                  │         │
│  │ - Dashboard de métricas              │         │
│  │ - Configuración de herramientas      │         │
│  │ - Logs en tiempo real                │         │
│  └──────────────┬──────────────────────┘         │
│                 │                                 │
│  ┌──────────────▼──────────────────────┐         │
│  │ FastMCP Server Multi-Tenant          │         │
│  │ Puerto: 8070 (interno)               │         │
│  │ Transport: HTTP Streamable           │         │
│  ├──────────────────────────────────────┤         │
│  │ Lee configuración de PostgreSQL      │         │
│  │ Autentica por token                  │         │
│  │ Ejecuta herramientas según cliente   │         │
│  │ Rate limiting por cliente            │         │
│  └──────────────┬──────────────────────┘         │
│                 │                                 │
│  ┌──────────────▼──────────────────────┐         │
│  │ Nginx Reverse Proxy                  │         │
│  │ Puertos: 80, 443                     │         │
│  ├──────────────────────────────────────┤         │
│  │ Routes:                              │         │
│  │ /mcp → FastMCP (8070)                │         │
│  │ /admin → Portal (8000)               │         │
│  │ SSL: Let's Encrypt                   │         │
│  └──────────────────────────────────────┘         │
│                                                   │
└───────────────────┬───────────────────────────────┘
                    │
          ┌─────────┴──────────┐
          │                    │
    ┌─────▼──────┐      ┌─────▼──────┐
    │ Cliente 1  │      │ Cliente 2  │
    │ Odoo       │      │ Odoo       │
    └────────────┘      └────────────┘
```

---

## 🔧 STACK TECNOLÓGICO

### Backend:
- **FastMCP** - Framework MCP para herramientas
- **FastAPI** - Portal de administración
- **PostgreSQL** - Base de datos
- **SQLAlchemy** - ORM
- **xmlrpc.client** - Conexión a Odoo

### Frontend:
- **Jinja2 Templates** - HTML server-side
- **CSS/JavaScript** - UI responsive
- **Chart.js** - Gráficas y métricas

### Infraestructura:
- **systemd** - Gestión de servicios
- **Nginx** - Reverse proxy y SSL
- **Let's Encrypt** - Certificados SSL
- **Ubuntu 22.04/24.04** - Sistema operativo

### Deployment:
- **Git** - Control de versiones
- **GitHub** - Repositorio
- **Automated deploys** - Pull en servidor

---

## 📦 SERVICIOS SYSTEMD

### Servicio 1: dunet-fastmcp.service
```ini
[Unit]
Description=Dunet FastMCP Server
After=network.target postgresql.service

[Service]
WorkingDirectory=/opt/dunet-fastmcp
EnvironmentFile=/opt/dunet-fastmcp/.env
ExecStart=/opt/dunet-fastmcp/venv/bin/python3 simple_server.py
Restart=always
```

### Servicio 2: dunet-admin.service
```ini
[Unit]
Description=Dunet Admin Portal
After=network.target postgresql.service

[Service]
WorkingDirectory=/opt/dunet-admin
ExecStart=/opt/dunet-admin/venv/bin/uvicorn app:app --port 8000
Restart=always
```

### Servicio 3: nginx
Configuración en `/etc/nginx/sites-available/dunet-mcp`

### Servicio 4: postgresql
Gestionado por sistema

---

## 🔐 SEGURIDAD

### Autenticación:
- **API Tokens** por cliente
- **Encriptación** de credenciales Odoo (AES-256)
- **HTTPS** obligatorio (Let's Encrypt)
- **Rate limiting** por cliente

### Aislamiento:
- **Cada cliente** tiene su configuración separada
- **Logs** por cliente
- **Permisos** granulares por herramienta

---

## 📈 ESCALABILIDAD

### Horizontal:
- Load balancer Nginx
- Múltiples servidores FastMCP
- PostgreSQL replicado

### Vertical:
- Upgrade de servidor (más RAM/CPU)
- Cache con Redis
- CDN para portal admin

---

## 💾 BASE DE DATOS

### Esquema PostgreSQL:

```sql
-- Clientes
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    odoo_url VARCHAR(500),
    odoo_db VARCHAR(100),
    odoo_username VARCHAR(255),
    odoo_password_encrypted TEXT,
    api_token VARCHAR(255) UNIQUE,
    plan VARCHAR(50),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Herramientas por cliente
CREATE TABLE client_tools (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    tool_name VARCHAR(100),
    enabled BOOLEAN DEFAULT TRUE,
    rate_limit_per_hour INTEGER DEFAULT 1000
);

-- Logs de uso
CREATE TABLE tool_usage (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    tool_name VARCHAR(100),
    timestamp TIMESTAMP DEFAULT NOW(),
    success BOOLEAN,
    execution_time_ms INTEGER,
    error_message TEXT
);

-- Configuración global
CREATE TABLE configs (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🌐 ENDPOINTS

### Portal Admin:
```
https://mcp.doonet.app/admin           - Dashboard
https://mcp.doonet.app/admin/clients   - Gestión clientes
https://mcp.doonet.app/admin/logs      - Logs
https://mcp.doonet.app/admin/api/...   - API REST
```

### FastMCP Server:
```
https://mcp.doonet.app/mcp             - Endpoint MCP
```

---

## 🔄 FLUJO DE USO

### Cliente nuevo:
1. Se registra en portal admin
2. Configura credenciales de su Odoo
3. Recibe API token
4. Conecta su agente de IA al MCP server
5. Agente usa herramientas

### Herramienta ejecutándose:
1. Agente IA llama: `consultar_rnc_dgii("131793916")`
2. FastMCP autentica token del cliente
3. Lee configuración Odoo del cliente desde PostgreSQL
4. Se conecta al Odoo del cliente
5. Ejecuta consulta RNC
6. Devuelve resultado al agente
7. Registra en logs

---

## 📊 MÉTRICAS A TRACKEAR

- Clientes activos
- Herramientas más usadas
- Tiempo promedio de ejecución
- Tasa de error por herramienta
- Uso por cliente (para facturación)

---

## 💰 MONETIZACIÓN

### Freemium:
- **Gratis:** 100 llamadas/mes, 2 herramientas
- **Basic ($20/mes):** 5,000 llamadas, todas las herramientas
- **Pro ($50/mes):** Ilimitado, soporte prioritario

### Costo operativo estimado:
- Servidor: $12/mes (Linode 2GB)
- PostgreSQL managed: $15/mes
- **Total:** ~$30/mes
- **Break-even:** 2 clientes pagos

---

## 🎯 CASOS DE USO

### Dunet (uso propio):
- Agente de voz atiende clientes
- Crea cotizaciones automáticamente
- Consulta RNC para validar clientes

### Cliente tipo (futuro):
- Empresa con Odoo
- Quiere agente de IA que acceda a su Odoo
- Paga $20-50/mes por el servicio
- No gestiona servidores

---

**Próximo documento:** `02_ARQUITECTURA_PROPUESTA.md`
