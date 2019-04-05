# -*- coding: utf-8 -*-
from odoo import http

# class CoreLastTest(http.Controller):
#     @http.route('/core_last_test/core_last_test/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/core_last_test/core_last_test/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('core_last_test.listing', {
#             'root': '/core_last_test/core_last_test',
#             'objects': http.request.env['core_last_test.core_last_test'].search([]),
#         })

#     @http.route('/core_last_test/core_last_test/objects/<model("core_last_test.core_last_test"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('core_last_test.object', {
#             'object': obj
#         })