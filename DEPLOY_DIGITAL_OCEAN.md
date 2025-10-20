# 🚀 DEPLOY EN DIGITAL OCEAN APP PLATFORM

Guía paso a paso para desplegar Dunet FastMCP Server en Digital Ocean.

---

## 📋 PRERREQUISITOS

1. ✅ Cuenta de Digital Ocean
2. ✅ Repositorio GitHub (ya creado): https://github.com/services-xrtechnology/dunet-fastmcp-server
3. ✅ Módulo Odoo `xr_fastmcp_doonet` instalado

---

## 🎯 PASO A PASO

### PASO 1: Subir código a GitHub

**Ya está listo** en el repositorio. Solo asegúrate de hacer commit y push de todos los archivos desde GitHub Desktop.

### PASO 2: Crear App en Digital Ocean

1. Ve a: https://cloud.digitalocean.com/apps
2. Click **"Create App"**
3. Selecciona **"GitHub"**
4. Autoriza acceso a tu cuenta GitHub si es primera vez
5. Selecciona repositorio: **services-xrtechnology/dunet-fastmcp-server**
6. Branch: **main**
7. Autodeploy: **Activado** ✅
8. Click **"Next"**

### PASO 3: Configurar App

Digital Ocean detectará automáticamente el archivo `.do/app.yaml`.

**Verificar:**
- **Name:** dunet-fastmcp-server
- **Region:** New York (o el que prefieras)
- **Plan:** Basic ($5/mes)

Click **"Next"**

### PASO 4: Configurar Variables de Entorno

**IMPORTANTE:** Configura estos valores:

| Variable | Valor | Tipo |
|----------|-------|------|
| `ODOO_URL` | `https://robust-briefly-mink.ngrok-free.app` | Text |
| `ODOO_DB` | `doonet` | Text |
| `ODOO_USERNAME` | `xavier@xrtechnology.com.do` | Text |
| `ODOO_PASSWORD` | `Santodomingo2828.` | **SECRET** |

**Marcar ODOO_PASSWORD como SECRET** (encriptado)

Click **"Next"**

### PASO 5: Review y Deploy

1. Revisar configuración
2. Click **"Create Resources"**
3. Esperar 3-5 minutos mientras deploya

---

## ✅ VERIFICAR QUE FUNCIONA

### Una vez desplegado:

Digital Ocean te dará una URL como:
```
https://dunet-fastmcp-server-xxxxx.ondigitalocean.app
```

### Probar:

**1. Portal Admin:**
```
https://dunet-fastmcp-server-xxxxx.ondigitalocean.app
```

Deberías ver el dashboard con estado del servidor.

**2. MCP Endpoint:**
```
https://dunet-fastmcp-server-xxxxx.ondigitalocean.app/mcp
```

**3. API Status:**
```bash
curl https://dunet-fastmcp-server-xxxxx.ondigitalocean.app/api/status
```

Debería devolver:
```json
{
  "server_running": true,
  "configured": true,
  "tools_active": 2
}
```

---

## 🔌 CONECTAR CON ELEVENLABS

### PASO 1: Copiar URL MCP
En el portal admin, copia la URL MCP (botón "Copiar")

### PASO 2: Dashboard ElevenLabs
1. Ve a: https://elevenlabs.io/app/conversational-ai
2. Abre tu agente "Doonet"
3. Pestaña **"Agent"** → sección **"Tools"**

### PASO 3: Añadir MCP Server
1. Click **"Add Tool"** → **"MCP Server"**
2. **URL:** `https://dunet-fastmcp-server-xxxxx.ondigitalocean.app/mcp`
3. **Save**

### PASO 4: Seleccionar Herramientas
Marca:
- ✅ consultar_rnc_dgii
- ✅ crear_cotizacion_dunet

### PASO 5: Actualizar System Prompt

Añade al prompt del agente:

```
# HERRAMIENTAS MCP

Tienes 2 herramientas:

1. consultar_rnc_dgii(rnc_cedula)
Úsala cuando cliente dé RNC/Cédula.

2. crear_cotizacion_dunet(plan_code, customer_email, customer_name, customer_rnc)
Úsala para crear cotización automática.

# FLUJO:
Cliente: "Necesito facturar e inventario"
TÚ: "Plan Básico $100/mes. ¿Tienes RNC?"
Cliente: "131793916"
TÚ: [USA consultar_rnc_dgii("131793916")]
Sistema: {"razon_social": "XR TECHNOLOGY SRL"}
TÚ: "Encontré: XR TECHNOLOGY SRL. ¿Es tu empresa?"
Cliente: "Sí, ¿email?"
Cliente: "juan@ejemplo.com"
TÚ: [USA crear_cotizacion_dunet("basico_monthly", "juan@ejemplo.com", "", "131793916")]
Sistema: {"quotation_url": "www.doonet.app/my/quotes/3"}
TÚ: "Listo: www.doonet.app/my/quotes/3"
```

---

## 🎉 ¡LISTO!

Tu agente de ElevenLabs ahora puede:
- ✅ Consultar RNC en DGII
- ✅ Crear cotizaciones automáticas
- ✅ Todo desde conversación de voz

---

## 📊 MONITOREO

### Ver logs en vivo:
`https://dunet-fastmcp-server-xxxxx.ondigitalocean.app/logs`

### Ver estado:
`https://dunet-fastmcp-server-xxxxx.ondigitalocean.app`

### Métricas Digital Ocean:
Dashboard de Digital Ocean muestra uso de CPU, memoria, requests.

---

## 🔄 ACTUALIZAR

Cualquier cambio que hagas en GitHub y hagas push, Digital Ocean lo deploya automáticamente en 2-3 minutos.

---

## 💡 PRÓXIMOS PASOS

1. ✅ Deploy completado
2. ⏳ Probar herramientas desde portal
3. ⏳ Conectar ElevenLabs
4. ⏳ Probar conversación completa
5. ⏳ Monitorear logs

---

**¡Tu servidor FastMCP está listo para producción!** 🎊
