# MF1215_3 · UF1889 · Día 22 · Casos de medición C1–C7, en orden
#
# Se ejecuta dentro de odoo shell, en la base de pruebas de volumen:
#   docker compose exec odoo odoo shell -d mf1215_rend --no-http
#   >>> exec(open('/mnt/extra-addons/gestion_eventos_empresa/scripts/medir_casos.py').read())
#
# C1–C4: técnicas del ORM, se miden con medir() (tiempo y número de consultas).
# C5–C7: índices, se miden con el plan de PostgreSQL. El «antes» se simula
#        prohibiendo a PostgreSQL usar índices solo en esta sesión (SET enable_…).
from datetime import timedelta

from odoo import fields
from odoo.tools import SQL

exec(open('/mnt/extra-addons/gestion_eventos_empresa/scripts/medir.py').read())

I = env['taller.inscripcion']
E = env['taller.evento']
ESTADOS = ['borrador', 'confirmada', 'cancelada']
CONFIRMADAS = [('state', '=', 'confirmada')]


def titulo(texto):
    print(f"\n=== {texto} " + "=" * max(0, 70 - len(texto)))


def ver_plan(etiqueta, consulta, sin=()):
    """Ejecuta EXPLAIN ANALYZE y muestra solo los nodos de lectura y el tiempo.

    :param sin: tipos de plan prohibidos en esta prueba, p. ej. ('indexscan', 'bitmapscan')
    """
    for tipo in sin:
        env.cr.execute(f"SET enable_{tipo} = off")
    env.cr.execute(SQL("EXPLAIN (ANALYZE, BUFFERS) %s", consulta))
    lineas = [l for (l,) in env.cr.fetchall()]
    env.cr.execute("RESET ALL")
    print(f"  {etiqueta}")
    for l in lineas:
        if any(p in l for p in ("Scan", "Heap Fetches", "Execution Time")):
            print("     ", l.strip()[:110])


# ---------------------------------------------------------------------------
titulo("C1 · Contar las confirmadas")
medir("C1a len(search())", lambda: len(I.search(CONFIRMADAS)))
medir("C1b search_count()", lambda: I.search_count(CONFIRMADAS))

# ---------------------------------------------------------------------------
titulo("C2 · Resumen por estado de 80 eventos (RF-16)")


def resumen_lento():
    eventos = E.search([], limit=80)
    return {e.id: tuple(I.search_count([('evento_id', '=', e.id), ('state', '=', s)])
                        for s in ESTADOS)
            for e in eventos}


def resumen_rapido():
    eventos = E.search([], limit=80)
    grupos = I._read_group([('evento_id', 'in', eventos.ids)],
                           ['evento_id', 'state'], ['__count'])
    conteo = {(ev.id, st): n for ev, st, n in grupos}
    return {e.id: tuple(conteo.get((e.id, s), 0) for s in ESTADOS) for e in eventos}


c2a = medir("C2a search_count x evento", resumen_lento)
c2b = medir("C2b _read_group", resumen_rapido)
print("  ¿Mismo resultado?", c2a == c2b)
if 'num_borrador' in E._fields:
    medir("C2c campos del modelo",
          lambda: [(e.num_borrador, e.num_confirmadas, e.num_canceladas)
                   for e in E.search([], limit=80)])

# ---------------------------------------------------------------------------
titulo("C3 · Confirmadas por mes, último año")
hace_un_anio = fields.Datetime.now() - timedelta(days=365)
dom3 = CONFIRMADAS + [('fecha_inscripcion', '>=', hace_un_anio)]


def por_mes_python():
    r = {}
    for i in I.search(dom3):
        k = fields.Datetime.context_timestamp(i, i.fecha_inscripcion).strftime('%Y-%m')
        r[k] = r.get(k, 0) + 1
    return r


def por_mes_bd():
    g = I._read_group(dom3, ['fecha_inscripcion:month'], ['__count'])
    return {m.strftime('%Y-%m'): n for m, n in g}


c3a = medir("C3a bucle Python", por_mes_python)
c3b = medir("C3b _read_group por mes", por_mes_bd)
print("  ¿Mismo resultado?", c3a == c3b, "·", len(c3a), "meses")

# ---------------------------------------------------------------------------
titulo("C4 · Correo de 2.000 inscripciones (prefetch)")
ids = I.search(CONFIRMADAS, limit=2000).ids

c4a = medir("C4a browse(id) uno a uno", lambda: [I.browse(i).partner_id.email for i in ids])
c4b = medir("C4b recorrer el recordset", lambda: [r.partner_id.email for r in I.browse(ids)])
print("  ¿Mismo resultado?", c4a == c4b)

# ---------------------------------------------------------------------------
titulo("C5 · Confirmadas de los últimos 30 días (índice en fecha_inscripcion)")
dom5 = CONFIRMADAS + [('fecha_inscripcion', '>=', fields.Datetime.now() - timedelta(days=30))]
print("  filas:", I.search_count(dom5))
c5 = I._search(dom5).select()
ver_plan("C5a sin índices", c5, sin=('indexscan', 'bitmapscan', 'indexonlyscan'))
ver_plan("C5b con índices", c5)

# ---------------------------------------------------------------------------
titulo("C6 · Lista de borradores, 80 filas (índice en state)")
c6 = I._search([('state', '=', 'borrador')], order=I._order, limit=80).select()
ver_plan("C6a sin índices", c6, sin=('indexscan', 'bitmapscan', 'indexonlyscan'))
ver_plan("C6b con índices", c6)

# ---------------------------------------------------------------------------
titulo("C7 · GROUP BY evento_id, state de 80 eventos (índice compuesto)")
c7 = SQL("SELECT evento_id, state, COUNT(*) FROM taller_inscripcion "
         "WHERE evento_id IN %s GROUP BY evento_id, state",
         tuple(E.search([], limit=80).ids))
ver_plan("C7a sin Index Only Scan", c7, sin=('indexonlyscan',))
ver_plan("C7b con el índice compuesto", c7)

print("\nFin. Anota tiempo, consultas y tipo de plan de cada caso en docs/rendimiento.md")