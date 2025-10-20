#!/usr/bin/env python3
"""
Servidor FastMCP 2.0 para Dunet
Herramientas IA para Odoo
"""
import os
import xmlrpc.client
from typing import Optional
from fastmcp import FastMCP
from dotenv import load_dotenv

# Cargar .env si existe
load_dotenv()

# Configuración desde variables de entorno
ODOO_URL = os.getenv('ODOO_URL', 'http://localhost:8069')
ODOO_DB = os.getenv('ODOO_DB', 'doonet')
ODOO_USERNAME = os.getenv('ODOO_USERNAME', 'admin')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD', 'admin')

# Crear servidor FastMCP
mcp = FastMCP("Dunet Tools")

def get_odoo():
    """Obtiene conexión autenticada a Odoo"""
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})

    if not uid:
        raise Exception(f"Autenticación fallida con Odoo: {ODOO_URL}")

    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    return models, uid, ODOO_PASSWORD


@mcp.tool()
def consultar_rnc_dgii(rnc_cedula: str) -> dict:
    """
    Consulta un RNC o Cédula en el portal oficial de la DGII.

    Obtiene información oficial del contribuyente incluyendo razón social,
    nombre comercial, estado y si es facturador electrónico.

    Args:
        rnc_cedula: Número de RNC (9 dígitos) o Cédula (11 dígitos)

    Returns:
        Información del contribuyente:
        - vat: RNC/Cédula
        - razon_social: Nombre oficial
        - nombre_comercial: Nombre comercial
        - estado: Estado (ACTIVO, etc.)
        - es_facturador_electronico: True/False
        - tipo_identificacion: 'rnc' o 'cedula'

        O en caso de error:
        - error: Mensaje del error
    """
    try:
        models, uid, password = get_odoo()

        result = models.execute_kw(
            ODOO_DB, uid, password,
            'dgii.rnc.lookup.tools', 'consultar',
            [rnc_cedula]
        )

        return result

    except Exception as e:
        return {'error': f'Error consultando: {str(e)}'}


@mcp.tool()
def crear_cotizacion_dunet(
    plan_code: str,
    customer_email: str,
    customer_name: Optional[str] = "",
    customer_rnc: Optional[str] = "",
    include_certification: Optional[bool] = False
) -> dict:
    """
    Crea una cotización en Odoo para un plan de suscripción Dunet.

    Args:
        plan_code: Código del plan (emprendedor_monthly, basico_monthly,
                   estandar_monthly, premium_monthly, o _annual)
        customer_email: Email del cliente (requerido)
        customer_name: Nombre del cliente (opcional si hay RNC)
        customer_rnc: RNC o Cédula (opcional, consulta DGII automático)
        include_certification: Incluir certificación DGII $100

    Returns:
        success: True si se creó correctamente
        quotation_url: URL pública de la cotización
        quotation_id: Código de la cotización (QUO-00123)
        quotation_name: Nombre del plan
        total: Monto total
        validity_days: Días de validez
        customer_name: Nombre del cliente

        O en caso de error:
        success: False
        error: Mensaje del error
    """
    try:
        models, uid, password = get_odoo()

        result = models.execute_kw(
            ODOO_DB, uid, password,
            'quotation.creator.tools', 'crear_cotizacion',
            [plan_code, customer_email, customer_name, customer_rnc, include_certification]
        )

        return result

    except Exception as e:
        return {
            'success': False,
            'error': f'Error: {str(e)}'
        }


@mcp.get("/health")
def health_check():
    """Health check para Digital Ocean"""
    return {"status": "ok", "service": "dunet-fastmcp", "tools": 2}

if __name__ == "__main__":
    # Iniciar servidor FastMCP
    print("="*60)
    print("🚀 DUNET FASTMCP SERVER 2.0")
    print("="*60)
    print(f"📡 Odoo: {ODOO_URL}")
    print(f"💾 Database: {ODOO_DB}")
    print(f"👤 User: {ODOO_USERNAME}")
    print(f"🔌 Modo: HTTP (puerto 8070)")
    print("="*60)
    print(f"🛠️  Herramientas disponibles:")
    print(f"   1. consultar_rnc_dgii")
    print(f"   2. crear_cotizacion_dunet")
    print("="*60)
    print(f"✅ Servidor listo\n")

    # Correr en modo HTTP para que ElevenLabs se conecte
    mcp.run(transport='sse', port=8070, host='0.0.0.0')
