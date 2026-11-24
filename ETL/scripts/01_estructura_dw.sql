-- 01_estructura_dw.sql · Almacen de Datos del embudo comercial (esquema lab)
-- Se puede ejecutar varias veces: IF NOT EXIST no falla si la tabla ya existe

-- Dimensión etapa: una fila por etapa del embudo comercial
CREATE TABLE IF NOT EXISTS lab.dim_etapa (
    etapa_key       serial          PRIMARY KEY,
    etapa_id_origen integer         NOT NULL UNIQUE,
    nombre          varchar(100)    NOT NULL,
    orden           integer,
    es_ganada       boolean          NOT NULL DEFAULT false
);

-- Dimensión comercial: una fila por usuario comercial (+ "sin comercial")
CREATE TABLE IF NOT EXISTS lab.dim_comercial (
    comercial_key       serial          PRIMARY KEY,
    comercial_id_origen integer         NOT NULL UNIQUE,
    nombre              varchar(150)    NOT NULL
);

-- Tabla de hechos: una fila por oportunidad (grano)
CREATE TABLE IF NOT EXISTS lab.hechos_oportunidades (
    oportunidad_key         serial          PRIMARY KEY,
    oportunidad_id_origen   integer         NOT NULL UNIQUE, 
    fecha_creacion          date            NOT NULL,
    etapa_key               integer         NOT NULL REFERENCES lab.dim_etapa (etapa_key),
    comercial_key           integer         NOT NULL REFERENCES lab.dim_comercial (comercial_key),
    ingreso_esperado        numeric(14,2)   NOT NULL,
    probabilidad            numeric(5,2)    NOT NULL,
    ingreso_ponderado       numeric(14,2)   NOT NULL
);

-- Registro de cargos (logs del proceso ETL)
CREATE TABLE IF NOT EXISTS lab.etl_log (
    log_id              serial          PRIMARY KEY,
    fecha_carga         timestamp       NOT NULL DEFAULT now(),
    proceso             varchar(60)     NOT NULL,
    tabla               varchar(60)     NOT NULL,
    filas               integer         NOT NULL,
    observaciones       text             
);