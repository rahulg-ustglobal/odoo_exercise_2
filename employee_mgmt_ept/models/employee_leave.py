from odoo import fields, models


class EmployeeLeave(models.Model):
    _name = "employee.leave.ept"
    _description = "Employee Leave Ept : It will store the information about the Employee Leave"

    employee_id = fields.Many2one('employee.ept')
    # department_id = fields.Many2one('employee.department.ept')
    start_date = fields.Date(string="Start Date",help="Here, Employee can select the start date")
    end_date = fields.Date(string="End Date",help="Here, Employee can select the end date")

    status = fields.Selection([('Draft', 'Draft'),
                               ('Approved', 'Approved'),
                               ('Refused', 'Refused'),
                               ('Cancelled', 'Cancelled'),
                               ('Draft', 'Draft')], default='Draft', help="It will show the leave-status")

    leave_description = fields.Char(string="Leave Description",required=True,help="It will give the text-box for the "
                                                                                  "Employee to describe reason about "
                                                                                  "leave")