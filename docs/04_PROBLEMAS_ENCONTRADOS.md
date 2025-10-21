# ⚠️ PROBLEMAS ENCONTRADOS - PROYECTO FASTMCP

**Fecha:** 20 Octubre 2025

---

## 🔴 PROBLEMAS TÉCNICOS

### 1. ElevenLabs requiere HTTPS obligatorio ⚠️

**Problema:**
ElevenLabs no acepta servidores MCP con HTTP, solo HTTPS.

**Mensaje error:**
```
"URL must use HTTPS"
```

**Soluciones intentadas:**
- ✅ ngrok (funciona, temporal)
- ⏳ Let's Encrypt (pendiente, permanente)
- ⏳ Cloudflare Tunnel (pendiente)

**Impacto:** Añade complejidad al deploy

---

### 2. FastMCP Cloud caído 🔴

**Problema:**
El servicio oficial https://fastmcp.cloud no respondía durante el desarrollo.

**Síntomas:**
- Website muy lento
- No carga dashboard
- Timeout en requests

**Solución:** Deploy propio en Linode

**Nota:** FastMCP Cloud es beta, puede tener problemas de disponibilidad

---

### 3. Digital Ocean App Platform incompatible ⚠️

**Problema:**
Digital Ocean no puede correr FastMCP correctamente.

**Errores encontrados:**
- Health checks fallan (FastMCP usa SSE/WebSocket)
- Puerto 8080 vs 8070 (conflictos)
- FastAPI + FastMCP integración compleja

**Intentos:**
- app.yaml custom
- Procfile
- Cambio de puertos
- Health check paths diferentes

**Resultado:** No funcionó confiablemente

**Solución:** Servidor dedicado (Linode) con systemd

---

### 4. Claude Desktop no soporta MCP remoto fácilmente ⚠️

**Problema:**
Claude Desktop solo funciona con comandos locales (stdio), no con URLs HTTP remotas.

**Error:**
```
Server disconnected
```

**Razón:** Claude Desktop espera `command` local, no `url` remota

**Soluciones evaluadas:**
- Proxy local con curl
- Cliente MCP personalizado
- npx @modelcontextprotocol/client-sse

**Estado:** No resuelto completamente

**Workaround:** Cliente necesita instalar proxy local

---

### 5. Python 3.9 incompatible con FastMCP ⚠️

**Problema:**
FastMCP requiere Python 3.10+

**En Mac local:** Python 3.9 (sistema)
**Solución:** Usar Python del Docker (3.10+) o servidor remoto

---

### 6. Conflictos de dependencias Python 🟡

**Problema:**
`typing-extensions` instalado por sistema conflictúa con pip

**Error:**
```
Cannot uninstall typing_extensions 4.10.0, RECORD file not found
```

**Solución:**
```bash
pip install --ignore-installed typing-extensions
# o
pip install --break-system-packages
```

---

### 7. Ubuntu 24.04 externally-managed-environment 🟡

**Problema:**
Ubuntu 24.04 protege instalación global de paquetes Python

**Error:**
```
error: externally-managed-environment
```

**Solución:**
- Usar virtual environment (recomendado)
- O `--break-system-packages` (para servidores dedicados)

---

### 8. Git merge conflicts en repositorio 🟡

**Problema:**
Repositorio GitHub tenía README inicial que conflictúa con nuestros archivos

**Soluciones:**
- git pull --allow-unrelated-histories
- Resolver conflicts manualmente
- GitHub Desktop ayuda visualmente

---

### 9. ElevenLabs API para MCP no documentada 🔴

**Problema:**
Endpoint `/v1/convai/mcp/create` existe en docs pero devuelve 404

**Intentado:**
```python
POST https://api.elevenlabs.io/v1/convai/mcp
```

**Resultado:** Not Found

**Solución actual:** Configuración manual desde dashboard web

**Impacto:** No se puede automatizar completamente vía API

---

### 10. FastMCP con FastAPI integración compleja 🟡

**Problema:**
Integrar FastMCP dentro de FastAPI (para portal admin) es complicado

**Error:**
```python
from fastmcp.server import create_sse_handler
ImportError: cannot import name 'create_sse_handler'
```

**Razón:** API cambió en FastMCP 2.0

**Solución:** Correr FastMCP separado, no integrado en FastAPI

---

## 🟢 SOLUCIONES QUE FUNCIONARON

### 1. systemd + venv ✅
**Mejor práctica Linux.** Cada servicio en su entorno virtual.

### 2. ngrok para HTTPS temporal ✅
**Funciona perfecto** para desarrollo y pruebas.

### 3. Linode API para crear servidores ✅
**Automatización completa** de infraestructura.

### 4. FastMCP HTTP Streamable ✅
**Nuevo estándar MCP 2025.** Más robusto que SSE.

### 5. Repositorio GitHub separado ✅
**Código limpio**, sin mezclar con otros proyectos.

---

## 📊 RESUMEN DE PROBLEMAS

| Problema | Severidad | Estado | Solución |
|----------|-----------|--------|----------|
| HTTPS requerido | Alta | Resuelto | ngrok temporal |
| FastMCP Cloud caído | Media | Workaround | Deploy propio |
| Digital Ocean incompatible | Media | Abandonado | Usar Linode |
| Claude Desktop remoto | Media | Pendiente | Proxy local |
| Python 3.9 | Baja | Resuelto | Usar 3.10+ |
| typing-extensions | Baja | Resuelto | --ignore-installed |
| Ubuntu 24.04 pip | Baja | Resuelto | venv |
| Git conflicts | Baja | Resuelto | Manual |
| ElevenLabs MCP API | Media | Workaround | Dashboard web |
| FastAPI integración | Media | Workaround | Servicios separados |

---

## 💡 LECCIONES APRENDIDAS

1. **HTTPS es obligatorio** para servicios cloud (ElevenLabs)
2. **systemd es la forma correcta** en Linux (no Docker necesariamente)
3. **Virtual environments siempre** (evita conflictos)
4. **FastMCP Cloud es nuevo** (puede tener downtime)
5. **MCP es estándar emergente** (aún inmaduro en algunos aspectos)
6. **Documentación es clave** (APIs cambian rápido)
7. **Empezar simple** (no multi-tenant desde día 1)

---

## 🔄 AJUSTES REALIZADOS

### De SSE a HTTP Streamable:
- **Antes:** `mcp.run(transport='sse')`
- **Después:** `mcp.run(transport='http', path='/mcp')`
- **Razón:** Estándar MCP 2025, mejor compatibilidad

### De Python -m fastmcp a ejecutable directo:
- **Antes:** `python3 -m fastmcp run ...`
- **Después:** `fastmcp run ...` o `python3 simple_server.py`
- **Razón:** Comandos más simples

### De puertos variables a fijos:
- **Puerto FastMCP:** 8070 (fijo)
- **Puerto Admin:** 8000 (fijo)
- **Nginx:** 80/443
- **Razón:** Evitar confusiones

---

**Próximo documento:** `05_PROXIMOS_PASOS.md`
