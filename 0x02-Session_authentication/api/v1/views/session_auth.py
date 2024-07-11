#!/usr/bin/env python3
""" view for Session Authentication """

from flask import request, jsonify, make_response
from models.user import User
from api.v1.views import app_views
import os


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login():
    """ log in using session token """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    pwd = request.form.get('password')
    if not pwd:
        return jsonify({"error": "password missing"}), 400

    cls_obj = User.search({"email": email})
    if not cls_obj:
        return jsonify({"error": "no user found for this email"}), 404
    elif not cls_obj[0].is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    # since cls_obj is a list of a single element
    # user = auth.create_session(list(cls_obj[0].keys())[0])
    user_session_id = auth.create_session(cls_obj[0].__dict__['id'])
    response = make_response(cls_obj[0].to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), user_session_id)

    return response
