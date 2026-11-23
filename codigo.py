Tarea = env["gestion_tareas.tarea"]

grupos = Tarea._read_group(
    domain=[("state", "=", "pendiente")],
    groupby=["partner_id"],
    aggregates=["__count"],
)
for partner, total in grupos:
    print(f'{partner.display_name or "Sin cliente"}: {total}')
