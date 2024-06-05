#!/usr/bin/env python3
""" module for managing session """

from models.base import Base


class UserSession(Base):
    """ User session classs """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize the session instance """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
