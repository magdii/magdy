# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class VendorBill(models.Model):
    _inherit = 'account.invoice'
    transporter = fields.Boolean(string="transporter", )