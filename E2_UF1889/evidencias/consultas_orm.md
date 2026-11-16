# Consultas ORM

## Tarea 1
### Identificar modelos

|Información| modelo Odoo | TablaPostgreSQL | Campos relevantes|
|-----------|-------------|-----------------|------------------|
| Cliente   | res.partner | res_partner     | id, name, email, is_company|
| Seguimiento| segimiento.cliente| seguimiento_cliente| id, name (asunto), cliente_id(Many2one --> res.partner, obligatorio, ondelete = 'restrict', indexado), fecha(Date, indexado), estado (Selection pendiente/realizado, indexado), notas
|

#### Relación
```
res_partner 1 ------ N seguimiento_cliente
    id <-------  cliente_id (FK, ON DELETE RESTRICT)
```

## Tarea 2
```python
Seguimiento = env['seguimiento.cliente']
clientes = env['res.partner'].search([('name', '=like', 'E2B Cliente%')], order = 'name')
lineas = []
for cliente in clientes:
    total = Seguimiento.search_count([('cliente_id', '=', cliente.id)])
    realizados = Seguimiento.search_count([('cliente_id', '=', cliente.id), 
                                            ('estado', '=', 'realizado')])
    lineas.append('%s: %d seguimientos (%d realizados)' % (cliente.name, total, realizados))
    
mensaje = '\n'.join(lineas) or ' sin datos'
log(mensaje)
action = {
    'type':'ir.actions.client',
    'tag':'display_notification',
    'params': {'title': 'Seguimientos por cliente', 'message': mensaje, 'sticky':True},
}
```
