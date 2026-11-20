# from odoo import http


# class GestionTareas(http.Controller):
#     @http.route('/gestion_tareas/gestion_tareas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_tareas/gestion_tareas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_tareas.listing', {
#             'root': '/gestion_tareas/gestion_tareas',
#             'objects': http.request.env['gestion_tareas.gestion_tareas'].search([]),
#         })

#     @http.route('/gestion_tareas/gestion_tareas/objects/<model("gestion_tareas.gestion_tareas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_tareas.object', {
#             'object': obj
#         })

