from odoo import models, fields, api

class ScannedItem(models.Model):
    _name = 'scanned.item'
    _description = 'Scanned Items'
    _order = 'scan_time desc'

    barcode = fields.Char(string='Barcode', required=True)
    scan_time = fields.Datetime(string='Scan Time', default=fields.Datetime.now)
    product_id = fields.Many2one('product.product', string='Product')
    processed = fields.Boolean(string='Processed', default=False)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)

    @api.model
    def create(self, vals):
        # Try to find product with this barcode
        if 'barcode' in vals:
            product = self.env['product.product'].search([('barcode', '=', vals['barcode'])], limit=1)
            if product:
                vals['product_id'] = product.id
        return super(ScannedItem, self).create(vals)