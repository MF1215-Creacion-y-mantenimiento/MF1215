-- P1 Filas: líneas de origen
SELECT (SELECT COUNT(*)
        FROM    sale_order_line l JOIN sale_order o ON o.id = l.order_id
        WHERE   o.state = 'sale' AND l.display_type IS NULL)    AS filas_origen,
        (SELECT COUNT(*) FROM lab.hechos_ventas)                AS filas_almacen;

-- P2 Cuadre del importe con el subtotal que calcula Odoo





-- P3 Hechos huérfanos (debe salir 0)




-- P4 Duplicados tras ejecutar el ETL dos veces




-- P5 Registro de cargas, la más reciente primero




-- P6 (si se conservan los datos de control de la E2 de la UF1888)