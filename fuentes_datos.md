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
| Nuevo archivo de metas generales | [Spreadsheet — metas Globales](https://docs.google.com/spreadsheets/d/1qu0WcC5NBB9cQ6Pyi49b-zeLuJDnWg1V/edit?usp=sharing&ouid=101643444773080448057&rtpof=true&sd=true) | Libro de Excel con metas comerciales y otras que **no vienen del sistema**. | `Son Varias Tablas: pdt1, pdt2` |
| Clientes TR — información complementaria (Google Sheets) | [Spreadsheet — clientes TR](https://docs.google.com/spreadsheets/d/1UYpYtRDp05Evt8v0Ogv6uWzlWIEjafQh/edit?usp=sharing&ouid=101643444773080448057&rtpof=true&sd=true) | Libro con información **actualizada o complementaria de los clientes** de Telas Real que no viene del sistema. | `DimClientes` *(complementaria)* |
| Lista de Precios | [Google Sheets](https://docs.google.com/spreadsheets/d/19KpBbfPrtPyYTekz-OlyLoYDh8Gzg5Ue/edit?usp=sharing&ouid=101643444773080448057&rtpof=true&sd=true) | Libro con información **de precios** de Telas Real que no viene del sistema. | `DBSales y DBListaPrecios` *(complementaria)* |



---

*Documentación complementaria del [README principal](./Readme.md).*
