# -*- coding: utf-8 -*-
"""
MF1215_3 · UF1890 · E1 — Datos de control «Atlantic Web Consulting»

Se ejecuta con la shell de Odoo (usa el ORM, no SQL):
    docker compose cp cargar_datos_e1.py odoo:/tmp/cargar_datos_e1.py
    docker compose exec odoo sh -c "odoo shell -d mf1215 --no-http < /tmp/cargar_datos_e1.py"

Se puede ejecutar varias veces: si los datos ya existen, no hace nada.
"""

from datetime import datetime

env = env(context=dict(env.context, lang="es_ES", tracking_disable=True))  # noqa: F821

Partner = env["res.partner"]
Categ = env["product.category"]
Product = env["product.product"]
Order = env["sale.order"]

if Partner.search_count([("ref", "=", "E1-ALFA")]):
    print("\n[E1] Los datos de control ya estaban cargados. No se ha hecho nada.\n")
else:
    es = env.ref("base.es")

    # ---------- Clientes (Gamma lleva espacios y no tiene ciudad: casos de limpieza)
    alfa = Partner.create(
        {
            "name": "E1 Cliente Alfa",
            "ref": "E1-ALFA",
            "is_company": True,
            "city": "Santa Cruz de Tenerife",
            "country_id": es.id,
            "email": "alfa@e1.test",
        }
    )
    beta = Partner.create(
        {
            "name": "E1 Cliente Beta",
            "ref": "E1-BETA",
            "is_company": True,
            "city": "Las Palmas de Gran Canaria",
            "country_id": es.id,
            "email": "beta@e1.test",
        }
    )
    gamma = Partner.create(
        {
            "name": "  E1 Cliente Gamma  ",
            "ref": "E1-GAMMA",
            "is_company": True,
            "country_id": es.id,
            "email": "gamma@e1.test",
        }
    )
    delta = Partner.create(
        {
            "name": "E1 Cliente Delta",
            "ref": "E1-DELTA",
            "is_company": True,
            "city": "La Laguna",
            "country_id": es.id,
            "email": "delta@e1.test",
        }
    )

    # ---------- Categorías y servicios
    c_des = Categ.create({"name": "E1 Desarrollo web"})
    c_alo = Categ.create({"name": "E1 Alojamiento"})
    c_man = Categ.create({"name": "E1 Mantenimiento"})

    def servicio(code, name, price, categ):
        return Product.create(
            {
                "default_code": code,
                "name": name,
                "type": "service",
                "list_price": price,
                "sale_ok": True,
                "categ_id": categ.id,
            }
        )

    p_des = servicio("E1-DES", "E1 Desarrollo web a medida", 1500.0, c_des)
    p_tie = servicio("E1-TIE", "E1 Tienda online", 2400.0, c_des)
    p_alo = servicio("E1-ALO", "E1 Alojamiento web anual", 240.0, c_alo)
    p_man = servicio("E1-MAN", "E1 Mantenimiento mensual", 90.0, c_man)
    p_seo = servicio("E1-SEO", "E1 Consultoría SEO (hora)", 60.0, c_man)

    # Se intenta dejar SEO sin categoría (caso «Sin categoría»). Si Odoo no lo permite, se queda en Mantenimiento.
    seo_sin_categ = False
    try:
        with env.cr.savepoint():
            p_seo.product_tmpl_id.categ_id = False
            env.flush_all()
            seo_sin_categ = True
    except Exception:
        p_seo.invalidate_recordset()

    # ---------- Pedidos
    def linea(prod, qty):
        return (0, 0, {"product_id": prod.id, "product_uom_qty": qty})

    def seccion(texto):
        return (0, 0, {"display_type": "line_section", "name": texto})

    def nota(texto):
        return (0, 0, {"display_type": "line_note", "name": texto})

    def pedido(cliente, fecha, lineas, estado):
        o = Order.create(
            {"partner_id": cliente.id, "date_order": fecha, "order_line": lineas}
        )
        if estado == "sale":
            o.action_confirm()
        elif estado == "cancel":
            o.action_cancel()
        o.write({"date_order": fecha})  # action_confirm pone la fecha de hoy
        return o

    p1 = pedido(
        alfa,
        datetime(2026, 3, 10, 10, 0),
        [
            seccion("Fase 1"),
            linea(p_des, 1),
            linea(p_man, 12),
            nota("Incluye formación inicial"),
        ],
        "sale",
    )
    p2 = pedido(alfa, datetime(2026, 5, 4, 10, 0), [linea(p_alo, 1)], "sale")
    p3 = pedido(
        beta,
        datetime(2026, 6, 15, 10, 0),
        [linea(p_tie, 1), linea(p_alo, 1), linea(p_man, 6)],
        "sale",
    )
    p4 = pedido(
        gamma,
        datetime(2026, 9, 20, 10, 0),
        [seccion("Auditoría"), linea(p_seo, 10)],
        "sale",
    )
    p5 = pedido(
        delta, datetime(2026, 10, 5, 10, 0), [linea(p_des, 1)], "draft"
    )  # presupuesto
    p6 = pedido(
        beta, datetime(2026, 10, 12, 10, 0), [linea(p_tie, 2)], "cancel"
    )  # cancelado

    env.cr.commit()

    print("\n[E1] Datos de control cargados:")
    for o in (p1, p2, p3, p4, p5, p6):
        print(
            f"   {o.name:10} {o.partner_id.name.strip():18} estado={o.state:6} "
            f"base imponible={o.amount_untaxed:9.2f}"
        )
    print(
        f"   SEO sin categoría: {'sí' if seo_sin_categ else 'no (Odoo exige categoría)'}\n"
    )
