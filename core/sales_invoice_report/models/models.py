# -*- coding: utf-8 -*-

from odoo import models, fields, api
class ResCompany(models.Model):
    _inherit = 'res.company'
    header = fields.Binary()
    footer = fields.Binary()