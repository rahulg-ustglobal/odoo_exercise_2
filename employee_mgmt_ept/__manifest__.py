{
    'name': 'Employee',
    'version': '1.0',
    'sequence': -100,
    'summary': 'Employee : This will store the information about the employee',
    'description': """Employee : This will store the information about the employee""",
    'depends': ['base'],
    'data': [
        'security/security_employee_mgmt.xml',
        'security/ir.model.access.csv',
        'views/employee_department.xml',
        'views/employee_department_shift.xml',
        'views/employee.xml',
        'views/employee_leave.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
