#!/usr/bin/env python3
"""
Dunet FastMCP Server con Portal de Administración
Punto de entrada principal
"""
import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    # Puerto desde variable de entorno (Digital Ocean usa 8080)
    port = int(os.getenv('PORT', 8080))

    print("="*70)
    print("🚀 DUNET FASTMCP SERVER CON PORTAL DE ADMINISTRACIÓN")
    print("="*70)
    print(f"\n📊 Portal Admin: http://localhost:{port}")
    print(f"🔌 MCP Endpoint: http://localhost:{port}/mcp")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print("\n✅ Servidor iniciando...\n")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # No reload en producción
        log_level="info"
    )
