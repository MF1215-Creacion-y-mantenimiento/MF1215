# MF1215_3 · UF1889 · Día 22 · Medición C2: resumen por estado de 80 eventos
from odoo import fields
# Importa el módulo de campos de Odoo. Este script no lo usa directamente; se deja por
# coherencia con medir_c1_c3.py, donde hacía falta para fields.Datetime. Si se quita,
# no pasa nada.

exec(open('/mnt/extra-addons/gestion_eventos_empresa/scripts/medir.py').read())
# Carga medir() y plan() en la sesión. Se usa exec y no import porque medir.py necesita
# la variable env, que solo existe dentro de odoo shell. El código de medir.py se ejecuta
# "aquí dentro" y ve ese env.

I = env['taller.inscripcion']
E = env['taller.evento']
# Recordsets vacíos de los dos modelos: el punto de partida para buscar, contar y agrupar.
# Nombres cortos porque se repiten mucho.

ESTADOS = ['borrador', 'confirmada', 'cancelada']
# Los tres valores técnicos del campo Selection state de la inscripción. Su orden fija el
# orden de los números en cada resultado: (borrador, confirmadas, canceladas).
# En mayúsculas por convenio de Python para una constante.


def resumen_lento():
    # Versión ANTES: el patrón N+1.
    eventos = E.search([], limit=80)
    # 1 consulta: los ids de los 80 primeros eventos, en el orden por defecto del modelo
    # (_order). Se fijan 80 porque es lo que muestra una lista de Odoo por página.
    # Dominio vacío [] = sin filtro. Si hay menos de 80 eventos, trae todos.

    return {e.id: tuple(I.search_count([('evento_id', '=', e.id), ('state', '=', s)])
                        for s in ESTADOS)
            for e in eventos}
    # Comprensión de diccionario: una entrada por evento.
    #   clave -> e.id (el id del evento)
    #   valor -> tupla de 3 números, uno por estado.
    # Por cada evento y cada estado lanza un search_count, es decir, un
    #   SELECT COUNT(*) FROM taller_inscripcion WHERE evento_id = X AND state = 'Y'
    # 80 eventos × 3 estados = 240 consultas, más la de los eventos = 241.
    # Cada consulta es rápida, pero son 241 viajes a PostgreSQL. Con 800 eventos serían
    # 2.401: el coste crece con el número de registros (N+1).
    # Resultado: {12: (3, 18, 1), 13: (0, 25, 2), ...}


def resumen_rapido():
    # Versión DESPUÉS: una sola consulta agrupada.
    eventos = E.search([], limit=80)
    # Los mismos 80 eventos que en la versión lenta (misma consulta, mismo orden), para
    # que la comparación sea justa. 1 consulta.

    grupos = I._read_group([('evento_id', 'in', eventos.ids)],
                           ['evento_id', 'state'], ['__count'])
    # _read_group(dominio, agrupar_por, agregados) genera UNA consulta:
    #   SELECT evento_id, state, COUNT(*) FROM taller_inscripcion
    #   WHERE evento_id IN (80 ids) GROUP BY evento_id, state
    # - eventos.ids                : lista de los 80 ids, para el IN.
    # - ['evento_id', 'state']     : un grupo por cada combinación evento + estado.
    # - ['__count']                : cuántas inscripciones hay en cada grupo.
    # Devuelve una lista de tuplas (evento, estado, número). Ejemplo:
    #   [(taller.evento(12,), 'borrador', 3), (taller.evento(12,), 'confirmada', 18), ...]
    # El evento llega como registro (recordset de 1), no como id. Una combinación sin
    # inscripciones NO aparece: si un evento no tiene canceladas, no hay tupla para eso.
    # Con el índice compuesto (evento_id, state), PostgreSQL resuelve esta consulta
    # leyendo solo el índice (Index Only Scan, caso C7).

    conteo = {(ev.id, st): n for ev, st, n in grupos}
    # Convierte la lista en un diccionario para buscar en un solo paso:
    #   {(12, 'borrador'): 3, (12, 'confirmada'): 18, ...}
    # La clave es una tupla (id_evento, estado). ev.id no lanza ninguna consulta: el id
    # ya viene en el registro.

    return {e.id: tuple(conteo.get((e.id, s), 0) for s in ESTADOS) for e in eventos}
    # Mismo formato exacto que resumen_lento(), para poder compararlos con ==.
    # conteo.get(clave, 0): si esa combinación no vino en los grupos (no hay inscripciones
    # en ese estado), vale 0. Sin el 0 por defecto daría None o KeyError.
    # Recorre eventos (no grupos) para que también salgan los eventos sin ninguna
    # inscripción, con (0, 0, 0), igual que en la versión lenta.
    # Total: 2 consultas, tenga la lista 80 eventos u 800.


c2a = medir("C2a search_count x evento", resumen_lento)
c2b = medir("C2b _read_group", resumen_rapido)
# medir(etiqueta, función) ejecuta la función 5 veces, vaciando antes la caché del ORM
# (env.invalidate_all), e imprime la mediana del tiempo y el número de consultas SQL.
# La función se pasa sin paréntesis: se entrega la función para que medir() la llame,
# no su resultado. medir() devuelve el resultado de la última ejecución: c2a y c2b son
# los dos diccionarios.

print("¿Mismo resultado?", c2a == c2b)
# Comprobación de corrección: optimizar no puede cambiar el resultado. == compara los
# dos diccionarios clave a clave y tupla a tupla. Debe salir True. Si sale False, lo
# habitual es haber olvidado el 0 por defecto o haber cambiado el orden de ESTADOS.

# C2c solo funciona después de añadir los campos al modelo y actualizar con -u
if 'num_borrador' in E._fields:
    # E._fields es el diccionario de campos que el modelo tiene registrados ahora mismo.
    # Si el campo aún no existe (no se ha implementado o falta el -u), se salta la
    # medición en vez de fallar con AttributeError.
    medir("C2c campos del modelo",
          lambda: [(e.num_borrador, e.num_confirmadas, e.num_canceladas)
                   for e in E.search([], limit=80)])
    # Simula lo que hace la vista lista: buscar 80 eventos y leer los 3 contadores.
    # Aquí sí hace falta lambda, porque la expresión no es una función con nombre.
    # Al leer e.num_borrador del primer evento, el ORM llama a
    # _compute_resumen_inscripciones con los 80 eventos a la vez (prefetch), no uno a
    # uno. El método rellena los 3 campos, así que num_confirmadas y num_canceladas ya
    # no consultan nada.
    # Esperado: unas 241 consultas con la versión lenta en el modelo y unas 2 con la
    # versión de _read_group.
else:
    print("C2c pendiente: el modelo aún no tiene num_borrador (falta implementar y -u)")