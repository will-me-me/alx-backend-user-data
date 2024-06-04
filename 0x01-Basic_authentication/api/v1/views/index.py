#!/usr/bin/env python3
""" Views - Index Route Module"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ Returns a jsonified status of the status route"""
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """Returns the number of each objects"""
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=["GET"], strict_slashes=False)
def raise_unauthorized() -> str:
    """Raises 401 unauthorized exception"""
    abort(401)


@app_views.route('/forbidden', methods=["GET"], strict_slashes=False)
def raise_forbidden() -> str:
    """Raises a 403 forbidden exception."""
    abort(403)
