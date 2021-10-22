from odoo import fields, models, api


class SaleOrderExtended(models.Model):
    _inherit = 'sale.order'

    lead_id = fields.Many2one(comodel_name='crm.lead', string="Opportunity Lead")

