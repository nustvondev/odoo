from odoo import  models, fields
from datetime import timedelta

class RealEstate(models.Model):
    _name = 'realestate.properties'
    _description = 'Here Real Estate information is stored.'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    photo = fields.Binary(string="Photo", attachment=True)

    post_code = fields.Char(string='Post Code', required=True)
    expected_price = fields.Integer(string='Expected price', required=True)
    bedrooms = fields.Integer(string='Bedrooms', default=3, required=True)
    facades = fields.Integer(string='Facades')
    garden = fields.Boolean()
    garden_orient = fields.Selection([('north', 'North'), ('south', 'South'),
        ('east', 'East'), ('west', 'West')], string='Garden orientation')
    garden_area = fields.Float(string='Garden Area(sqm)')

    available_from = fields.Date(string='Available from', default= fields.datetime.now(), copy=False)
    deadline = fields.Date(string='Deadline', inverse="_inverse_total")
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False, compute="_compute_total")
    living_area = fields.Float(string='Living area(sqm)', required=True, default=1000)
    garage = fields.Boolean()
    status = fields.Selection([("new", "New"), ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("canceled", "Canceled")],
        copy=False, default="new")
    active = fields.Boolean(default=True)