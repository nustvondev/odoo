# -*- coding: utf-8 -*-
{
    'name': 'Kiểm Kho',
    'version': '18.0.1.0.0',
    'summary': 'Hệ thống quản lý kiểm kho với barcode scanner',
    'description': """
        Ứng dụng Kiểm Kho
        =================
        
        Tính năng chính:
        * Quét mã vạch sản phẩm
        * Quản lý danh sách sản phẩm kiểm kho
        * Giao diện thân thiện với người dùng
        * Xử lý batch kiểm kho
        * Báo cáo kiểm kho
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'category': 'Inventory/Inventory',
    'depends': ['base', 'stock', 'product'],
    'data': [
        'data/sequence_data.xml',
        'security/ir.model.access.csv',
        'views/kiem_kho_views.xml',
        'views/kiem_kho_session_views.xml',
        'views/kiem_kho_line_views.xml',
        'views/kiem_kho_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'kiem_kho/static/src/css/kiem_kho.css',
            'kiem_kho/static/src/js/kiem_kho.js',
        ],
    },
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
