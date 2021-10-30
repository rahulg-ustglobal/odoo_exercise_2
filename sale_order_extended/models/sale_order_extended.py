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

        # move_ids = sale_order_lines.move_ids.filtered(
        #     lambda move: move.forecast_availability > 0 and move.state not in ['done', 'cancel'])
        
        for moves in move_ids:
            lambda move: move.forecast_availability > 0 and move.state not in ['done', 'cancel']

        sale_order_line_ids = move_ids.sale_line_id.ids

        action = {
            'name': _('Tree of Products'),
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', sale_order_line_ids)],
            'view_mode': 'tree',
            'res_model': 'sale.order.line',
        }
        return action

    def _confirm_validate_btn(self):
        for order in self:
            if any(expense_policy not in [False, 'no'] for expense_policy in
                   order.order_line.mapped('product_id.expense_policy')):
                if not order.analytic_account_id:
                    order._create_analytic_account()
        return True

    def confirm_validate_btn(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._confirm_validate_btn()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True
