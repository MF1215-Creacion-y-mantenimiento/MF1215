-- Ventas por cliente
SELECT  c.nombre                    AS  cliente,
        COUNT(DISTINCT h.pedido)    AS pedido,
        SUM(h.total)                AS importe_total
FROM    lab.hechos_ventas h
JOIN    lab.dim_cliente c ON c.cliente_key = h.cliente_key
GROUP   BY  c.nombre
ORDER   BY importe_total DESC;

-- Ventas por producto
SELECT  p.nombre                    AS producto,
        p.categoria,
        SUM(h.cantidad)             AS cantidad_vendida,
        SUM(h.total)                AS importe_total
FROM    lab.hechos_ventas   h
JOIN    lab.dim_producto    p ON    p.producto_key = h.producto_key
GROUP   BY p.nombre, p.categoria
ORDER   BY importe_total DESC;

-- Ventas totales
SELECT  SUM(total)                  AS importe_total,
        COUNT(DISTINCT pedido)      AS pedidos,
        COUNT(*)                    AS lineas
FROM    lab.hechos_ventas;
