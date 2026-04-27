"""
config.py — Configuración base reutilizable para todos los scripts
Telas Real BI Project
"""

import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY  = os.getenv("TELAS_API_KEY")
BASE_URL = "https://d19o5nz7emxr7x.cloudfront.net"
HEADERS  = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

# ─── Endpoints de interés ─────────────────────────────────────────
# Formato: "Nombre": ("endpoint", "clave_json", "tabla_odoo")
ENDPOINTS = {
    # ── Live ──────────────────────────────────────────────────────
    "Catálogo Productos": (
        "/api/v1/products/catalog",
        "products",
        "product.template"
    ),
    "Telas Sublimables": (
        "/api/v1/products/sublimable",
        "fabrics",
        "product.template"
    ),
    "Clientes Summary": (
        "/api/v1/customers/summary",
        "by_store",
        "res.partner"
    ),
    "Sales by Store": (
        "/api/v1/sales/by-store",
        "stores", # CLAVE SUGERIDA POR 02_ver_claves.py
        "modelo.odoo"
    ),
    # ── Partial / Blocked — descomentar cuando estén disponibles ──
    # "Ventas Summary": (
    #     "/api/v1/sales/summary",
    #     "metrica_plana",
    #     "sale.order"
    # ),
    # "Inventario Stock": (
    #     "/api/v1/inventory/stock",
    #     "stock",
    #     "stock.quant"
    # ),
    # "Producción Summary": (
    #     "/api/v1/production/summary",
    #     "by_state",
    #     "mrp.production"
    # ),
}


def _get(endpoint: str, params: dict = None) -> dict:
    """Cliente HTTP base con manejo de errores."""
    if not API_KEY:
        raise ValueError("❌ TELAS_API_KEY no encontrada en .env")

    r = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=HEADERS,
        params=params or {},
        timeout=30
    )

    if r.status_code == 401:
        raise PermissionError("❌ API Key inválida")
    if r.status_code == 403:
        raise PermissionError("❌ Sin permisos para este endpoint")

    r.raise_for_status()
    return r.json()