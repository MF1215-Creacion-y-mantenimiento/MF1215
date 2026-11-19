# from odoo import http


# class GestionEntregas(http.Controller):
#     @http.route('/gestion_entregas/gestion_entregas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_entregas/gestion_entregas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_entregas.listing', {
#             'root': '/gestion_entregas/gestion_entregas',
#             'objects': http.request.env['gestion_entregas.gestion_entregas'].search([]),
#         })

#     @http.route('/gestion_entregas/gestion_entregas/objects/<model("gestion_entregas.gestion_entregas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_entregas.object', {
#             'object': obj
#         })

