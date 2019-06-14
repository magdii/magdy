# -*- coding: utf-8 -*-
# © 2017 Jérôme Guerriat
# © 2017 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from odoo import fields, models, api
_logger = logging.getLogger(__name__)


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    def _search_required_task_id(self, operator, value):
        return []

    is_projects_active = fields.Boolean(string='Any Active Projects',
                                       compute='compute_is_active', store=True)
    required_task_id = fields.Boolean(compute="_compute_required_task_id", search="_search_required_task_id", string='Task Required', readonly=True)

    @api.multi
    def _compute_required_task_id(self):
        for account in self:
            orders = self.env['sale.order'].sudo().search([('project_id','=',account.id)])
            account.required_task_id = False
            if not orders:
                continue
            for order in orders:
                cost_lines = [a for a in order.sudo().order_line if a.sudo().product_id and a.sudo().product_id.invoice_policy == 'cost']
                task_lines = [a for a in order.sudo().order_line if a.sudo().product_id and a.sudo().product_id.track_service == 'task']
                _logger.info(cost_lines)
                if len(task_lines) > 1 or (len(task_lines)==1 and len(cost_lines)==1):
                    account.required_task_id = True
                    break
            

    @api.multi
    @api.depends('project_ids')
    def compute_is_active(self):
        for account in self:
            account.is_projects_active = \
                any(project.active for project in account.project_ids)


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.multi
    @api.constrains('active')
    def recompute_account_active(self):
        for project in self:
            project.analytic_account_id.compute_is_active()
