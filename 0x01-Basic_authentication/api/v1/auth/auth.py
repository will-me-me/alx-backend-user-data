#!/usr/bin/env python3
"""Auth Module"""

from typing import TypeVar, List


class Auth:
    """Custom Auth Implementation"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if route requires authenticated."""
        if not path or not excluded_paths:
            return True
        for e_path in excluded_paths:
            e_len = len(e_path) - 1
            if path[:e_len] == e_path[:e_len] or (
                    path[-1] != '/' and path + '/'[:e_len] == e_path[:e_len]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the Authorization header from the request"""
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns current user."""
        return None
