# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class WmsScannerController(http.Controller):
    @http.route('/wms/scanner', type='http', auth='user', website=False)
    def scanner(self, **kwargs):
        return request.render('wms_barcode_scanner.scanner_page', {})