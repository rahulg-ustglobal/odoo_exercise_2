from odoo import fields, models


class EmployeeEpt(models.Model):
    _name = "employee.ept"
    _description = "Employee Ept : It will store the information about the Employee"

    name = fields.Char(string="Employee Name",required=True,help="It will accepts the employee Name name")
    department_name_id = fields.Many2one('employee.department.ept')
    shift_id = fields.Many2one('employee.department.shift.ept')
    job_position = fields.Char(string="Job Position",help="It will accept the job position of the employee")
    salary = fields.Float(string="Salary",digits=(6,2),help="It will accept the salary of the employee")
    hire_date = fields.Date(string="Hire Date",help="It will accept the hire date of the employee")
    gender = fields.Selection([('Male','Male'),
                               ('Female','Female'),
                               ('Transgender','Transgender')],help="It will accept the gender of the employee")
    job_type = fields.Selection([('Permanent','Permanent'),
                               ('Ad_Hoc','Ad_Hoc')],help="It will accept the job type of the employee")
    is_manager = fields.Boolean(string="Is Manager",help="It will give the checkbox for the tick")
    manager_id = fields.Many2one('employee.ept')
    related_user_id = fields.Many2one('res.users')
    employee_ids = fields.One2many('employee.ept', 'manager_id')
    # increment_percentage = fields.Float()
