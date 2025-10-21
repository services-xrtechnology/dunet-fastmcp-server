# 🚀 Dunet FastMCP Server

Servidor FastMCP 2.0 con herramientas de IA para Odoo.

## 🛠️ Herramientas

- **consultar_rnc_dgii**: Consulta RNC/Cédula en DGII
- **crear_cotizacion_dunet**: Crea cotizaciones en Odoo

## 🌐 Servidor en Producción

**IP:** 173.230.131.241
**Endpoint HTTP:** http://173.230.131.241:8070/mcp
**Transport:** HTTP Streamable (estándar MCP 2025)

## 🔌 Conectar con IA

### ElevenLabs (requiere HTTPS):
Usa ngrok o SSL: `https://tu-url/mcp`

### Claude Desktop:
```json
{
  "mcpServers": {
    "dunet": {
      "command": "curl",
      "args": ["-N", "http://173.230.131.241:8070/mcp"]
    }
  }
}
```

## 💻 Ejecutar

```bash
python3 simple_server.py
```

## 📦 Deploy

Ver `install_production.sh` para instalación completa con systemd.
