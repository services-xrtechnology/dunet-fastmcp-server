"""
Base de datos SQLite para configuración
"""
import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict

DB_PATH = "database/dunet_fastmcp.db"

def init_db():
    """Inicializa la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla de configuración
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            odoo_url TEXT NOT NULL,
            odoo_db TEXT NOT NULL,
            odoo_username TEXT NOT NULL,
            odoo_password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabla de logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            level TEXT,
            tool_name TEXT,
            message TEXT,
            details TEXT
        )
    ''')

    # Tabla de herramientas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            enabled BOOLEAN DEFAULT 1,
            calls_count INTEGER DEFAULT 0,
            last_used TIMESTAMP
        )
    ''')

    # Insertar herramientas por defecto
    tools = [
        ('consultar_rnc_dgii', 'Consulta RNC/Cédula en portal DGII'),
        ('crear_cotizacion_dunet', 'Crea cotizaciones automáticas en Odoo')
    ]

    for tool_name, description in tools:
        cursor.execute('''
            INSERT OR IGNORE INTO tools (name, description)
            VALUES (?, ?)
        ''', (tool_name, description))

    conn.commit()
    conn.close()

def get_config() -> Optional[Dict]:
    """Obtiene configuración actual"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM config ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)
    return None

def save_config(config: Dict):
    """Guarda nueva configuración"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insertar nueva config
    cursor.execute('''
        INSERT INTO config (odoo_url, odoo_db, odoo_username, odoo_password, updated_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        config['odoo_url'],
        config['odoo_db'],
        config['odoo_username'],
        config['odoo_password'],
        datetime.now()
    ))

    conn.commit()
    conn.close()

def add_log(level: str, tool_name: str, message: str, details: str = ""):
    """Añade entrada al log"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO logs (level, tool_name, message, details)
        VALUES (?, ?, ?, ?)
    ''', (level, tool_name, message, details))

    conn.commit()
    conn.close()

def get_logs(limit: int = 100) -> List[Dict]:
    """Obtiene últimos logs"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM logs
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def increment_tool_usage(tool_name: str):
    """Incrementa contador de uso de herramienta"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE tools
        SET calls_count = calls_count + 1,
            last_used = ?
        WHERE name = ?
    ''', (datetime.now(), tool_name))

    conn.commit()
    conn.close()
