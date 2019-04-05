# -*- coding: utf-8 -*-
{
    'name': "Transportion Bill",
    'summary': """Transportion Bill""",
    'description': """""",

    'author': 'Mahmoud Abd El-aziz',
    'website': '',
    'category': 'Sale',
    'version': '10.1',
    'depends': ['account','sale','delivery'],
    'data': [
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/delivery.xml',
        'views/delivery_method_wizard.xml',
        'views/quotation_report.xml',
    ],
    'demo': [
    ],
}