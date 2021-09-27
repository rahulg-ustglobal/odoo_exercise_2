from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _name = "sale.order.line.ept"
    _description = "Sale Order Line Ept : It will store the information about the Sale Order Line"

    order_no_id = fields.Many2one('sale.order.ept')
    product_id = fields.Many2one('product.ept')
    description = fields.Text(string="Description", help="This field will accept the description in the form of text format")
    quantity = fields.Float(string="Quantity", digits=(6, 2), help="This field will accept the quantity of the product")
    unit_price = fields.Float(string="Unit Price", digits=(6, 2), help="This field will accept the unit price of the "
                                                                       "product")
    state = fields.Selection([('Draft', 'Draft'),
                              ('Confirmed', 'Confirmed'),
                              ('Cancelled', 'Cancelled')], help="This field will accept the state of the product")
    uom_id = fields.Many2one('product.uom.ept')

    subtotal_without_tax = fields.Float(string="Subtotal Without Tax", help="This field will accept the subtotal but "
                                                                            "without tax",
                                        compute="subtotal_without_tax_calculation",store=True)

    @api.onchange('product_id')
    def product_unit_price(self):
        self.unit_price = self.product_id.cost_price

    @api.depends('quantity', 'unit_price')
    def subtotal_without_tax_calculation(self):
        self.subtotal_without_tax += self.quantity * self.unit_price
