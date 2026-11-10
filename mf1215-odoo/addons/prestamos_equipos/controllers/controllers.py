# from odoo import http


# class PrestamosEquipos(http.Controller):
#     @http.route('/prestamos_equipos/prestamos_equipos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/prestamos_equipos/prestamos_equipos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('prestamos_equipos.listing', {
#             'root': '/prestamos_equipos/prestamos_equipos',
#             'objects': http.request.env['prestamos_equipos.prestamos_equipos'].search([]),
#         })

#     @http.route('/prestamos_equipos/prestamos_equipos/objects/<model("prestamos_equipos.prestamos_equipos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('prestamos_equipos.object', {
#             'object': obj
#         })

