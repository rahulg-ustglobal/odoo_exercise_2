from odoo import fields, models, api


class StockLocation(models.Model):
    _name = "stock.location.ept"
    _description = "Stock Location Ept : It will store the information about the Stock Location"

    name = fields.Char(string="Name",required=True,
                       help="This field will accept the Name of the Stock Location")
    parent_id = fields.Many2one(comodel_name='stock.location.ept',string="Parent",
                                help="This field will accept the Parent")
    location_type = fields.Selection([('Vendor','Vendor'),
                                      ('Customer','Customer'),
                                      ('Internal','Internal'),
                                      ('Inventory Loss','Inventory Loss'),
                                      ('Production','Production'),
                                      ('Transit','Transit'),
                                      ('View','View')],string="Location Type",
                                     help="This field will accept the Location type of the Stock Location")
    is_scrap_location = fields.Boolean(string="Scrap Location",help="This field will accept the Scrap Location")

