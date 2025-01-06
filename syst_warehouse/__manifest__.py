# -*- coding: utf-8 -*-
{
    'name': "Warehouse",

    'summary': """
        Warehouse""",

    'description': """
        Warehouse
    """,

    'author': "Lion Younes",
    'website': "https://www.linkedin.com/in/lion-younes",

    'category': 'Warehouse',
    'version': '0.1',

    'depends': ['base','analytic','mail'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'configuration/request_config.xml',
        'views/product_name.xml',
        'views/quantity.xml',
        'views/division.xml',
        'views/request.xml',
        'views/stock.xml',
        'views/stock_template.xml',
        'views/menu_items.xml',
    ],
}
