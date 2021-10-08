from odoo import fields, models, api


class ProductStockUpdate(models.Model):
    _name = "product.stock.update.ept"
    _description = "Product Stock Update Ept : It will store the information about the Product Stock Update"

    location_id = fields.Many2one(comodel_name='stock.location.ept', string="Location",
                                  help="This field will accept the Location ID")
    # add onchange to find the current stock
    available_stock = fields.Float(string="Available Stock", digits=(6, 2),
                                   help="This field will accept the Available Stock")
    # which is there in the system

    counted_qty = fields.Float(string="Counted Qty", digits=(6, 2),
                               help="This field will accept the Counted Qty")

    difference_qty = fields.Float(string="Difference Qty", digits=(6, 2), compute='difference_calculation',
                                  store=False, help="This field will accept the Difference Qty")

    # compute(counted - current) - store - False

    @api.onchange('location_id')
    def _onchange_selected_location(self):
        if self.location_id:
            product = self.env['product.ept'].browse(self._context.get('active_id'))
            self.available_stock = product.with_context(location_id=self.location_id.id).product_stock

    def action_update_stock(self):
        product = self.env['product.ept'].browse(self._context.get('active_id'))
        inventory_lines = []
        inventory_line_vals = {
            'product_id': product.id,
            'available_qty': self.available_stock,
            'counted_product_qty': self.counted_qty
        }
        inventory_lines.append((0, 0, inventory_line_vals))
        inventory_record = self.env['stock.inventory.ept'].create(
            {
                'location_id': self.location_id.id,
                'inventory_line_ids': inventory_lines,
                'name': 'Inv Adj Of '
            }
        )
        inventory_record.action_validate()

    def difference_calculation(self):
        self.difference_qty = 0
        for quantity in self:
            quantity.difference_qty = quantity.counted_qty - quantity.available_stock
