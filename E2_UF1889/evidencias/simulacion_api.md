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

