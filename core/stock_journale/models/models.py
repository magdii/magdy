# -*- coding: utf-8 -*-

from collections import defaultdict

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


# class CrmLead(models.Model):
#     _inherit = "crm.lead"

    # @api.multi
    # def mark_lost_new(self):
    #     print "login_user::",self.env.user
    #     print "user_id::::::",self.user_id
    #     if self.env.user == self.user_id:
    #         raise UserError(_('please modify the form'))
    #     return {
    #             'type': 'ir.actions.act_window',
    #             'name': 'Crm Lead',
    #             'res_model':'crm.lead.lost',
    #             # 'res_id': service_order.id,
    #             # 'context': {'default_is_logistic': True,
    #             #             'default_logistic_export_id':exp_obj.id,
    #             #             'default_so_po':'sale',
    #                         # 'default_purchase_order':exp_obj.purchase_order.id,
    #                         # },
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             'target': 'new',
    #     }


class ProductTemplate(models.Model):
    _inherit = "product.template"

    average_product_price2 = fields.Float()

class StockQuant(models.Model):
    _inherit = "stock.quant"

    is_quant = fields.Boolean(string="Is Quant")
    stock_qty = fields.Float(string="quantity")

    @api.multi
    def _compute_inventory_value(self):
        quants = self.env['stock.quant']
        real_value_quants = self.filtered(lambda quant: quant.product_id.cost_method == 'real' and not quant.is_quant)
        for quant in real_value_quants:
            quant.inventory_value = quant.cost * quant.qty
        value_quants = self.filtered(lambda q: q.is_quant)
        quants |= real_value_quants
        quants |= value_quants
        for rec in value_quants:
            rec.inventory_value = rec.stock_qty * rec.qty
        return super(StockQuant, self - quants)._compute_inventory_value()

    def _create_account_move_line(self, move, credit_account_id, debit_account_id, journal_id):
        # group quants by cost
        new_price = 0.0
        new_quantity = 0.0
        price_x = 0.0
        qty_z = 0.0
        x = []
        z = []
        l = []
        print "move:::::::::::::::::::::::::", move.product_uom_qty
        # print "product:::::::::::::::::::::::::", move.product_id.id
        # print "picking_type_id::::::::::::::", move.picking_id.picking_type_id.default_location_dest_id.name
        if move.picking_type_id.code == 'outgoing':
            product_obj = self.search([
                ('product_id', '=', move.product_id.id),
                ('location_id', '=', move.picking_id.picking_type_id.default_location_dest_id.id),
            ])

            if product_obj:
                for rec in product_obj:
                    new_price += rec.inventory_value
                    new_quantity += rec.qty
            quant_cost_qty = defaultdict(lambda: 0.0)
            for quant in self:
                quant_cost_qty[quant.cost] += quant.qty

            AccountMove = self.env['account.move']
            for cost, qty in quant_cost_qty.iteritems():
                move_lines = move._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id)
                if move_lines:
                    product_ids = self.env['product.product'].browse(move_lines[0][2]['product_id'])
                    product_avg = product_ids.average_product_price2
                    product_cost = product_ids.standard_price
                    # x.append(move_lines[0][2]['debit'])
                    price2 = 0.0
                    for rec in self:
                        if rec.is_quant:
                            price2 = product_avg * move_lines[0][2]['quantity']
                        else:
                            one_piece = rec.inventory_value / rec.qty
                            price2= one_piece * move_lines[0][2]['quantity']
                            # price2 = product_cost * move_lines[0][2]['quantity']
                    x.append(price2)
                    z.append(move_lines[0][2]['quantity'])
                    price2 = 0.0
                    print"move_lines:::::::::::::", move_lines
                    print"move_lines_quantity:::::::::::::", move_lines[0][2]['quantity']
                    print"move_lines_debit:::::::::::::", move_lines[0][2]['debit']
                    l.append(move_lines)
                    # date = self._context.get('force_period_date', fields.Date.context_today(self))
                    # new_account_move = AccountMove.create({
                    #     'journal_id': journal_id,
                    #     'line_ids': move_lines,
                    #     'date': date,
                    #     'ref': move.picking_id.name})
                    # new_account_move.post()
            for i in x:
                price_x += i
            for r in z:
                qty_z += r
            total_price = new_price + price_x
            total_qty = new_quantity + qty_z
            average_price = total_price / total_qty
            product_price = move.product_uom_qty * average_price
            move.product_id.average_product_price2 = average_price
            print "price:::::::::", new_price
            print "zzzzzzz:::::::::::::::", z
            print "price_x:::::::::::::::", price_x
            print "QTY:::::::::::", new_quantity
            print "xxxxxxx:::::::::::::::", x
            print "qty_z:::::::::::::::", qty_z
            print "total_price:::::::::::::::", total_price
            print "total_qty:::::::::::::::", total_qty
            print "average_price:::::::::::::::", average_price
            print "product_price:::::::::::::::", product_price
            print "lllllllllllll:::::::::::::::", l
            print "lllllllllllll:::::::::::::::", l[0]
            f = dict(l[0][0][2])
            g = dict(l[0][1][2])
            f['debit'] = product_price
            g['credit'] = product_price
            f['quantity'] = qty_z
            g['quantity'] = qty_z
            print "debit:::::::::::::::", l[0][0]
            print "credit:::::::::::::::", l[0][1]
            print "ffffff:::::::::::::::", f
            print "gggggg:::::::::::::::", g
            date = self._context.get('force_period_date', fields.Date.context_today(self))
            move_lines_new = [(0, 0, f), (0, 0, g)]
            new_account_move = AccountMove.create({
                'journal_id': journal_id,
                'line_ids': move_lines_new,
                'date': date,
                'ref': move.picking_id.name})
            new_account_move.post()
            print "move_lines_new::::::::::", move_lines_new
            product_obj2 = self.search([
                ('product_id', '=', move.product_id.id),
                ('location_id', '=', move.picking_id.picking_type_id.default_location_dest_id.id),
            ])
            if product_obj2:
                for rec2 in product_obj2:
                    print "rec2:::::::::::", rec2
                    print "rec2_qty:::::::::::", rec2.qty
                    print "average_price:::::::::::", average_price
                    rec2.update({
                        'is_quant': True,
                        'stock_qty': average_price,
                        # 'inventory_value': rec2.qty * average_price,
                    })
                    # print "inventory_value:::::::::::", rec2.inventory_value
        else:
            quant_cost_qty = defaultdict(lambda: 0.0)
            for quant in self:
                quant_cost_qty[quant.cost] += quant.qty

            AccountMove = self.env['account.move']
            for cost, qty in quant_cost_qty.iteritems():
                move_lines = move._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id)
                if move_lines:
                    date = self._context.get('force_period_date', fields.Date.context_today(self))
                    new_account_move = AccountMove.create({
                        'journal_id': journal_id,
                        'line_ids': move_lines,
                        'date': date,
                        'ref': move.picking_id.name})
                    new_account_move.post()


# class getJournal(models.Model):
#     _inherit = "stock.move"
#
#     def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id):
#         """
#         Generate the account.move.line values to post to track the stock valuation difference due to the
#         processing of the given quant.
#         """
#         self.ensure_one()
#
#         if self._context.get('force_valuation_amount'):
#             valuation_amount = self._context.get('force_valuation_amount')
#         else:
#             if self.product_id.cost_method == 'average':
#                 valuation_amount = cost if self.location_id.usage == 'supplier' and self.location_dest_id.usage == 'internal' else self.product_id.standard_price
#             else:
#                 valuation_amount = cost if self.product_id.cost_method == 'real' else self.product_id.standard_price
#         # the standard_price of the product may be in another decimal precision, or not compatible with the coinage of
#         # the company currency... so we need to use round() before creating the accounting entries.
#         debit_value = self.company_id.currency_id.round(valuation_amount * qty)
#
#         # check that all data is correct
#         if self.company_id.currency_id.is_zero(debit_value):
#             if self.product_id.cost_method == 'standard':
#                 raise UserError(_("The found valuation amount for product %s is zero. Which means there is probably a configuration error. Check the costing method and the standard price") % (self.product_id.name,))
#             return []
#         credit_value = debit_value
#
#         if self.product_id.cost_method == 'average' and self.company_id.anglo_saxon_accounting:
#             # in case of a supplier return in anglo saxon mode, for products in average costing method, the stock_input
#             # account books the real purchase price, while the stock account books the average price. The difference is
#             # booked in the dedicated price difference account.
#             if self.location_dest_id.usage == 'supplier' and self.origin_returned_move_id and self.origin_returned_move_id.purchase_line_id:
#                 debit_value = self.origin_returned_move_id.price_unit * qty
#             # in case of a customer return in anglo saxon mode, for products in average costing method, the stock valuation
#             # is made using the original average price to negate the delivery effect.
#             if self.location_id.usage == 'customer' and self.origin_returned_move_id:
#                 debit_value = self.origin_returned_move_id.price_unit * qty
#                 credit_value = debit_value
#         partner_id = (self.picking_id.partner_id and self.env['res.partner']._find_accounting_partner(self.picking_id.partner_id).id) or False
#         if self.picking_id.picking_type_id.code == 'outgoing':
#             new_price = 0.0
#             new_quantity = 0.0
#             qty_new = 0.0
#             product_price_new = 0.0
#
#             product_obj = self.env['stock.quant'].search([
#                 ('product_id', '=', self.product_id.id),
#                 ('location_id', '=', self.picking_id.picking_type_id.default_location_dest_id.id),
#             ])
#
#             if product_obj:
#                 for rec in product_obj:
#                     # new_price += rec.stock_unit_price
#                     new_price += rec.inventory_value
#                     new_quantity += rec.qty
#             # product_price = new_price / len(product_obj)
#             product_move_price = self.product_id.standard_price * self.product_uom_qty
#             new_mix_price = new_price + product_move_price
#             new_mix_qty = new_quantity + self.product_uom_qty
#             new_mix = new_mix_price / new_mix_qty
#             if new_mix_qty < self.product_uom_qty:
#                 raise UserError(_('please select Small Quantity'))
#             else:
#                 qty_new = self.product_uom_qty
#
#             total_mix_price=qty_new*new_mix
#             debit_line_vals = {
#                 'name': self.name,
#                 'product_id': self.product_id.id,
#                 'quantity': qty,
#                 'product_uom_id': self.product_id.uom_id.id,
#                 'ref': self.picking_id.name,
#                 'partner_id': partner_id,
#                 'debit': total_mix_price,
#                 'credit': 0,
#                 'account_id': debit_account_id,
#             }
#             credit_line_vals = {
#                 'name': self.name,
#                 'product_id': self.product_id.id,
#                 'quantity': qty,
#                 'product_uom_id': self.product_id.uom_id.id,
#                 'ref': self.picking_id.name,
#                 'partner_id': partner_id,
#                 'credit': total_mix_price,
#                 'debit': 0,
#                 'account_id': credit_account_id,
#             }
#             new_price = 0.0
#             new_quantity = 0.0
#             qty_new = 0.0
#             product_price_new = 0.0
#         else:
#             debit_line_vals = {
#             'name': self.name,
#             'product_id': self.product_id.id,
#             'quantity': qty,
#             'product_uom_id': self.product_id.uom_id.id,
#             'ref': self.picking_id.name,
#             'partner_id': partner_id,
#             'debit': debit_value if debit_value > 0 else 0,
#             'credit': -debit_value if debit_value < 0 else 0,
#             'account_id': debit_account_id,
#             }
#             credit_line_vals = {
#                 'name': self.name,
#                 'product_id': self.product_id.id,
#                 'quantity': qty,
#                 'product_uom_id': self.product_id.uom_id.id,
#                 'ref': self.picking_id.name,
#                 'partner_id': partner_id,
#                 'credit': credit_value if credit_value > 0 else 0,
#                 'debit': -credit_value if credit_value < 0 else 0,
#                 'account_id': credit_account_id,
#             }
#
#         res = [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
#         print "res :::::::::::::",res
#         if credit_value != debit_value:
#             # for supplier returns of product in average costing method, in anglo saxon mode
#             diff_amount = debit_value - credit_value
#             price_diff_account = self.product_id.property_account_creditor_price_difference
#             if not price_diff_account:
#                 price_diff_account = self.product_id.categ_id.property_account_creditor_price_difference_categ
#             if not price_diff_account:
#                 raise UserError(_('Configuration error. Please configure the price difference account on the product or its category to process this operation.'))
#             price_diff_line = {
#                 'name': self.name,
#                 'product_id': self.product_id.id,
#                 'quantity': qty,
#                 'product_uom_id': self.product_id.uom_id.id,
#                 'ref': self.picking_id.name,
#                 'partner_id': partner_id,
#                 'credit': diff_amount > 0 and diff_amount or 0,
#                 'debit': diff_amount < 0 and -diff_amount or 0,
#                 'account_id': price_diff_account.id,
#             }
#             res.append((0, 0, price_diff_line))
#         return res
