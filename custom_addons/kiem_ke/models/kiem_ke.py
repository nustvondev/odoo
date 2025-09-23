from odoo import fields, models

class KiemKe(models.Model):
    _name = "kiem_ke.scanned_item"
    _description = "Scanned Item"
    _order = "scanned_at desc"

    name = fields.Char(string="Item Name", required=True)
    barcode = fields.Char(string="Barcode", required=True, index=True, unique=True)
    scanned_at = fields.Datetime(string="Scanned At", default=fields.Datetime.now)
    scanned_by = fields.Char(string="Scanned By", required=True)