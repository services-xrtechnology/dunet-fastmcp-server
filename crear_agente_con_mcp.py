#!/usr/bin/env python3
import requests

API_KEY = "sk_c19f361c55961db4a61cc4ff9f9b022635671689b81b1187"
MCP_SERVER_URL = "http://173.230.131.241:8070/sse"

system_prompt = """# IDENTIDAD
Eres la asistente virtual de Dunet (pronuncia: Du-net).
Dunet ofrece Odoo (pronuncia: O-du), el ERP número uno del mundo.

# PRONUNCIACIÓN
- Dunet = Du-net
- Odoo = O-du
- DGII = Degi

# BENEFICIOS PRINCIPALES
1. AUTO-IMPLEMENTADO AL INSTANTE
2. FACTURACIÓN ELECTRÓNICA NATIVA

# HERRAMIENTAS MCP DISPONIBLES

Tienes 2 herramientas poderosas:

1. consultar_rnc_dgii(rnc_cedula)
USA cuando cliente dé RNC o Cédula.
Devuelve datos oficiales de Degi.

2. crear_cotizacion_dunet(plan_code, customer_email, customer_name, customer_rnc)
USA para crear cotización.

# PLANES
- emprendedor_monthly $60
- basico_monthly $100
- estandar_monthly $180
- premium_monthly $300

# FLUJO
Cliente: "Necesito facturar e inventario"
TÚ: "Plan Básico $100/mes. ¿Tienes RNC?"
Cliente: "131793916"
TÚ: [USA consultar_rnc_dgii("131793916")]
Sistema: {"razon_social": "XR TECHNOLOGY SRL"}
TÚ: "Encontré: XR TECHNOLOGY SRL. ¿Es tu empresa?"
Cliente: "Sí"
TÚ: "¿Email?"
Cliente: "juan@ejemplo.com"
TÚ: [USA crear_cotizacion_dunet("basico_monthly", "juan@ejemplo.com", "", "131793916")]
TÚ: "Listo: [URL cotización]"

# TONO
Natural, conversacional, enfoque en beneficios."""

payload = {
    "name": "Doonet",
    "conversation_config": {
        "agent": {
            "prompt": {
                "prompt": system_prompt,
                "llm": "gemini-2.0-flash-001",
                "temperature": 0.7,
                "max_tokens": 800,
                "native_mcp_server_ids": [MCP_SERVER_URL]
            },
            "first_message": "¡Hola! Soy la asistente de Dunet. Cuéntame, ¿cómo puedo ayudarte?",
            "language": "es"
        },
        "tts": {
            "model_id": "eleven_flash_v2_5",
            "voice_id": "FGY2WhTYpPnrIDTdsKH5",
            "optimize_streaming_latency": 4,
            "stability": 0.60,
            "similarity_boost": 0.75,
            "speed": 1.2
        },
        "conversation": {
            "max_duration_seconds": 600
        },
        "turn": {
            "turn_timeout": 5
        }
    }
}

headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}

print("🤖 Creando agente Doonet con servidor MCP integrado...")
print(f"   MCP Server: {MCP_SERVER_URL}")

response = requests.post(
    "https://api.elevenlabs.io/v1/convai/agents/create",
    headers=headers,
    json=payload
)

print(f"Status: {response.status_code}")

if response.status_code in [200, 201]:
    data = response.json()
    agent_id = data.get('agent_id')
    print(f"\n✅ ¡AGENTE CREADO CON MCP!")
    print(f"\n📋 Agent ID: {agent_id}")
    print(f"🔌 MCP Server conectado: {MCP_SERVER_URL}")
    print(f"🛠️  Herramientas disponibles:")
    print(f"   - consultar_rnc_dgii")
    print(f"   - crear_cotizacion_dunet")
    print(f"\n🎤 Pruébalo en: https://elevenlabs.io/app/conversational-ai")

    with open('AGENT_ID.txt', 'w') as f:
        f.write(agent_id)
    print(f"💾 ID guardado en AGENT_ID.txt")
else:
    print(f"❌ Error: {response.text}")
