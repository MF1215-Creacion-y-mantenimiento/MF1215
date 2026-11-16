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
### Opción más eficiente / read_group

```python
grupos = env['seguimiento.cliente']._read_group(
    domain = [('cliente_id.name', '=like', 'E2B Cliente%')],
    groupby = ['cliente_id', 'estado'],
    aggregates = ['__count'],
    order = 'cliente_id',
)
mensaje = '\n'.join('%s · %s: %d' % (cliente.name, estado, n) for cliente, estado, n in grupos)
log(mensaje)
action = {'type':'ir.actions.client', 'tag':'display_notification', 
    'params': {'title': 'Seguimientos (read_group)', 'message': mensaje, 'sticky':True}}

```

## Tarea 3 Campo calculado

```python

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    
    seguimiento_ids = fields.One2many(
        comodel_name = "seguimiento.cliente",
        inverse_name = "cliente_id",
        string = "Seguimientos",
    )
    
    num_seguimientos = fields.Integer(
        string = "Nº de seguimientos",
        compute = "_compute_num_seguimientos",
        store = True,
        help = "Total de seguimientos registrados para el cliente.",
    )
    num_seguimientos_realizados = fields.Integer(
        string = "Nº de seguimientos realizados",
        compute = "_compute_num_seguimientos",
        store = True,
        help = "Seguimientos del cliente en estado 'Realizado'.",
    )
    @api.depends("seguimiento_ids", "seguimientos_ids.estado")
    def _compute_num_seguimientos(self):
        for partner in self:
            partner.num_seguimientos = len(partner.seguimiento_ids)
            partner.num_seguimientos_realizados = len(
                partner.seguimiento_ids.filtered(lambda s: s.estado == "realizado")
            )
            
    def action_ver_seguimientos(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_windows",
            "name": "Seguimientos",
            "res_model": "seguimiento.cliente",
            "view_model": "list,form",
            "domain": [("cliente_id", "=", self.id)],
            "context": {"default_clietne_id": self.id},
        }
```