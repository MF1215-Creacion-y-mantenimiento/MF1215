BEGIN;

TRUNCATE lab.bod_hechos_ventas, lab.bod_dim_cliente, lab.bod_dim_producto, lab.bod_dim_tiempo
    RESTART IDENTITY;

1. Dimensión cliente: solo clientes con algún pedido confirmado

WITH ins AS (
    INSERT INTO lab.bod_dim_cliente (id_origen, nombre, ciudad, pais)
    SELECT  c.id,
            btrim(c.nombre),
            COALESCE(NULLIF(btrim(c.ciudad), ''), 'Sin ciudad'),
            COALESCE(p.nombre ->> 'es_ES', 'Sin país')
    FROM lab.erp_cliente c 
    LEFT JOIN lab.erp_pais p ON p.id = c.pais_id
    WHERE EXISTS (SELECT 1 FROM lab.erp_pedido o
                WHERE o.cliente_id = c.id AND o.estado = 'confirmado')
    RETURNING 1)
    INSERT INTO lab.bod_etl_log (tabla, filas) SELECT 'bod_dim_cliente', count(*) FROM ins;

2. Dimensión producto: 

WITH ins AS (
    INSERT INTO lab.bod_dim_producto (id_origen, nombre, categoria)
    SELECT  pr.id,
            btrim(pr.nombre ->> 'es_ES'),
            COALESCE(cat.nombre, 'Sin categoría')
    FROM lab.erp_producto pr
    LEFT JOIN lab.erp_categoria cat ON cat.id = pr.categoria_id
    RETURNING 1)
INSERT INTO lab.bod_etl_log (tabla, filas) SELECT 'bod_dim_producto', count(*) FROM ins;

3. Dimensión tiempo: fechas distintas de los pedidos confirmados
WITH ins AS (
    INSERT INTO lab.bod_dim_tiempo (fecha_key, fecha, dia, mes, trimestre, anio)
    SELECT DISTINCT
            to_char(o.fecha_pedido::date, 'YYYYMMDD')::int,
            o.fecha_pedido::date,
            extract(day       FROM o.fecha_pedido)::smallint,
            extract(month     FROM o.fecha_pedido)::smallint,
            extract(quarter   FROM o.fecha_pedido)::smallint,
            extract(year      FROM o.fecha_pedido)::smallint
    FROM lab.erp_pedido o
    WHERE o.estado = 'confirmado'
    RETURNING 1)
INSERT INTO lab.bod_etl_log (tabla, filas) SELECT 'bod_dim_tiempo', count(*) FROM ins;

4. Hechos: líneas de producto 
WITH ins AS (
    INSERT INTO lab.bod_hechos_ventas
        (id_linea_origen, referencia, cliente_key, producto_key, fecha_key,
        cantidad, precio_unitario, descuento, total)
    SELECT l.id, o.referencia, dc.cliente_key, dp.producto_key,
        to_char(o.fecha_pedido::date, 'YYYYMMDD')::int,
        l.cantidad, l.precio_unitario, l.descuento,
        round(l.cantidad * l.precio_unitario * (1 - l.descuento / 100), 2)
    FROM lab.erp_linea_pedido l
    JOIN lab.erp_pedido o           ON o.id = l.pedido_id
    JOIN lab.bod_dim_cliente dc     ON dc.id_origen = o.cliente_id
    JOIN lab.bod_dim_producto dp    ON dp.id_origen = l.producto_id
    WHERE o.estado = 'confirmado'
    AND l.tipo_linea IS NULL
    RETURNING 1)
INSERT INTO lab.bod_etl_log (tabla, filas) SELECT 'bod_hechos_ventas', count(*) FROM ins;

COMMIT;
