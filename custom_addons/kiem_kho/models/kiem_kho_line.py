# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KiemKhoLine(models.Model):
    _name = 'kiem.kho.line'
    _description = 'Dòng Kiểm Kho'
    _order = 'create_date desc'

    session_id = fields.Many2one(
        'kiem.kho.session',
        string='Phiên kiểm kho',
        required=True,
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        'product.product',
        string='Sản phẩm'
    )
    barcode = fields.Char(string='Mã vạch', readonly=False)

    # bỏ store=True để tránh conflict khi chỉ có barcode mà chưa chọn product
    product_name = fields.Char(
        string='Tên sản phẩm',
        compute='_compute_product_info'
    )

    scanned_qty = fields.Float('Số lượng quét', default=1.0)

    theoretical_qty = fields.Float(
        'Số lượng lý thuyết',
        compute='_compute_theoretical_qty'
    )
    difference_qty = fields.Float(
        'Chênh lệch',
        compute='_compute_difference',
        store=True
    )

    scan_time = fields.Datetime(
        'Thời gian quét',
        default=fields.Datetime.now
    )
    notes = fields.Text('Ghi chú')

    # ----------------------------------------------------
    # COMPUTE METHODS
    # ----------------------------------------------------
    @api.depends('product_id', 'barcode')
    def _compute_product_info(self):
        """Hiển thị tên sản phẩm hoặc barcode nếu chưa có product."""
        for line in self:
            if line.product_id:
                line.product_name = line.product_id.display_name
            else:
                line.product_name = f"Mã vạch: {line.barcode}" if line.barcode else ""

    @api.depends('product_id', 'session_id.location_id')
    def _compute_theoretical_qty(self):
        """Lấy số lượng tồn kho theo location trong session."""
        for line in self:
            if line.product_id and line.session_id.location_id:
                stock_quant = self.env['stock.quant'].search([
                    ('product_id', '=', line.product_id.id),
                    ('location_id', '=', line.session_id.location_id.id)
                ], limit=1)
                # Odoo 18: quantity thường vẫn dùng được
                line.theoretical_qty = stock_quant.quantity if stock_quant else 0.0
            else:
                line.theoretical_qty = 0.0

    @api.depends('scanned_qty', 'theoretical_qty')
    def _compute_difference(self):
        """Tính chênh lệch giữa quét và lý thuyết."""
        for line in self:
            line.difference_qty = line.scanned_qty - line.theoretical_qty

    # ----------------------------------------------------
    # CREATE OVERRIDE
    # ----------------------------------------------------
    @api.model
    def create(self, vals):
        """Tự động tìm product từ barcode nếu chưa chọn product_id."""
        if vals.get('barcode') and not vals.get('product_id'):
            product = self.env['product.product'].search([
                ('barcode', '=', vals['barcode'])
            ], limit=1)
            if product:
                vals['product_id'] = product.id
        return super(KiemKhoLine, self).create(vals)

    # ----------------------------------------------------
    # CONSTRAINTS
    # ----------------------------------------------------
    @api.constrains('barcode', 'session_id')
    def _check_unique_barcode_per_session(self):
        """Đảm bảo barcode duy nhất trong 1 phiên kiểm kho."""
        for line in self:
            if line.barcode:
                existing = self.search([
                    ('session_id', '=', line.session_id.id),
                    ('barcode', '=', line.barcode),
                    ('id', '!=', line.id)
                ])
                if existing:
                    raise ValidationError(
                        _('Mã vạch "%s" đã tồn tại trong phiên kiểm kho này!') % line.barcode
                    )

    @api.constrains('product_id', 'barcode')
    def _check_product_required(self):
        """Nếu có barcode thì phải tìm thấy product_id hợp lệ."""
        for line in self:
            if line.barcode and not line.product_id:
                raise ValidationError(
                    _('Không tìm thấy sản phẩm cho mã vạch %s!') % line.barcode
                )
