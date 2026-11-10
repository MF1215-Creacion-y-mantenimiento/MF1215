from odoo import models, fields


class seguimiento_clientes(models.Model):
    _name = "seguimiento_clientes.seguimiento_clientes"
    _description = "seguimiento_clientes.seguimiento_clientes"

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
