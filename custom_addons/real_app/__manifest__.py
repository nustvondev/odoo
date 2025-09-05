{
    'name': "The Real Estate Advertisement demo 1",
    'version': '1.0',
    'summary': "Demo tutorial The Real Estate Advertisement App",
    'author': "hoanh",
    'website': "https://github.com/nustvondev",
    'category': 'Sales',
    'depends': [],   # luôn cần base
    'data': [
        'security/ir.model.access.csv',
        'views/property_views.xml',
        'views/real_estate_views.xml',
        'views/menu_items_views.xml',


    ],            # có thể để trống nếu chưa có view/data
    'installable': True,
    'application': True,
    'license': 'GPL-3',
}
