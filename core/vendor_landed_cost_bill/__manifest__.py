# -*- coding: utf-8 -*-
{
    'name': "Vendor Landed cost Bill",
    'summary': """Vendor Landed cost Bill""",
    'description': """""",
    'author': "Magdy Salah",
    'website': "http://www.yourcompany.com",
    'category': 'inventory',
    'version': '0.1',
    'depends': ['account','stock','stock_landed_costs'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_landed_cost.xml',
        'views/vendor_landed_cost.xml',
    ],
}