# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    transpoter = fields.Boolean(string="Transporter", )