from odoo import fields, models, api


class ResPartner(models.Model):
    _name = "res.partner.ept"
    _description = "Res Partner Ept : It will store the information about the Res Partner"

    name = fields.Char(string="Name", required=True, help="This field will accept the name the Res Partner")
    street_1 = fields.Char(string="Street 1", help="This field will accept the street_1 address of the Res Partner")
    street_2 = fields.Char(string="Street 2", help="This field will accept the street_2 address of the Res Partner")
    country_id = fields.Many2one(comodel_name='res.country.ept', string="Country ID",
                                 help="This field will accept the Country ID")
    state_id = fields.Many2one(comodel_name='res.state.ept', string="State",
                               help="This field will accept the state id")
    city_id = fields.Many2one(comodel_name='res.city.ept', string="City"
                              , help="This field will accept the city")
    zip_code = fields.Char(string="Zip Code", help="This field will accept the zip_code of the Res Partner")
    email = fields.Char(string="Email", help="This field will accept the email of the Res Partner")
    mobile = fields.Char(string="Mobile No", help="This filed will accepts the mobile number of the Res Partner")
    phone = fields.Char(string="Phone", help="This filed will accept the phone number of the Res Partner")
    photo = fields.Image(string="", help="This will accept the image of the Res Partner")
    website = fields.Char(string="Website", help="This will accept the website of the Res Partner")
    active = fields.Boolean(string="Active", help="This field will show the check-box", default=True)
    parent_id = fields.Many2one(comodel_name='res.partner.ept', string="Parent",
                                help="This field will accept the parent id")
    child_ids = fields.One2many(comodel_name='res.partner.ept', inverse_name='parent_id', string="Child",
                                help="This field will accept the Child ids")
    address_type = fields.Selection([('Invoice', 'Invoice'),
                                     ('Shipping', 'Shipping'), ('Contact', 'Contact')], string="Address Type",
                                    help="This field will create the drop down menu about address type")
