from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class Entrega(models.Model):
    _name = "gestion_entregaas.entrega"
    _description = "Entrega de almacén"
    _order = "fecha desc, id desc"
    
    name = fields.Char(string="Referencia", required=True)
    partner_id = fields.Many2one(
        "res.partner",
        string="Cleinte",
        required=True,
        )