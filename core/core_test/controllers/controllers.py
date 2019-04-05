# -*- coding: utf-8 -*-
from odoo import http

# class CoreTest(http.Controller):
#     @http.route('/core_test/core_test/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/core_test/core_test/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('core_test.listing', {
#             'root': '/core_test/core_test',
#             'objects': http.request.env['core_test.core_test'].search([]),
#         })

#     @http.route('/core_test/core_test/objects/<model("core_test.core_test"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('core_test.object', {
#             'object': obj
#         })