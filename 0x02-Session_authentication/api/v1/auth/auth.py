#!/usr/bin/env python3
""" Auth Module """

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Auth Class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth """
        if not path:
            return True
        if not excluded_paths:
            return True
        if path in excluded_paths:
            return False
        for paths in excluded_paths:
            if paths[:-1] == path:
                return False
            if paths[:-1] in path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Auth Header """
        if not request:
            return None
        if not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current session user """
        return None

    def session_cookie(self, request=None):
        """Returns cookie from a request object"""
        if not request:
            return
        if not request.cookies:
            return
        return request.cookies.get(getenv('SESSION_NAME'))
