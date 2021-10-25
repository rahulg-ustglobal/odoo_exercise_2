{
    'name': 'Sales Order Extended',
    'version': '1.0',
    'sequence': -100,
    'summary': 'Sales Order Extended : This will store the information about the Sales Order Extended',
    'description': """Sales Order Extended : This will store the information about the Sales Order Extended""",
    'depends': ['sale_crm'],
    'data': [
        'data/product_data_extended.xml',
        'data/crm_tag_extended.xml',
        'views/sale_order_extended.xml',
        'views/product_extended.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
