#!/usr/bin/env python3
""" Basic Flask app """

from flask import Flask, jsonify, request, abort, make_response
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def index():
    """ index/home page """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def new_user():
    """ registers new users """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ Log in """
    email = request.form.get("email")
    pwd = request.form.get("password")
    if AUTH.valid_login(email, pwd):
        response = make_response(jsonify(
            {"email": email, "message": "logged in"}
        ))
        session_id = AUTH.create_session(email)
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
