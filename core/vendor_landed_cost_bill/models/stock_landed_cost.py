# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class VendorLandedCostBill(models.Model):
    _inherit = 'stock.landed.cost'

    is_landed_cost = fields.Boolean()

    @api.multi
    def create_landed_cost_bill(self):
        invoice_object = self.env['account.invoice']
        invoice_line = self.env['account.invoice.line']
        for record in self:
            for line in record.cost_lines:
                invoice_id = invoice_object.create({
                    'type':'in_invoice',
                    'partner_id':line.landed_cost_vendor_id.id,
                })
                invoice_line.create({
                    'invoice_id': invoice_id.id,
                    'product_id': line.product_id.id,
                    'name': line.product_id.name,
                    'quantity': 1,
                    'price_unit': line.price_unit,
                    'account_id': line.account_id.id,
                })
                line.bill_id = invoice_id.id
            record.is_landed_cost = True


class VendorLandedCostBill(models.Model):
    _inherit = 'stock.landed.cost.lines'

    landed_cost_vendor_id = fields.Many2one(comodel_name="res.partner", string="Vendor", )
    bill_id = fields.Many2one(comodel_name="account.invoice", string="Bill", readonly=True )
