# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class kiem_ke(models.Model):
#     _name = 'kiem_ke.kiem_ke'
#     _description = 'kiem_ke.kiem_ke'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

