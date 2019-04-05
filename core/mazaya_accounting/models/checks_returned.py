# -*- coding: utf-8 -*-

from odoo import models, fields, api


class account_check_returned(models.Model):
    _name = 'check.returned'

    name = fields.Char('Check', index=True,default="New",readonly=True)
    partner_id = fields.Many2one("res.partner", "customer")
    financial_type = fields.Selection([('bank_check', 'Bank Check'),
                                       ('checks_written', 'Checks written'),
                                       ('banknotes', 'Banknotes'),
                                       ('insurance_paper', 'Insurrance Paper')],
                                      string='Financial Type', )
    sale_id = fields.Many2one("sale.order", string="Sale Ref")
    page_num=fields.Text("Page Num")
    bank=fields.Text("Bank")
    checks_line_ids = fields.One2many("check.returned.line", "checks_id", string="Checks")

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('returned_check') or '/'
        vals['name'] = seq
        return super(account_check_returned, self).create(vals)


class ChecksLine(models.Model):
    _name = 'check.returned.line'

    checks_id = fields.Many2one("check.returned", string="Checks")
    partner_id = fields.Many2one(related="checks_id.partner_id", string="customer")
    name = fields.Many2one("account.check.line", domain=[('state','=','returned')],string="Check Num")
    due_date = fields.Date('Due Date', )
    amount = fields.Float('Amount')
    status = fields.Selection(
        [('new', 'New'), ('paied', 'Paied'),('returned', 'Returned'), ],
        string=' Check Status', )

    @api.onchange('name')
    def _onchange_check_num(self):
        self.due_date = self.name.due_date
        self.amount = self.name.amount
        self.status = self.name.state
