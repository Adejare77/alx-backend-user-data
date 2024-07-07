#!/usr/bin/env python3
"""Encrypting passwords using bcrypt."""

import bcrypt


def hash_password(password: str) -> bytes:
    """ returns a salted, hashed password, which is a byte string """
    # convert password to bytes
    passwd = password.encode('utf-8')
    # Hash password using hashpw with salt addition using gensalt()
    hashed = bcrypt.hashpw(passwd, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate that the provided password matches the hashed password

    Args:
        hashed_password (bytes): The hashed password in bytes
        password (str): The original password before hashing

    Returns:
        bool: True if the above are equal, else False
    """
    # convert original password to bytes
    passwd = password.encode('utf-8')
    if bcrypt.checkpw(passwd, hashed_password):
        return True
    return False
