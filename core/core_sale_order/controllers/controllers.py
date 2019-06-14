# -*- coding: utf-8 -*-
from odoo import http

# class CoreSaleOrder(http.Controller):
#     @http.route('/core_sale_order/core_sale_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/core_sale_order/core_sale_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('core_sale_order.listing', {
#             'root': '/core_sale_order/core_sale_order',
#             'objects': http.request.env['core_sale_order.core_sale_order'].search([]),
#         })

#     @http.route('/core_sale_order/core_sale_order/objects/<model("core_sale_order.core_sale_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('core_sale_order.object', {
#             'object': obj
#         })