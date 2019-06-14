# -*- coding: utf-8 -*-
{
    'name': "sale orders report",

    'summary': """
        get sale orders report
        """,

    'description': """
       sale order report
    """,
    'author': "magdy",
    'website': "http://www.yourcompany.com",
    'category': 'sale',
    'version': '0.1',
    'depends': ['base','sale'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'wizard/sale_order.xml',
        'report/sale_order.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}