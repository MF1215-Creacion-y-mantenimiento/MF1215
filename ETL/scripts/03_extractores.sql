-- 03_extractores.sql · Consultas sobre el almacén (nunca sobre las tablas de Odoo)

-- C1. Embudo por etapa
SELECT  e.nombre                    AS etapa,
        COUNT(*)                    AS oportunidades,
        SUM(h.ingreso_esperado)     AS ingreso_esperado,
        SUM(h.ingreso_ponderado)    AS ingreso_ponderado
FROM    lab.hechos_oportunidades h
JOIN    lab.dim_etapa e ON e.etapa_key = h.etapa_key
GROUP BY    e.nombre, e.orden
ORDER BY    e.orden;

-- C2. Embudo por comercial
SELECT  c.nombre                    AS comercial,
        COUNT(*)                    AS oportunidades,
        SUM(h.ingreso_esperado)     AS ingreso_esperado,
        SUM(h.ingreso_ponderado)    AS ingreso_ponderado
FROM    lab.hechos_oportunidades h
JOIN    lab.dim_comercial c ON c.comercial_key = h.comercial_key
GROUP BY    c.nombre
ORDER BY    ingreso_ponderado DESC;

-- C3. Totales del embudo
SELECT  COUNT(*)                    AS oportunidades,
        SUM(ingreso_esperado)       AS ingreso_esperado,
        SUM(ingreso_ponderado)      AS ingreso_ponderado,
        ROUND(SUM(ingreso_ponderado) / NULLIF(SUM(ingreso_esperado), 0) * 100, 2) AS probabilidad_media_pct
FROM    lab.hechos_oportunidades;