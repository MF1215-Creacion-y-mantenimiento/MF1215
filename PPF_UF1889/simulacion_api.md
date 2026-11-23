# Simulación de integración: CRM -> Odoo19(API JSON-2)
1. Endpoint y método http
   - URL:http//localhost:8069/json/2/gestion_tareas.tarea/search_read
   - Método: HTTP:POST
   - Patrón gerneral: /json/2/<modelo>/<método>. Aquí el modelo es gestion_tareas.tarea y el método del ORM es search_read, que filtra (search) y devuelve los campos pedidos (read) en una sola llamada.

2. Cabeceras
   
   | Cabecera | Valor | para qué |
   |---------|---------|---------|
   | Authorization| 
   | Content-Type |
   | X-Odoo-Database |
   | User-Agent |
   |

   La clave API se genera en Odoo: Miperfil > Preferencias > Seguridad de la cuenta > Nueva clave API.


   3. Cuerpo JSON de la petición

```json
{
    "domain":[
        ["partner_id", "=", ""],
        ["state", "=","pendiente"]
    ],
    "fields":[]
    "order":....
    "context":{....}
}

```

4. Respuesta JSON de ejemplo (200 OK)

```json



````


