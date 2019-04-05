# -*- coding: utf-8 -*-
from openerp import http

# class Mothida(http.Controller):
#     @http.route('/mothida/mothida/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mothida/mothida/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mothida.listing', {
#             'root': '/mothida/mothida',
#             'objects': http.request.env['mothida.mothida'].search([]),
#         })

#     @http.route('/mothida/mothida/objects/<model("mothida.mothida"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mothida.object', {
#             'object': obj
#         })