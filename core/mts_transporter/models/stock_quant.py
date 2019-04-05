# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class StockPicking(models.Model):

    _inherit = 'stock.quant'

    stock_unit_price = fields.Float(string="Unit Price",compute="_compute_stock_unit_price", )

    @api.multi
    def _compute_stock_unit_price(self):
        for record in self:
            record.stock_unit_price = record.inventory_value / record.qty