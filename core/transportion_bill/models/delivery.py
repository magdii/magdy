# -*- coding: utf-8 -*-

from odoo import api, fields, models

class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    partner_id = fields.Many2one('res.partner',string='Vendor', domain="[('transpoter', '=', True)]", )
    routes_ids = fields.One2many("routes.pricing",inverse_name="delivery_id")


    @api.constrains('partner_id')
    def _compute_routes(self):
        for record in self:
            if record.partner_id:
                for line in record.partner_id.routes_ids:
                    routes_id = self.env['routes.pricing'].create({
                        'delivery_id':record.id,
                        'from_city':line.from_city.id,
                        'to_city':line.to_city.id,
                        'unit':line.unit,
                        'cost_price':line.cost_price,
                        'sale_price':line.sale_price,
                    })
                    record.routes_ids |= routes_id