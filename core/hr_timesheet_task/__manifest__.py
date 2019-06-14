# -*- coding: utf-8 -*-
# Copyright 2016 Niboo SPRL, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR - Task In Timesheets',
    'category': 'HR',
    'summary': 'Allow the user to select task in a timesheet',
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'version': '0.1',
    'description': '''
    The user is now able to select a task in a timesheet
        ''',
    'author': 'Niboo, Camptocamp SA, Odoo Community Association (OCA)',
    'depends': [
        'hr_timesheet_sheet',
        # 'project_timesheet',
    ],
    'data': [
        'views/hr_timesheet_assets.xml',
        'views/hr_timesheet_view.xml',
    ],
    'qweb': [
        'static/src/xml/hr_timesheet_task.xml',
    ],
    'installable': True,
    'application': False,
}
