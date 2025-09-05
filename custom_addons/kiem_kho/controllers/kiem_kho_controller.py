# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json


class KiemKhoController(http.Controller):

    @http.route('/kiem_kho/scanner/<int:session_id>', type='http', auth='user', website=True)
    def scanner_interface(self, session_id, **kwargs):
        """Giao diện quét barcode"""
        session = request.env['kiem.kho.session'].browse(session_id)
        if not session.exists():
            return request.redirect('/web')
        
        # Lấy danh sách items đã quét
        lines = session.line_ids.sorted('scan_time', reverse=True)
        
        return request.render('kiem_kho.scanner_template', {
            'session': session,
            'lines': lines,
            'session_id': session_id
        })
    
    @http.route('/kiem_kho/add_item', type='json', auth='user', methods=['POST'])
    def add_item(self, session_id, barcode, **kwargs):
        """API thêm item qua barcode"""
        try:
            session = request.env['kiem.kho.session'].browse(session_id)
            if not session.exists() or session.state != 'in_progress':
                return {
                    'success': False,
                    'message': 'Phiên kiểm kho không hợp lệ hoặc đã kết thúc'
                }
            
            # Kiểm tra barcode đã tồn tại
            existing_line = request.env['kiem.kho.line'].search([
                ('session_id', '=', session_id),
                ('barcode', '=', barcode)
            ])
            
            if existing_line:
                return {
                    'success': False,
                    'message': 'Mã vạch này đã được quét!'
                }
            
            # Tạo dòng mới
            line = request.env['kiem.kho.line'].create({
                'session_id': session_id,
                'barcode': barcode,
                'scanned_qty': 1.0
            })
            
            return {
                'success': True,
                'message': 'Đã thêm sản phẩm thành công',
                'line_data': {
                    'id': line.id,
                    'barcode': line.barcode,
                    'product_name': line.product_name,
                    'scan_time': line.scan_time.strftime('%H:%M:%S')
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @http.route('/kiem_kho/remove_item', type='json', auth='user', methods=['POST'])
    def remove_item(self, line_id, **kwargs):
        """API xóa item"""
        try:
            line = request.env['kiem.kho.line'].browse(line_id)
            if not line.exists():
                return {
                    'success': False,
                    'message': 'Không tìm thấy dòng cần xóa'
                }
            
            line.unlink()
            return {
                'success': True,
                'message': 'Đã xóa sản phẩm'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @http.route('/kiem_kho/get_session_data', type='json', auth='user', methods=['POST'])
    def get_session_data(self, session_id, **kwargs):
        """API lấy dữ liệu phiên"""
        try:
            session = request.env['kiem.kho.session'].browse(session_id)
            if not session.exists():
                return {'success': False, 'message': 'Phiên không tồn tại'}
            
            lines_data = []
            for line in session.line_ids.sorted('scan_time', reverse=True):
                lines_data.append({
                    'id': line.id,
                    'barcode': line.barcode,
                    'product_name': line.product_name,
                    'scan_time': line.scan_time.strftime('%H:%M:%S')
                })
            
            return {
                'success': True,
                'total_items': len(lines_data),
                'lines': lines_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
