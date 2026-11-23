from odoo import fields, models
from odoo.exceptions import UserError


class Tarea(models.Model):
    _name = "gestion_tareas.tarea"
    _description = "Tarea sobre cliente"
    _order = "fecha desc, id desc"

    name = fields.Char(
        string="Tarea",
        required=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Cliente",
        index=True,
    )
    fecha = fields.Date(
        string="Fecha",
        default=fields.Date.context_today,
    )
    state = fields.Selection(
        selection=[
            ("pendiente", "Pendiente"),
            ("finalizada", "Finalizada"),
        ],
        string="Estado",
        default="pendiente",
        required=True,
    )

    def action_finalizar(self):
        """Pasa las tareas a 'finalizada'. Error si alguna ya lo está."""
        finalizadas = self.filtered(lambda t: t.state == "finalizada")
        if finalizadas:
            nombres = ", ".join(finalizadas.mapped("name"))
            raise UserError(
                f"No se puede finalizar: la tarea «{nombres}» ya está finalizada."
            )
        self.write({"state": "finalizada"})
        return True
