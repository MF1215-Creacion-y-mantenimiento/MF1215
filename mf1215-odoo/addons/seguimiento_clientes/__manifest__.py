{
    "name": "Seguimiento de clientes",
    "version": "19.0.1.0.0",
    "summary": "Registro de los seguimientos comerciales realizados a los clientes",
    "category": "Sales/CRM",
    "author": "MF1215_3 · 013_L1SFC2400073424",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/seguimiento_cliente_views.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "application": True,
    "installable": True,
}
