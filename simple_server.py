#!/usr/bin/env python3
"""
Servidor FastMCP Simplificado para Dunet
Solo herramientas MCP, sin portal admin (por ahora)
"""
import os
import xmlrpc.client
from typing import Optional
from fastmcp import FastMCP
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

# Config
ODOO_URL = os.getenv('ODOO_URL', 'https://robust-briefly-mink.ngrok-free.app')
ODOO_DB = os.getenv('ODOO_DB', 'doonet')
ODOO_USERNAME = os.getenv('ODOO_USERNAME', 'xavier@xrtechnology.com.do')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD', 'Santodomingo2828.')

# Crear servidor
mcp = FastMCP("Dunet Tools")

def get_odoo():
    """Conexión a Odoo"""
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    if not uid:
        raise Exception(f"Auth failed: {ODOO_URL}")
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    return models, uid, ODOO_PASSWORD

@mcp.tool()
def consultar_rnc_dgii(rnc_cedula: str) -> dict:
    """Consulta RNC/Cédula en DGII"""
    try:
        models, uid, password = get_odoo()
        return models.execute_kw(
            ODOO_DB, uid, password,
            'dgii.rnc.lookup.tools', 'consultar',
            [rnc_cedula]
        )
    except Exception as e:
        return {'error': str(e)}

@mcp.tool()
def crear_cotizacion_dunet(
    plan_code: str,
    customer_email: str,
    customer_name: Optional[str] = "",
    customer_rnc: Optional[str] = "",
    include_certification: Optional[bool] = False
) -> dict:
    """Crea cotización en Odoo"""
    try:
        models, uid, password = get_odoo()
        return models.execute_kw(
            ODOO_DB, uid, password,
            'quotation.creator.tools', 'crear_cotizacion',
            [plan_code, customer_email, customer_name, customer_rnc, include_certification]
        )
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Iniciar servidor con HTTP Streamable (estándar MCP 2025)
if __name__ == "__main__":
    print("="*60)
    print("🚀 DUNET FASTMCP SERVER")
    print("="*60)
    print(f"📡 Odoo: {ODOO_URL}")
    print(f"💾 Database: {ODOO_DB}")
    print(f"🔌 Transport: HTTP Streamable")
    print(f"🌐 Endpoint: http://0.0.0.0:8070/mcp")
    print("="*60)
    print("🛠️  Herramientas:")
    print("   1. consultar_rnc_dgii")
    print("   2. crear_cotizacion_dunet")
    print("="*60)
    print("✅ Servidor listo\n")

    # HTTP Streamable (nuevo estándar MCP marzo 2025)
    mcp.run(transport='http', host='0.0.0.0', port=8070, path='/mcp')
