-- 02_etl.sql · ETL del embudo comercial: Odoo (public) -> almacén (lab)
-- Carga completa: vacía el almacén y lo vuelve a llenar. Repetirla no duplica datos.
BEGIN;

-- 0. Vaciar las tablas del almacén (los hechos primero: dependen de las dimensiones)
TRUNCATE lab.hechos_oportunidades, lab.dim_etapa, lab.dim_comercial RESTART IDENTITY;

-- 1. Dimensión etapa
INSERT INTO lab.dim_etapa (etapa_id_origen, nombre, orden, es_ganada)
SELECT s.id,
       TRIM(COALESCE(s.name ->> 'es_ES', s.name ->> 'en_US')),   -- name es jsonb (campo traducible)
       s.sequence,
       COALESCE(s.is_won, false)
FROM   crm_stage s;

INSERT INTO lab.etl_log (proceso, tabla, filas)
SELECT 'ETL embudo', 'dim_etapa', COUNT(*) FROM lab.dim_etapa;

-- 2. Dimensión comercial: miembro «Sin comercial» + usuarios con oportunidades
INSERT INTO lab.dim_comercial (comercial_id_origen, nombre)
VALUES (0, 'Sin comercial');

INSERT INTO lab.dim_comercial (comercial_id_origen, nombre)
SELECT u.id,
       TRIM(p.name)
FROM   res_users u
JOIN   res_partner p ON p.id = u.partner_id
WHERE  u.id IN (SELECT DISTINCT user_id FROM crm_lead WHERE user_id IS NOT NULL);

INSERT INTO lab.etl_log (proceso, tabla, filas)
SELECT 'ETL embudo', 'dim_comercial', COUNT(*) FROM lab.dim_comercial;

-- 3. Hechos: oportunidades activas, con sus claves de dimensión y medidas calculadas
INSERT INTO lab.hechos_oportunidades
       (oportunidad_id_origen, fecha_creacion, etapa_key, comercial_key,
        ingreso_esperado, probabilidad, ingreso_ponderado)
SELECT l.id,
       l.create_date::date,
       de.etapa_key,
       dc.comercial_key,
       COALESCE(l.expected_revenue, 0),
       ROUND(COALESCE(l.probability, 0)::numeric, 2),
       ROUND(COALESCE(l.expected_revenue, 0) * COALESCE(l.probability, 0)::numeric / 100, 2)
FROM   crm_lead l
JOIN   lab.dim_etapa     de ON de.etapa_id_origen     = l.stage_id
JOIN   lab.dim_comercial dc ON dc.comercial_id_origen = COALESCE(l.user_id, 0)
WHERE  l.type = 'opportunity'
  AND  l.active = true;

INSERT INTO lab.etl_log (proceso, tabla, filas)
SELECT 'ETL embudo', 'hechos_oportunidades', COUNT(*) FROM lab.hechos_oportunidades;

COMMIT;