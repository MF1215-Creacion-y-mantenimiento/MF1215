-- C1. Ventas por cliente
SELECT c.nombre AS cliente, count(DISTINCT h.referencia) AS pedidos, sum(h.total) AS importe
FROM lab.bod_hechos_ventas h JOIN lab.bod_dim_cliente c USING (cliente_key)
GROUP BY c.nombre ORDER BY importe DESC;

-- C2. Ventas por productos
SELECT p.nombre AS producto, p.categoria, sum(h.cantidad) AS unidades, sum(h.total) AS importe
FROM lab.bod_hechos_ventas h JOIN lab.bod_dim_producto p USING (producto_key)
GROUP BY p.nombre, p.categoria ORDER BY  importe DESC;

-- C3. Ventas totales
SELECT sum(total) AS importe_total, count(DISTINCT referencia) AS pedidos, count(*) AS lineas
FROM lab.bod_hechos_ventas;

-- C4. Ventas por año y mes
SELECT t.anio, t.mes, sum(h.total) AS importe
FROM lab.bod_hechos_ventas h JOIN lab.bod_dim_tiempo t USING (fecha_key)
GROUP BY t.anio, t.mes ORDER BY t.anio, t.mes;

-- C5. Análisis tip cubo: categoría + trimestre con subtotales
SELECT  COALESCE(p.categoria, 'TOTAL categorías') AS categoría,
        COALESCE('T' || t.trimestre, 'Total año') AS trimestre,
        sum(h.total) AS importe
FROM lab.bod_hechos_ventas h 
JOIN lab.bod_dim_producto p USING (producto_key)
JOIN lab.bod_dim_tiempo   t USING (fecha_key)
GROUP BY ROLLUP (p.categoria, t.trimestre)
ORDER BY p.categoria NULLS LAST, t.trimestre NULLS LAST;