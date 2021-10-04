from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _name = "sale.order.ept"
    _description = "Sale Order Ept : It will store the information about the Sale Order"

    name = fields.Char(string="Order No", required=True, help="This field will accept the order no of the product")
    partner_id = fields.Many2one(comodel_name='res.partner.ept', string="Partner",
                                 help="This field will accept the Partner ID", required=True)

    partner_invoice_id = fields.Many2one(comodel_name='res.partner.ept', string="Partner Invoice Address",
                                         help="This field will accept the Partner Invoice Address")

    partner_shipping_id = fields.Many2one(comodel_name='res.partner.ept', string="Partner Shipping Address",
                                          help="This field will accept the Partner Shipping Address")

    sale_order_date = fields.Date(string="Sale Order Date", required=True, help="This field will accept the sale order "
                                                                                "date of the product")

    order_line_ids = fields.One2many(comodel_name='sale.order.line.ept', inverse_name='order_no_id',
                                     string="Order Line", help="This field will accept the Order Line")

    salesperson_id = fields.Many2one(comodel_name='res.users', string="Salesperson",
                                     help="This field will accept the Salesperson")

    state = fields.Selection([('Draft', 'Draft'),
                              ('Confirmed', 'Confirmed'),
                              ('Done', 'Done'),
                              ('Cancelled', 'Cancelled')], default="Draft",
                             help="This field will show the status of the sale order")

    total_weight = fields.Float(string="Total Weight", digits=(6, 2), help="This field will accept the total weight",
                                compute="total_weight_calculation", store=False)

    total_volume = fields.Float(string="Total Volume", digits=(6, 2), help="This field will accept the total volume",
                                compute="total_volume_calculation", store=False)

    order_total = fields.Float(string="Order Total", digits=(6, 2), help="This field will accept the order total",
                               compute="order_total_calculation", store=True)

    lead_id = fields.Many2one(comodel_name='crm.lead.ept', string="Lead", help="This field will accept the lead")

    warehouse_id = fields.Many2one(comodel_name='stock.warehouse.ept', string="Warehouse",
                                   help="This field will accept the Warehouse ID")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.ept')
        return super(SaleOrder, self).create(vals)

    @api.depends('order_line_ids')
    def total_weight_calculation(self):
        for orders in self:
            weight = 0
            for order_line in orders.order_line_ids:
                weight += order_line.quantity * order_line.product_id.weight
            orders.total_weight = weight

    @api.depends('order_line_ids')
    def total_volume_calculation(self):
        for orders in self:
            volume = 0
            for order_line in orders.order_line_ids:
                volume += order_line.quantity * order_line.product_id.volume
            orders.total_volume = volume

    @api.depends('order_line_ids')
    def order_total_calculation(self):
        for orders in self:
            r_orders = 0
            for order_line in orders.order_line_ids:
                r_orders += order_line.subtotal_without_tax
            orders.order_total = r_orders

    @api.onchange('partner_id')
    def customer_auto_address_type(self):
        if self.partner_id:
            invoice_address = self.env["res.partner.ept"].search(
                [('address_type', '=', 'Invoice'), ('parent_id', '=', self.partner_id.id)], limit=1)
            self.partner_invoice_id = invoice_address
            shipping_address = self.env["res.partner.ept"].search(
                [('address_type', '=', 'Shipping'), ('parent_id', '=', self.partner_id.id)], limit=1)
            self.partner_shipping_id = shipping_address

    # Button function with name as a action_confirm
    def action_confirm_sale(self):
        picking_vals = self.prepare_picking()
        stock_picking = self.env['stock.picking.ept'].create(picking_vals)
        move_vals = self.prepare_move(stock_picking)
        self.env['stock.move.ept'].create(move_vals)
        self.state = "Confirmed"

    def prepare_picking(self):
        picking_vals = {
            'partner_id': self.partner_id.id,
            'sale_order_id': self.id,
            'transaction_type': 'Out'
        }

        return picking_vals

    def prepare_move(self, stock_picking):
        move_lines_vals = []
        customer_location = self.env['stock.location.ept'].search([('location_type', '=', 'Customer')], limit=1)
        if not customer_location:
            raise ValidationError("Location is not found please try again !!!")
        else:
            for order_line in self.order_line_ids:
                move_values = {
                    'product_id': order_line.product_id.id,
                    'name': "Product Name " + order_line.product_id.name,
                    'uom_id': order_line.uom_id.id,
                    'qty_to_deliver': order_line.quantity,
                    'sale_line_id': order_line.id,
                    'picking_id': stock_picking.id,
                    'source_location_id': self.warehouse_id.stock_location_id.id,
                    'destination_location_id': customer_location.id
                }

                move_lines_vals.append(move_values)
            return move_lines_vals
