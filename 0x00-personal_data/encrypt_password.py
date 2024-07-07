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
