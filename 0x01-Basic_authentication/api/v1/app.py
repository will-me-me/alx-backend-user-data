#!/usr/bin/env python3
""" API End Point Routes module"""

from flask import Flask, jsonify, abort, request
from os import getenv
from flask_cors import (CORS, cross_origin)
import os
from api.v1.views import app_views
from typing import Tuple


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def before_request():
    """Checks permission of user"""
    if not auth:
        return
    if not auth.require_auth(request.path,
                             ['/api/v1/status/',
                              '/api/v1/unauthorized/', '/api/v1/forbidden/']):
        return
    if not auth.authorization_header(request):
        abort(401)
    if not auth.current_user(request):
        abort(403)


@app.errorhandler(404)
def not_found(error) -> Tuple[str, int]:
    """ 404 Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> Tuple[str, int]:
    """401 unauthorized request error handler"""
    return jsonify({'error': 'Unauthorized'}), 401


@app.errorhandler(403)
def forbidden(error) -> Tuple[str, int]:
    """403 unauthorized request handler"""
    return jsonify({'error': 'Forbidden'}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
