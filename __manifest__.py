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
    'depends': ['point_of_sale', 'base'],  # Add other dependencies as needed
    'data': [
        'security/ir.model.access.csv',
        'views/partner_views.xml',
        'views/product_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

