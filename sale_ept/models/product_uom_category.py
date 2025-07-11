from odoo import fields, models


class ProductUomCategory(models.Model):
    _name = "product.uom.category.ept"
    _description = "Product Uom Category Ept : It will store the information about the Product Uom Category"

    name = fields.Char(string="Name", required=True, help="This field will accept the name")
    uom_ids = fields.One2many(comodel_name='product.uom.ept', inverse_name='uom_category_id', string="UOM",
                              help="This field will accept the UOM IDS")
