from odoo import fields, models, api


class StockInventory(models.Model):
    _name = "stock.inventory.line.ept"
    _description = "Stock Inventory Line Ept : It will store the information about the Stock Inventory Line"

    product_id = fields.Many2one(comodel_name='product.ept', string="Product", required=True,
                                 help="This field will accept the Product ID")

    available_qty = fields.Float(string="System Quantity", digits=(6, 2), readonly=True,
                                 help="This field will accept the available quantity of the product")

    counted_product_qty = fields.Float(string="Actual Quantity", digits=(6, 2),
                                       help="This field will accept the actual quantity of the product")

    difference = fields.Float(string="Difference", digits=(6, 2), store=False, compute="product_difference_calculation",
                              help="This field will accept the difference about the products")

    inventory_id = fields.Many2one(comodel_name='stock.inventory.ept', string="Inventory",
                                   help="This field will accept the Inventory ID")

    # compute(counted_product_qty - available_qty) - store - False
    def product_difference_calculation(self):
        for inventory_products in self:
            inventory_products.difference = inventory_products.counted_product_qty - inventory_products.available_qty
