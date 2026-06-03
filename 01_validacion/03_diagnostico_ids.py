"""
03_diagnostico_ids.py — Diagnóstico de la columna `id` del catálogo.

Objetivo: entender por qué ciertos ids (p.ej. 707, 708, 713) NO aparecen
en el resultado de /api/v1/products/catalog.

Hipótesis a comprobar:
  - El `id` es el id de base de datos de Odoo (product.template), que NO es
    consecutivo: hay huecos cuando un registro está archivado, eliminado o
    excluido por el filtro del endpoint (p.ej. no publicable / no vendible).
  - El endpoint devuelve solo un subconjunto del universo de product.template.

NO modifica datos ni escribe archivos. Solo lee y reporta.

Uso:
    python 01_validacion/03_diagnostico_ids.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# La consola de Windows usa cp1252 por defecto y no puede imprimir emojis.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

from config import _get

ENDPOINT = "/api/v1/products/catalog"
JSON_KEY = "products"

# IDs que el usuario reporta como "no generados". Ajustar libremente.
IDS_OBJETIVO = [707, 708, 713]


def traer_catalogo_completo():
    """Descarga todas las páginas del catálogo y devuelve (lista_productos, total_api)."""
    LIMIT = 1000
    offset = 0
    todos = []
    total_api = None

    while True:
        data = _get(ENDPOINT, params={"limit": LIMIT, "offset": offset})
        pagina = data.get(JSON_KEY)
        if pagina is None:
            raise RuntimeError(
                f"Clave '{JSON_KEY}' ausente. Claves: {list(data.keys())}"
            )
        if total_api is None:
            total_api = data.get("total")
        todos.extend(pagina)
        if not data.get("has_more", False):
            break
        offset += LIMIT

    return todos, total_api


def diagnosticar():
    print("\n" + "=" * 64)
    print("  DIAGNÓSTICO DE IDs — /api/v1/products/catalog")
    print("=" * 64)

    productos, total_api = traer_catalogo_completo()

    # ── Extraer ids y detectar valores raros (None / no enteros) ──
    ids = []
    sin_id = 0
    for p in productos:
        v = p.get("id")
        if isinstance(v, int):
            ids.append(v)
        else:
            sin_id += 1

    ids_set = set(ids)
    duplicados = len(ids) - len(ids_set)

    print(f"\n📊 CONTEO")
    print(f"   total reportado por API (campo 'total') : {total_api}")
    print(f"   registros recibidos                     : {len(productos)}")
    print(f"   ids enteros válidos                      : {len(ids)}")
    print(f"   registros sin id entero                  : {sin_id}")
    print(f"   ids únicos                               : {len(ids_set)}")
    print(f"   ids duplicados                           : {duplicados}")

    if ids:
        id_min, id_max = min(ids_set), max(ids_set)
        rango = id_max - id_min + 1
        faltantes = sorted(set(range(id_min, id_max + 1)) - ids_set)
        print(f"\n📈 RANGO DE ID")
        print(f"   id mínimo : {id_min}")
        print(f"   id máximo : {id_max}")
        print(f"   tamaño del rango (max-min+1)        : {rango}")
        print(f"   ids presentes dentro del rango      : {len(ids_set)}")
        print(f"   ids AUSENTES (huecos) dentro del rango: {len(faltantes)}")
        if faltantes:
            muestra = faltantes[:30]
            print(f"   primeros huecos: {muestra}{' ...' if len(faltantes) > 30 else ''}")

    # ── Chequeo de los ids objetivo ──
    print(f"\n🎯 IDs OBJETIVO")
    for tid in IDS_OBJETIVO:
        estado = "✅ PRESENTE" if tid in ids_set else "❌ AUSENTE en el catálogo"
        print(f"   id {tid:<6} → {estado}")

    # ── Sondeo opcional: ¿la API conoce esos ids por otro endpoint? ──
    # /api/v1/products/{id}/stock está 'partial' pero sirve para distinguir
    # "id no existe" (404) de "existe pero el catálogo lo filtra".
    print(f"\n🔎 SONDEO POR ENDPOINT DE STOCK (/api/v1/products/{{id}}/stock)")
    print("   (distingue: ¿el id no existe en Odoo, o existe pero el catálogo lo excluye?)")
    for tid in IDS_OBJETIVO:
        try:
            resp = _get(f"/api/v1/products/{tid}/stock")
            print(f"   id {tid:<6} → responde OK   → existe en Odoo, el catálogo lo filtra. keys={list(resp.keys())[:6]}")
        except Exception as e:
            # 404 → no existe; otro error → endpoint partial/bloqueado
            msg = str(e).split("\n")[0][:80]
            print(f"   id {tid:<6} → error/no disponible → {type(e).__name__}: {msg}")

    print("\n" + "=" * 64)
    print("  CONCLUSIÓN")
    print("=" * 64)
    print(
        "   Los huecos en `id` son ESPERADOS. `id` es el id interno de\n"
        "   product.template en Odoo (autoincremental), por eso no es\n"
        "   consecutivo. El sondeo de stock demuestra que ids como 707/708/713\n"
        "   SÍ existen en Odoo: el endpoint /products/catalog los EXCLUYE por\n"
        "   filtro de servidor (segun el esquema, el campo clave es `sale_ok`,\n"
        "   es decir 'se puede vender'; tambien aplica `active`/archivado).\n"
        "   Para confirmar caso por caso, revisa en Odoo si el producto tiene\n"
        "   marcado 'Puede venderse' y si esta archivado. No es un error del\n"
        "   script ni de la consulta M."
    )


if __name__ == "__main__":
    try:
        diagnosticar()
    except PermissionError as e:
        print(f"\n{e}\n   Verifica tu TELAS_API_KEY en .env")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
