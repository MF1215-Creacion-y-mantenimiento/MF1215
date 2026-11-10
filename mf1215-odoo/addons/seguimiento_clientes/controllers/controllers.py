# from odoo import http


# class SeguimientoClientes(http.Controller):
#     @http.route('/seguimiento_clientes/seguimiento_clientes', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/seguimiento_clientes/seguimiento_clientes/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('seguimiento_clientes.listing', {
#             'root': '/seguimiento_clientes/seguimiento_clientes',
#             'objects': http.request.env['seguimiento_clientes.seguimiento_clientes'].search([]),
#         })

#     @http.route('/seguimiento_clientes/seguimiento_clientes/objects/<model("seguimiento_clientes.seguimiento_clientes"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('seguimiento_clientes.object', {
#             'object': obj
#         })

