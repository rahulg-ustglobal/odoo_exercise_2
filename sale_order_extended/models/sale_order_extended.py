from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError



class SaleOrderExtended(models.Model):
    _inherit = 'sale.order'

    lead_id = fields.Many2one(comodel_name='crm.lead', string="New Opportunity")

    def action_confirm(self):
        product = self.env.ref('sale_order_extended.product_data')

        # order_line = self.env['sale.order.line'].create(
        #     {
        #         'product_id': product.id,
        #         'product_uom_qty': 1,
        #         'price_unit': product.price,
        #     })

        self.order_line = [(0, 0,
                            {
                                'product_id': product.id,
                                'product_uom_qty': 1,
                                'price_unit': product.price,
                            })]

        return super(SaleOrderExtended, self).action_confirm()

    def manage_deposits_btn(self):
        # for order_line in self.order_line:
        #     if order_line.product_id.deposit_product_id:
        #         deposit_product = order_line.product_id.deposit_product_id
        #         sale_order_line = self.env['sale.order.line'].write({
        #                                     'product_id': deposit_product.id,
        #                                     'product_uom_qty': order_line.product_uom_qty * order_line.product_id.deposit_product_qty,
        #                                     'price_unit': deposit_product.lst_price,
        #                                     'product_uom': deposit_product.uom_id
        #         })
        #      else:
        #           raise ValidationError("You can't create deposit product one more time..!!!")

        for order_line in self.order_line:
            if order_line.product_id.deposit_product_id:
                if order_line.child_id:
                    order_line.child_id.product_uom_qty = order_line.product_uom_qty * order_line.product_id.deposit_product_qty
                else:
                    deposit_product = order_line.product_id.deposit_product_id
                    sale_order_line_list = [(0, 0, {
                        'product_id': deposit_product.id,
                        'product_uom_qty': order_line.product_uom_qty * order_line.product_id.deposit_product_qty,
                        'price_unit': deposit_product.lst_price,
                        'product_uom': deposit_product.uom_id.id,
                        'parent_id': order_line.id,
                    })]
                    self.order_line = sale_order_line_list

    def get_products_btn(self):
        for order_line in self.order_line:
            current_products = order_line.product_id
            other_sale_order_lines = self.env['sale.order'].search(['current_product','!=',''])
