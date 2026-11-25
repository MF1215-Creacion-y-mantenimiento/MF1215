-- estructura_dw.sql . Almacén de ventas en estrella (esquema lab)
-- Repetible: IF NOT EXISTS no falla si las tablas no existe

-- Dimensión cliente: una fila por cliente con venta
CREATE TABLE IF NOT EXISTS lab.dim_cliente (
    cliente_key             serial          PRIMARY KEY,        --clave subrogada
    cliente_id_origen       integer         NOT NULL UNIQUE,    --res_partner.id
    nombre                  varchar(200)    NOT NULL,
    ciudad                  varchar(100)    NOT NULL,
    pais                    varchar(100)    NOT NULL              
);

-- Dimensión producto: una fila por producto (servicio) vendido
CREATE TABLE IF NOT EXISTS lab.dim_producto (
    producto_key             serial          PRIMARY KEY,
    producto_id_origen       integer         NOT NULL UNIQUE,    --product_product.id
    nombre                  varchar(200)    NOT NULL,
    catageria               varchar(200)    NOT NULL
);

-- Tabla de hechos: una fila por línea de pedido confirmada (grano)
CREATE TABLE IF NOT EXISTS lab.hechos_ventas (
    venta_key               serial          PRIMARY KEY,
    linea_id_origen         integer         NOT NULL UNIQUE,    -- sale_order_line.id
    pedido                  varchar(50)     NOT NULL,
    fecha                   date            NOT NULL,
    cliente_key             integer         NOT NULL REFERENCES lab.dim_cliente (cliente_key),
    producto_key            integer         NOT NULL REFERENCES lab.dim_producto (producto_key),
    cantidad                numeric(12,2)   NOT NULL,
    precio_unitario         numeric(12,2)   NOT NULL,
    total                   numeric(14,2)   NOT NULL            
);

-- Registro de cargas
CREATE TABLE IF NOT EXISTS lab.etl_log (
    log_id              serial          PRIMARY KEY,
    fecha_carga         timestamp       NOT NULL DEFAULT now(),
    proceso             varchar(60)     NOT NULL,
    tabla               varchar(60)     NOT NULL,
    filas               integer         NOT NULL,
    observaciones       text             
);