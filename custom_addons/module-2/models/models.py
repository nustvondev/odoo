# -*- coding: utf-8 -*-
from email.policy import default

from odoo import models, fields, api


class Player(models.Model):
    _name = 'hoanh.player'
    _description = 'Player model created by Hoanh'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', required=True)
    country = fields.Char(string='Country', required=True)
    image = fields.Binary(string='Image', required=True)
    gender = fields.Selection([('male', 'Male'), ('femele', 'Female')], string='Gender', default='male')
    dob = fields.Date(string='Date of Birth', required=True)
    height = fields.Float(string='Height', required=True)
    weight = fields.Float(string='Weight', required=True)
