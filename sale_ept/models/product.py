from odoo import fields, models, api


class Product(models.Model):
    _name = "product.ept"
    _description = "Product Ept : It will store the information about the Product"

    name = fields.Char(string="Name", required=True, help="This field will accept the name")

    sku = fields.Char(string="SKU", required=True, help="This field will accepts the product sku number")

    weight = fields.Float(string="Weight", digits=(6, 2), help="This field will accept the weight of the "
                                                               "product up to the two decimal places")

    length = fields.Float(string="Length", digits=(6, 2), help="This field will accept the length")

    volume = fields.Float(string="Volume", digits=(6, 2), help="This field will accept the volume")

    width = fields.Float(string="Width", digits=(6, 2), help="This field will accept the width")

    barcode = fields.Char(string="Barcode", help="This field will accept the barcode of the product")

    product_type = fields.Selection([('Storable', 'Storable'),
                                     ('Consumable', 'Consumable'),
                                     ('Service', 'Service')], help="This field will accept the "
                                                                   "drop_down menu about product_type")

    sale_price = fields.Float(string="Sale Price", digits=(6, 2), help="This field will accept the sale_price of "
                                                                       "the product", default=1.00)

    cost_price = fields.Float(string="Cost Price", digits=(6, 2), help="This field will accept the cost_price of "
                                                                       "the product", default=1.00)

    category_id = fields.Many2one(comodel_name='product.category.ept', string="Category ID",
                                  help="This field will accept the Category ID")

    uom_id = fields.Many2one(comodel_name='product.uom.ept', string="UOM ID",
                             help="This field will accept the UOM ID")

    product_stock = fields.Float(string="Product Stock", store=False, compute="product_stock_calculation",
                                 help="This field will accept the Product Stock", digits=(6, 2))

    tax_ids = fields.Many2many(string="Customer Taxes",comodel_name='account.tax.ept', help="This field will accept "
                                                                                            "the Tax IDs"
                               ,domain=[('tax_use', '=', 'Sales')])

    # domain - load only Sales Type of tax

    def product_stock_calculation(self):
        # warehouse = self.env['stock.warehouse.ept'].search([])
        # stock_location = []
        # for stock_locations in warehouse:
        #     location_s = stock_locations.stock_location_id.id
        #     stock_location.append(location_s)

        warehouse = self.env['stock.warehouse.ept'].search([])
        stock_location = []
        location = self.env.context.get('location_id')
        if location:
            stock_location.append(location)
        else:
            stock_location = [location.stock_location_id.id for location in warehouse]

        for record in self:
            record.product_stock = 0
            move_line_in = self.env['stock.move.ept'].search(
                [('destination_location_id', 'in', stock_location), ('product_id', '=', record.id),
                 ('state', '=', 'Done')])

            for stock in move_line_in:
                record.product_stock += stock.qty_delivered

            move_line_out = self.env['stock.move.ept'].search(
                [('source_location_id', 'in', stock_location), ('product_id', '=', record.id),
                 ('state', '=', 'Done')])

            for stock in move_line_out:
                record.product_stock -= stock.qty_delivered

    def action_product_stock_update(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale_ept.action_product_stock_update_wizard")
        return action
