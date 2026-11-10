{
    "name": "Seguimiento de clientes",
    "version": "19.0.1.0.0",
    "summary": "Registro de los seguimientos comerciales realizados a los clientes",
    "category": "Sales/CRM",
    "author": "Rafael Martín",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "application": True,
    "installable": True,
}
