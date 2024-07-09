#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
if os.getenv('AUTH_TYPE'):
    if os.getenv('AUTH_TYPE') == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif os.getenv('AUTH_TYPE') == 'auth':
        from api.v1.auth.auth import Auth
        auth = Auth()


@app.before_request
def before_request():
    """Filtering each request"""
    if auth:
        path_list = ['/api/v1/status/', '/api/v1/unauthorized/',
                     '/api/v1/forbidden/']
        if auth.require_auth(request.path, path_list):
            if auth.authorization_header(request) == None:
                abort(401)
            if auth.current_user(request) == None:
                abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ forbidden """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
