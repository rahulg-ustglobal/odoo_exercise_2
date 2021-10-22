from odoo import fields, models, api


class CrmLeadExtended(models.Model):
    _inherit = 'crm.lead'

    def action_new_quotation(self):
        quotation = super(CrmLeadExtended,self).action_new_quotation()
        category_lead = self.env.ref('sale_order_extended.tag_from_lead')
        quotation['context']['default_tag_ids'].extend(category_lead.ids)
        quotation['context']['default_lead_id'] = self.id
        return quotation

