# Servidor FastMCP para Dunet

Servidor FastMCP 2.0 que expone herramientas de Odoo para agentes de IA.

## Instalación

### 1. Instalar dependencias:
```bash
pip3 install -r requirements.txt
```

### 2. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### 3. Iniciar servidor:
```bash
python3 server.py
```

El servidor estará disponible en: `http://localhost:8070/mcp`

## Herramientas Disponibles

### consultar_rnc_dgii
Consulta RNC o Cédula en portal DGII.

### crear_cotizacion_dunet
Crea cotización en Odoo automáticamente.

## Deploy en FastMCP Cloud

1. Subir a GitHub
2. Conectar en https://fastmcp.cloud
3. Configurar variables de entorno
4. Deploy automático

URL resultante: `https://dunet-tools.fastmcp.app/mcp`

## Uso con ElevenLabs

Dashboard → Agent → Tools → Add MCP Server → URL del FastMCP

## Uso con Claude Code

```bash
claude mcp add dunet --url http://localhost:8070/mcp
```
