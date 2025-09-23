# -*- coding: utf-8 -*-
# from odoo import http


# class KiemKe(http.Controller):
#     @http.route('/kiem_ke/kiem_ke', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kiem_ke/kiem_ke/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kiem_ke.listing', {
#             'root': '/kiem_ke/kiem_ke',
#             'objects': http.request.env['kiem_ke.kiem_ke'].search([]),
#         })

#     @http.route('/kiem_ke/kiem_ke/objects/<model("kiem_ke.kiem_ke"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kiem_ke.object', {
#             'object': obj
#         })

