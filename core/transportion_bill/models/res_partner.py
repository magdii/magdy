# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    transpoter = fields.Boolean()
    routes_ids = fields.One2many("routes.pricing", inverse_name="partner_id")

class RoutesPricing(models.Model):
    _name = 'routes.pricing'
    _description = 'New Description'

    delivery_id = fields.Many2one('delivery.carrier')
    partner_id = fields.Many2one('res.partner')
    from_city = fields.Many2one('res.partner')
    to_city = fields.Many2one('res.partner')
    unit = fields.Selection(string="unit", selection=[('whole', 'Whole'), ('Ton', 'Ton'), ],default='whole' )
    cost_price = fields.Float(string="Cost Price")
    sale_price = fields.Float(string="Sale Price")