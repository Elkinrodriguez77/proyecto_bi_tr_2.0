// =============================================================
// productos_catalogo.m — Power Query (M)
// Endpoint: GET /api/v1/products/catalog
// Tabla Odoo: product.template
// Estado: ✅ Live (bug paginación pendiente — max 50 productos)
// =============================================================

let
    BaseUrl  = "https://d19o5nz7emxr7x.cloudfront.net",
    ApiKey   = "TU_API_KEY_AQUI",

    Response = Web.Contents(
        BaseUrl,
        [
            RelativePath = "api/v1/products/catalog",
            Headers = [
                Authorization = "Bearer " & ApiKey,
                Accept        = "application/json"
            ]
        ]
    ),

    Json       = Json.Document(Response),
    Tabla      = Table.FromList(Json[products], Splitter.SplitByNothing(), {"registro"}),
    Expand     = Table.ExpandRecordColumn(Tabla, "registro",
                    {"id","name","list_price","default_code",
                     "uom_id","is_sublimable_fabric","qty_available"}),

    // uom_id viene como lista [id, nombre] → separar en dos columnas
    AddUomId   = Table.AddColumn(Expand,   "uom_id_num",  each [uom_id]{0}),
    AddUomName = Table.AddColumn(AddUomId, "uom_name",    each [uom_id]{1}),
    DropUom    = Table.RemoveColumns(AddUomName, {"uom_id"}),

    Typed = Table.TransformColumnTypes(DropUom, {
        {"id",                   Int64.Type},
        {"name",                 type text},
        {"list_price",           Currency.Type},
        {"default_code",         type text},
        {"uom_id_num",           Int64.Type},
        {"uom_name",             type text},
        {"is_sublimable_fabric", type logical},
        {"qty_available",        type number}
    })

in
    Typed


// =============================================================
// telas_sublimables.m — Power Query (M)
// Endpoint: GET /api/v1/products/sublimable
// Tabla Odoo: product.template (filtro is_sublimable_fabric=true)
// Estado: ✅ Live
// =============================================================

/*
let
    BaseUrl  = "https://d19o5nz7emxr7x.cloudfront.net",
    ApiKey   = "TU_API_KEY_AQUI",

    Response = Web.Contents(
        BaseUrl,
        [
            RelativePath = "api/v1/products/sublimable",
            Headers = [
                Authorization = "Bearer " & ApiKey,
                Accept        = "application/json"
            ]
        ]
    ),

    Json       = Json.Document(Response),
    Tabla      = Table.FromList(Json[fabrics], Splitter.SplitByNothing(), {"registro"}),
    Expand     = Table.ExpandRecordColumn(Tabla, "registro",
                    {"id","name","list_price","default_code","qty_available"}),
    AddDesigns = Table.AddColumn(Expand, "total_designs_available",
                    each Json[total_designs_available]),

    Typed = Table.TransformColumnTypes(AddDesigns, {
        {"id",                      Int64.Type},
        {"name",                    type text},
        {"list_price",              Currency.Type},
        {"default_code",            type text},
        {"qty_available",           type number},
        {"total_designs_available", Int64.Type}
    })

in
    Typed
*/


// =============================================================
// clientes_por_tienda.m — Power Query (M)
// Endpoint: GET /api/v1/customers/summary
// Tabla Odoo: res.partner
// Estado: ✅ Live — 45,896 clientes
// =============================================================

/*
let
    BaseUrl  = "https://d19o5nz7emxr7x.cloudfront.net",
    ApiKey   = "TU_API_KEY_AQUI",

    Response = Web.Contents(
        BaseUrl,
        [
            RelativePath = "api/v1/customers/summary",
            Headers = [
                Authorization = "Bearer " & ApiKey,
                Accept        = "application/json"
            ]
        ]
    ),

    Json    = Json.Document(Response),

    // Métricas generales (una fila)
    Metricas = #table(
        {"metrica", "valor"},
        {
            {"total_clientes",      Json[total]},
            {"empresas",            Json[companies]},
            {"personas",            Json[persons]},
            {"con_email",           Json[with_email]},
            {"con_telefono",        Json[with_phone]},
            {"cobertura_email_pct", Json[email_coverage_pct]}
        }
    ),

    // Por tienda (una fila por tienda)
    ByStore = Table.RenameColumns(
        Record.ToTable(Json[by_store]),
        {{"Name", "tienda"}, {"Value", "clientes"}}
    ),
    TypedByStore = Table.TransformColumnTypes(ByStore, {
        {"tienda",   type text},
        {"clientes", Int64.Type}
    })

    // Retorna Metricas o TypedByStore según la tabla que necesites
in
    TypedByStore
*/


// =============================================================
// PENDIENTES — descomentar cuando los endpoints estén Live
// =============================================================

// ventas_summary.m
// Endpoint: GET /api/v1/sales/summary
// Tabla Odoo: sale.order
// Estado: 🔴 Blocked — sin sale.order históricos
// Estructura: métrica plana (1 sola fila)
// Clave JSON: N/A (usar Record.ToTable directamente)

// inventario_stock.m
// Endpoint: GET /api/v1/inventory/stock
// Tabla Odoo: stock.quant
// Estado: 🟡 Partial — esperando carga de stock inicial
// Clave JSON: "stock" (lista)

// produccion_summary.m
// Endpoint: GET /api/v1/production/summary
// Tabla Odoo: mrp.production
// Estado: 🔴 Blocked — work centers + BOM pendientes
// Clave JSON: "by_state" (dict con 5 estados)