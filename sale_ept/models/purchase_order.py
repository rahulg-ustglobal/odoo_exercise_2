from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _name = "purchase.order.ept"
    _description = "Purchase Order Ept : It will store the information about the Purchase Order"

    warehouse_id = fields.Many2one(comodel_name='stock.warehouse.ept', string="Warehouse",
                                   help="This field will accept the Warehouse ID")

    partner_id = fields.Many2one(comodel_name='res.partner.ept', string="Partner",
                                 help="This field will accept the Partner ID")
    # Vendor / Supplier

    order_date = fields.Date(string="Order Date", help="This field will accept the Order Date")

    name = fields.Char(string="Name", help="This field will accept the Name")

    state = fields.Selection([('Draft', 'Draft'),
                              ('Confirm', 'Confirm'),
                              ('Done', 'Done'),
                              ('Cancelled', 'Cancelled')], string="State",
                             help="This field will accept the State")

    purchase_order_line_ids = fields.One2many(comodel_name='purchase.order.line.ept', inverse_name='purchase_order_id',
                                              string="Purchase Order Line",
                                              help="This field will accept the Purchase Order Line IDS")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order.ept')
        return super(PurchaseOrder, self).create(vals)

    def prepare_picking(self):
        picking = {
            'partner_id': self.partner_id.id,
            'purchase_order_id': self.id,
            'transaction_type': 'In'
        }
        return picking

    def prepare_move(self, stock_picking):
        move_lines_vals = []
        vendor_location = self.env['stock.location.ept'].search([('location_type', '=', 'Vendor')],limit=1)
        if not vendor_location:
            raise ValidationError("Location is not found please try again !!!")
        else:
            for purchase_order_line in self.purchase_order_line_ids:
                stock_move = {
                    'product_id': purchase_order_line.product_id.id,
                    'uom_id': purchase_order_line.uom_id.id,
                    'qty_to_deliver': purchase_order_line.quantity,
                    'purchase_line_id': purchase_order_line.id,
                    'picking_id': stock_picking.id,
                    # Set Location
                    'source_location_id': vendor_location.id,
                    'destination_location_id': self.warehouse_id.stock_location_id.id
                }

                move_lines_vals.append(stock_move)
            return move_lines_vals

    # Button function with name as a action_confirm
    def action_confirm_purchase(self):
        picking_vals = self.prepare_picking()
        stock_picking = self.env['stock.picking.ept'].create(picking_vals)
        move_vals = self.prepare_move(stock_picking)
        stock_move = self.env['stock.move.ept'].create(move_vals)
        self.state = "Confirm"
