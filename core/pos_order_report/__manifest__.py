# -*- coding: utf-8 -*-
{
    'name': "pos order report",
    'summary': """pos order report""",
    'description': """""",
    'author': "Magdy Salah",
    'website': "http://www.yourcompany.com",
    'category': 'point of sale',
    'version': '0.1',
    'depends': ['point_of_sale','report'],
    'qweb': ['static/src/xml/pos.xml'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'reports/selling_line_report.xml',
        'views/pos_template.xml',
        'views/pos.xml',
    ],
}