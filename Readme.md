# Accesos importantes:

| Descripción | Path Local | URL (Si aplica) |
| ------- | ------- | ------- |
| Nuevo portal web (código fuente) | OneDrive\Data World\Clientes\Telas Real\proyecto_bi | [Git Hub](https://github.com/Elkinrodriguez77/telasreal_portalbi) | 
| Dash PBI Comercial | OneDrive\Data World\Clientes\Telas Real\BI | Sin públicar en portal web aún |
| Solicitudes de ajustes comerciales | OneDrive\Data World\Clientes\Telas Real\Backlog_Solicitudes | [Enlace OneDrive](https://1drv.ms/w/c/7922b0b09328d329/IQBcH_EvrZ5qSbp1TC07eSFiAbbKKj87WH94MXCDVyxGFuQ?e=9ubFuB) |


# Telas Real — Proyecto BI
**Integración API Odoo → Python → Power Query → Power BI Service**

> **Fuente de verdad:** Odoo vía XML-RPC  
> **Base URL:** `https://d19o5nz7emxr7x.cloudfront.net`  
> **Autenticación:** `Authorization: Bearer <API_KEY>`  
> **Última actualización:** Abril 2026

---

## Estructura del proyecto

```
TelasReal_BI/
│
├── config.py                          ← Configuración central (endpoints, cliente HTTP)
├── .env                               ← API Key (NO subir al repo)
├── .gitignore
│
├── 01_validacion/
│   └── 01_validar_conexion.py         ← PASO 1: Verificar API Key y estado de endpoints
│
├── 02_exploracion/
│   ├── 02_ver_claves.py               ← PASO 2a: Inspeccionar claves de un endpoint nuevo
│   └── 03_explorar_schema.py          ← PASO 2b: Schema completo + tipos M sugeridos
│
├── 03_power_query/
│   └── consultas_m.m                  ← PASO 3: Consultas M listas para Power BI Desktop
│
└── 04_documentacion/
    └── README.md                      ← Este archivo
```

---

## Instalación

```bash
# 1. Instalar dependencias
pip install requests pandas python-dotenv

# 2. Crear archivo .env en la raíz del proyecto
echo "TELAS_API_KEY=tu_api_key_aqui" > .env
```

---

## Flujo de trabajo

```
┌─────────────────────────────────────────────────────────────┐
│  PASO 1  Validar conexión     → 01_validar_conexion.py      │
│  PASO 2a Ver claves           → 02_ver_claves.py            │
│  PASO 2b Explorar schema      → 03_explorar_schema.py       │
│  PASO 3  Construir consulta M → consultas_m.m               │
│  PASO 4  Probar en Desktop    → Power BI Desktop            │
│  PASO 5  Publicar en Service  → Scheduled Refresh           │
└─────────────────────────────────────────────────────────────┘
```

---

## PASO 1 — Validar conexión

**Archivo:** [`01_validacion/01_validar_conexion.py`](/01_validacion/01_validar_conexion.py)

Verifica que tu API Key es válida y muestra el estado actual de
todos los endpoints en tiempo real.

```bash
python 01_validacion/01_validar_conexion.py
```

**Output esperado:**
```
✅ Conexión exitosa
   Snapshot date : 2026-04-13
   Endpoints Live: 11
   Partial       : 4
   Blocked       : 8
```

> ⚠️ Si falla aquí, no continúes. Verifica tu `.env` y la API Key.

---

## PASO 2a — Ver claves de un endpoint nuevo

**Archivo:** [`02_exploracion/02_ver_claves.py`](/02_exploracion/02_ver_claves.py)

Usar cada vez que agregues un endpoint nuevo al proyecto.
Edita la variable `ENDPOINT_A_INSPECCIONAR` en el archivo y ejecuta:

```bash
python 02_exploracion/02_ver_claves.py
```

**Output esperado:**
```
Claves raíz de /api/v1/products/catalog:
  'products' (list): [{'id': 368, 'name': 'ACETATO...  ← DATOS (50 items)
  'count'    (int):  50
  
💡 Clave sugerida para config.py: 'products'
```

**Después de correrlo:**
1. Copia la clave sugerida
2. Agrégala al diccionario `ENDPOINTS` en [`config.py`](../config.py)

---

## PASO 2b — Explorar schema completo

**Archivo:** [`02_exploracion/03_explorar_schema.py`](/02_exploracion/03_explorar_schema.py)

Analiza todos los endpoints definidos en `config.py` y genera el
schema con tipos de datos y código M sugerido.

```bash
python 02_exploracion/03_explorar_schema.py
```

**Output esperado:**
```
📋 SCHEMA:
   Columna                             Tipo         Nulos    Únicos   Ejemplo
   id                                  int64        0%       50       368
   name                                object       0%       50       ACETATO AZUL CIELO C#45
   list_price                          float64      0%       8        14500.0
   ...

⚠️  ALERTAS DE CALIDAD:
   • 'uom_id' — contiene listas → requiere expansión en M

💡 TIPOS SUGERIDOS PARA POWER QUERY (M):
   Table.TransformColumnTypes(Expand, {
       {"id",         Int64.Type},
       {"name",       type text},
       ...
   })
```

**Después de correrlo:**
1. Copia los tipos M sugeridos del output
2. Construye la consulta en `03_power_query/consultas_m.m`

---

## PASO 3 — Construir consulta Power Query (M)

**Archivo:** [`03_power_query/consultas_m.m`](/03_power_query/consultas_m.m)

Contiene las consultas M listas para cada endpoint.

### Regla crítica — siempre usar `RelativePath`

```m
// ❌ INCORRECTO — PBI Service no puede refrescar
Web.Contents("https://dominio.com/api/v1/endpoint", [Headers = [...]])

// ✅ CORRECTO — PBI Service refresca sin Gateway
Web.Contents("https://dominio.com", [RelativePath = "api/v1/endpoint", Headers = [...]])
```

### Consultas disponibles

| Consulta | Estado | Archivo |
|---|---|---|
| Catálogo de Productos | ✅ Lista | `consultas_m.m` → sección productos_catalogo |
| Telas Sublimables | ✅ Lista | `consultas_m.m` → sección telas_sublimables |
| Clientes por Tienda | ✅ Lista | `consultas_m.m` → sección clientes_por_tienda |
| Ventas Summary | 🔴 Pendiente | Descomentar cuando haya `sale.order` en Odoo |
| Inventario Stock | 🟡 Pendiente | Descomentar cuando se cargue stock inicial |
| Producción Summary | 🔴 Pendiente | Descomentar cuando se configuren work centers |

---

## PASO 4 — Probar en Power BI Desktop

1. Abre Power BI Desktop
2. `Inicio → Transformar datos → Editor avanzado`
3. Pega la consulta M del archivo `consultas_m.m`
4. Reemplaza `TU_API_KEY_AQUI` con tu key real
5. Verifica que la tabla carga correctamente

---

## PASO 5 — Publicar en Power BI Service

### Configuración de credenciales

| Campo | Valor |
|---|---|
| Authentication method | `Anonymous` |
| Privacy level | `Organizational` |
| Skip test connection | ✅ **Marcado obligatorio** |

> **¿Por qué Anonymous?** PBI Service no soporta custom headers en
> su interfaz de credenciales. La API Key viaja en el código M.
> El test falla porque la API no expone endpoint raíz `/` — es normal.

### Programar refresh automático

1. Dataset → `...` → **Configuración**
2. **Actualización programada** → Activar
3. Zona horaria: `UTC-05:00 Bogotá`
4. Frecuencia: **Diaria 6:00 AM**
5. **Aplicar**

### Validar refresh

```
Dataset → ... → Actualizar ahora → Historial de actualización → ✅ Correcta
```

---

## Cómo agregar un endpoint nuevo

```
1. Ejecutar PASO 1 → confirmar que el endpoint está Live en readiness

2. Editar 02_ver_claves.py:
   ENDPOINT_A_INSPECCIONAR = "/api/v1/nuevo_endpoint"
   → Ejecutar → anotar la clave JSON sugerida

3. Agregar a config.py → ENDPOINTS:
   "Nombre": ("/api/v1/nuevo_endpoint", "clave_json", "modelo.odoo")

4. Ejecutar 03_explorar_schema.py
   → Copiar los tipos M del output

5. Agregar nueva sección en consultas_m.m
   → Usar la plantilla base + tipos M copiados

6. Probar en Power BI Desktop → publicar
```

---

## Bugs y limitaciones conocidas

### Bug — Paginación rota en `/api/v1/products/catalog`

| Campo | Detalle |
|---|---|
| Detectado | Abril 2026 |
| Reportado a | Emmanuel (dev API) |
| Estado | ⏳ Pendiente corrección |

**Problema:** El parámetro `offset` es ignorado — siempre devuelve
los mismos 50 registros causando loop infinito al paginar.

**Evidencia:**
```
offset=0   → IDs: [368, 369, 370...] ← siempre igual
offset=50  → IDs: [368, 369, 370...] ← siempre igual
offset=100 → IDs: [368, 369, 370...] ← siempre igual
```

**Impacto:** La documentación indica 93 productos en Odoo,
solo 50 son accesibles vía API actualmente.

**Corrección solicitada a Emmanuel:**
```json
// Agregar campo total al response:
{ "products": [...], "count": 50, "total": 93 }
// Y que offset funcione, o aceptar limit=1000
```

---

## Estado de endpoints (Abril 2026)

| Endpoint | Estado | ETA |
|---|---|---|
| `/api/v1/products/catalog` | ✅ Live | — |
| `/api/v1/products/sublimable` | ✅ Live | — |
| `/api/v1/customers/summary` | ✅ Live | — |
| `/api/v1/customers/lookup` | ✅ Live | — |
| `/api/v1/inventory/stock` | 🟡 Partial | Cliente/Alejo |
| `/api/v1/sales/summary` | 🔴 Blocked | Al iniciar ventas |
| `/api/v1/sales/by-store` | 🔴 Blocked | Al iniciar ventas |
| `/api/v1/sales/by-product` | 🔴 Blocked | Al iniciar ventas |
| `/api/v1/sales/trend` | 🔴 Blocked | Al iniciar ventas |
| `/api/v1/production/summary` | 🔴 Blocked | W6-W12 |
| `/api/v1/inventory/alerts` | 🔴 Blocked | Cliente/Alejo |
| `/api/v1/customers/top` | 🔴 Blocked | Al iniciar ventas |

---

*Documentación mantenida por el equipo BI — Telas Real 2026*