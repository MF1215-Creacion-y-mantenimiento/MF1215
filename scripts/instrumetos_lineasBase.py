# Se ejecuta en una terminal del equipo, no dentro de Python:
# ----------------------------------------------------------------
#   docker compose exec odoo odoo shell -d mf1215_rend --no-http
# ----------------------------------------------------------------
# - docker compose exec odoo : ejecuta un comando dentro del contenedor "odoo".
# - odoo shell               : abre un intérprete de Python con Odoo cargado. Ya existen
#                              las variables env (entorno del ORM), self (el usuario) y odoo.
# - -d mf1215_rend           : base de pruebas de rendimiento (5.000 contactos, 100.000
#                              inscripciones). Nunca la base de trabajo mf1215.
# - --no-http                : no arranca el servidor web. El contenedor ya ocupa el
#                              puerto 8069 y en el shell no se necesita.

exec(open('/mnt/extra-addons/gestion_eventos_empresa/scripts/medir.py').read())
# Lee el fichero medir.py del addon (montado en /mnt/extra-addons) y ejecuta su código
# en esta sesión. Así quedan definidas medir() y plan(), que usan la variable env del shell.
# No se usa import porque medir.py necesita ese env y no es un módulo de Python instalado.

I = env['taller.inscripcion']
# Recordset vacío del modelo. Es el punto de partida para search, search_count y
# _read_group. Se le pone un nombre corto porque se repite mucho.

dom = [('state', '=', 'confirmada')]
# Dominio del ORM: solo las inscripciones confirmadas. Se traduce a
# WHERE state = 'confirmada'. El campo state tiene index=True desde hoy.

# ---------------- C1: contar ----------------
medir("C1a len(search())", lambda: len(I.search(dom)))
# search() ejecuta SELECT id ... WHERE ... ORDER BY ... y trae TODOS los ids a Python.
# Con ellos construye un recordset y len() lo cuenta en Python. Se transfieren y ordenan
# decenas de miles de ids solo para obtener un número.
# El lambda es necesario porque medir() espera una función que pueda llamar varias veces,
# no el resultado ya calculado.

medir("C1b search_count()", lambda: I.search_count(dom))
# search_count() ejecuta SELECT COUNT(*) ... WHERE ...: la base de datos cuenta y devuelve
# un solo entero, sin ORDER BY y sin transferir ids.
# Referencia medida: 108 ms frente a 10 ms.

# ---------------- C3: agrupar por mes ----------------
from datetime import timedelta
desde = fields.Datetime.now() - timedelta(days=365)
# Hace un año, en UTC. fields.Datetime.now() devuelve un datetime naive en UTC, que es
# como Odoo guarda todas las fechas con hora.
# (fields está disponible en el shell; si no lo estuviera: from odoo import fields)

dom3 = dom + [('fecha_inscripcion', '>=', desde)]
# Confirmadas y del último año. Sumar listas equivale a un AND entre las condiciones.

def por_mes_python():
    # Versión A: traer los registros y agrupar en Python.
    r = {}
    for i in I.search(dom3):                 # 1 consulta: los ids que cumplen el dominio
        ts = fields.Datetime.context_timestamp(i, i.fecha_inscripcion)
        # Al leer i.fecha_inscripcion por primera vez, el ORM carga ese campo para un bloque
        # de hasta 1.000 registros (prefetch). Eso es 1 consulta por cada 1.000 registros.
        # context_timestamp pasa la fecha de UTC a la zona horaria del usuario. Sin esto,
        # una inscripción del 1 de mayo a las 00:30 en España (30 de abril en UTC) contaría
        # en abril y no coincidiría con la versión B.
        k = ts.strftime('%Y-%m')             # clave del mes: '2026-05'
        r[k] = r.get(k, 0) + 1               # contador por mes
    return r

def por_mes_bd():
    # Versión B: que agrupe PostgreSQL.
    g = I._read_group(dom3, ['fecha_inscripcion:month'], ['__count'])
    # _read_group(dominio, agrupar_por, agregados) ejecuta una sola consulta del tipo
    #   SELECT date_trunc('month', <fecha en la zona del usuario>), COUNT(*) ... GROUP BY 1
    # - 'fecha_inscripcion:month' : agrupa por mes, en la zona horaria del contexto.
    # - '__count'                 : número de registros de cada grupo.
    # Devuelve una lista de tuplas (inicio_del_mes, número).
    # Es la versión interna de read_group, que en Odoo 19 está obsoleta para código nuevo.
    return {m.strftime('%Y-%m'): n for m, n in g}
    # Mismo formato que la versión A ({'2026-05': n, ...}), para poder compararlas.

a = medir("C3a bucle", por_mes_python)
b = medir("C3b _read_group", por_mes_bd)
# Aquí se pasa la función sin paréntesis (no hay lambda porque no tiene argumentos).
# medir() devuelve el resultado de la última repetición, así que a y b son los diccionarios.
# Referencia medida: 764 ms y 54 consultas frente a 30 ms y 1 consulta.

a == b   # True, 13 meses
# Prueba de que la optimización no cambia el resultado: mismos meses y mismas cifras.
# Salen 13 claves porque 365 días hacia atrás abarcan el mes actual (incompleto),
# los 11 anteriores y el final del mes de hace un año.# Se ejecuta en una terminal del equipo, no dentro de Python:
#   docker compose exec odoo odoo shell -d mf1215_rend --no-http
# - docker compose exec odoo : ejecuta un comando dentro del contenedor "odoo".
# - odoo shell               : abre un intérprete de Python con Odoo cargado. Ya existen
#                              las variables env (entorno del ORM), self (el usuario) y odoo.
# - -d mf1215_rend           : base de pruebas de rendimiento (5.000 contactos, 100.000
#                              inscripciones). Nunca la base de trabajo mf1215.
# - --no-http                : no arranca el servidor web. El contenedor ya ocupa el
#                              puerto 8069 y en el shell no se necesita.

exec(open('/mnt/extra-addons/gestion_eventos_empresa/scripts/medir.py').read())
# Lee el fichero medir.py del addon (montado en /mnt/extra-addons) y ejecuta su código
# en esta sesión. Así quedan definidas medir() y plan(), que usan la variable env del shell.
# No se usa import porque medir.py necesita ese env y no es un módulo de Python instalado.

I = env['taller.inscripcion']
# Recordset vacío del modelo. Es el punto de partida para search, search_count y
# _read_group. Se le pone un nombre corto porque se repite mucho.

dom = [('state', '=', 'confirmada')]
# Dominio del ORM: solo las inscripciones confirmadas. Se traduce a
# WHERE state = 'confirmada'. El campo state tiene index=True desde hoy.

# ---------------- C1: contar ----------------
medir("C1a len(search())", lambda: len(I.search(dom)))
# search() ejecuta SELECT id ... WHERE ... ORDER BY ... y trae TODOS los ids a Python.
# Con ellos construye un recordset y len() lo cuenta en Python. Se transfieren y ordenan
# decenas de miles de ids solo para obtener un número.
# El lambda es necesario porque medir() espera una función que pueda llamar varias veces,
# no el resultado ya calculado.

medir("C1b search_count()", lambda: I.search_count(dom))
# search_count() ejecuta SELECT COUNT(*) ... WHERE ...: la base de datos cuenta y devuelve
# un solo entero, sin ORDER BY y sin transferir ids.
# Referencia medida: 108 ms frente a 10 ms.

# ---------------- C3: agrupar por mes ----------------
from datetime import timedelta
desde = fields.Datetime.now() - timedelta(days=365)
# Hace un año, en UTC. fields.Datetime.now() devuelve un datetime naive en UTC, que es
# como Odoo guarda todas las fechas con hora.
# (fields está disponible en el shell; si no lo estuviera: from odoo import fields)

dom3 = dom + [('fecha_inscripcion', '>=', desde)]
# Confirmadas y del último año. Sumar listas equivale a un AND entre las condiciones.

def por_mes_python():
    # Versión A: traer los registros y agrupar en Python.
    r = {}
    for i in I.search(dom3):                 # 1 consulta: los ids que cumplen el dominio
        ts = fields.Datetime.context_timestamp(i, i.fecha_inscripcion)
        # Al leer i.fecha_inscripcion por primera vez, el ORM carga ese campo para un bloque
        # de hasta 1.000 registros (prefetch). Eso es 1 consulta por cada 1.000 registros.
        # context_timestamp pasa la fecha de UTC a la zona horaria del usuario. Sin esto,
        # una inscripción del 1 de mayo a las 00:30 en España (30 de abril en UTC) contaría
        # en abril y no coincidiría con la versión B.
        k = ts.strftime('%Y-%m')             # clave del mes: '2026-05'
        r[k] = r.get(k, 0) + 1               # contador por mes
    return r

def por_mes_bd():
    # Versión B: que agrupe PostgreSQL.
    g = I._read_group(dom3, ['fecha_inscripcion:month'], ['__count'])
    # _read_group(dominio, agrupar_por, agregados) ejecuta una sola consulta del tipo
    #   SELECT date_trunc('month', <fecha en la zona del usuario>), COUNT(*) ... GROUP BY 1
    # - 'fecha_inscripcion:month' : agrupa por mes, en la zona horaria del contexto.
    # - '__count'                 : número de registros de cada grupo.
    # Devuelve una lista de tuplas (inicio_del_mes, número).
    # Es la versión interna de read_group, que en Odoo 19 está obsoleta para código nuevo.
    return {m.strftime('%Y-%m'): n for m, n in g}
    # Mismo formato que la versión A ({'2026-05': n, ...}), para poder compararlas.

a = medir("C3a bucle", por_mes_python)
b = medir("C3b _read_group", por_mes_bd)
# Aquí se pasa la función sin paréntesis (no hay lambda porque no tiene argumentos).
# medir() devuelve el resultado de la última repetición, así que a y b son los diccionarios.
# Referencia medida: 764 ms y 54 consultas frente a 30 ms y 1 consulta.

a == b   # True, 13 meses
# Prueba de que la optimización no cambia el resultado: mismos meses y mismas cifras.
# Salen 13 claves porque 365 días hacia atrás abarcan el mes actual (incompleto),
# los 11 anteriores y el final del mes de hace un año.