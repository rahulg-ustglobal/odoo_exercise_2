from odoo import fields, models, api


class SaleOrderExtended(models.Model):
    _inherit = 'sale.order'
    _description = "Sale Order : It will store the information about the Sale Order"

    # lead_id = fields.Many2one(comodel_name='crm.lead', string="Lead")
