# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import re
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo.exceptions import ValidationError


class account_check(models.Model):
    _name = 'account.check'
    _inherit = ['mail.thread']

    name = fields.Char('Check', index=True, default="New", readonly=True)
    partner_id = fields.Many2one("res.partner", "customer", required=True)
    financial_type = fields.Selection([('bank_check', 'Bank Check'), ('r_bank_check', 'Regular Bank Check'),
                                       ('g_bank_check', 'Guaranteed Bank Check'),
                                       ('checks_written', 'Checks written'),
                                       ('banknotes', 'Banknotes'),
                                       ('insurance_paper', 'Insurrance Paper')],
                                      string='Financial Type', default='bank_check')
    sale_id = fields.Many2one("sale.order", string="Sale Ref")
    sale_order_amount = fields.Monetary(related='sale_id.amount_total', string="Order Amount",
                                        currency_field='company_currency_id')
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True,
                                          help='Utility field to express amount currency')
    bank_id = fields.Many2one("res.bank", string="Customer Check Bank")
    checks_line_ids = fields.One2many("account.check.line", "checks_id", string="Checks")
    start_serial = fields.Char(string="Start Serial")
    strat_date = fields.Date(string="Start Date")
    journal_id = fields.Many2one(comodel_name="account.journal", string="Note Receivable Journal")

    # m.baset start
    check_state = fields.Selection(
        [('new', 'Draft'), ('revision_done', 'Revision Done')], string="Check Document", readonly=True,
        index=True, copy=False, default='new', track_visibility='onchange')

    @api.multi
    def action_new(self):
        self.check_state = 'new'

    @api.multi
    def action_done(self):
        sumAmount = sum(line.amount for line in self.checks_line_ids)
        if self.sale_order_amount != int(round(sumAmount)):
            print int(round(sumAmount))
            raise ValidationError(_("The Amount has been changed"))
        else:
            acc_line = 0
            if self.financial_type == 'bank_check':
                seq = self.env['ir.sequence'].next_by_code('account_check') or '/'
                self.name = seq
            elif self.financial_type == 'r_bank_check':
                seq = self.env['ir.sequence'].next_by_code('r_account_check') or '/'
                self.name = seq
            elif self.financial_type == 'g_bank_check':
                seq = self.env['ir.sequence'].next_by_code('g_account_check') or '/'
                self.name = seq
            self.check_state = 'revision_done'
            for i in self:
                acc_check_line = self.env['account.check.line'].search([('checks_id', '=', i.id)])
                for j in acc_check_line:
                    acc_journal = self.env['account.move'].create({
                        'journal_id': self.journal_id.id,
                        'ref': self.name
                    })
                    acc_line = acc_line + 1
                    if acc_line:
                        self.env['account.move.line'].with_context(check_move_validity=False).create(
                            {
                                'move_id': acc_journal.id,
                                'debit': j.amount,
                                'account_id': i.partner_id.property_account_receivable_id.id,
                                'partner_id': i.partner_id.id,
                                'name': j.name,
                                'date_maturity': j.due_date,
                            })
                        j.state = 'in_safe'

    @api.multi
    def update_check_serial_date(self):
        if self.start_serial and self.strat_date:
            serial = re.split('(\d+)', self.start_serial)
            count = 0
            for line in self.checks_line_ids:
                line.write({'name': serial[0] + str(int(serial[1]) + count).zfill(len(serial[1])),
                            'bank_id': self.bank_id.id,
                            'due_date': str(
                                datetime.strptime(self.strat_date, '%Y-%m-%d') + relativedelta.relativedelta(
                                    months=+count))})
                count += 1
        else:
            raise ValidationError(_("Plz enter start seq  and start date"))


class ChecksLine(models.Model):
    _name = 'account.check.line'
    _inherit = ['mail.thread']

    @api.multi
    @api.onchange('checks_id.partner_id')
    def get_partner(self):
        for i in self:
            i.partner_id = i.checks_id.partner_id.id

    checks_id = fields.Many2one("account.check", string="Document #", readonly=True)
    partner_id = fields.Many2one("res.partner", string="customer", compute='get_partner')
    sale_id = fields.Many2one("sale.order", related="checks_id.sale_id", string="Sale Ref")
    name = fields.Char('Check Num')
    bank_id = fields.Many2one("res.bank", string="Bank")
    amount = fields.Float('Amount')
    due_date = fields.Date('Due Date')
    invoice_id = fields.Many2one('account.invoice', string="Invoice Ref", readonly=True)
    check_dep_journal_id = fields.Many2one(comodel_name="account.journal", string="Check Deposit Journal")
    note_recev_account_id = fields.Many2one(comodel_name="account.account", string="Note Receivable Account")

    check_paid_journal_id = fields.Many2one(comodel_name="account.journal", string="Check Paid Journal")
    paid_account_id = fields.Many2one(comodel_name="account.account", string="Paid Account")

    check_returned_journal_id = fields.Many2one(comodel_name="account.journal", string="Check Returned Journal")
    returned_account_id = fields.Many2one(comodel_name="account.account", string="Returned Account")
    state = fields.Selection(
        [('new', 'New'), ('in_safe', 'In safe'), ('check_deposit', 'Check Deposit'), ('paid', 'Paid'),
         ('returned', 'Returned')], string='Check Status', default="new", track_visibility='onchange', readonly=True)
    check_state = fields.Selection(
        [('new', 'New'), ('revision_done', 'Revision Done')], related="checks_id.check_state")

    _sql_constraints = [
        ('name_bank_uniq', 'unique (name,bank_id)', "This check number with this bank already exists !"),
    ]

    @api.multi
    def action_check_deposit(self):
        for i in self:
            acc_journal = self.env['account.move'].create({
                'journal_id': i.check_dep_journal_id.id,
                'ref': i.name
            })
            if acc_journal:
                self.env['account.move.line'].with_context(check_move_validity=False).create({
                    'move_id': acc_journal.id,
                    'debit': i.amount,
                    'account_id': i.note_recev_account_id.id,
                    'partner_id': i.partner_id.id,
                    'name': i.name,
                    'date_maturity': i.due_date,
                })
                self.state = 'check_deposit'

    @api.multi
    def action_check_paid(self):
        for i in self:
            acc_journal = self.env['account.move'].create({
                'journal_id': i.check_paid_journal_id.id,
                'ref': i.name
            })
            if acc_journal:
                self.env['account.move.line'].with_context(check_move_validity=False).create({
                    'move_id': acc_journal.id,
                    'debit': i.amount,
                    'account_id': i.paid_account_id.id,
                    'partner_id': i.partner_id.id,
                    'name': i.name,
                    'date_maturity': i.due_date,
                })
                self.state = 'paid'

    @api.multi
    def action_check_returned(self):
        for i in self:
            acc_journal = self.env['account.move'].create({
                'journal_id': i.check_returned_journal_id.id,
                'ref': i.name
            })
            if acc_journal:
                self.env['account.move.line'].with_context(check_move_validity=False).create({
                    'move_id': acc_journal.id,
                    'debit': i.amount,
                    'account_id': i.returned_account_id.id,
                    'partner_id': i.partner_id.id,
                    'name': i.name,
                    'date_maturity': i.due_date,
                })
                self.state = 'returned'

    # @api.multi
    # def create_invoice(self):
    #     invoice_obj = self.env['account.invoice']
    #     line_obj = self.env['account.invoice.line']
    #     sale_journal = self.env['account.journal'].search([('type', '=', 'sale')])[0]
    #     sale_journal_id = sale_journal.id
    #
    #     invoice_id = invoice_obj.create({
    #         'partner_id': self.partner_id.id,
    #         'date_invoice': self.due_date,
    #         'type': 'out_invoice',
    #         'journal_id': sale_journal_id,
    #         'account_id': self.partner_id.property_account_receivable_id.id,
    #         'origin': self.sale_id.name,
    #     })
    #     sale_account_id = sale_journal.default_debit_account_id.id if sale_journal.default_debit_account_id \
    #         else sale_journal.default_credit_account_id.id
    #     for i in self.sale_id.order_line:
    #         line_id = line_obj.create({
    #             'invoice_id': invoice_id.id,
    #             'product_id': i.product_id.id,
    #             'price_unit': self.amount,
    #             'name': i.name,
    #             'account_id': sale_account_id,
    #             'quantity': 1,
    #
    #         })
    #         break
    #
    #     self.invoice_id = invoice_id.id
    #     self.state = 'paied'

    @api.multi
    def action_returned(self):
        self.state = 'returned'
