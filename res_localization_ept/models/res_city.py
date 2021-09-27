from odoo import fields, models


class ResLocalizationCity(models.Model):
    _name = "res.city.ept"
    _description = "Res City Ept : It will store the information about City"

    name = fields.Char(string="City Name", help="It will accepts the customer name")
    state_id = fields.Many2one('res.state.ept')
