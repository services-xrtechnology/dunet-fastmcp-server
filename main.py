#!/usr/bin/env python3
"""
Dunet FastMCP Server con Portal de Administración
Punto de entrada principal
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("="*70)
    print("🚀 DUNET FASTMCP SERVER CON PORTAL DE ADMINISTRACIÓN")
    print("="*70)
    print("\n📊 Portal Admin: http://localhost:8070")
    print("🔌 MCP Endpoint: http://localhost:8070/mcp")
    print("📚 API Docs: http://localhost:8070/docs")
    print("\n✅ Servidor iniciando...\n")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8070,
        reload=True,  # Auto-reload en desarrollo
        log_level="info"
    )
