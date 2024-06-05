#!/usr/bin/env python3
""" Index module"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ Returns the status of the API """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ Returns the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def reject() -> str:
    """
    Return aborts with description message
    """
    abort(401, description="Unauthorized")


@app_views.route('/forbidden', methods=["GET"], strict_slashes=False)
def raise_forbidden() -> str:
    """
    Returns Forbidden
    """
    abort(403, description="Forbidden")
