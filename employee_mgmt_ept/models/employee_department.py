from odoo import fields, models


class EmployeeDepartment(models.Model):
    _name = "employee.department.ept"
    _description = "Employee Department Ept : It will store the information about the Employee Department"

    name = fields.Char(string="Department Name", required=True, help="It will accepts the department Name name")
    employee_ids = fields.One2many('employee.ept', 'department_name_id')
    department_manager_id = fields.Many2one('res.users')
