# Rendimiento con grandes volúmenes

Addon `gestion_eventos_empresa` · versión 19.0.1.3.0 · Fase 5 (11/11/2026)
Autor/a: _______________________

## 1. Método

- Base de pruebas: `mf1215_rend` (copia de `mf1215`)
- Volumen: ___ contactos VOL · ___ eventos VOL · ___ inscripciones (semilla 1215)
- Reparto por estado (`SELECT state, count(*) FROM taller_inscripcion GROUP BY state;`):

| state | count |
|---|---|
| borrador | |
| confirmada | |
| cancelada | |

- Instrumentos: `medir()` (mediana de 5 ejecuciones, caché vacía, `env.cr.sql_log_count`) y `plan()` (EXPLAIN ANALYZE, BUFFERS)
- Equipo: _______________________ (CPU, RAM, Docker Desktop)
- Reglas aplicadas: mismos datos · caché vacía · mediana · mismo resultado · un cambio cada vez

## 2. Mediciones antes y después

| Caso | Descripción | Antes (ms) | Consultas | Después (ms) | Consultas | Mejora | Técnica |
|---|---|---|---|---|---|---|---|
| C1 | Contar confirmadas | | | | | | search_count |
| C2 | Resumen de 80 eventos (RF-16) | | | | | | _read_group |
| C2 | Resumen de 1.000 eventos | | | | | | _read_group |
| C2 alt. | Resumen con filtered() | | | — | — | — | — |
| C3 | Confirmadas por mes (último año) | | | | | | _read_group con :month |
| C4 | Correo de 2.000 inscripciones | | | | | | prefetch |
| C5 | Confirmadas últimos 30 días | | | | | | índice fecha_inscripcion |
| C6 | Inscripciones en borrador | | | | | | índice state |
| C7 | Consulta del resumen (psql) | | | | | | índice (evento_id, state) |

¿Coincide el resultado antes y después en cada caso? (a == b): _______

## 3. Planes de ejecución

### C5 · antes
```
(pegar aquí la salida de plan())
```
Tipo de nodo: ___ · rows estimado / real: ___ / ___ · Rows Removed by Filter: ___ · Execution Time: ___

### C5 · después
```
(pegar aquí la salida de plan())
```
Tipo de nodo: ___ · rows estimado / real: ___ / ___ · Execution Time: ___

### Otros planes (C6, C7, state = 'confirmada')
```
```

## 4. Cambios en el código y justificación

| Cambio | Fichero | Qué consulta mejora | Medida | Por qué |
|---|---|---|---|---|
| Resumen con _read_group | models/taller_evento.py | | | |
| No almacenar el resumen (sin store) | models/taller_evento.py | | | |
| index=True en fecha_inscripcion | models/taller_inscripcion.py | | | |
| index=True en state | models/taller_inscripcion.py | | | |
| models.Index('(evento_id, state)') | models/taller_inscripcion.py | | | |

Respuestas de P4 (prefetch):
1. ¿Por qué C4b hace 4 consultas y no 2?
2. ¿Por qué C4a hace menos de 4.000?
3. ¿Por qué filtered() es más lenta que la versión 1 con muchas menos consultas?

## 5. Coste de los índices

| | 19.0.1.2.0 | 19.0.1.3.0 |
|---|---|---|
| Tamaño de la tabla | | |
| Número de índices | | |
| Tamaño de los índices (`pg_indexes_size`) | | |
| Alta de 5.000 inscripciones (opcional) | | |

## 6. Observaciones

- Zona horaria al agrupar por mes:
- Índices redundantes:
- Índice que no se borra al quitar index=True:
- Otras:
