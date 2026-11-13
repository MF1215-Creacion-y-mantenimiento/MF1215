import base64
import csv
import io
import logging
import time
from datetime import timedelta

#--- Odoo ---
from odoo import api, fields, models
from odoo.tools import split_every

_logger = logging.getLogger(__name__)

class TallerExportacion(models.Model):
    _name = 'taller.exportacion'
    _description = "Exportación de inscripciones"
    _order = 'fecha_inicio desc, id desc'

    name = fields.Char(string="Referencia", deafault="/", readonly=True, copy=False)
    origen = fields.Selection(
        [('manual', "Manual"), ('planificada', "Planificada")],
        string="Origen", required=True, default='manual', readonly=True
    )
    usuario_id = fields.Many2one(
        'res.users', string="Usuario", default=lambda self: self.env.user, readonly=True
    )
    
    fecha_inicio = fields.Datetime(string="Inicio", default=fields.Datetime.now, readonly=True)
    duracion = fields.Float(string="Duración (s)", digits=(16, 3), readonly=True)
    filtros = fields.Text(string="Filtros", readonly=True)
    desde = fields.Datetime(string="Periódo desde (UTC)", readonly=True)
    hasta = fields.Datetime(string="Periódo hasta (UTC)", readonly=True)
    num_registros = fields.Integer(string="Filas", readonly=True)

    estado = fields.Selection(
        [('en_curso', "En curos"), ('ok', "Correcta"), ('error', "Error")],
        string="Resultado", required=True, default='en_curso', readonly=True
    )
    mensaje = fields.Text(string="Mensaje", readonly=True)
    adjunto_id = fields.Many2one('ir.attachment', string="Fichero", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('taller.exportacion') or '/'

        return super().create(vals_list)
    