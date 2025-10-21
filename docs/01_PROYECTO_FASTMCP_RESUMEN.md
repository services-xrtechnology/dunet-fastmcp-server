# 📋 PROYECTO FASTMCP DUNET - RESUMEN EJECUTIVO

**Fecha Inicio:** 20 Octubre 2025
**Estado:** En pausa - Reevaluando arquitectura
**Autor:** XR Technology

---

## 🎯 ¿QUÉ ES ESTE PROYECTO?

Sistema de herramientas MCP (Model Context Protocol) que permite a agentes de IA (ElevenLabs, Claude, ChatGPT) interactuar con Odoo para:

1. **Consultar RNC/Cédula** en portal DGII automáticamente
2. **Crear cotizaciones** en Odoo desde conversaciones de voz/chat
3. **Automatizar ventas** con IA conversacional

---

## 💡 OBJETIVO ORIGINAL

### Para Dunet (Uso interno):
Agente de voz de ElevenLabs que puede:
- Atender clientes 24/7
- Consultar datos fiscales en DGII
- Crear cotizaciones al instante
- Cerrar ventas automáticamente

### Para el futuro (Modelo SaaS):
Vender el servicio a otros negocios:
- Cliente paga $20-50/mes
- Instala módulo Odoo
- Se conecta a nuestro servidor FastMCP
- Sus agentes de IA acceden a su Odoo

---

## 🏗️ COMPONENTES DEL PROYECTO

### 1. Módulo Odoo: `xr_fastmcp_doonet`
**Ubicación:** `/Users/trabajo/Desktop/MacMini/Desarrollo-Odoo/desarrollo_personalizado/sub-desarrollo1/xr_fastmcp_doonet/`

**Modelos:**
- `dgii.rnc.lookup.tools` - Consulta RNC en DGII
- `quotation.creator.tools` - Crea cotizaciones

### 2. Servidor FastMCP
**Ubicación:** Este repositorio
**Archivo principal:** `simple_server.py`

**Herramientas:**
- `consultar_rnc_dgii(rnc_cedula)`
- `crear_cotizacion_dunet(plan_code, email, name, rnc)`

### 3. Infraestructura
**Servidor Linode:**
- IP: 173.230.131.241
- Ubuntu 24.04
- FastMCP instalado con systemd
- ngrok para HTTPS

---

## 💰 MODELO DE NEGOCIO FUTURO

### Producto: "XR AI Tools for Odoo"

**Tier 1: Basic ($20/mes)**
- consultar_rnc_dgii
- crear_cotizacion
- crear_lead_crm

**Tier 2: Pro ($40/mes)**
- Todo Tier 1 +
- crear_factura
- consultar_inventario
- reportes_basicos

**Tier 3: Enterprise ($80/mes)**
- Todo Tier 2 +
- analisis_financiero
- reportes_personalizados
- integraciones_custom

**Ventaja:** Ingresos recurrentes, escalable, barrera de salida alta.

---

## 📊 ESTADO ACTUAL

### ✅ LO QUE FUNCIONA:
- Servidor FastMCP corriendo
- 2 herramientas implementadas
- Conexión a Odoo vía XML-RPC
- systemd configurado
- ngrok para HTTPS

### ⏸️ LO QUE FALTA:
- Integración completa con ElevenLabs
- Portal de administración
- SSL permanente
- Sistema multi-tenant
- Base de datos PostgreSQL

---

## 🔄 DECISIÓN PENDIENTE

**Opción A: Continuar con FastMCP**
- Pro: Estándar universal (Claude, ChatGPT, ElevenLabs)
- Contra: Complejo, problemas de compatibilidad

**Opción B: Server Tools de ElevenLabs**
- Pro: Simple, funciona YA, bien documentado
- Contra: Solo ElevenLabs (vendor lock-in)

**Recomendación:** Empezar con Server Tools (Opción B) para Dunet.
Después evaluar FastMCP para vender como producto.

---

## 📝 PRÓXIMOS PASOS

Ver documento: `05_PROXIMOS_PASOS.md`

---

**Fecha:** 20 Octubre 2025
**Para retomar:** Leer esta carpeta `/docs/` completa
