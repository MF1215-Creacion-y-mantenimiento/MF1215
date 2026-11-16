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