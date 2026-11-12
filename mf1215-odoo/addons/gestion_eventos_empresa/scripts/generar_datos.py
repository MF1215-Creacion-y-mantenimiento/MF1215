# -*- coding: utf-8 -*-
"""
generar_datos.py · MF1215_3 · UF1889 · Sesión 7 (11/11/2026)

Crea datos de volumen en una COPIA de la base para medir rendimiento:
    5.000 contactos VOL · 1.000 eventos VOL · 100.000 inscripciones
    (≈ 80 % confirmadas, 15 % canceladas, 5 % borrador)

Uso (PowerShell, desde C:\\MF1215\\mf1215-odoo-windows):
    docker compose exec odoo odoo db duplicate mf1215 mf1215_rend
    docker compose exec odoo sh -c "odoo shell -d mf1215_rend --no-http < /mnt/extra-addons/gestion_eventos_empresa/scripts/generar_datos.py"

Protecciones:
    - Solo se ejecuta en la base mf1215_rend.
    - No se ejecuta dos veces (comprueba si ya hay contactos VOL).
Los datos se crean con el ORM (en lotes) para que se apliquen restricciones,
campos calculados y claves ajenas. Semilla fija: 1215.
"""
import random
import time
from datetime import timedelta
from odoo import fields

BASE_PERMITIDA = 'mf1215_rend'
SEMILLA = 1215
N_CONTACTOS = 5000
N_EVENTOS = 1000
INSCRIPCIONES_POR_EVENTO = 100          # 1.000 × 100 = 100.000
PLAZAS_POR_EVENTO = 150                 # > 100 para no chocar con la restricción de plazas
DIAS_HISTORIA = 540                     # fechas de inscripción repartidas en ~18 meses
LOTE = 10000
PESOS_ESTADO = [('confirmada', 80), ('cancelada', 15), ('borrador', 5)]

CTX = dict(tracking_disable=True, mail_create_nolog=True,
           mail_notrack=True, mail_create_nosubscribe=True)


def valor_por_defecto(env, campo, nombre_base):
    """Valor genérico para un campo obligatorio que no tiene default."""
    t = campo.type
    if t in ('char', 'text', 'html'):
        return nombre_base
    if t in ('integer', 'float', 'monetary'):
        return 1
    if t == 'boolean':
        return True
    if t == 'date':
        return fields.Date.today()  # noqa: F821
    if t == 'datetime':
        return fields.Datetime.now()  # noqa: F821
    if t == 'selection':
        sel = campo._description_selection(env)
        return sel[0][0] if sel else False
    if t == 'many2one':
        reg = env[campo.comodel_name].search([], limit=1)
        if not reg:
            raise SystemExit("Falta al menos un registro de %s para rellenar %s"
                             % (campo.comodel_name, campo.name))
        return reg.id
    return False


def completar_obligatorios(env, modelo, vals, nombre_base):
    """Rellena los campos obligatorios sin valor por defecto que falten en vals."""
    Modelo = env[modelo]
    defaults = Modelo.default_get(list(Modelo._fields))
    for nombre, campo in Modelo._fields.items():
        if (campo.required and nombre not in vals and nombre not in defaults
                and not campo.compute and not campo.related
                and nombre not in ('id', 'create_uid', 'create_date',
                                   'write_uid', 'write_date', 'display_name')):
            vals[nombre] = valor_por_defecto(env, campo, nombre_base)
    return vals


def main():
    t_inicio = time.time()
    assert env.cr.dbname == BASE_PERMITIDA, (  # noqa: F821
        "Ejecuta este script en %s, no en %s" % (BASE_PERMITIDA, env.cr.dbname))  # noqa: F821
    e = env(context=dict(env.context, **CTX))  # noqa: F821

    Partner = e['res.partner']
    Evento = e['taller.evento']
    Inscripcion = e['taller.inscripcion']

    if Partner.search_count([('name', '=like', 'VOL %')], limit=1):
        raise SystemExit("Ya hay contactos VOL en %s: el script ya se ejecutó." % BASE_PERMITIDA)

    rnd = random.Random(SEMILLA)
    ahora = fields.Datetime.now()  # noqa: F821

    # ---------------------------------------------------------------- contactos
    print("Creando %d contactos..." % N_CONTACTOS)
    vals_p = [{
        'name': 'VOL Contacto %05d' % i,
        'email': 'vol%05d@ejemplo.test' % i,
    } for i in range(1, N_CONTACTOS + 1)]
    contactos = Partner.browse()
    for k in range(0, len(vals_p), LOTE):
        contactos |= Partner.create(vals_p[k:k + LOTE])
    ids_contactos = contactos.ids

    # ------------------------------------------------------------------ eventos
    print("Creando %d eventos..." % N_EVENTOS)
    f_fecha = Evento._fields.get('fecha')
    f_plazas = Evento._fields.get('plazas')
    f_state_ev = Evento._fields.get('state')
    estado_ev = None
    if f_state_ev and f_state_ev.type == 'selection':
        claves = [k for k, _ in f_state_ev._description_selection(e)]
        for pref in ('confirm', 'abiert', 'public', 'activ'):
            estado_ev = next((k for k in claves if pref in k), None)
            if estado_ev:
                break

    vals_e = []
    for i in range(1, N_EVENTOS + 1):
        v = {'name': 'VOL Evento %04d' % i}
        if f_fecha:
            dt = ahora + timedelta(days=rnd.randint(1, 365), hours=rnd.randint(8, 18))
            v['fecha'] = dt.date() if f_fecha.type == 'date' else dt.replace(minute=0, second=0)
        if f_plazas:
            v['plazas'] = PLAZAS_POR_EVENTO
        if estado_ev:
            v['state'] = estado_ev
        vals_e.append(completar_obligatorios(e, 'taller.evento', v, v['name']))
    eventos = Evento.create(vals_e)

    # ------------------------------------------------------------ inscripciones
    total = N_EVENTOS * INSCRIPCIONES_POR_EVENTO
    print("Creando %d inscripciones en lotes de %d..." % (total, LOTE))
    estados = [s for s, _ in PESOS_ESTADO]
    pesos = [p for _, p in PESOS_ESTADO]
    tiene_fecha_insc = 'fecha_inscripcion' in Inscripcion._fields

    plantilla = completar_obligatorios(
        e, 'taller.inscripcion',
        {'evento_id': eventos[0].id, 'partner_id': ids_contactos[0], 'state': 'borrador'},
        'VOL')
    extra = {k: v for k, v in plantilla.items()
             if k not in ('evento_id', 'partner_id', 'state')}

    confirmados_por_evento = {}
    pendientes = []
    creadas = 0
    for ev in eventos:
        socios = rnd.sample(ids_contactos, INSCRIPCIONES_POR_EVENTO)  # sin repetir: respeta UNIQUE
        for pid in socios:
            st = rnd.choices(estados, weights=pesos)[0]
            v = dict(extra, evento_id=ev.id, partner_id=pid, state=st)
            if tiene_fecha_insc:
                v['fecha_inscripcion'] = ahora - timedelta(
                    days=rnd.randint(0, DIAS_HISTORIA),
                    hours=rnd.randint(0, 23), minutes=rnd.randint(0, 59))
            pendientes.append(v)
            if st == 'confirmada':
                confirmados_por_evento.setdefault(ev.id, []).append(pid)
        if len(pendientes) >= LOTE:
            Inscripcion.create(pendientes)
            creadas += len(pendientes)
            pendientes = []
            e.invalidate_all()
            print("  %6d / %d" % (creadas, total))
    if pendientes:
        Inscripcion.create(pendientes)
        creadas += len(pendientes)
        print("  %6d / %d" % (creadas, total))

    # ------------------------------- participantes = confirmados (consulta Q8)
    campo_part = None
    for nombre, campo in Evento._fields.items():
        if campo.type == 'many2many' and campo.comodel_name == 'res.partner' and not campo.compute:
            if campo_part is None or 'particip' in nombre:
                campo_part = nombre
    if campo_part:
        print("Asignando confirmados al campo %s de cada evento..." % campo_part)
        for ev in eventos:
            ev.write({campo_part: [(6, 0, confirmados_por_evento.get(ev.id, []))]})

    # ------------------------------------------------- estadísticas y commit
    e.flush_all()
    for tabla in ('res_partner', Evento._table, Inscripcion._table):
        e.cr.execute('ANALYZE "%s"' % tabla)
    e.cr.commit()
    print("Terminado: %d contactos, %d eventos, %d inscripciones (%.0f s)"
          % (len(contactos), len(eventos), creadas, time.time() - t_inicio))


main()
