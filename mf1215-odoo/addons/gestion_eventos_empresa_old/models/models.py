# from odoo import models, fields, api


# class gestion_eventos_empresa(models.Model):
#     _name = 'gestion_eventos_empresa.gestion_eventos_empresa'
#     _description = 'gestion_eventos_empresa.gestion_eventos_empresa'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

