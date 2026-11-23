# gestion_tareas · Gestión de tareas sobre clientes (Odoo 19)

## Qué hace

Registra las tareas que la empresa realiza sobre sus clientes (llamadas,
visitas, presupuestos…) y controla su estado: pendiente o finalizada.
Incluye filtro de pendientes, agrupación por cliente, botón «Finalizar» con
validación y permite intercambiar datos por CSV y API JSON-2.

## Componentes

- Modelo `gestion_tareas.tarea`: name (obligatorio), partner_id (cliente,
  res.partner), fecha (hoy por defecto), state (pendiente/finalizada).
- Vistas list, form y search; acción y menú «Gestión de tareas › Tareas».
- Método `action_finalizar`: finaliza la tarea o lanza UserError si ya lo está.
- Permisos completos para usuarios internos (base.group_user).

## Instalación

1. Copiar la carpeta `gestion_tareas` en la carpeta `addons` del proyecto.
2. Ejecutar:

       docker compose exec odoo odoo -d mf1215 -i gestion_tareas --stop-after-init --no-http
       docker compose restart odoo

3. Para actualizar tras un cambio, usar `-u gestion_tareas` y reiniciar.

Dependencias: base y contacts.

## Uso

1. Menú Gestión de tareas › Tareas › Nuevo.
2. Indicar nombre y cliente; la fecha se rellena con el día actual.
3. Pulsar Finalizar cuando la tarea esté hecha.
4. Usar el filtro Pendientes y la agrupación Cliente para el seguimiento.

## Flujo de datos entre sistemas

- **Origen de los clientes:** son contactos de `res.partner` (módulo
  Contactos), compartidos con el resto de Odoo y sincronizables con el CRM.
- **Entrada automática de tareas:**
  - Por lotes con CSV: el CRM exporta un fichero con columna `id` y se importa
    desde la vista lista (o con una tarea programada).
  - En tiempo real con API JSON-2: el CRM llama a
    `/json/2/gestion_tareas.tarea/create` o `search_read` (ver simulacion_api.md).
- **Evitar duplicados:** cada tarea lleva un identificador externo estable
  (columna `id`, p. ej. `gt_imp_001`). Odoo lo guarda en `ir.model.data`; al
  reimportar, si el identificador existe, actualiza el registro en lugar de
  crear otro. Por API, el CRM guarda el id de Odoo devuelto y consulta antes
  de crear.

## Documentación oficial consultada (Odoo 19, en inglés)

| URL | Qué he aplicado |
|-----|-----------------|
| https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html | Tipos de campo, default con función y firma de `_read_group` |
| https://www.odoo.com/documentation/19.0/developer/reference/user_interface/view_architectures.html | Etiqueta `<list>`, filtros y group_by en la vista search |
| https://www.odoo.com/documentation/19.0/developer/reference/external_api.html | Endpoint /json/2, cabeceras bearer y X-Odoo-Database, formato de respuesta |