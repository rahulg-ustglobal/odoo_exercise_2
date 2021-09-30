from odoo import fields, models, api
from openerp.exceptions import ValidationError


class CrmLead(models.Model):
    _name = "crm.lead.ept"
    _description = "Crm Lead Ept : It will store the information about the Crm Lead"

    _rec_name = 'partner_id'
    # team_leader = fields.Many2one(comodel_name="res.users", string="Team Leader",
    #                               help="This field will accept the Team Leader")

    partner_id = fields.Many2one(comodel_name='res.partner.ept', string="Partner ID",
                                 help="This field will accept the partner id")
    order_ids = fields.One2many(comodel_name='sale.order.ept', inverse_name='lead_id', string="Order ID",
                                help="This field will accept the order ids", readonly=True)
    # 'keep it readonly, record will not be generated from here, it is just for the display purpose'
    team_id = fields.Many2one(comodel_name='crm.team.ept', string="Team",
                              help="This field will accept the team ID")
    user_id = fields.Many2one(comodel_name='res.users', string="Salesperson",
                              help="This field will accept the user ID")
    lead_line_ids = fields.One2many(comodel_name='crm.lead.line.ept', inverse_name='lead_id', string="Lead Lines",
                                    help="This field will accept the lead lines")
    state = fields.Selection([('New', 'New'),
                              ('Qualified', 'Qualified'),
                              ('Proposition', 'Proposition'),
                              ('Won', 'Won'),
                              ('Lost', 'Lost')], default='New', help="This field will accept the "
                                                                     "state of the order")
    won_date = fields.Date(string="Won Date", help="This field will accept the won date")
    lost_reason = fields.Text(string="Lost Reason", help="This field will accept the Lost reason in "
                                                         "the form of text format")
    next_followup_date = fields.Date(string="Next Followup Date", help="This field will accept "
                                                                       "the next followup date")
    partner_name = fields.Char(string="Partner Name", help="This field will accept the partner name")
    partner_email = fields.Char(string="Partner Email", help="This field will accept the partner email")
    partner_country_id = fields.Many2one(comodel_name='res.country.ept', string="Partner Country",
                                         help="This field will accept the Partner Country")
    partner_state_id = fields.Many2one(comodel_name='res.state.ept', string="Partner State",
                                       help="This field will accept the Partner State ID")
    partner_city_id = fields.Many2one(comodel_name='res.city.ept', string="Partner City",
                                      help="This field will accept the Partner City ID")

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
        self.won_date = fields.Date.today()

    # Button function with name as a action_lost_reason
    def action_lost_reason(self):
        self.state = "Lost"
        self.lost_reason = 'Not Interested'

    # Sale order preparation Method with values in the form of dictionary
    def prepare_sale_order(self):
        prepare = {
            'name': "Order of " + self.partner_id.name,
            'partner_id': self.partner_id.id,
            'sale_order_date': fields.Date.today(),
            'lead_id': self.id
        }
        return prepare

    # Button function with name as a action_lost_reason
    def action_generate_sale_quotation(self):
        if self.partner_id:
            create_vals = self.prepare_sale_order()
            sale_order = self.env['sale.order.ept'].create(create_vals)
            for lead_line in self.lead_line_ids:
                lead_line_values = {
                    'order_no_id': sale_order.id,
                    'product_id': lead_line.product_id.id,
                    'description': lead_line.name,
                    'quantity': lead_line.expected_sell_qty,
                    'unit_price': lead_line.product_id.sale_price,
                }
                self.env['sale.order.line.ept'].create(lead_line_values)
        else:
            raise ValidationError("You have to create the customer first !!!")

    # Button function with name as a action_create_customer
    def action_create_customer(self):
        partner = self.env['res.partner.ept'].create({
            'name': self.partner_name,
            'email': self.partner_email,
            'country_id': self.partner_country_id.id,
            'state_id': self.partner_state_id.id,
            'city_id': self.partner_city_id.id
        })
        self.partner_id = partner.id
