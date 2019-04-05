# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class LandedCostLine(models.Model):
    _inherit = 'stock.landed.cost.lines'

    @api.model
    def _get_landed_cost_product(self):
        return self.env['product.product'].search([('name', 'ilike', 'Freight')], limit=1)
        # product_id = self.env['product.product']
        # product_obj = product_id.search([('name', 'ilike', 'Freight')], limit=1)
        # print "<<<<<<<<<<<<<"
        # if product_obj:
        #     print "11111111111111"
        #     self.product_id = product_obj.id
        #     return self.product_id
        # else:
        #     print "555555555555"
        #     product = product_id.create({
        #         'name': 'Freight',
        #         'type': 'product',
        #         'categ_id': 1,
        #     })
        #     self.product_id = product.id
        #     return self.product_id




    product_id = fields.Many2one('product.product', 'Product', reuired=False, default=_get_landed_cost_product)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    type = fields.Selection(string="Type",
                            selection=[('own_truck', 'Own Truck'),
                                       ('third_party_truck', 'Third Party Truck'),
                                       ('customer_truck', 'Customer Truck'), ],
                            required=False,
                            default='customer_truck', )
    freight_type = fields.Selection(string="Freight Type",
                                    selection=[('per_trip', 'Per Trip'),
                                               ('per_ton', 'Per Ton'), ],
                                    required=False, )
    Transporter_id = fields.Many2one(comodel_name="res.partner",
                                     string="Transporter",
                                     required=True,
                                     domain=[('transpoter', '=', True)])
    supplier_freight = fields.Float(string="Supplier Freight", )
    bill_reference = fields.Char(string="Bill Reference", )
    driver_name = fields.Char(string="Driver Name", )
    driver_mobile_no = fields.Char(string="Driver Mobile No", )
    vehicle_no = fields.Char(string="Vehicle No", )
    transporter_account_id = fields.Many2one(comodel_name="account.invoice",
                                             string="Transporter Bill",
                                             readonly=True, )
    is_third = fields.Boolean(compute="_compute_is_third")
    bill_state = fields.Selection(selection=[('draft','Draft'),
                                             ('proforma', 'Pro-forma'),
                                             ('proforma2', 'Pro-forma'),
                                             ('open', 'Open'),
                                             ('paid', 'Paid'),
                                             ('cancel', 'Cancelled'),
                                             ], related="transporter_account_id.state", )
    is_bill = fields.Boolean()
    is_landed = fields.Boolean()
    landed_cost_id = fields.Many2one('stock.landed.cost', string="Landed Cost", )


    @api.multi
    @api.depends('type')
    def _compute_is_third(self):
        if self.type == 'customer_truck':
           self.is_third=True

    @api.multi
    def Create_landed_cost(self):
        landed_cost = self.env['stock.landed.cost']
        landed_cost_line = self.env['stock.landed.cost.lines']
        account_journal = self.env['account.journal'].search([('type', '=', 'general')], limit=1)
        product_ids = self.env['product.product']
        product_obj=product_ids.search([('name', 'like', 'Freight')])
        landed_id = landed_cost.create({
            'date': fields.date.today(),
            'account_journal_id': account_journal.id,
            'picking_ids': [(6, 0, [self.id])],
        })
        landed_cost_line.create({
            'cost_id': landed_id.id,
            'product_id': product_obj.id,
            'split_method': 'by_current_cost_price',
            'price_unit': self.supplier_freight,
        })
        self.landed_cost_id = landed_id.id
        self.is_landed = True
        return {
                'type': 'ir.actions.act_window',
                'name': _('Landed Cost'),
                'res_model': 'stock.landed.cost',
                'res_id': landed_id.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
              }

    @api.multi
    def Create_Transporter_Bill(self):
        product_ids = self.env['product.product']
        product_obj=product_ids.search([('name', 'like', 'Freight')])
        account_invoice_id = self.env['account.invoice']
        account_invoice_line_id = self.env['account.invoice.line']
        total = 0.0
        if product_obj:
            product_id = product_obj
        else:
            product_id = product_ids.create({
                'name': 'Freight',
                'type': 'product',
                'categ_id': 1,
            })
        for rec in self:
            total = sum(line.product_uom_qty for line in rec.move_lines)
        account_obj = account_invoice_id.create({
            'partner_id': self.Transporter_id.id,
            'journal_id': self.env['account.journal'].search([('type', '=', 'purchase')])[0].id,
            'name': self.bill_reference,
            'type': 'in_invoice',
            'transporter': True,
        })
        account_invoice_line_id.create({
            'invoice_id': account_obj.id,
            'product_id': product_id.id,
            'name': product_id.name,
            'quantity': 1,
            'price_unit': self.supplier_freight * total if self.freight_type == 'per_ton' else self.supplier_freight,
            'account_id': product_id.property_account_expense_id.id if product_id.property_account_expense_id else product_id.categ_id.property_stock_account_input_categ_id.id,
        })
        self.transporter_account_id = account_obj.id
        self.is_bill = True
        return {
                'type': 'ir.actions.act_window',
                'name': _('vendor bill'),
                'res_model': 'account.invoice',
                'res_id': account_obj.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
              }

