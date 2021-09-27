from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResLocalizationState(models.Model):
    _name = "res.state.ept"
    _description = "Res State Ept : It will stores the information about State"

    name = fields.Char(string="State Name", help="It will accepts the states name")
    state_code = fields.Char(string="State Code", help="It will accepts the country code")
    country_id = fields.Many2one('res.country.ept')
    city_ids = fields.One2many('res.city.ept', 'state_id')

    @api.constrains('state_code')
    def check_state_code(self):
        for rec in self:
            state_codes = self.search([('state_code', '=', rec.state_code), ('id', '!=', rec.id)])
            if state_codes:
                raise ValidationError(f"State code is already available {rec.state_code}")
