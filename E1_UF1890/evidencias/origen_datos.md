#### Tabla resuelta

|Información|Modelo Odoo|Tabla PostgreSQL|Campos utilizados|
|---|---|---|---|
|Cliente|res.partner|res_partner|id,name,city,country_id|
|País del cliente|res.country|res_clountry|id,name(jsonb)|
|Prodcuto/servicio|product.product|product_product|id,product_tmpl_id|
|Plantilla producto|product.template|product_template|name(jsonb),categ_id|
|Categoría producto|prodcut.category|prodcut_category|id,name|
|Pedido de venta|sale.order|sale_order|id,name,partner_id,date_order,state|
|Línea de pedido|sale.order.line|sale_order_line|id,order_id,product_id,product_uom_qty,price_unit,discount,price_subtotal,display_type|

#### Regla de filtrado (lo que hay que deducir)

|Regla|Condición|Por qué|
|---|---|---|
|Solo ventas confirmadas|sale_order.sate = 'sale'|Los presupuestos(draft, sent) y los cancelados(cancel)no son ventas. En Odoo 19 el pedido bloqueado sigue en ```sale```|
|Solo líneas de producto|sale_order_line.display_type IS NULL|Las secciones(line_section)y las notas(line_note)son líneas de texto sin producto ni importe|


#### Estructura del almacén

|Concepto|En esta solución|
|---|---|
|Hecho|```lab.hechos_ventas```: una fila por línea de pedido|
|Medidas|```cantidad```,```precio_unitario```,```total```|
|Dimensiones|```lab.dim_cliente```(nombre, ciudad, país) y ```lab.dim_producto```(nombre, categoría)|
|Claves subrrogadas|cliente_key, producto_key, independientes de los id de Odoo|
|Trazabilidad|```cliente_id_origen```, ```producto_id_origen```, ```linea_id_origen```, ```pedido```|
|Cubo|Hechos de ventas + sus dimensiones: el importe se puede ver por cliente, por producto, por fecha o por cualquier combinación|
|Multicubo|El cubo de ventas de hoy y el embudo de ayer, unidos por las dimensiones que compartieran.|
|

#### Proceso ETL
|Fase|En esta solución|
|---|---|
|Extracción|sale_order_line,sale_order,res_partner,res_country,product_product,product_template,product_category|
|Transformación|TRIM de nombres;ciudad,país y categoría vacíos -> "sin ..."; texto de los jsonb;filtro de pedidos confirmados y líneas de producto;cálculo del total|
|Carga|INSERT...SELECT en orden dimensiones -> hechos, todo en una transacción|
|Registro|Una fila en lab.etl_log por tabla cargada|
|
