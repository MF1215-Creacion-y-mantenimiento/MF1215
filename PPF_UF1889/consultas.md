# Consulta ORM: tareas pendientes por cliente

## Código (odoo shell -d mf1215)

    grupos = env['gestion_tareas.tarea']._read_group(
        domain=[('state', '=', 'pendiente')],
        groupby=['partner_id'],
        aggregates=['__count'],
    )
    for partner, total in grupos:
        print(f'{partner.display_name or "Sin cliente"}: {total}')

## Resultado obtenido

    Cliente Alfa: 2
    Cliente Beta: 1

## Justificación de eficiencia

_read_group delega el filtrado y el recuento en PostgreSQL con una única
consulta WHERE + GROUP BY + COUNT, de modo que solo viaja a Python un total
por cliente, en lugar de cargar todas las tareas y contarlas una a una.