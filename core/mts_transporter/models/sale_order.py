# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    type = fields.Selection(string="Type",
                            selection=[('own_truck', 'Own Truck'),
                                       ('third_party_truck', 'Third Party Truck'),
                                       ('customer_truck', 'Customer Truck'), ],
                            required=False, )
    freight_type = fields.Selection(string="Freight Type",
                                    selection=[('per_trip', 'Per Trip'),
                                               ('per_ton', 'Per Ton'), ],
                                    default='per_trip',
                                    required=False, )
    Transporter_id = fields.Many2one(comodel_name="res.partner", string="Transporter",
                                     domain=[('transpoter', '=', True)])
    customer_freight = fields.Float(string="Customer Freight", )
    supplier_freight = fields.Float(string="Supplier Freight", )
    bill_reference = fields.Char(string="Bill Reference", )
    driver_name = fields.Char(string="Driver Name", )
    vehicle_no = fields.Char(string="Vehicle No", )
    is_third = fields.Boolean(compute="_compute_is_third")
    is_bill = fields.Boolean()
    transporter_account_id = fields.Many2one(comodel_name="account.invoice",
                                             string="Transporter Bill",
                                             readonly=True, )
    bill_state = fields.Selection(selection=[('draft','Draft'),
                                             ('proforma', 'Pro-forma'),
                                             ('proforma2', 'Pro-forma'),
                                             ('open', 'Open'),
                                             ('paid', 'Paid'),
                                             ('cancel', 'Cancelled'),
                                             ], related="transporter_account_id.state", )

    # @api.multi
    # def delivery_set(self):
    #     res = super(SaleOrder, self).delivery_set()
    #     self.customer_freight = self.delivery_price
    #     return res

    @api.multi
    @api.constrains('freight_type')
    def _check_freight_type(self):
        for record in self:
            quantity = 0.0
            lst = []
            if record.freight_type == 'per_ton':
                for line in record.order_line:
                    # quantity = line.product_uom_qty
                    lst.append(line.product_uom_qty)
                    # print ">>>>quantity111", quantity
                    if line.is_delivery:
                        print ">>>>quantity",lst[0]
                        line.price_unit = lst[0] * record.customer_freight

    @api.multi
    @api.constrains('customer_freight')
    def _check_customer_freight(self):
        for record in self:
            quantity = 0.0
            lst = []
            if record.freight_type == 'per_ton':
                for line in record.order_line:
                    # quantity = line.product_uom_qty
                    lst.append(line.product_uom_qty)
                    # print ">>>>quantity111", quantity
                    if line.is_delivery:
                        print ">>>>quantity",lst[0]
                        line.price_unit = lst[0] * record.customer_freight

    @api.multi
    @api.depends('carrier_id')
    def _compute_is_third(self):
        print ">>>>>>>>>>> ",self.carrier_id.name
        if self.carrier_id.name == 'Customer Truck':
           self.is_third=True

    @api.multi
    def delivery_set(self):

        # Remove delivery products from the sale order
        self._delivery_unset()

        for order in self:
            carrier = order.carrier_id
            if carrier:
                if order.state not in ('draft', 'sent'):
                    raise UserError(_('The order state have to be draft to add delivery lines.'))

                if carrier.delivery_type not in ['fixed', 'base_on_rule']:
                    # Shipping providers are used when delivery_type is other than 'fixed' or 'base_on_rule'
                    price_unit = order.carrier_id.get_shipping_price_from_so(order)[0]
                else:
                    # Classic grid-based carriers
                    carrier = order.carrier_id.verify_carrier(order.partner_shipping_id)
                    if not carrier:
                        raise UserError(_('No carrier matching.'))
                    price_unit = carrier.get_price_available(order)
                    if order.company_id.currency_id.id != order.pricelist_id.currency_id.id:
                        price_unit = order.company_id.currency_id.with_context(date=order.date_order).compute(price_unit, order.pricelist_id.currency_id)

                final_price = price_unit * (1.0 + (float(self.carrier_id.margin) / 100.0))
                if self.is_third == True:
                    final_price1 = final_price
                else:
                    final_price1 = self.customer_freight
                order._create_delivery_line(carrier, final_price1)

            else:
                raise UserError(_('No carrier set for this order.'))

        return True

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
            total = sum(line.product_uom_qty for line in rec.order_line if line.is_delivery == False)
        account_obj = account_invoice_id.create({
            'partner_id': self.Transporter_id.id,
            'journal_id': self.env['account.journal'].search([('type', '=', 'purchase')])[0].id,
            'type': 'in_invoice',
            'name': self.bill_reference,
            'transporter': True,
        })
        account_invoice_line_id.create({
            'invoice_id': account_obj.id,
            'product_id': product_id.id,
            'name': product_id.name,
            'quantity': 1,
            'price_unit': self.supplier_freight * total if self.freight_type == 'per_ton' else self.supplier_freight ,
            'account_id': product_id.property_account_expense_id.id if product_id.property_account_expense_id else product_id.categ_id.property_stock_account_input_categ_id.id,
            # 'account_id': self.Transporter_id.property_account_payable_id.id,
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

