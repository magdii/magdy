# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def post(self):
        res = super(AccountMove, self).post()
        asset_id = self.env['account.asset.asset']
        for rec in self:
            for line in rec.line_ids:
                if line.asset_category_id:
                    asset_id.create({
                        'name': line.name,
                        'category_id': line.asset_category_id.id,
                        'value': line.debit if line.debit > line.credit else line.credit,
                    })
        return res



class LandedCostLine(models.Model):
    _inherit = 'account.move.line'

    asset_category_id = fields.Many2one('account.asset.category', string='Asset Category')

    @api.onchange('asset_category_id')
    def onchange_asset_category_id(self):
        for rec in self:
            rec.account_id = rec.asset_category_id.account_asset_id.id
