from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Entrega(models.Model):
    _name = "gestion_entregas.entrega"
    _description = "Entrega de almacén"
    _order = "fecha desc, id desc"

    name = fields.Char(string="Referencia", required=True)
    partner_id = fields.Many2one(
        "res.partner",
        string="Cliente",
        required=True,
    )
    fecha = fields.Date(string="Fecha", default=fields.Date.context_today)

    bultos = fields.Integer(string="Bultos", default=1)

    importe = fields.Float(string="Importe €")

    state = fields.Selection(
        selection=[
            ("pendiente", "Pendiente"),
            ("entregada", "Entregada"),
        ],
    )
