from odoo import fields, models, api


class ResLocalizationCountry(models.Model):
    _name = "res.country.ept"
    _description = "Res Country Ept : It will stores the information about Country"

    name = fields.Char(string="Country Name", help="It will accepts the country name")
    country_code = fields.Char(string="Country Code", help="It will accepts the country code")
    state_ids = fields.One2many('res.state.ept', 'country_id')

    _sql_constraints = [('check_the_unique_country_code','UNIQUE(country_code)','Please enter the unique country code')]


    # create Method : Overridden
    @api.model
    def create(self, vals1):
        values1 = super(ResLocalizationCountry, self).create(vals1)
        return values1

    # write Method : Overridden
    def write(self, vals2):
        values2 = super(ResLocalizationCountry, self).write(vals2)
        return values2

    # unlink Method : Overridden
    def unlink(self):
        values3 = super(ResLocalizationCountry, self).unlink()
        return values3

    # copy Method : Overridden
    def copy(self,default=None):
        # if default is None:
        #     default={}
        # if default.get('name'):
        #     default['name']=("%s(Copy)",self.name)
        default = {'name': self.name + '(copy)'}
        return super(ResLocalizationCountry, self).copy(default)

    # search Method : Overridden
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        res = super(ResLocalizationCountry, self).search(args, offset, limit, order, count)
        return res
