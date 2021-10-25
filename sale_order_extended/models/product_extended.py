from odoo import fields, models, api


class ProductProductExtended(models.Model):
    _inherit = "product.product"

    deposit_product_id = fields.Many2one(comodel_name='product.product', string="Deposit Product Id",
                                         help="This field will accept the Deposit Product")
    deposit_product_qty = fields.Integer(string="Deposit Product Qty",
                                         help="This field will accept the Deposit Product Qty")
