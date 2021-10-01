from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _name = "purchase.order.line.ept"
    _description = "Purchase Order Line Ept : It will store the information about the Purchase Order Line"

    purchase_order_id = fields.Many2one(comodel_name='purchase.order.ept', string="Purchase Order",
                                        help="This field will accept the Purchase Order")

    product_id = fields.Many2one(comodel_name='product.ept', string="Product",
                                 help="This field will accept the Product ID")

    name = fields.Text(string='Description', help="This field will accept the Name in the form of Text")
    # Text - based on onchange method of product_id

    quantity = fields.Float(string="Quantity", help="This field will accept the Quantity of the order", digits=(6, 2))

    cost_price = fields.Float(string="Cost Price", help="This field will accept the Cost Price of the product",
                              digits=(6, 2))

    state = fields.Selection([('Draft', 'Draft'),
                              ('Confirmed', 'Confirmed'),
                              ('Done', 'Done'),
                              ('Cancelled', 'Cancelled')], string="State",
                             help="This field will accept the State")

    uom_id = fields.Many2one('product.uom.ept')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order.line.ept')
        return super(PurchaseOrderLine, self).create(vals)

    @api.onchange('product_id')
    def description_auto(self):
        self.name = self.product_id.name
