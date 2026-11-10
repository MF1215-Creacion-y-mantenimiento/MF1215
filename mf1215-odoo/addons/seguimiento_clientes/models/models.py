from odoo import fields, models
from odoo.exceptions import UserError


class SeguimientoCliente(models.Model):
    _name = "seguimiento.cliente"
    _description = "Seguimiento comercial de cliente"
    _order = "fecha desc, id desc"

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Asunto del seguimiento, p. ej. «Llamada para presentar la oferta».",
    )
    cliente_id = fields.Many2one(
        comodel_name="res.partner",
        string="Cliente",
        required=True,
        ondelete="restrict",
        index=True,
    )
    fecha = fields.Date(
        string="Fecha",
        required=True,
        default=fields.Date.context_today,
        index=True,
    )
    estado = fields.Selection(
        selection=[
            ("pendiente", "Pendiente"),
            ("realizado", "Realizado"),
        ],
        string="Estado",
        required=True,
        default="pendiente",
        index=True,
    )
    notas = fields.Text(string="Notas")

    def action_marcar_realizado(self):
        """Botón «Marcar como realizado»: pasa los seguimientos a 'realizado'."""
        if self.filtered(lambda s: s.estado == "realizado"):
            raise UserError("El seguimiento ya está marcado como realizado.")
        self.write({"estado": "realizado"})
        return True
