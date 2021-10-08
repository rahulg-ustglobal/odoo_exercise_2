from odoo import fields, models, api


class StockInventory(models.Model):
    _name = "stock.inventory.ept"
    _description = "Stock Inventory Ept : It will store the information about the Stock Inventory"

    name = fields.Char(string="Name", required=True, help="This field will accept the name")

    state = fields.Selection([('Draft', 'Draft'),
                              ('In-Progress', 'In-Progress'),
                              ('Done', 'Done'),
                              ('Cancelled', 'Cancelled')], string="State", default="Draft",
                             help="This field will accept the state of the inventory")

    location_id = fields.Many2one(comodel_name='stock.location.ept', string="Location",
                                  help="This field will accept the Location of the inventory")
    # location where the adjustment is to be done and qty will be calculated for this location

    inventory_date = fields.Date(string="Date", default=fields.Date.today(),
                                 help="This field will accept the Inventory Date with default as today")

    inventory_line_ids = fields.One2many(comodel_name='stock.inventory.line.ept', inverse_name='inventory_id',
                                         string="Inventory Line",
                                         help="This field will accept the Inventory Line")

    def action_start_inventory(self):
        for inventory_line in self.inventory_line_ids:
            inventory_line.available_qty = inventory_line.product_id.with_context(
                {'location_id': self.location_id.id}).product_stock
        self.state = 'In-Progress'

    def action_validate(self):
        inventory_loss_location = self.env['stock.location.ept'].search([('location_type', '=', 'Inventory Loss')],limit=1)
        move_line = []
        move_record = self.env['stock.move.ept']
        for line in self.inventory_line_ids:
            move_vals = {
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'uom_id': line.product_id.uom_id.id,
                'qty_to_deliver': abs(line.difference),
                'qty_delivered': abs(line.difference),
                'state': 'Done'
            }

            if line.difference == 0:
                pass
            elif line.difference < 0:
                move_vals.update({
                    'source_location_id': self.location_id.id,
                    'destination_location_id': inventory_loss_location.id,
                })
                move_line.append(move_vals)
            else:
                move_vals.update({
                    'source_location_id': inventory_loss_location.id,
                    'destination_location_id': self.location_id.id,
                })
                move_line.append(move_vals)
        move_record.create(move_line)
        self.state = 'Done'

    def action_cancelled(self):
        self.state = "Cancelled"
