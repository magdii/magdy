# -*- coding: utf-8 -*-
from openerp import models, fields
from openerp.addons import decimal_precision as dp

class ResPartner(models.Model):
    _name = 'res.partners'
    name = fields.Char('Name', required=True)
    email = fields.Char('Email')
    date = fields.Date('Date')
    is_company = fields.Boolean('Is a company')
    parent_id = fields.Many2one('res.partner', 'Related Company')
    child_ids = fields.One2many('res.partner', 'parent_id','Contacts')

    # today_str = fields.Date.context_today()
    # val1 = {'name': u'Eric Idle',
    #         'email': u'eric.idle@example.com',
            # 'date': today_str}
    # val2 = {'name': u'John Cleese',
    #         'email': u'john.cleese@example.com',
            # 'date': today_str}
    # partner_val = {
    #         'name': u'Flying Circus',
    #         'email': u'm.python@example.com',
            # 'date': today_str,
            # 'is_company': True,
            # 'child_ids': [(0, 0, val1),
            #               (0, 0, val2),
            #              ]
            # }
    # record = self.env['res.partners'].create(partner_val)