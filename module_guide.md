# cách tạo module trong odoo


Tạo module bằng command sau:

```shell
 python3 odoo-bin scaffold <tên_module> <đường_dẫn_đến_addons>
```

ví dụ:

```shell
 python3 odoo-bin scaffold kiem_ke /home/hoanh/work/odoo/custom_addons
```

Lúc này trong thư mục custom_addons sẽ xuất hiện một thư mục kiem_ke với các file cơ bản của một module.

Tiếp theo, bạn cần chỉnh sửa file `__manifest__.py` để định nghĩa thông tin về module của bạn. Ví dụ:

```python
{
    'name': 'Kiểm Kê',
    'version': '1.0',
    'summary': 'Module quản lý kiểm kê kho',
    'description': 'Module này giúp quản lý quá trình kiểm kê hàng hóa trong kho.',
    'author': 'Tên của bạn',
    'website': 'http://www.yourwebsite.com',
    'category': 'Warehouse',
    'depends': ['base', 'stock'],
    'data': [
        # Danh sách các file XML, CSV cần nạp
    ],
    'installable': True,
    'application': True,
}
```

Sau đó tìm đêến cách thức tạo model:

Follow theo tài liệu: https://www.odoo.com/documentation/18.0/developer/tutorials/server_framework_101/03_basicmodel.html

tiến hành tạo model trong file `models/<models>.py`(có thể tham khảo custom thêm tại https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html#reference-orm-fields):

ví dụ file `models/kiem_ke.py`:
```python
from odoo import fields, models

class KiemKe(models.Model):
    _name = "kiem_ke.scanned_item"
    _description = "Scanned Item"
    _order = "scanned_at desc"

    name = fields.Char(string="Item Name", required=True)
    barcode = fields.Char(string="Barcode", required=True, index=True, unique=True)
    scanned_at = fields.Datetime(string="Scanned At", default=fields.Datetime.now)
    scanned_by = fields.Char(string="Scanned By", required=True)
```
sao khi tạo model xong, bạn cần khai báo model trong file `__init__.py`:

```python
# -*- coding: utf-8 -*-

from . import models
from . import kiem_ke
``` 

tiếp đến việc cấu hình quyền truy cập cho model trong file `security/ir.model.access.csv`:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_kiem_ke_kiem_ke,access_kiem_ke_kiem_ke,model_kiem_ke,base.group_user,1,1,1,1
```

sau khi cấu hình quyền truy cập xong, tiến hành khai báo phần security trong file `__manifest__.py`:

```python
...# code exiting
'data': [
        'security/ir.model.access.csv'
    ]
...
```


mwpf-ajx9-tjm9