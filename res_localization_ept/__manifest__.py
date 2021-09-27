{
    'name': 'Localization',
    'version': '1.0',
    'sequence': -100,
    'summary': 'Localization : This will store the information about localization',
    'description': """Localization : This will store the information about localization""",
    'depends': ['sales_team'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_country.xml',
        'views/res_state.xml',
        'views/res_city.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
