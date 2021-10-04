from odoo import fields, models, api


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

    # Button function with name as a action_validate
    def action_validate(self):
        for convert_state in self.move_ids:
            convert_state.state = 'Done'
        self.state = "Done"

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('stock.picking.ept')
        return super(StockPicking, self).create(vals)
