from odoo import fields, models, api


class SaleOrderExtended(models.Model):
    _inherit = 'sale.order'

    lead_id = fields.Many2one(comodel_name='crm.lead', string="New Opportunity")

    def action_confirm(self):
        product = self.env.ref('sale_order_extended.product_data')

        self.order_line = [(0, 0,
                            {
                                'product_id': product.id,
                                'product_uom_qty': 1,
                                'price_unit': product.price,
                            })]
        return super(SaleOrderExtended, self).action_confirm()
