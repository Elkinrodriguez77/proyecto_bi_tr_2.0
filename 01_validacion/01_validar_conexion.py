"""
01_validar_conexion.py — Paso 1: Verificar que la API Key es válida
y ver el estado en tiempo real de todos los endpoints.

Ejecutar primero siempre antes de cualquier otro script.

Uso:
    python 01_validacion/01_validar_conexion.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# La consola de Windows usa cp1252 por defecto y no puede imprimir emojis
# (✅, ❌, etc.). Forzamos UTF-8 en la salida para evitar UnicodeEncodeError.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

from config import _get


def validar_conexion():
    print("\n" + "="*60)
    print("  PASO 1 — VALIDAR CONEXIÓN")
    print("="*60)

    try:
        data = _get("/api/v1/meta/readiness")

        print(f"\n✅ Conexión exitosa")
        print(f"   Snapshot date : {data['snapshot_date']}")
        print(f"   Endpoints Live: {data['overall_summary']['live']}")
        print(f"   Partial       : {data['overall_summary']['partial']}")
        print(f"   Blocked       : {data['overall_summary']['blocked']}")

        print(f"\n📋 ESTADO POR ENDPOINT:")
        print(f"   {'Endpoint':<45} {'Estado'}")
        print(f"   {'-'*45} {'-'*10}")

        for endpoint, info in data["endpoints"].items():
            estado  = info.get("status", "?")
            icono   = "✅" if estado == "live" else ("🟡" if estado == "partial" else "🔴")
            blocker = f" ← {info['blocker']}" if "blocker" in info else ""
            print(f"   {endpoint:<45} {icono} {estado}{blocker}")

        return True

    except PermissionError as e:
        print(f"\n{e}")
        print("   Verifica tu TELAS_API_KEY en el archivo .env")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False


if __name__ == "__main__":
    ok = validar_conexion()
    if ok:
        print("\n✅ Listo para continuar con el Paso 2")
        print("   → Ejecuta: python 01_validacion/02_explorar_catalogo_productos.py")
    else:
        print("\n❌ Corrige la conexión antes de continuar")