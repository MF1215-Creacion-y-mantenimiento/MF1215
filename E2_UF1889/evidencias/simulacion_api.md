# Simualción mediante API 

**Entorno:** local  ·  **base:** mf1215.  ·  **Odoo:** 19 Community ·  **Herramienta:** Postman

## 1. API utilizada 
(JSON-2: URL, autenticación, formato del cuerpo y de la respuesta)

## 2. La petición 
```http
POST http://localhost:8069/json/2/res.partner/search_read
Authorization: Barrer <clave API>
X-Odoo-Database: mf1215
Content-type: application/json

{
    "domain":[["name", "=like", "E2B%"]],
    "fields":["name", "email", "num_seguimientos", "num_seguimientos_realizados"],
    "order": "name"
}

```

## 3. Respuesta 

```json
[
    {
        "id": 50,
        "name": "E2B Cliente Alfa",
        "email": "alfa@e2b.test",
        "num_seguimientos": 4,
        "num_seguimientos_realizados": 3
    },
    {
        "id": 51,
        "name": "E2B Cliente Beta",
        "email": "beta@e2b.test",
        "num_seguimientos": 2,
        "num_seguimientos_realizados": 1
    },
    {
        "id": 52,
        "name": "E2B Cliente Gamma",
        "email": "gamma@e2b.test",
        "num_seguimientos": 0,
        "num_seguimientos_realizados": 0
    }
]
```
![Petición y respuesta de Postman](captura.png)

**Comprobación:** Alfa 4/3 · Beta 2/1 · Gamma 0/0 --> coincide con los datos de control

## 4. Prueba de seguridad
Clave falsa -> 401 <<invalid apikey>>

## 5. Mensaje para el sistema destino
```json
{
    "cabecera": {
        "origen": "odoo19/mf1215",
        "tipo_transaccion": "sincronizacion_lote",
        "operacion": "upsert",
        "generado_UTC": "2026-11-17T19:02:00Z",
        "version_esquema": "1.0",
        "num_registros": 3
    },
    "clientes": [
        {
            "ref_externa": "mf1215.res_partner.50",
            "nombre": "E2B Cliente Alfa",
            "email": "alfa@e2b.test",
            "seguimientos": {"total": 4, "realizados": 3, "pendientes": 1},
            "detalle": [
                {"id": 1, "asunto": "S1 · Llamada de presentación", "fecha": "2026-11-17", "estado": "realizado"},
                .
                .
                .
            ]
        },
        {
            "ref_externa": "mf1215.res_partner.51",
            "nombre": "E2B Cliente Beta",
            "email": "beta@e2b.test",
            .
            .
            .
            .
        }

        {
            .
            .
            .
            .
            .
            "detalle": []
        }
    ]
}

```