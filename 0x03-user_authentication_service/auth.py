#!/usr/bin/env python3
""" Hash passwords """

import bcrypt


def _hash_password(password: str) -> bytes:
    """ restuned salted hashed password in bytes """
    if not password:
        return None
    pwd = password.encode()
    hashed_password = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed_password
