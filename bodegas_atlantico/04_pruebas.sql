-- P1. Filas: origen que cumple las reglas frente a hechos cargados
SELECT (SELECT count(*) FROM lab.erp_linea_pedido l JOIN lab.erp_pedido o ON o.id = l.pedido_id
        WHERE o.estado = 'confirmado' AND l.tipo_linea IS NULL) AS filas_almacen;

-- P2. Importe: sujma de subtotasl en origen frente a toal del almacén
SELECT (SELECT sum(l.subtotal) FROM lab.erp_linea_pedido l JOIN lab.erp_pedido o ON o.id = l.pedido_id
       WHERE o.estado = 'confirmado' AND l.tipo_linea IS NULL ) AS importe_origen,
       (SELECT sum(total) FROM lab.bod_hechos_ventas) AS importe_almacen;

-- P3. Hechos huérfanos
SELECT count(*) AS huerfanos
FROM lab.bod_hechos_ventas h 
LEFT JOIN lab.bod_dim_cliente c USING (cliente_key)
LEFT JOIN lab.bod_dim_producto p USING (producto_key)
LEFT JOIN lab.bod_dim_tiempo t USING (fecha_key)
WHERE c.cliente_key IS NULL OR p.producto_key IS NULL OR t.fecha_key IS NULL;

-- P4. Coherencia entre consultas
SELECT (SELECT sum(importe) FROM (SELECT sum(total) importe FROM lab.bod_hechos_ventas GROUP BY cliente_key) x) AS suma_por_cliente,
        (SELECT sum(total) FROM lab.bod_hechos_ventas) AS total;

-- P5. Sin duplicadostras la recarga
SELECT count(*) AS filas, count(DISTINCT id_linea_origen) AS lineas_distintas FROM LAB.bod_hechos_ventas;