from odoo import fields, models

class StudentInformation(models.Model):
    _name = "student.ept"
    _description = "Student Ept : It will stores the information about the Student"

    name = fields.Char(string="Student Name",required=True,help="It will accepts the student name")
    student_class = fields.Char(string="Class", required=True, help="It will accepts the student class")
    birth_date = fields.Date(string="Date of Birth",required=True,help="It will accepts the date of birth of the "
                                                                       "student")
    courses_ids = fields.Many2many('course.ept')
