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

    def product_stock_calculation(self):
        self.product_stock = 0
        warehouse = self.env['stock.warehouse.ept'].search([])
        for products in warehouse:
            pass
