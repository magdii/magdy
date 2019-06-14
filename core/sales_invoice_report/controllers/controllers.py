# -*- coding: utf-8 -*-
from odoo import http

# class SalesInvoiceReport(http.Controller):
#     @http.route('/sales_invoice_report/sales_invoice_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_invoice_report/sales_invoice_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_invoice_report.listing', {
#             'root': '/sales_invoice_report/sales_invoice_report',
#             'objects': http.request.env['sales_invoice_report.sales_invoice_report'].search([]),
#         })

#     @http.route('/sales_invoice_report/sales_invoice_report/objects/<model("sales_invoice_report.sales_invoice_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_invoice_report.object', {
#             'object': obj
#         })