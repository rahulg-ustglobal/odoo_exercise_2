from odoo import fields, models, api


class SaleOrderLineExtended(models.Model):
    _inherit = "sale.order.line"

    parent_id = fields.Many2one(comodel_name='sale.order.line')  # order_line
    child_id = fields.One2many('sale.order.line', 'parent_id')  # deposit_product
