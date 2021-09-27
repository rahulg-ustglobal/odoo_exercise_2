from odoo import fields, models


class CrmTeam(models.Model):
    _name = "crm.team.ept"
    _description = "Crm Team Ept : It will store the information about the Crm Team"

    name = fields.Char(string="Name", required=True, help="This field will accept the name")
    team_leader = fields.Many2one(comodel_name="res.users")
