from odoo import fields, models, api


class StockWarehouse(models.Model):
    _name = "stock.warehouse.ept"
    _description = "Stock Warehouse Ept : It will store the information about the Stock Warehouse"

    name = fields.Char(string="Warehouse Name", help="This field will accept the Warehouse Name", required=True)
    short_code = fields.Char(string="Short Code", help="This field will accept the Short code", required=True)
    address_id = fields.Many2one(comodel_name='res.partner.ept', string="Address",
                                 help="This field will accept the address")
    stock_location_id = fields.Many2one(comodel_name='stock.location.ept', string="Stock Location",
                                        help="This field will accept the Stock Location")
    view_location_id = fields.Many2one(comodel_name="stock.location.ept", string="View Location",
                                       help="This field will accept the View Location")

    @api.model
    def create(self, vals):
        location_view = self.env['stock.location.ept'].create({
            'name': 'View:' + vals['short_code'],
            'location_type': 'View',
        })

        stock_location = self.env['stock.location.ept'].create({
            'name': 'Internal:' + vals['short_code'],
            'parent_id': location_view.id,
            'location_type': 'Internal'
        })

        vals.update({'stock_location_id': stock_location.id,
                     'view_location_id': location_view.id})

        return super(StockWarehouse, self).create(vals)
