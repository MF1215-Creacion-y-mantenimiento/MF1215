# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class TallerInscripcion(models.Model):
    _name = 'taller.inscripcion'
    _description = 'Inscripción a un evento'
    _order = 'evento_id, fecha_inscripcion desc'
    _rec_name = 'partner_id'

    evento_id = fields.Many2one('taller.evento', string="Evento",
                                required=True, ondelete='cascade', index=True)
    partner_id = fields.Many2one('res.partner', string="Contacto",
                                 required=True, ondelete='restrict', index=True)
    email = fields.Char(related='partner_id.email', string="Correo")
    fecha_evento = fields.Datetime(related='evento_id.fecha', string="Fecha del evento")
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ], string="Estado", default='borrador', required=True)
    fecha_inscripcion = fields.Datetime(string="Fecha de inscripción",
                                        default=fields.Datetime.now,
                                        readonly=True)
    notas = fields.Text(string="Notas")

    _inscripcion_unica = models.Constraint(
        'UNIQUE(evento_id, partner_id)',
        "Este contacto ya está inscrito en el evento.")

    # Fase 4: validación de plazas (una consulta para todos los eventos afectados)
    @api.constrains('state', 'evento_id')
    def _check_plazas_evento(self):
        eventos = self.filtered(lambda i: i.state == 'confirmada').evento_id
        if not eventos:
            return
        grupos = self._read_group(
            domain=[('evento_id', 'in', eventos.ids), ('state', '=', 'confirmada')],
            groupby=['evento_id'],
            aggregates=['__count'],
        )
        for evento, total in grupos:
            if total > evento.plazas:
                raise ValidationError(
                    "No quedan plazas en %s (%d plazas, %d confirmadas)."
                    % (evento.name, evento.plazas, total))

    def action_confirmar(self):
        for insc in self:
            if insc.state != 'borrador':
                raise UserError("Solo se pueden confirmar inscripciones en borrador.")
        self.write({'state': 'confirmada'})
        for insc in self:
            insc.evento_id.participante_ids = [(4, insc.partner_id.id)]
        return True

    def action_cancelar(self):
        for insc in self:
            if insc.state == 'cancelada':
                raise UserError("La inscripción ya está cancelada.")
        self.write({'state': 'cancelada'})
        for insc in self:
            insc.evento_id.participante_ids = [(3, insc.partner_id.id)]
        return True

    def action_borrador(self):
        for insc in self:
            if insc.state != 'cancelada':
                raise UserError("Solo se pueden reabrir inscripciones canceladas.")
        self.write({'state': 'borrador'})
        return True

    def unlink(self):
        if any(i.state == 'confirmada' for i in self):
            raise UserError("No se puede borrar una inscripción confirmada: cancélala antes.")
        return super().unlink()
