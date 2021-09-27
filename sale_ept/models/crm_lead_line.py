from odoo import fields, models, api


class CrmLeadLine(models.Model):
    _name = "crm.lead.line.ept"
    _description = "Crm Lead Line Ept : It will store the information about the Crm Lead Line"

    product_id = fields.Many2one(comodel_name='product.ept')
    name = fields.Text(string='Description', help="This field will accept the description of the product")
    expected_sell_qty = fields.Float(string="Expected Salary Quantity", help="This field will accept the "
                                                                             "expected salary quantity")
    uom_id = fields.Many2one(comodel_name='product.uom.ept')
    lead_id = fields.Many2one(comodel_name='crm.lead.ept')

    @api.onchange('product_id')
    def product_description(self):
        self.name = self.product_id.name
