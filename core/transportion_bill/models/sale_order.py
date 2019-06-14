# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from openerp.exceptions import UserError


class RoutesPricing(models.Model):
    _inherit = 'sale.order'

    from_city = fields.Many2one('res.partner')
    to_city = fields.Many2one('res.partner')
    unit = fields.Selection(string="unit", selection=[('whole', 'Whole'), ('Ton', 'Ton'), ],default='whole', )
    cost_price = fields.Float(string="Cost Price")
    sale_price = fields.Float(string="Sale Price")
    price = fields.Float(string="Price")
    partner_transporter_id = fields.Many2one('res.partner',string='Vendor', domain="[('transpoter', '=', True)]", )
    include_transportation_fees = fields.Boolean()
    transportation_fees_bill = fields.Many2one('account.invoice', readonly=True, )

    @api.multi
    def action_get_transportation_bill_line(self):
        for record in self:
            for line in record.order_line:
                if line.is_delivery == True:
                    return {
                            'type': 'ir.actions.act_window',
                            'name': _('delivery method'),
                            'res_model': 'delivery.method.wizard',
                            'view_type': 'form',
                            'view_mode': 'form',
                            'context': {'default_from_city': self.from_city.id,
                                        'default_to_city': self.to_city.id,
                                        'default_unit': self.unit,
                                        'default_price': self.price,
                                        'default_partner_transporter_id': self.partner_transporter_id.id,
                                        'default_product_id': line.product_id.id,
                                        },
                            'target': 'new',
                          }

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

                # final_price = price_unit * (1.0 + (float(self.carrier_id.margin) / 100.0))
                final_price = 0.0
                quantity = 0.0
                for line in carrier.routes_ids:
                    if line.to_city == self.to_city and line.from_city == self.from_city :
                        if line.unit == 'whole':
                            final_price = line.sale_price
                        else:
                            for qty in self.order_line:
                                quantity += qty.product_uom_qty
                            final_price = line.sale_price * quantity
                order.price = final_price
                order._create_delivery_line(carrier, final_price)
            else:
                raise UserError(_('No carrier set for this order.'))

        return True

    @api.onchange('from_city', 'to_city', 'carrier_id')
    def _onchange_to_city(self):
        if self.to_city and self.from_city:
            to_city = []
            from_city = []
            delivery_method_id = self.env['delivery.carrier'].search([('id','=',self.carrier_id.id)])
            if delivery_method_id:
                for record in delivery_method_id:
                    for line in record.routes_ids:
                        to_city.append(line.to_city)
                        from_city.append(line.from_city)
                        if self.to_city in to_city and self.from_city in from_city :
                            if line.to_city == self.to_city and line.from_city == self.from_city :
                                self.cost_price = line.cost_price
                                self.sale_price = line.sale_price
                                self.unit = line.unit
                                self.partner_transporter_id = record.partner_id.id
                        elif self.to_city not in to_city and self.from_city in from_city:
                            raise UserError(_('Please check Your City To It is not found in the delivery method.'))
                        elif self.to_city in to_city and self.from_city not in from_city:
                            raise UserError(_('Please check Your City From It is not found in the delivery method.'))
