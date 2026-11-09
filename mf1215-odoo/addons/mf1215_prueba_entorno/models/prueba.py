from odoo import fields, models


class PruebaEntorno(models.Model):
    _name = 'mf1215.prueba.entorno'
    _description = 'Prueba del entorno'
    _rec_name = 'alumno'

    alumno = fields.Char(string='Alumno', required=True)
    mensaje = fields.Char(string='Mensaje', default='¡Mi entorno funciona!')
