-- 04_pruebas.sql · Comprobaciones de la carga

-- P1. Filas: origen que cumple las reglas frente a la filas cargadas

SELECT  (SELECT COUNT(*) FROM crm_lead WHERE type = 'opportunity' AND active = true)    AS filas_origen,
        (SELECT COUNT(*) FROM lab.hechos_oportunidades)                                 AS filas_almacen;

-- P2. Cuadre del importe con el origen
SELECT  (SELECT SUM(expected_revenue) FROM crm_lead WHERE type = 'opportunity' AND active = true) AS  importe_origen,
        (SELECT SUM(ingreso_esperado) FROM lab.hechos_oportunidades)                              AS importe_almacen;

-- P3. Hechos huérfanos (deben salir 0)
SELECT COUNT(*) AS huerfanos
FROM    lab.hechos_oportunidades h
LEFT JOIN   lab.dim_etapa       e   ON  e.etapa_key = h.etapa_key
LEFT JOIN   lab.dim_comercial   c   ON  c.comercial_key = h.comercial_key
WHERE       e.etapa_key IS NULL     OR  c.comercial_key IS NULL;

-- P4. Duplicados tras ejecutar el ETL dos veces (no debe salir ninguna fila)
SELECT oportunidad_id_origen, COUNT(*)
FROM   lab.hechos_oportunidades
GROUP BY    oportunidad_id_origen
HAVING COUNT(*) > 1;

-- P5. Datos de control (oportunidades GUIA)
SELECT COUNT(*) AS oportunidades, SUM(h.ingreso_esperado) AS esperado, SUM(h.ingreso_ponderado) AS ingreso_ponderado
FROM lab.hechos_oportunidades h
JOIN crm_lead l ON l.id = h.oportunidad_id_origen
WHERE l.name LIKE 'GUIA %';

-- P6. Registro de cargas, la más reciente primero
SELECT * FROM lab.etl_log ORDER BY log_id DESC LIMIT 6;