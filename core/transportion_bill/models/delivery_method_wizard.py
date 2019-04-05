# -*- coding: utf-8 -*-

from odoo import api, fields, models,_


class DeliveryMethodWizard(models.TransientModel):
    _name = "delivery.method.wizard"

    from_city = fields.Many2one('res.partner')
    to_city = fields.Many2one('res.partner')
    unit = fields.Selection(string="unit", selection=[('whole', 'Whole'), ('Ton', 'Ton'), ],default='whole', )
    price = fields.Float(string="Price")
    partner_transporter_id = fields.Many2one('res.partner',string='Vendor', domain="[('transpoter', '=', True)]", )
    product_id = fields.Many2one('product.product', string='Product', )

    def create_delivery_method_invoice(self):
        account_invoice_id = self.env['account.invoice']
        account_invoice_line_id = self.env['account.invoice.line']
        account_obj = account_invoice_id.create({
            'partner_id': self.partner_transporter_id.id,
        })
        account_invoice_line_id.create({
            'invoice_id': account_obj.id,
            'product_id': self.product_id.id,
            'name': self.product_id.name,
            'quantity': 1,
            'price_unit': self.price,
            'account_id': self.partner_transporter_id.property_account_receivable_id.id,
        })
        context = self.env.context
        active_ids = context.get('active_ids', [])
        sale_obj = self.env['sale.order'].browse(active_ids[0])
        sale_obj.transportation_fees_bill = account_obj.id
        return {
                'type': 'ir.actions.act_window',
                'name': _('customer invoice'),
                'res_model': 'account.invoice',
                'res_id': account_obj.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
              }

