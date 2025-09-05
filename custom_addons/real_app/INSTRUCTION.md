## Manifests trong Module Odoo

Manifest trong Odoo là một tệp siêu dữ liệu (`__manifest__.py`) mô tả module của bạn. Nó chứa một từ điển Python duy nhất, trong đó mỗi khóa chỉ định một thuộc tính của module.

### Các trường manifest có sẵn:

* **`name`**: Tên của module.
* **`version`**: Phiên bản của module, nên tuân theo quy tắc phiên bản ngữ nghĩa.
* **`summary`**: Một tóm tắt ngắn gọn về chức năng của module.
* **`description`**: Mô tả chi tiết cho module.
* **`author`**: Tên tác giả của module.
* **`website`**: URL trang web của tác giả.
* **`license`**: Giấy phép phân phối cho module (ví dụ: `LGPL-3`, `GPL-3`).
* **`category`**: Danh mục phân loại trong Odoo (ví dụ: `Sales`, `Inventory`, `Services`).
* **`depends`**: Danh sách các module khác phải được cài đặt trước khi cài đặt module này.
* **`data`**: Danh sách các tệp dữ liệu (XML, CSV) sẽ được tải khi cài đặt hoặc cập nhật module.
* **`demo`**: Danh sách các tệp dữ liệu demo chỉ được tải ở chế độ demo.
* **`auto_install`**: Nếu `True`, module sẽ tự động được cài đặt nếu tất cả các module phụ thuộc của nó đã được cài đặt.
* **`external_dependencies`**: Một từ điển chứa các phụ thuộc bên ngoài của Python và/hoặc các tệp nhị phân.
* **`application`**: Nếu `True`, module sẽ được coi là một ứng dụng chính trong Odoo.
* **`installable`**: Nếu `True`, người dùng có thể cài đặt module từ giao diện người dùng. Mặc định là `True`.
* **`maintainer`**: Người hoặc tổ chức chịu trách nhiệm bảo trì module.
* **`{pre_init, post_init, uninstall}_hook`**: Các "hook" để thực thi mã Python trước khi cài đặt, sau khi cài đặt hoặc khi gỡ cài đặt module.

---

### Ví dụ về tệp `__manifest__.py`:

Đây là một ví dụ về nội dung của tệp manifest cho một ứng dụng "To-Do" đơn giản.

```python
{
    'name': "To-Do App",
    'version': '1.0',
    'summary': "Simple To-Do List App",
    'website': "[https://github.com/nustvondev](https://github.com/nustvondev)",
    'author': "hoanh",
    'depends': [],
    'category':'Services',
    'data': [],
    'license':'GPL-3',
    'installable': True,
    'application': True,
}
```















Note:

```
2025-09-04 15:55:34,583 26775 WARNING inventory odoo.modules.loading: The models ['real.property'] have no access rules in module real_app, consider adding some, like:
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
```


```shell
python3 odoo-bin -c .odoorc -d inventory -u real_app
```