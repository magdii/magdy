from __future__ import print_function

from openerp import models, fields, api, _
from datetime import datetime
from dateutil import relativedelta


class ReportWizard(models.TransientModel):
    """sale report wizard"""

    _name = "account.wizard"

    Transporter_id = fields.Many2one(comodel_name="res.partner", string="Transporter",
                                     domain=[('transpoter', '=', True)])
    # partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", )
    date_from = fields.Date(string='Date from ', )
    date_to = fields.Date(string='Date to ', )
    state = fields.Selection([
            ('draft','Draft'),
            ('proforma', 'Pro-forma'),
            ('proforma2', 'Pro-forma'),
            ('open', 'Open'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled'),
        ], string='Bill Status', )

    @api.multi
    def check_report(self):
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'date': self.date_from,
            'ids': active_ids,
            'model': 'sale.order',
            'form': self.read(['date_from', 'date_to', 'Transporter_id'])[0]
        }

        return self.env['report'].get_action(self, 'mts_transporter.sale_order_report')

    @api.multi
    def get_sale_orders_report(self, date_from, date_to, Transporter_id):
        """sale orders report"""
        vals = []
        partners = []
        # print (">>>>>>>>>>>>>>Transporter", Transporter_id)
        # print (">>>>>>>>>>>>>>Transporter_id", self.Transporter_id)
        # print (">>>>>>>>>>>>>>partner_id", self.partner_id)
        # print (">>>>>>>>>>>>>>date_from", date_from)
        # print (">>>>>>>>>>>>>>date_to", date_to)
        if self.Transporter_id:
            transporter_ids = self.Transporter_id
        else:
            transporter_ids2 = self.env['res.partner'].search([])
            for partner_obj in transporter_ids2:
                partners.append(partner_obj.id)

        if date_to:
            date_t = date_to
        else:
            date_t = fields.date.today()
        sale_ids = self.env['account.invoice'].search([('partner_id', '=', transporter_ids.id if self.Transporter_id else partners),
                                                       ('state', '=', self.state),
                                                       ('date_invoice', '>=', date_from),
                                                       ('date_invoice', '<=', date_t), ])
        for i in sale_ids:
            val = {
                    "name": i.number,
                    "total_amount": i.amount_untaxed,
                    "tax_amount": i.amount_tax,
                    "total_amount_taxes": i.amount_total,
                    # "paid_amount": i.amount_untaxed,
                }
            vals.append(val)
        return vals