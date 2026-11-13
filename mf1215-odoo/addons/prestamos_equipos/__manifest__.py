{
    "name": "Préstamos de equipos",
    "summary": "Registro de equipos prestados a clientes",
    "description": """
Registro de los equipos prestados a clientes: equipo, cliente, fecha y estado.
    """,
    "author": "MF1215",
    "category": "Tools",
    "version": "19.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "application": True,
    "installable": True,
}
