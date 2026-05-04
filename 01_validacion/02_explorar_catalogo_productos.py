"""
02_explorar_catalogo_productos.py — Consulta /api/v1/products/catalog
y muestra dimensiones y primeras filas del dataset.

Uso:
    python 01_validacion/02_explorar_catalogo_productos.py
"""

import sys
import os
import openpyxl
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from config import _get

ENDPOINT  = "/api/v1/products/catalog"
JSON_KEY  = "products"


def explorar_catalogo():
    print("\n" + "="*60)
    print("  CATÁLOGO DE PRODUCTOS — Exploración inicial")
    print("="*60)

    try:
        LIMIT   = 1000
        offset  = 0
        todos   = []

        while True:
            data = _get(ENDPOINT, params={"limit": LIMIT, "offset": offset})

            pagina = data.get(JSON_KEY)
            if pagina is None:
                claves = list(data.keys())
                print(f"\n⚠️  Clave '{JSON_KEY}' no encontrada.")
                print(f"   Claves disponibles en la respuesta: {claves}")
                return

            todos.extend(pagina)

            if offset == 0:
                print(f"\n🔬 DIAGNÓSTICO RAW — x_codigo_anterior (primeros 5 registros):")
                for i, prod in enumerate(pagina[:5]):
                    val  = prod.get("x_codigo_anterior", "⚠️ CAMPO AUSENTE")
                    tipo = type(val).__name__
                    # Mostrar bytes exactos del nombre del campo para detectar caracteres invisibles
                    clave_bytes = "x_codigo_anterior".encode("utf-8").hex()
                    print(f"   [{i}] tipo={tipo!r:10}  valor={val!r}  (clave hex={clave_bytes})")

            total    = data.get("total", "?")
            has_more = data.get("has_more", False)
            print(f"   Página offset={offset:>5} → {len(pagina)} registros  |  total API: {total}  |  has_more: {has_more}")

            if not has_more:
                break
            offset += LIMIT

        df = pd.DataFrame(todos)

        print(f"\n📐 DIMENSIONES:")
        print(f"   Filas   : {df.shape[0]:,}")
        print(f"   Columnas: {df.shape[1]}")

        print(f"\n🔍 PRIMERAS 10 FILAS:")
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", 120)
        print(df.head(10).to_string(index=True))

        df.to_excel("validar.xlsx", index=False)

        print(f"\n📋 COLUMNAS DISPONIBLES ({df.shape[1]}):")
        for col in df.columns:
            print(f"   • {col}  [{df[col].dtype}]")

    except PermissionError as e:
        print(f"\n{e}")
        print("   Verifica tu TELAS_API_KEY en el archivo .env")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


if __name__ == "__main__":
    explorar_catalogo()
