from odoo import fields, models, api


class StockMove(models.Model):
    _name = "stock.move.ept"
    _description = "Stock Move Ept : It will store the information about the Stock Move"

    name = fields.Char(string="Description", help="This field will accept the name in the form of description")
    # label - “Description” - “Product Name: Source Location -> Destination Location”

    product_id = fields.Many2one(comodel_name='product.ept', required=True, string="Product",
                                 help="This field will accept the Product ID")

    uom_id = fields.Many2one(comodel_name='product.uom.ept', string="UOM ID", required=True,
                             help="This field will accept the UOM ID")

    source_location_id = fields.Many2one(comodel_name='stock.location.ept', string="Source Location",
                                         help="This field will accept the Source Location")

    destination_location_id = fields.Many2one(comodel_name='stock.location.ept', string="Destination Location",
                                              help="This field will accept the Destination Location")

    qty_to_deliver = fields.Float(string="Demand", readonly=True, help="This field will accept the quantity to deliver")

    qty_delivered = fields.Float(string="Delivery", digits=(6, 2),
                                 help="This field will accept the Quantity Delivered in the form of float")

    state = fields.Selection([('Draft', 'Draft'),
                              ('Done', 'Done'),
                              ('Cancelled', 'Cancelled')], default="Draft", string="State",
                             help="This field will accept the State")

    sale_line_id = fields.Many2one(comodel_name='sale.order.line.ept', string="Sale Line",
                                   help="This field will accept the Sale Line")

    purchase_line_id = fields.Many2one(comodel_name='purchase.order.line.ept', string="Purchase Line",
                                       help="this field will accept the Purchase Line")

    stock_inventory_id = fields.Many2one(comodel_name='stock.inventory.ept', string="Stock Inventory",
                                         help="This field will accept the Stock Inventory")

    picking_id = fields.Many2one(comodel_name='stock.picking.ept', string="Picking",
                                 help="This field will accept the Picking ID")