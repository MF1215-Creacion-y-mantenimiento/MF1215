# from odoo import http


# class GestionEventosEmpresa(http.Controller):
#     @http.route('/gestion_eventos_empresa/gestion_eventos_empresa', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_eventos_empresa/gestion_eventos_empresa/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_eventos_empresa.listing', {
#             'root': '/gestion_eventos_empresa/gestion_eventos_empresa',
#             'objects': http.request.env['gestion_eventos_empresa.gestion_eventos_empresa'].search([]),
#         })

#     @http.route('/gestion_eventos_empresa/gestion_eventos_empresa/objects/<model("gestion_eventos_empresa.gestion_eventos_empresa"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_eventos_empresa.object', {
#             'object': obj
#         })

