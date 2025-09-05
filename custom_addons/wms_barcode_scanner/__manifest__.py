# -*- coding: utf-8 -*-
{
    "name": "WMS Barcode Scanner 1",
    "summary": "Scan & manage barcodes in a clean UI",
    "version": "1.0.0",
    "category": "Inventory",
    "author": "Your Company",
    "website": "https://your-company.example",
    "license": "LGPL-3",
    "depends": ["base", "web", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/templates.xml",
        "views/menu.xml",
    ],
    "assets": {
        # Đảm bảo hoạt động khi render theo layout backend hoặc mở bằng URL
        "web.assets_backend": [
            "wms_barcode_scanner/static/src/css/scanner.css",
            "wms_barcode_scanner/static/src/js/scanner.js",
        ],
        "web.assets_frontend": [
            "wms_barcode_scanner/static/src/css/scanner.css",
            "wms_barcode_scanner/static/src/js/scanner.js",
        ],
    },
    "installable": True,
    "application": False,
}