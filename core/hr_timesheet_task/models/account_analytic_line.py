# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, api, _
from odoo.exceptions import AccessError
_logger = logging.getLogger(__name__)

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.multi
    @api.depends('account_id')
    def _compute_required_task_id(self):
        for line in self:
            if not line.is_timesheet or not self.env.context.get('default_is_timesheet'):
                line.required_task_id = False
                continue
            if line.account_id:
                line.required_task_id = line.sudo().account_id.required_task_id
                continue
            line.required_task_id = False


    def _search_required_task_id(self, operator, value):
        return []

    required_task_id = fields.Boolean(compute="_compute_required_task_id", search="_search_required_task_id", string='Task Required')

    @api.multi
    @api.onchange('account_id')
    def onchange_account_id_task(self):
        _logger.info('onchange_account_id_task')
        for line in self:
            if line.account_id:
                line.required_task_id = line.account_id.required_task_id
            line.task_id = False
            orders = self.env['sale.order'].sudo().search([('project_id','=',line.account_id.id)])
            _logger.info(orders)
            if not orders:
                continue
            for order in orders:
                cost_lines = [a for a in order.sudo().order_line if a.sudo().product_id and a.sudo().product_id.invoice_policy == 'cost']
                task_lines = [a for a in order.sudo().order_line if a.sudo().product_id and a.sudo().product_id.track_service == 'task']
                if len(task_lines) == 1 and len(cost_lines) == 1:
                    line.task_id = self.env['project.task'].search([('sale_line_id','=',cost_lines[0].id)], limit=1).id

    @api.multi
    def write(self, vals):
        if vals.get('task_id') != None:
            for line in self:
                if line.required_task_id and not vals.get('task_id'):
                    raise AccessError(_('Task is Required'))
        if vals.get('required_task_id') != None:
            del vals['required_task_id']
        return super(AccountAnalyticLine, self).write(vals)

    @api.model
    def create(self, vals):
        if vals.get('is_timesheet') and vals.get('account_id') and not vals.get('task_id'):
            if self.env['account.analytic.account'].browse(vals['account_id']).required_task_id:
                raise AccessError(_('Task is Required'))
        return super(AccountAnalyticLine, self).create(vals)
