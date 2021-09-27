from odoo import fields, models


class ProductCategory(models.Model):
    _name = "product.category.ept"
    _description = "Product Category Ept : It will store the information about the Product Category"

    name = fields.Char(String="Name", required=True, help="This field will store the information about name")
    parent_id = fields.Many2one(comodel_name='product.category.ept')
