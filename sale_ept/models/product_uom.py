from odoo import fields, models


class ProductUom(models.Model):
    _name = "product.uom.ept"
    _description = "Product Uom Ept : It will store the information about the Product Uom"

    name = fields.Char(string="Name", required=True, help="This field will accept the name")
    uom_category_id = fields.Many2one(comodel_name='product.uom.category.ept')
