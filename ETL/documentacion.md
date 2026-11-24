# Almacén del embudo comercial · Documentación
1. Orígenes de datos
   Tabla del paso 1 (modelo, tabla, campos, por qué) y reglas de filtrado
2. Estructura creada
   Esquema en estrella: tabla de hechos, dimensiones, medidas y claves.
   Qué es un cubo y cómo sería un multicubo con este almacén.
3. Proceso ETL
   Orden de ejecución de los scripts.
   Extracción, transformación(reglas de limpeza y cálculos) y carga.
   Registro de cargas: qué guarda lab.etl_log y una captura de su contenido.
4. Pruebas y resultados
   Resultado de cada prueba (P1-P6) y de cada extractor.
5. Incidencias
   Preoblema encontrado · causa · solución
6. Documentación consultada
   Fuente · apartado · para qué se usó.
   |Fuente|Apartado|para qué| 
   |---|---|---|
   |PostgreSQL 16 · JSON Functions and Operators| Operador ->>|Sacar el texto de los campos traducibles|
   |PostgreSQL 16 · INSERT|INSERT....SELECT|Cargar una tabla a partir de una consulta|
   |PostgreSQL 16 · TRUNCATE|RESTART IDENTITY|Vaciar el almacén y reiniciar las claves subrogadas|


   ```
    ETL/
    |-- scripts/
        |-- 01_estructura_dw.sql
        |-- 02_etl.sql
        |-- 03_extractores.sql
        |-- 04_pruebas.sql
    |-- documentacion.md
    |-- capturas/


   ```

