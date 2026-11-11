# -*- coding: utf-8 -*-
"""
medir.py · MF1215_3 · UF1889 · Sesión 7 (11/11/2026)

Instrumentos de medida para odoo shell:
    >>> exec(open('/mnt/extra-addons/gestion_eventos_empresa/scripts/medir.py').read())

medir(nombre, funcion, repeticiones=5)
    Ejecuta la función con la caché del ORM vacía en cada repetición.
    Imprime la mediana del tiempo, las consultas SQL y un resumen del resultado.
    Devuelve el resultado de la última ejecución (para comparar a == b).

plan(modelo, dominio)
    Muestra el EXPLAIN (ANALYZE, BUFFERS) de la consulta que genera el ORM
    para ese dominio. Ojo: ANALYZE ejecuta la consulta de verdad.
"""
import statistics
import time

from odoo.tools import SQL


def _resumen(r):
    if isinstance(r, (int, float)):
        return str(r)
    if hasattr(r, '_name') and hasattr(r, 'ids'):
        return '%s(%d registros)' % (r._name, len(r))
    if isinstance(r, dict):
        return 'dict(%d claves)' % len(r)
    if isinstance(r, (list, tuple)):
        return '%s(%d elementos)' % (type(r).__name__, len(r))
    texto = repr(r)
    return texto if len(texto) <= 40 else texto[:37] + '...'


def medir(nombre, funcion, repeticiones=5):
    tiempos, consultas, resultado = [], [], None
    for _ in range(repeticiones):
        env.invalidate_all()                      # noqa: F821  caché vacía
        antes = env.cr.sql_log_count              # noqa: F821  consultas hasta ahora
        t0 = time.perf_counter()
        resultado = funcion()
        tiempos.append((time.perf_counter() - t0) * 1000)
        consultas.append(env.cr.sql_log_count - antes)  # noqa: F821
    print('%-32s %8.1f ms %7d consultas  -> %s' % (
        nombre, statistics.median(tiempos),
        int(statistics.median(consultas)), _resumen(resultado)))
    return resultado


def plan(modelo, dominio):
    env.invalidate_all()                          # noqa: F821
    consulta = env[modelo]._search(dominio).select()  # noqa: F821
    env.cr.execute(SQL('EXPLAIN (ANALYZE, BUFFERS) %s', consulta))  # noqa: F821
    for (linea,) in env.cr.fetchall():            # noqa: F821
        print(linea)


print('medir() y plan() cargados.')
