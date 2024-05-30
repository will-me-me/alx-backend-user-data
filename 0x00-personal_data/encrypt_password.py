#!/usr/bin/env python3
""" Encrypt Password Module """
import bcrypt


def hash_password(password: str) -> bytes:
    """Password hasher"""
    encoded_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(encoded_password, salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Password verifier"""
    encoded_password = password.encode("utf-8")
    return bcrypt.checkpw(encoded_password, hashed_password)
