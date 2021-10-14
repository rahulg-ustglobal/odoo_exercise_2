from odoo import fields, models


class EmployeeEpt(models.Model):
    _name = "employee.ept"
    _description = "Employee Ept : It will store the information about the Employee"

    name = fields.Char(string="Employee Name", required=True, help="It will accepts the employee Name name")
    department_name_id = fields.Many2one(comodel_name='employee.department.ept', string="Department Name",
                                         help="This field will accept the Department Name")
    shift_id = fields.Many2one(comodel_name='employee.department.shift.ept', string="Shift",
                               help="This field will accept the Shift ID")
    job_position = fields.Char(string="Job Position", help="It will accept the job position of the employee")
    salary = fields.Float(string="Salary", digits=(6, 2), help="It will accept the salary of the employee")
    hire_date = fields.Date(string="Hire Date", help="It will accept the hire date of the employee")
    gender = fields.Selection([('Male', 'Male'),
                               ('Female', 'Female'),
                               ('Transgender', 'Transgender')], string="Gender",
                              help="It will accept the gender of the employee")
    job_type = fields.Selection([('Permanent', 'Permanent'),
                                 ('Ad_Hoc', 'Ad_Hoc')], string="Job Type"
                                , help="It will accept the job type of the employee")
    is_manager = fields.Boolean(string="Is Manager", help="It will give the checkbox for the tick")
    manager_id = fields.Many2one(comodel_name='employee.ept', string="Manager",
                                 help="This field will accept the Manager ID")
    related_user_id = fields.Many2one(comodel_name='res.users', string="Related User",
                                      help="This field will accept the Related User ID")
    employee_ids = fields.One2many(comodel_name='employee.ept', inverse_name='manager_id', string="Employee",
                                   help="This field will accept the Employee IDs")
    # increment_percentage = fields.Float()
