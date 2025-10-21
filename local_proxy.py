#!/usr/bin/env python3
"""
Proxy MCP Local para Claude Desktop
Conecta a servidor FastMCP remoto y lo expone como stdio
"""
import sys
import json
import asyncio
import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

REMOTE_SERVER = "http://173.230.131.241:8070/sse"

async def main():
    """Proxy que conecta stdio (Claude) con HTTP (servidor remoto)"""

    # Conectar al servidor remoto vía SSE
    async with httpx.AsyncClient() as http_client:
        async with ClientSession(
            read_stream=sys.stdin.buffer,
            write_stream=sys.stdout.buffer
        ) as session:

            # Conectar al servidor remoto
            await session.initialize()

            # Mantener conexión abierta
            while True:
                await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
