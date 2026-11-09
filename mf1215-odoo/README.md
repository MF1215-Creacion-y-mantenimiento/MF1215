# Entorno local MF1215 · Odoo 19 + PostgreSQL 16

Abre una terminal en esta carpeta (`MF1215/mf1215-odoo`) y usa estas órdenes.
Son iguales en Windows (PowerShell), macOS y Linux.

| Quiero… | Orden |
|---|---|
| Arrancar | `docker compose up -d` |
| Ver el estado | `docker compose ps` |
| Parar (los datos se conservan) | `docker compose stop` |
| Ver errores en directo (Ctrl+C para salir) | `docker compose logs -f --tail=100 odoo` |
| Crear el esqueleto de un módulo | `docker compose exec odoo odoo scaffold nombre_modulo /mnt/extra-addons` |
| Instalar un módulo por primera vez | `docker compose exec odoo odoo -d mf1215 -i nombre_modulo --stop-after-init --no-http` y después `docker compose restart odoo` |
| Aplicar cambios en un módulo | `docker compose exec odoo odoo -d mf1215 -u nombre_modulo --stop-after-init --no-http` y después `docker compose restart odoo` |
| Consola SQL (`\q` para salir) | `docker compose exec db psql -U odoo -d mf1215` |

En Linux, crea el esqueleto del módulo como root y recupera los ficheros:

```
docker compose exec -u root odoo odoo scaffold nombre_modulo /mnt/extra-addons
sudo chown -R "$USER":"$USER" addons/nombre_modulo
```

Accesos (solo desde tu equipo):

| | Dirección | Usuario | Contraseña |
|---|---|---|---|
| Odoo | http://localhost:8069 | admin | admin |
| PostgreSQL | localhost:5432, base mf1215 | odoo | odoo |
| Gestor de bases | http://localhost:8069/web/database/manager | — | maestra: admin |

Primera vez (solo una vez): crea la base `mf1215` en español, con España como país y datos de
demostración, e instala Contactos, CRM, Ventas e Inventario:

```
docker compose exec odoo odoo db init mf1215 --language es_ES --country ES --with-demo
docker compose exec odoo odoo module install -d mf1215 contacts crm sale_management stock
docker compose restart odoo
```

Después entra en http://localhost:8069 con admin / admin y activa el modo desarrollador
(Ajustes, al final de la página).

Para borrar todo (bases incluidas, sin tocar `addons`): `docker compose down --volumes`.
