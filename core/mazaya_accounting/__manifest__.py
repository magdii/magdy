# -*- coding: utf-8 -*-
{
    'name': "Mazaya Accounting",

    'summary': """
       Mazaya accounting mangament""",

    'description': """
       
    """,

    'author': "Mazaya Team",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/checks.xml',
        'views/checks_returned.xml',
        'views/payment_view.xml',
        'views/invoice_view.xml',
        'reports/sales_bill_report.xml',
    ],

}
