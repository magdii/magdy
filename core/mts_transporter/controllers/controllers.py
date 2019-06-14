# -*- coding: utf-8 -*-
from odoo import http

# class MtsTransporter(http.Controller):
#     @http.route('/mts_transporter/mts_transporter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mts_transporter/mts_transporter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mts_transporter.listing', {
#             'root': '/mts_transporter/mts_transporter',
#             'objects': http.request.env['mts_transporter.mts_transporter'].search([]),
#         })

#     @http.route('/mts_transporter/mts_transporter/objects/<model("mts_transporter.mts_transporter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mts_transporter.object', {
#             'object': obj
#         })