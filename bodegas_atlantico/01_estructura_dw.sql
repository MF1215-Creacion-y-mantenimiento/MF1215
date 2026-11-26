-- Solución: Bodegas Atlantico · prefijo bod_
-- Crear si no existe

CREATE SCHEMA IF NOT EXISTS lab;

CREATE TABLE IF NOT EXISTS lab.bod_dim_cliente (
    cliente_key     serial          PRIMARY KEY,
    id_origen       integer         NOT NULL UNIQUE,
    nombre          varchar         NOT NULL,
    ciudad          varchar         NOT NULL,
    pais            varchar         NOT NULL
);

CREATE TABLE IF NOT EXISTS lab.bod_dim_producto (
    producto_key    serial          PRIMARY KEY,
    id_origen       integer         NOT NULL UNIQUE,
    nombre          varchar         NOT NULL,
    categoria       varchar         NOT NULL        
);

CREATE TABLE IF NOT EXISTS lab.bod_dim_tiempo (
    fecha_key       integer         PRIMARY KEY,    -- AAAAMMDD
    fecha           date            NOT NULL UNIQUE,
    dia             smallint        NOT NULL,
    mes             smallint        NOT NULL,
    trimestre       smallint        NOT NULL,
    anio            smallint        NOT NULL
);

CREATE TABLE IF NOT EXISTS lab.bod_hechos_ventas (
    venta_key       serial          PRIMARY KEY,
    id_linea_origen integer         NOT NULL UNIQUE,
    referencia      varchar         NOT NULL,
    cliente_key     integer         NOT NULL REFERENCES lab.bod_dim_cliente(cliente_key),
    producto_key    integer         NOT NULL REFERENCES lab.bod_dim_producto(producto_key),
    fecha_key       integer         NOT NULL REFERENCES lab.bod_dim_tiempo(fecha_key),
    cantidad        numeric(10,2)   NOT NULL,
    precio_unitario numeric(10,2)   NOT NULL,
    descuento       numeric(5,2)    NOT NULL,
    total           numeric(12,2)   NOT NULL    
);

CREATE TABLE IF NOT EXISTS lab.bod_etl_log (
    id              serial          PRIMARY KEY,
    momento         timestamp       NOT NULL DEFAULT now(),
    tabla           varchar         NOT NULL,
    filas           integer         NOT NULL
);