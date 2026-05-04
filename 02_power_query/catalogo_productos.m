// =============================================================
// catalogo_productos.m — Power Query (M)
// Endpoint : GET /api/v1/products/catalog
// Tabla Odoo: product.template
// Paginación: limit=1000, loop automático por has_more
// =============================================================

let
    BaseUrl = "https://d19o5nz7emxr7x.cloudfront.net",
    ApiKey  = "TU_API_KEY_AQUI",
    Limit   = 1000,

    GetPage = (offset as number) as record =>
        Json.Document(
            Web.Contents(
                BaseUrl,
                [
                    RelativePath = "api/v1/products/catalog",
                    Query   = [limit = Number.ToText(Limit), offset = Number.ToText(offset)],
                    Headers = [Authorization = "Bearer " & ApiKey, Accept = "application/json"]
                ]
            )
        ),

    // ── La transformación ocurre DENTRO del selector de List.Generate
    // para acceder al record JSON crudo antes de que M normalice tipos.
    // Diagnóstico confirmó que Text.From(prod[x_codigo_anterior]) funciona
    // cuando se accede directo al JSON — aquí replicamos esa misma lógica.
    PageList = List.Generate(
        () => [res = GetPage(0), offset = 0],
        each [res][products] <> null,
        each if [res][has_more] = true
             then [res = GetPage([offset] + Limit), offset = [offset] + Limit]
             else [res = [products = null, has_more = false], offset = 0],
        each List.Transform([res][products], (prod) =>
            let
                // ── codigo_antiguo: mismo patrón que el diagnóstico ──
                codigoRaw    = try Text.From(prod[x_codigo_anterior]) otherwise null,
                codigoLimpio = if codigoRaw = null or codigoRaw = "false" then null
                               else Text.Trim(codigoRaw),
                partes = if codigoLimpio = null then {}
                         else Text.Split(codigoLimpio, ","),
                cod1   = if List.Count(partes) >= 1 then Text.Trim(partes{0}) else null,
                cod2   = if List.Count(partes) >= 2 then Text.Trim(partes{1}) else null,

                // ── uom_id y categ_id: listas [id, nombre] ──────────
                uomRaw      = try prod[uom_id]    otherwise null,
                uomId       = try uomRaw{0}        otherwise null,
                uomNombre   = try uomRaw{1}        otherwise null,
                categRaw    = try prod[categ_id]  otherwise null,
                categId     = try categRaw{0}      otherwise null,
                categNombre = try categRaw{1}      otherwise null,

                // ── Campos texto que Odoo devuelve false cuando están vacíos
                codigoAlfa  = try Text.From(prod[x_codigo_alfanumerico]) otherwise null,
                codigoAlfa2 = if codigoAlfa = null or codigoAlfa = "false" then null else codigoAlfa,
                defCode     = try Text.From(prod[default_code])          otherwise null,
                defCode2    = if defCode = null or defCode = "false"     then null else defCode
            in [
                id                    = try prod[id]                   otherwise null,
                name                  = try prod[name]                 otherwise null,
                list_price            = try prod[list_price]           otherwise null,
                default_code          = defCode2,
                is_sublimable_fabric  = try prod[is_sublimable_fabric] otherwise null,
                qty_available         = try prod[qty_available]        otherwise null,
                x_rendimiento         = try prod[x_rendimiento]        otherwise null,
                x_codigo_alfanumerico = codigoAlfa2,
                x_is_legacy           = try prod[x_is_legacy]          otherwise null,
                uom_id_num            = uomId,
                uom_name              = uomNombre,
                categ_id_num          = categId,
                categ_name            = categNombre,
                codigo_antiguo_1      = cod1,
                codigo_antiguo_2      = cod2
            ]
        )
    ),

    AllRecords = List.Combine(PageList),

    // Table.FromRecords — misma función que el diagnóstico usa y funciona
    Tabla = Table.FromRecords(AllRecords),

    Typed = Table.TransformColumnTypes(Tabla, {
        {"id",                    Int64.Type},
        {"name",                  type text},
        {"list_price",            Currency.Type},
        {"default_code",          type text},
        {"is_sublimable_fabric",  type logical},
        {"qty_available",         type number},
        {"x_rendimiento",         type number},
        {"x_codigo_alfanumerico", type text},
        {"x_is_legacy",           type logical},
        {"uom_id_num",            Int64.Type},
        {"uom_name",              type text},
        {"categ_id_num",          Int64.Type},
        {"categ_name",            type text},
        {"codigo_antiguo_1",      type text},
        {"codigo_antiguo_2",      type text}
    })

in
    Typed
