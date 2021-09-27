{
    'name': 'Student',
    'version': '1.0',
    'sequence': -100,
    'summary': 'Student : This will store the information about the student',
    'description': """Student : This will store the information about the student""",
    'depends': ['sales_team'],
    'data': [
        'security/ir.model.access.csv',
        'views/student.xml',
        'views/course.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
