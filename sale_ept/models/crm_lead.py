from odoo import fields, models


class CrmLead(models.Model):
    _name = "crm.lead.ept"
    _description = "Crm Lead Ept : It will store the information about the Crm Lead"

    name = fields.Char(string="Name", required=True, help="This field will accept the name")
    team_leader = fields.Many2one(comodel_name="res.users")

    partner_id = fields.Many2one(comodel_name='res.partner.ept')
    # order_ids = fields.One2many(inverse_name='sale.order.line.ept', 'order_no_id')
    # 'keep it readonly, record will not be generated from here, it is just for the display purpose'
    team_id = fields.Many2one(comodel_name='crm.team.ept')
    user_id = fields.Many2one(comodel_name='res.users')
    # lead_line_ids = fields.One2many('crm.lead.line.ept', 'lead_id')
    state = fields.Selection([('New', 'New'),
                              ('Qualified', 'Qualified'),
                              ('Proposition', 'Proposition'),
                              ('Won', 'Won'),
                              ('Lost', 'Lost')])
    won_date = fields.Date(string="Won Date", help="This field will accept the won date")
    lost_reason = fields.Text(string="Lost Reason", help="This field will accept the Lost reason in "
                                                         "the form of text format")
    next_followup_date = fields.Date(string="Next Followup Date", help="This field will accept "
                                                                       "the next followup date")
    partner_name = fields.Char(string="Partner Name", help="This field will accept the partner name")
    partner_email = fields.Char(string="Partner Email", help="This field will accept the partner email")
    partner_country_id = fields.Many2one(comodel_name='res.country.ept')
    partner_state_id = fields.Many2one(comodel_name='res.state.ept')
    partner_city_id = fields.Many2one(comodel_name='res.city.ept')

    # Button function with name as a action_new
    def action_new(self):
        self.state = "New"

    # Button function with name as a action_qualified
    def action_qualified(self):
        self.state = "Qualified"

    # Button function with name as a action_proposition
    def action_proposition(self):
        self.state = "Proposition"

    # Button function with name as a action_won_date
    def action_won_date(self):
        self.state = "Won"
        self.won_date = fields.date.today()

    # Button function with name as a action_lost_reason
    def action_lost_reason(self):
        self.state = "Lost"
        self.lost_reason = 'Not Interested'

    # Button function with name as a action_lost_reason
    def action_generate_sale_quotation(self):
        self.state = "Generate Sale Quotation"
