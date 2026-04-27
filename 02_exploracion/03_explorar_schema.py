"""
03_explorar_schema.py — Paso 2b: Explorar el schema completo de todos
los endpoints definidos en config.py.

Genera:
- Estructura del JSON raíz
- Schema de columnas con tipos de datos
- Alertas de calidad (nulos, tipos mixtos, listas)
- Código M sugerido listo para copiar a Power Query

Uso:
    python 02_exploracion/03_explorar_schema.py
"""

import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import _get, ENDPOINTS

# ─── Mapa de tipos Python → Power Query (M) ───────────────────────
TIPO_MAP = {
    "int64":   "Int64.Type",
    "float64": "type number",
    "object":  "type text",
    "bool":    "type logical",
}


def detectar_tipo_mixto(serie):
    try:
        tipos = serie.dropna().apply(
            lambda x: type(x).__name__ if not isinstance(x, list) else "list"
        ).unique()
        return list(tipos)
    except Exception:
        return ["indeterminado"]


def clasificar_estructura(data: dict) -> tuple:
    """Detecta si el JSON es lista, dict anidado o métrica plana."""
    for k, v in data.items():
        if isinstance(v, list):
            return "lista", k, len(v)
    for k, v in data.items():
        if isinstance(v, dict):
            return "dict_datos", k, len(v)
    return "metrica_plana", None, 1


def explorar_schema(nombre: str, endpoint: str, clave_lista: str):
    print(f"\n{'='*65}")
    print(f"  SCHEMA: {nombre}")
    print(f"  Endpoint: {endpoint}")
    print(f"{'='*65}")

    try:
        data = _get(endpoint)
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

    # Campos raíz
    print("\n📦 CAMPOS RAÍZ:")
    for k, v in data.items():
        if k != clave_lista:
            print(f"   {k}: {v}")

    # Extraer registros según tipo de estructura
    estructura, _, _ = clasificar_estructura(data)
    registros = data.get(clave_lista)

    if estructura == "metrica_plana" or clave_lista == "metrica_plana":
        # Tratar como un solo registro
        registros = [data]
    elif isinstance(registros, dict):
        registros = [{"key": k, "value": v} for k, v in registros.items()]

    if not registros:
        print(f"\n⚠️  Sin registros — endpoint bloqueado o vacío")
        print(f"   Agrega a ENDPOINTS comentado hasta que esté Live")
        return None

    df = pd.json_normalize(registros)
    print(f"\n📊 {len(df)} filas x {len(df.columns)} columnas")

    # Schema detallado
    print(f"\n📋 SCHEMA:")
    print(f"   {'Columna':<35} {'Tipo':<12} {'Nulos':<8} {'Únicos':<8} {'Ejemplo'}")
    print(f"   {'-'*35} {'-'*12} {'-'*8} {'-'*8} {'-'*25}")

    schema = []
    for col in df.columns:
        tipo      = str(df[col].dtype)
        nulos     = df[col].isna().sum()
        nulos_pct = f"{nulos/len(df)*100:.0f}%"
        try:
            unicos = df[col].apply(
                lambda x: str(x) if isinstance(x, list) else x
            ).nunique()
        except Exception:
            unicos = "N/A"
        ejemplo = str(df[col].dropna().iloc[0]) if len(df[col].dropna()) > 0 else "N/A"
        ejemplo = ejemplo[:30] + "..." if len(ejemplo) > 30 else ejemplo

        print(f"   {col:<35} {tipo:<12} {nulos_pct:<8} {str(unicos):<8} {ejemplo}")
        schema.append({
            "columna": col, "tipo_python": tipo,
            "nulos_pct": nulos_pct, "valores_unicos": unicos, "ejemplo": ejemplo
        })

    # Alertas de calidad
    print(f"\n⚠️  ALERTAS DE CALIDAD:")
    alertas = False
    for col in df.columns:
        nulos = df[col].isna().sum()
        if nulos > 0:
            print(f"   • '{col}' — {nulos} nulos ({nulos/len(df)*100:.0f}%)")
            alertas = True
        tipos_detectados = detectar_tipo_mixto(df[col])
        if len(tipos_detectados) > 1:
            print(f"   • '{col}' — tipos mixtos: {tipos_detectados}")
            alertas = True
        if df[col].dropna().apply(lambda x: isinstance(x, list)).any():
            print(f"   • '{col}' — contiene listas → requiere expansión en M")
            alertas = True
    if not alertas:
        print("   ✅ Sin alertas")

    # Tipos M sugeridos
    print(f"\n💡 TIPOS SUGERIDOS PARA POWER QUERY (M):")
    print(f"   Copia esto al archivo 03_power_query/{nombre.replace(' ','_').lower()}.m\n")
    print(f"   Table.TransformColumnTypes(Expand, {{")
    for item in schema:
        tipo_m = TIPO_MAP.get(item["tipo_python"], "type text")
        print(f'       {{"{item["columna"]}", {tipo_m}}},')
    print(f"   }})")

    print(f"\n  → Siguiente paso:")
    print(f"     Copia los tipos M y construye la consulta en:")
    print(f"     03_power_query/{nombre.replace(' ','_').lower()}.m")

    return df


# ─── Ejecutar todos los endpoints del diccionario ─────────────────
if __name__ == "__main__":
    print("\n" + "="*65)
    print("  PASO 2b — EXPLORAR SCHEMAS")
    print("="*65)

    resultados = {}
    for nombre, (endpoint, clave, tabla_odoo) in ENDPOINTS.items():
        df = explorar_schema(nombre, endpoint, clave)
        if df is not None:
            resultados[nombre] = df

    print(f"\n{'='*65}")
    print(f"  RESUMEN FINAL")
    print(f"{'='*65}")
    for nombre, df in resultados.items():
        print(f"  ✅ {nombre:<30} {len(df)} filas x {len(df.columns)} cols")

    print(f"\n  → Siguiente paso:")
    print(f"     Construye las consultas M en la carpeta 03_power_query/")
    print(f"     Guíate con las plantillas del README.md")