from odoo import _, api, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.multi
    @api.onchange('sale_order_id')
    def get_remaining_payments(self):
        for rec in self:
            rec.remaining = rec.sale_order_amount - rec.sale_order_id.total_payments

    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    sale_order_amount = fields.Monetary(related='sale_order_id.amount_total', string="Order Amount",
                                        currency_field='company_currency_id')
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True,
                                          help='Utility field to express amount currency')
    remaining = fields.Monetary(string='Remaining Payment', compute='get_remaining_payments')

    @api.onchange('sale_order_id')
    def onchange_sale_order(self):
        self.partner_id = self.sale_order_id.partner_id.id
