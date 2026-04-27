"""
02_ver_claves.py — Paso 2a: Inspeccionar las claves raíz de cualquier endpoint.

Usar cuando se agrega un endpoint nuevo al proyecto para saber
qué clave JSON contiene los datos antes de correr el explorador completo.

Uso:
    python 02_exploracion/02_ver_claves.py

Luego edita el endpoint en la variable ENDPOINT_A_INSPECCIONAR.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import _get

# ─── Cambia este valor para inspeccionar cualquier endpoint ───────
ENDPOINT_A_INSPECCIONAR = "/api/v1/sales/by-store"
# ──────────────────────────────────────────────────────────────────


def ver_claves(endpoint: str):
    print("\n" + "="*60)
    print("  PASO 2a — VER CLAVES DEL ENDPOINT")
    print("="*60)
    print(f"\n  Endpoint: {endpoint}\n")

    try:
        data = _get(endpoint)

        print(f"  {'Clave':<30} {'Tipo':<15} {'Preview'}")
        print(f"  {'-'*30} {'-'*15} {'-'*30}")

        clave_sugerida = None

        for k, v in data.items():
            tipo    = type(v).__name__
            preview = str(v)[:50] + "..." if len(str(v)) > 50 else str(v)

            # Identificar visualmente la clave con los datos
            if isinstance(v, list):
                tag = f"← DATOS ({len(v)} items)"
                if clave_sugerida is None:
                    clave_sugerida = k
            elif isinstance(v, dict):
                tag = f"← DATOS ({len(v)} keys)"
                if clave_sugerida is None:
                    clave_sugerida = k
            else:
                tag = ""

            print(f"  {k:<30} {tipo:<15} {preview}  {tag}")

        print(f"\n  💡 Clave sugerida para config.py: '{clave_sugerida}'")
        print(f"\n  Siguiente paso:")
        print(f"  → Agrega al diccionario ENDPOINTS en config.py:")
        print(f'    "{endpoint}": ("{endpoint}", "{clave_sugerida}", "modelo.odoo"),')
        print(f"  → Luego ejecuta: python 02_exploracion/03_explorar_schema.py")

    except Exception as e:
        print(f"  ❌ Error: {e}")


if __name__ == "__main__":
    ver_claves(ENDPOINT_A_INSPECCIONAR)