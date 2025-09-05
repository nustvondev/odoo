# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class KiemKhoSession(models.Model):
    _name = 'kiem.kho.session'
    _description = 'Phiên Kiểm Kho'
    _order = 'create_date desc'

    name = fields.Char('Tên phiên', required=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('in_progress', 'Đang thực hiện'),
        ('done', 'Hoàn thành'),
        ('cancelled', 'Hủy bỏ')
    ], string='Trạng thái', default='draft', tracking=True)
    user_id = fields.Many2one('res.users', string='Người thực hiện', 
                             default=lambda self: self.env.user, required=True)
    location_id = fields.Many2one('stock.location', string='Kho kiểm', required=True)
    start_date = fields.Datetime('Ngày bắt đầu', default=fields.Datetime.now)
    end_date = fields.Datetime('Ngày kết thúc')
    
    line_ids = fields.One2many('kiem.kho.line', 'session_id', string='Danh sách sản phẩm')
    total_lines = fields.Integer('Tổng số dòng', compute='_compute_total_lines')
    
    notes = fields.Text('Ghi chú')
    
    @api.depends('line_ids')
    def _compute_total_lines(self):
        for record in self:
            record.total_lines = len(record.line_ids)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('kiem.kho.session') or _('New')
        return super(KiemKhoSession, self).create(vals)
    
    def action_start(self):
        """Bắt đầu phiên kiểm kho"""
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Chỉ có thể bắt đầu phiên ở trạng thái nháp!'))
        self.state = 'in_progress'
        self.start_date = fields.Datetime.now()
    
    def action_finish(self):
        """Hoàn thành phiên kiểm kho"""
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('Chỉ có thể hoàn thành phiên đang thực hiện!'))
        self.state = 'done'
        self.end_date = fields.Datetime.now()
    
    def action_cancel(self):
        """Hủy phiên kiểm kho"""
        self.ensure_one()
        if self.state == 'done':
            raise UserError(_('Không thể hủy phiên đã hoàn thành!'))
        self.state = 'cancelled'
    
    def action_reset_to_draft(self):
        """Đặt lại về trạng thái nháp"""
        self.ensure_one()
        self.state = 'draft'
        self.start_date = False
        self.end_date = False
