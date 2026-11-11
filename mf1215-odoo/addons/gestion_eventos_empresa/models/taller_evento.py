# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TallerEvento(models.Model):
    _name = 'taller.evento'
    _description = 'Evento de empresa'
    _order = 'fecha desc, name'

    name = fields.Char(string="Nombre", required=True)
    fecha = fields.Datetime(string="Fecha", required=True,
                            default=fields.Datetime.now)
    instructor_id = fields.Many2one('res.partner', string="Instructor")
    plazas = fields.Integer(string="Plazas", default=20, required=True)
    descripcion = fields.Text(string="Descripción")

    inscripcion_ids = fields.One2many('taller.inscripcion', 'evento_id',
                                      string="Inscripciones")
    participante_ids = fields.Many2many('res.partner',
                                        'taller_evento_participante_rel',
                                        'evento_id', 'partner_id',
                                        string="Participantes")

    # Fase 2: calculados almacenados (se ordena y agrupa por ellos)
    plazas_ocupadas = fields.Integer(string="Plazas ocupadas",
                                     compute='_compute_ocupacion', store=True)
    plazas_libres = fields.Integer(string="Plazas libres",
                                   compute='_compute_ocupacion', store=True)
    ocupacion = fields.Float(string="Ocupación (%)",
                             compute='_compute_ocupacion', store=True,
                             aggregator='avg')

    _plazas_positivas = models.Constraint(
        'CHECK(plazas > 0)', "El número de plazas debe ser mayor que cero.")

    @api.depends('plazas', 'inscripcion_ids.state')
    def _compute_ocupacion(self):
        confirmadas = {}
        if self._origin.ids:
            grupos = self.env['taller.inscripcion']._read_group(
                domain=[('evento_id', 'in', self._origin.ids),
                        ('state', '=', 'confirmada')],
                groupby=['evento_id'],
                aggregates=['__count'],
            )
            confirmadas = {evento.id: total for evento, total in grupos}
        for evento in self:
            ocupadas = confirmadas.get(evento._origin.id, 0)
            evento.plazas_ocupadas = ocupadas
            evento.plazas_libres = evento.plazas - ocupadas
            evento.ocupacion = (100.0 * ocupadas / evento.plazas) if evento.plazas else 0.0

    @api.onchange('plazas')
    def _onchange_plazas(self):
        if self.plazas and self.plazas < self.plazas_ocupadas:
            return {'warning': {
                'title': "Plazas insuficientes",
                'message': "Hay más inscripciones confirmadas que plazas.",
            }}

    @api.constrains('plazas')
    def _check_plazas(self):
        for evento in self:
            if evento.plazas < evento.plazas_ocupadas:
                raise ValidationError(
                    "El evento %s tiene %d inscripciones confirmadas y solo %d plazas."
                    % (evento.name, evento.plazas_ocupadas, evento.plazas))
