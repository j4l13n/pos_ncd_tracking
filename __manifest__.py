# -*- coding: utf-8 -*-
{
    'name': 'POS NCD Tracking',
    'version': '0.1',
    'category': 'Healthcare',
    'summary': 'Module for managing patients with Non-Communicable Diseases and product tracking in POS.',
    'description': """
        POS NCD Tracking Module for Patient and Product Management.
        This module integrates with the existing Odoo POS functionalities to manage and monitor patients with NCDs.
    """,
    'author': 'Julien at ADFinance Rwanda Ltd',
    'website': '',
    'depends': ['base', 'point_of_sale'],  # Add other dependencies as needed
    'data': [
        'security/ir.model.access.csv',
        'data.xml',
        'views/ncd_communication_log_views.xml',
        'views/partner_views.xml',
        'views/product_views.xml',
        'views/pos_ncd_views.xml',
        'views/settings_view.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_ncd_tracking/static/src/js/ncd_pos.js',  # Include your JavaScript file
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3',
}

