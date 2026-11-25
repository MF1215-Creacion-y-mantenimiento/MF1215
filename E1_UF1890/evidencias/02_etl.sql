-- etl.sql ETL ventas: Odoo (public) -> almacén (lab)
BEGIN;

TRUNCATE lab.hechos_ventas, lab.dim_cliente, lab.dim_producto RESTART IDENTITY;

-- Dimensión cliente
INSERT INTO lab.dim_cliente (cliente_id_origen, nombre, ciudad, pais)
SELECT  p.id,
        TRIM(p.name),
        COALESCE(NULLIF(TRIM(p.city), ''), 'Sin ciudad'),
        COALESCE(c.name ->> 'es_ES', c.name ->> 'en_US', 'Sin país')
FROM    res_partner p
LEFT    JOIN res_country c ON c.id = p.country_id
WHERE   p.id IN (SELECT partner_id FROM sale_order WHERE state = 'sale');

INSERT INTO lab.etl_log (proceso, tabla, filas)
SELECT 'ETL ventas', 'dim_cliente', COUNT(*) FROM lab.dim_cliente;

-- Dimensión producto:
INSERT INTO lab.dim_producto (producto_id_origen, nombre, categoria)
SELECT  pp.id,
        TRIM(COALESCE(pt.name ->> 'es_ES', pt.name ->> 'en_US')),
        COALESCE(pc.name, 'Sin categoria')
FROM    product_product pp
JOIN    product_template pt ON pt.id = pp.product_tmpl_id
LEFT    JOIN product_category pc ON pc.id = pt.categ_id
WHERE   pp.id IN (SELECT l.product_id
                    FROM    sale_order_line l
                    JOIN    sale_order o ON o.id = l.order_id
                    WHERE   o.state = 'sale'
                    AND     l.display_type IS NULL);

INSERT INTO lab.etl_log (proceso, tabla, filas)
SELECT 'ETL ventas', 'dim_producto', COUNT(*) FROM lab.dim_producto;

-- Hechos: líneas de producto de pedidos confirmados
INSERT INTO lab.hechos_ventas
        (linea_id_origen, pedido, fecha, cliente_key, producto_key,
        cantidad, precio_unitario, total)
SELECT  l.id,
        o.name,
        o.date_order::date,
        dc.cliente_key,
        dp.producto_key,
        l.product_uom_qty,
        ROUND(l.price_unit::numeric, 2),
        ROUND(l.product_uom_qty * l.price_unit::numeric * (1 - COALESCE(l.discount, 0) / 100), 2)
FROM    sale_order_line l
JOIN    sale_order o        ON o.id = l.order_id
JOIN    lab.dim_cliente dc  ON dc.cliente_id_origen = o.partner_id
JOIN    lab.dim_producto dp ON dp.producto_id_origen = l.product_id
WHERE   o.state = 'sale'
AND     l.display_type IS NULL;


INSERT INTO lab.etl_log (proceso, tabla, filas)
SELECT 'ETL ventas', 'hechos_ventas', COUNT(*) FROM lab.hechos_ventas;

COMMIT;