// =============================================================
// diagnostico_codigo_anterior.m
// Prueba mínima — pegar en nueva consulta en blanco en PBI
// Objetivo: confirmar si M puede leer x_codigo_anterior
// =============================================================

let
    BaseUrl = "https://d19o5nz7emxr7x.cloudfront.net",
    ApiKey  = "TU_API_KEY_AQUI",

    Response = Web.Contents(
        BaseUrl,
        [
            RelativePath = "api/v1/products/catalog",
            Query   = [limit = "10", offset = "0"],
            Headers = [
                Authorization = "Bearer " & ApiKey,
                Accept        = "application/json"
            ]
        ]
    ),

    Json     = Json.Document(Response),
    Products = Json[products],

    // Sin List.Transform, sin tablas, sin expand.
    // Solo acceso directo al campo en cada record.
    Resultado = Table.FromRecords(
        List.Transform(Products, (prod) => [
            id              = prod[id],
            name            = prod[name],
            valor_crudo     = try prod[x_codigo_anterior]        otherwise "ERROR-NO-EXISTE",
            como_texto      = try Text.From(prod[x_codigo_anterior]) otherwise "ERROR-NO-EXISTE",
            tipo_en_m       = try Value.Type(prod[x_codigo_anterior]) otherwise "ERROR"
        ])
    )

in
    Resultado
