"""
App de Administración FastMCP Dunet
Portal web para configurar y gestionar el servidor FastMCP
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import os
from typing import Optional
from datetime import datetime

# Importar servidor FastMCP
import sys
sys.path.append('..')
from server import mcp, get_odoo

# Crear app FastAPI
app = FastAPI(
    title="Dunet FastMCP Admin",
    description="Portal de administración para FastMCP Server",
    version="1.0.0"
)

# Servir archivos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Modelos Pydantic
class ConfigOdoo(BaseModel):
    odoo_url: str
    odoo_db: str
    odoo_username: str
    odoo_password: str

class TestConnection(BaseModel):
    success: bool
    message: str
    uid: Optional[int] = None

# Base de datos simple (SQLite)
from database.models import init_db, get_config, save_config, get_logs

# Inicializar BD
init_db()

# ========================================
# RUTAS DE LA INTERFAZ WEB
# ========================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Dashboard principal"""
    config = get_config()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "config": config,
        "server_status": "running",
        "tools_count": 2
    })

@app.get("/config", response_class=HTMLResponse)
async def config_page(request: Request):
    """Página de configuración"""
    config = get_config()
    return templates.TemplateResponse("config.html", {
        "request": request,
        "config": config
    })

@app.get("/logs", response_class=HTMLResponse)
async def logs_page(request: Request):
    """Página de logs"""
    logs = get_logs(limit=100)
    return templates.TemplateResponse("logs.html", {
        "request": request,
        "logs": logs
    })

# ========================================
# API ENDPOINTS
# ========================================

@app.get("/api/config")
async def get_configuration():
    """Obtiene configuración actual"""
    config = get_config()
    # No devolver password
    if config:
        config_safe = config.copy()
        config_safe['odoo_password'] = '***' if config.get('odoo_password') else ''
        return config_safe
    return {}

@app.post("/api/config")
async def save_configuration(config: ConfigOdoo):
    """Guarda nueva configuración"""
    try:
        # Guardar en BD
        save_config(config.dict())

        # Actualizar variables de entorno
        os.environ['ODOO_URL'] = config.odoo_url
        os.environ['ODOO_DB'] = config.odoo_db
        os.environ['ODOO_USERNAME'] = config.odoo_username
        os.environ['ODOO_PASSWORD'] = config.odoo_password

        return {"success": True, "message": "Configuración guardada"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/test-connection")
async def test_connection():
    """Prueba conexión con Odoo"""
    try:
        models, uid, password = get_odoo()
        return {
            "success": True,
            "message": "Conexión exitosa con Odoo",
            "uid": uid
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "uid": None
        }

@app.get("/api/tools")
async def get_tools():
    """Lista herramientas MCP disponibles"""
    return {
        "tools": [
            {
                "name": "consultar_rnc_dgii",
                "description": "Consulta RNC/Cédula en portal DGII",
                "enabled": True,
                "calls_count": 0
            },
            {
                "name": "crear_cotizacion_dunet",
                "description": "Crea cotizaciones automáticas en Odoo",
                "enabled": True,
                "calls_count": 0
            }
        ]
    }

@app.get("/api/status")
async def get_status():
    """Estado del servidor"""
    config = get_config()
    has_config = bool(config and config.get('odoo_url'))

    return {
        "server_running": True,
        "configured": has_config,
        "tools_active": 2,
        "uptime": "Running",
        "last_updated": datetime.now().isoformat()
    }

# ========================================
# INTEGRAR FASTMCP EN FASTAPI
# ========================================

# Montar servidor MCP en /mcp
from fastmcp.server import create_sse_handler

mcp_handler = create_sse_handler(mcp)
app.mount("/mcp", mcp_handler)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando Dunet FastMCP Admin...")
    print("📊 Dashboard: http://localhost:8070")
    print("🔌 MCP Endpoint: http://localhost:8070/mcp")
    uvicorn.run(app, host="0.0.0.0", port=8070)
