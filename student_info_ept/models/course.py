from odoo import fields, models

class CourseInformation(models.Model):
    _name = "course.ept"
    _description = "Course Ept : It will stores the information about the Course"

    name = fields.Char(string="Course Name",required=True,help="It will accepts the course name")
    students_ids = fields.Many2many('student.ept')

