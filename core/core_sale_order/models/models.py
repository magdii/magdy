# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True,
                                     groups='core_sale_order.sale_order_security_group',
                                     readonly=True, compute='_amount_all', track_visibility='always')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True,
                                 groups='core_sale_order.sale_order_security_group',
                                 compute='_amount_all', track_visibility='always')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True,
                                   groups='core_sale_order.sale_order_security_group',
                                   compute='_amount_all', track_visibility='always')
