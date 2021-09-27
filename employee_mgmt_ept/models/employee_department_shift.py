from odoo import fields, models


class EmployeeDepartmentShift(models.Model):
    _name = "employee.department.shift.ept"
    _description = "Employee Department Shift : It will store the information about the Employee shift"
    _rec_name = 'shift'

    shift = fields.Selection([('Morning', 'Morning'),
                              ('Afternoon', 'Afternoon'),
                              ('Evening', 'Evening'),
                              ('Night', 'Night')],
                             help="It will accepts the dropdown menu about shift type of the employee")

    employee_ids = fields.One2many('employee.ept', 'shift_id')
