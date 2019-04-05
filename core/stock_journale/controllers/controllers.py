# -*- coding: utf-8 -*-
from odoo import http

# class StockJournale(http.Controller):
#     @http.route('/stock_journale/stock_journale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_journale/stock_journale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_journale.listing', {
#             'root': '/stock_journale/stock_journale',
#             'objects': http.request.env['stock_journale.stock_journale'].search([]),
#         })

#     @http.route('/stock_journale/stock_journale/objects/<model("stock_journale.stock_journale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_journale.object', {
#             'object': obj
#         })