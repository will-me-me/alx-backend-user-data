#!/usr/bin/env python3

""" BasicAuth Module """

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User
from models.base import DATA
from flask import request


class BasicAuth(Auth):
    """ BasicAuth Class """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extracts auth header. """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decodes base64 auth header """
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            cred = base64.b64decode(base64_authorization_header)
        except Exception:
            return None
        return base64.b64decode(base64_authorization_header).decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts email and password from user object """
        if not decoded_base64_authorization_header:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        col_index = decoded_base64_authorization_header.find(':')
        return (decoded_base64_authorization_header[:col_index],
                decoded_base64_authorization_header[col_index+1:])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ User email from credentials """
        if not user_email or type(user_email) != str:
            return
        if not user_pwd or type(user_pwd) != str:
            return
        if 'User' not in DATA:
            return
        for user in User.search({'email': user_email}):
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ BasicAuth auth TheMatrix """
        authe = self.extract_base64_authorization_header(
                request.headers.get('Authorization'))
        dec_header = self.decode_base64_authorization_header(
                authe)
        user_cre = self.extract_user_credentials(dec_header)
        ret_user = self.user_object_from_credentials(user_cre[0], user_cre[1])
        return ret_user
