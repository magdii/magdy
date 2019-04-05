from __future__ import print_function

from openerp import models, fields, api, _
from datetime import datetime
from dateutil import relativedelta


class ReportWizard(models.TransientModel):
    """sale report wizard"""

    _name = "sale.wizard"

    date_from = fields.Date(string='Date from ', required=True,)
    date_to = fields.Date(string='Date to ', required=True,)

    @api.multi
    def check_report(self):
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'date': self.date_from,
            'ids': active_ids,
            'model': 'sale.order',
            'form': self.read(['date_from','date_to'])[0]
        }

        return self.env['report'].get_action(self, 'core_last_test.sale_order_report')

    @api.multi
    def get_sale_orders_report(self):
        """sale orders report"""
        vals = []
        sale_ids = self.env['sale.order'].search([])
        # ('date_from', '>=', date_from),
        # ('date_to', '<=', date_to)
        for i in sale_ids:
            val = {
                    "name": i.name,
                    "total_amount": i.amount_untaxed,
                    "tax_amount": i.amount_tax,
                    "total_amount_taxes": i.amount_total,
                    "paid_amount": i.amount_untaxed,
                }
            vals.append(val)
        return vals