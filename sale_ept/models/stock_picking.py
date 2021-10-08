from odoo import fields, models, api

from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _name = "stock.picking.ept"
    _description = "Stock Picking Ept : It will store the information about the Stock Picking"

    name = fields.Char(string="Name", help="This field will accept the name")
    # Generate the sequence and should automatically be generated when record is created

    partner_id = fields.Many2one(comodel_name='res.partner.ept', string="Partner",
                                 help="This field will accept the Partner ID")
    # here the shipping partner of sales order should be set or vendor information should be set during purchase order

    state = fields.Selection([('Draft', 'Draft'),
                              ('Done', 'Done'),
                              ('Cancelled', 'Cancelled')], default="Draft",
                             string="State", help="This field will accept the state")
    sale_order_id = fields.Many2one(comodel_name='sale.order.ept', string="Sale Order",
                                    help="This field will accept the Sale Order ID")

    purchase_order_id = fields.Many2one(comodel_name='purchase.order.ept', string="Purchase Order",
                                        help="This field will accept the Purchase Order ID")

    transaction_type = fields.Selection([('In', 'In'), ('Out', 'Out')], string="Transaction Type",
                                        help="This field will accept the Transaction Type")

    move_ids = fields.One2many(comodel_name='stock.move.ept', inverse_name='picking_id', string="Move",
                               help="This field will accept the Move IDs")

    transaction_date = fields.Date(string="Transaction Date", default=fields.date.today(),
                                   help="This field will accept the Transaction Date and It will also"
                                        "accept the default date as a today")

    back_order_id = fields.Many2one(comodel_name='stock.picking.ept', string="Back Order ID",
                                    help="This field will accept the Back Order ID")

    # Button function with name as a action_validate
    def action_validate(self):
        # for convert_state in self.move_ids:
        #     convert_state.state = 'Done'
        # self.state = "Done"
        move_lines = []
        for line in self.move_ids:
            line.state = 'Done'
            check_done_qty = any(qty_final.qty_delivered > 0 for qty_final in self.move_ids)
            if not check_done_qty:
                raise ValidationError("Please you have to enter some numbers")
            else:
                if line.qty_delivered != line.qty_to_deliver:
                    move_vals = {
                        'name': line.name,
                        'product_id': line.product_id.id,
                        'uom_id': line.uom_id.id,
                        'source_location_id': line.source_location_id.id,
                        'destination_location_id': line.destination_location_id.id,
                        'qty_to_deliver': line.qty_to_deliver - line.qty_delivered,
                        'sale_line_id': line.sale_line_id.id,
                        'purchase_line_id': line.purchase_line_id.id
                    }
                    line['qty_to_deliver'] = line.qty_delivered
                    move_lines.append((0, 0, move_vals))
        if move_lines:

            created_order = self.env['stock.picking.ept'].create(
                {
                    'name': self.name + '/' + self.transaction_type,
                    'partner_id': self.partner_id.id,
                    'back_order_id': self.id,
                    'transaction_type': self.transaction_type,
                    'sale_order_id': self.sale_order_id.id,
                    'purchase_order_id': self.purchase_order_id.id,
                    'move_ids': move_lines
                }
            )
        else:
            if self.transaction_type == 'Out':
                self.sale_order_id.state = "Done"
                for line in self.sale_order_id.order_line_ids:
                    line.state = 'Done'
            else:
                self.purchase_order_id.state = "Done"
                for line in self.purchase_order_id.purchase_order_line_ids:
                    line.state = 'Done'

        self.state = 'Done'

    def action_cancelled_sale(self):
        for move_lines in self.move_ids:
            move_lines.state = "Cancelled"
            move_lines.qty_delivered = move_lines.qty_to_deliver
        self.state="Cancelled"

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('stock.picking.ept')
        return super(StockPicking, self).create(vals)
