# Accesos importantes:

| Descripción | Path Local | URL (Si aplica) |
| ------- | ------- | ------- |
| Nuevo portal web (código fuente) | OneDrive\Data World\Clientes\Telas Real\proyecto_bi | [Git Hub](https://github.com/Elkinrodriguez77/telasreal_portalbi) | 
| Dash PBI Comercial | OneDrive\Data World\Clientes\Telas Real\BI | Sin públicar en portal web aún |
| Solicitudes de ajustes comerciales | OneDrive\Data World\Clientes\Telas Real\Backlog_Solicitudes | [Enlace OneDrive](https://1drv.ms/w/c/7922b0b09328d329/IQBcH_EvrZ5qSbp1TC07eSFiAbbKKj87WH94MXCDVyxGFuQ?e=9ubFuB) |
| Requerimientos globales de reportes | No Aplica | [Enlace Drive](https://docs.google.com/spreadsheets/d/1CShe2RY7EFQ6s0m8tUqLUXv9_qt4iy-SsJTllQ--jk8/edit?usp=sharing) |


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
│  PASO 2  Construir consulta M → consultas_m.m               │
│  PASO 3  Probar en Desktop    → Power BI Desktop            │
│  PASO 4  Publicar en Service  → Scheduled Refresh           │
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

## PASO 2 — Construir consulta Power Query (M)

**Archivo:** [`02_power_query/consultas_m.m`](/02_power_query/consultas_m.m)

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

## Mapeo de consultas Python → Power Query (M)

Cada script de exploración en Python tiene su consulta M equivalente lista para Power BI.
Úsalos en paralelo: Python para verificar los datos en terminal, M para cargarlos en el modelo.

| Script Python | Archivo M | Endpoint | Descripción | Estado |
|---|---|---|---|---|
| [`01_validacion/02_explorar_catalogo_productos.py`](/01_validacion/02_explorar_catalogo_productos.py) | [`02_power_query/catalogo_productos.m`](/02_power_query/catalogo_productos.m) | `/api/v1/products/catalog` | Catálogo completo de productos: precio, stock disponible, código interno, unidad de medida, categoría, rendimiento y código alfanumérico. Paginación automática — trae todos los registros aunque el catálogo crezca. | ✅ Lista |

> A medida que se activen nuevos endpoints, agregar aquí la fila correspondiente siguiendo el mismo patrón.

---

## PASO 3 — Probar en Power BI Desktop

1. Abre Power BI Desktop
2. `Inicio → Transformar datos → Editor avanzado`
3. Pega la consulta M del archivo `consultas_m.m`
4. Reemplaza `TU_API_KEY_AQUI` con tu key real
5. Verifica que la tabla carga correctamente

---

## PASO 4 — Publicar en Power BI Service

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

### ~~Bug — Paginación rota en `/api/v1/products/catalog`~~ — ✅ Resuelto

| Campo | Detalle |
|---|---|
| Detectado | Abril 2026 |
| Resuelto | Mayo 2026 |
| Solución | Usar `?limit=1000&offset=0` — el endpoint acepta hasta `limit=1000` |
| Total real | 689 productos — confirmado vía `total` en el response |

El endpoint devuelve `total`, `has_more` y `offset` para paginar correctamente.
Los scripts de Python y M ya implementan el loop automático por `has_more`.

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