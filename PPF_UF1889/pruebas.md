# Pruebas del módulo gestion_tareas

| Nº | Caso | Pasos | Resultado esperado | Resultado obtenido | Estado |
|----|------|-------|--------------------|--------------------|--------|
| 1 | Crear tarea | Tareas › Nuevo, nombre "Llamada inicial", cliente Alfa, guardar | Se guarda con estado Pendiente y fecha de hoy | Guardada, estado Pendiente, fecha 20/11/2026 | OK |
| 2 | Finalizar tarea | Abrir la tarea 1 y pulsar Finalizar | Estado pasa a Finalizada | Barra de estado en Finalizada | OK |
| 3 | Finalizar de nuevo | Pulsar Finalizar en la misma tarea | UserError con mensaje claro, sin cambios | Aparece "No se puede finalizar: la tarea «Llamada inicial» ya está finalizada." | OK |
| 4 | Filtrar pendientes | Lista › Filtros › Pendientes | Solo tareas en estado Pendiente | 3 de 5 registros, todos Pendiente | OK |
| 5 | Agrupar por cliente | Lista › Pendientes + Agrupar por Cliente | Un grupo por cliente con su recuento | Alfa (2), Beta (1); coincide con consultas.md | OK |
| 6 | Importar CSV | Importar importacion.csv | 5 tareas nuevas | 5 registros creados | OK |
| 7 | Reimportar CSV modificado | Cambiar gt_imp_004 a finalizada e importar de nuevo | 0 nuevas, gt_imp_004 actualizada | Total sin cambios (10), gt_imp_004 Finalizada | OK |
| 8 | Nombre obligatorio | Crear tarea sin nombre | Odoo no permite guardar | Campo marcado en rojo, no guarda | OK |