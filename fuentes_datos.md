# Fuentes de datos — Telas Real (Proyecto BI)

← [Volver al README](./Readme.md)

## Introducción

Este archivo resume los orígenes de datos que alimentan el proyecto de Business Intelligence de Telas Real: tipo de fuente, enlace técnico o identificador del endpoint y la tabla equivalente dentro del modelo de Power BI cuando aplica.

---

## Inventario de fuentes

| Fuente | url_endpoint / enlace | Descripción | Tabla en Power BI |
| --- | --- | --- | --- |
| Metas KPI (Google Sheets) | [Spreadsheet — metas KPI](https://docs.google.com/spreadsheets/d/1qkdX7Mz13WGjY635yizUQ-3C-JCuK2mw04iNw38UWVg/edit?usp=sharing) | Hoja donde se ingresan los datos de KPI que actualmente **no vienen del sistema**. | `DB_Kpis` |
| Catálogo de productos (consulta Power Query `02_power_query/catalogo_productos.m`) | **Base URL:** `https://d19o5nz7emxr7x.cloudfront.net` — **`RelativePath`:** `api/v1/products/catalog` *(autenticación Bearer; no incluir API Key en este documento)* | API JSON vía `Web.Contents`; la consulta M está versionada en el repositorio. | `Dim_02_power_query/catalogo_productos` |

---

*Documentación complementaria del [README principal](./Readme.md).*
