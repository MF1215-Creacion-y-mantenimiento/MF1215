-- P1 Filas: líneas de origen
SELECT (SELECT COUNT(*)
        FROM    sale_order_line l JOIN sale_order o ON o.id = l.order_id
        WHERE   o.state = 'sale' AND l.display_type IS NULL)    AS filas_origen,
        (SELECT COUNT(*) FROM lab.hechos_ventas)                AS filas_almacen;

-- P2 Cuadre del importe con el subtotal que calcula Odoo
SELECT (SELECT SUM(l.price_subtotal)
        FROM sale_order_line l JOIN sale_order o ON o.id = l.order_id
        WHERE o.state = 'sale' AND l.display_type IS NULL)      AS importe_origen,
        (SELECT SUM(total) FROM lab.hechos_ventas)              AS importe_almacen;          


-- P3 Hechos huérfanos (debe salir 0)
SELECT COUNT(*)  AS huerfanos
FROM lab.hechos_ventas h
LEFT JOIN lab.dim_cliente c ON c.cliente_key = h.cliente_key
LEFT JOIN lab.dim_producto p ON p.producto_key = h.producto_key
WHERE c.cliente_key IS NULL
OR p.producto_key IS NULL;

-- P4 Duplicados tras ejecutar el ETL dos veces
SELECT linea_id_origen, COUNT(*)
FROM lab.hechos_ventas
GROUP BY linea_id_origen
HAVING COUNT(*) > 1;

-- P5 Registro de cargas, la más reciente primero
SELECT * FROM lab.etl_log WHERE proceso = 'ETL ventas' ORDER BY log_id DESC LIMIT 6;

-- P6 (si se conservan los datos de control de la E2 de la UF1888)
SELECT nombre, COUNT(DISTINCT h.pedido) AS pedidos, SUM(h.total) AS importe
FROM lab.hechos_ventas h JOIN lab.dim_cliente c ON c.cliente_key = h.cliente_key
WHERE c.nombre LIKE 'E2 %'
GROUP BY c.nombre ORDER BY c.nombre;