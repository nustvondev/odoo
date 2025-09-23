import xmlrpc.client


url='http://localhost:8069'
username = 'admin'
password = 'admin'
db = 'inven'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
print(common.version())

uid= common.authenticate(db, username, password, {})
print(uid)