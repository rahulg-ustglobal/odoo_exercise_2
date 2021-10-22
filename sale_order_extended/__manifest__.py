{
    'name': 'Sales Order Extended',
    'version': '1.0',
    'sequence': -100,
    'summary': 'Sales Order Extended : This will store the information about the Sales Order Extended',
    'description': """Sales Order Extended : This will store the information about the Sales Order Extended""",
    'depends': ['sale_crm'],
    'data': [
        'data/product.xml',
        'views/sale_order.xml',
        'data/crm_tag.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
