from odoo import fields, models


class PrestamoEquipo(models.Model):
    _name = "prestamo.equipo"
    _description = "Préstamo de equipo"
    _order = "fecha desc, id desc"

    name = fields.Char(string="Equipo", required=True)

    cliente_id = fields.Many2one(
        "res.partner",
        string="Cliente",
        required=True,
    )

    fecha = fields.Date(
        string="Fecha de préstamo",
        required=True,
        default=fields.Date.context_today,
    )

    estado = fields.Selection(
        [
            ("prestado", "Prestado"),
            ("devuelto", "Devuelto"),
        ],
        string="Estado",
        required=True,
        default="prestado",
    )
    notas = fields.Text(string="Notas")
