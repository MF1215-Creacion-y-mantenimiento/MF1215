# docker compose exec odoo odoo shell -d mf1215_rend --no-http
exec(open('/mnt/extra-addons/gestion_eventos_empresa/scripts/medir.py').read())
I = env['taller.inscripcion']
dom = [('state', '=', 'confirmada')]
medir("C1a len(search())", lambda: len(I.search(dom)))
medir("C1b search_count()", lambda: I.search_count(dom))

from datetime import timedelta
desde = fields.Datetime.now() - timedelta(days=365)
dom3 = dom + [('fecha_inscripcion', '>=', desde)]

def por_mes_python():
    r = {}
    for i in I.search(dom3):
        ts = fields.Datetime.context_timestamp(i, i.fecha_inscripcion)
        k = ts.strftime('%Y-%m')
        r[k] = r.get(k, 0) + 1
    return r

def por_mes_bd():
    g = I._read_group(dom3, ['fecha_inscripcion:month'], ['__count'])
    return {m.strftime('%Y-%m'): n for m, n in g}

a = medir("C3a bucle", por_mes_python)
b = medir("C3b _read_group", por_mes_bd)
a == b   # True, 13 meses