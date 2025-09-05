from odoo import fields, models


class Property(models.Model):
    _name = 'real.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    postcode = fields.Char(string='Postcode')
    birth_date = fields.Date(string='Birth Date')
    price = fields.Float(string='Price')
    height = fields.Integer(string='Height')
    is_male = fields.Boolean(string='Male', default=False)
    country_id = fields.Selection([('binh thanh','hcm'),('hoan kiem','ha noi')], string='Country', default='hoan kiem')

    # id, crerated_at, updated_at