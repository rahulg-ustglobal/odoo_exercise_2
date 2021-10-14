from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _name = "sale.order.line.ept"
    _description = "Sale Order Line Ept : It will store the information about the Sale Order Line"

    order_no_id = fields.Many2one(comodel_name='sale.order.ept', string="Order No",
                                  help="This field will accept the Order No")
    product_id = fields.Many2one(comodel_name='product.ept', string="Product",
                                 help="This field will accept the Product")
    description = fields.Text(string="Description",
                              help="This field will accept the description in the form of text format")
    quantity = fields.Float(string="Quantity", digits=(6, 2), help="This field will accept the quantity of the product")
    unit_price = fields.Float(string="Unit Price", digits=(6, 2), help="This field will accept the unit price of the "
                                                                       "product")
    state = fields.Selection([('Draft', 'Draft'),
                              ('Confirmed', 'Confirmed'),
                              ('Cancelled', 'Cancelled')],
                             help="This field will accept the state of the product",
                             default="Draft")
    uom_id = fields.Many2one(comodel_name='product.uom.ept', string="UOM ID",
                             help="This field will accept the uom id")

    subtotal_without_tax = fields.Float(string="Subtotal Without Tax", help="This field will accept the subtotal but "
                                                                            "without tax",
                                        compute="subtotal_without_tax_calculation", store=True)

    stock_move_ids = fields.One2many(comodel_name='stock.move.ept', inverse_name='sale_line_id', readonly=True,
                                     help="This field will accept the Stock Move Ids")

    delivered_qty = fields.Float(string="Delivered Qty", compute="delivered_qty_calculation", digits=(6, 2),
                                 store=False,
                                 help="This field will accept the Delivered Qty")

    # It should scan through all the validated delivery orders and calculate the the total delivered quantities

    cancelled_qty = fields.Float(string="Cancelled Qty", compute="cancelled_qty_calculation", store=False,
                                 help="This field will accept the Cancelled Qty")

    # It should scan through all the cancelled delivery orders and calculate the the total delivered quantities

    warehouse_id = fields.Many2one(comodel_name='stock.warehouse.ept',string="Warehouse",
                                   help="This field will accept the Warehouse ID")

    tax_ids = fields.Many2many(comodel_name='account.tax.ept',string="Tax Ids",
                               help="This field will accept the Tax Ids")



    @api.onchange('product_id')
    def product_unit_price(self):
        self.unit_price = self.product_id.cost_price

    @api.depends('quantity', 'unit_price')
    def subtotal_without_tax_calculation(self):
        for line in self:
            line.subtotal_without_tax += line.quantity * line.unit_price

    def delivered_qty_calculation(self):
        for rec in self:
            delivered_qty = 0
            if rec.stock_move_ids:
                for stock_move in rec.stock_move_ids:
                    if stock_move.state == 'Done':
                        delivered_qty += stock_move.qty_delivered
            rec.delivered_qty = delivered_qty

    def cancelled_qty_calculation(self):
        # self.cancelled_qty=0
        for rec in self:
            cancelled_qty = 0
            if rec.stock_move_ids:
                for stock_move in rec.stock_move_ids:
                    if stock_move.state == 'Cancelled':
                        cancelled_qty += stock_move.qty_delivered
            rec.cancelled_qty = cancelled_qty
