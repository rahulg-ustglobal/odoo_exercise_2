from odoo import fields, models


class AccountTax(models.Model):
    _name = "account.tax.ept"
    _description = "Account Tax Ept : It will store the information about the Account Tax"

    name = fields.Char(string="Name", required=True, help="This field will accept the name")
    tax_use = fields.Selection([('None', 'None'),
                                ('Sales', 'Sales'),
                                ('Purchase', 'Purchase')], string="Tax Use",
                               help="This field will accept the Tax Use")

    tax_value = fields.Float(string="Amount", digits=(6, 2),
                             help="This field will accept the Tax Value")

    tax_amount_type = fields.Selection([('Percentage', 'Percentage'), ('Fixed', 'Fixed')],
                                       string="Tax Amount Type", default="Percentage")


