from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class SaleOrderExtended(models.Model):
    _inherit = 'sale.order'

    lead_id = fields.Many2one(comodel_name='crm.lead', string="New Opportunity")

    def action_confirm(self):
        # product = self.env.ref('sale_order_extended.product_data')
        # self.order_line = [(0, 0,
        #                     {
        #                         'product_id': product.id,
        #                         'product_uom_qty': 1,
        #                         'price_unit': product.price,
        #                     })]

        return super(SaleOrderExtended, self).action_confirm()

    def manage_deposits_btn(self):
        for order_line in self.order_line:
            if order_line.product_id.deposit_product_id:
                if order_line.child_ids:
                    order_line.child_ids.product_uom_qty = order_line.product_uom_qty * order_line.product_id.deposit_product_qty
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

    def manage_products_btn(self):
        for order_line in self.order_line:
            sale_order_lines = self.order_line.search(
                [('product_id', '=', order_line.product_id.id), ('order_id', '!=', self.id)])
        move_ids = sale_order_lines.move_ids

        move_ids = sale_order_lines.move_ids.filtered(
            lambda move: move.forecast_availability > 0 and move.state not in ['done', 'cancel'])

        sale_order_line_ids = move_ids.sale_line_id.ids

        action = {
            'name': _('Tree of Products'),
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', sale_order_line_ids)],
            'view_mode': 'tree',
            'res_model': 'sale.order.line',
        }
        return action

    def confirm_validate_btn(self):
        pass
