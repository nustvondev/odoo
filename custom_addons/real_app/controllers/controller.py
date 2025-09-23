# -*- coding: utf-8 -*-


from odoo import http
from odoo.http import request


class KiemKe(http.Controller):
    @http.route('/Token/authenticate', type='http', auth="none",
                methods=['POST'], csrf=False, save_session=False, cors="*")
    def get_token(self):
        byte_string = request.httprequest.data
        data = json.loads(byte_string.decode('utf-8'))
        username = data['username']
        password = data['password']
        user_id = request.session.authenticate(request.db, username, password)
        if not user_id:
            return json.dumps({"error": "Invalid Username or Password."})
        env = request.env(user=request.env.user.browse(user_id))
        env['res.users.apikeys.description'].check_access_make_key()
        token = env['res.users.apikeys']._generate("", username)
        payload = {
            'user_id': user_id,
            'username': username,
            'password': password,
            'token': token
        }
        return json.dumps({
            "data": payload,
            "responsedetail": {
                "messages": "UserValidated",
                "messagestype": 1,
                "responsecode": 200
            }
        })


