#!/usr/bin/env python3
""" Hash passwords """

import bcrypt
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ restuned salted hashed password in bytes """
    if not password:
        return None
    pwd = password.encode()
    hashed_password = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ return a new user if not exists else raise error """
        try:
            all_users = self._db._session.query(User).all()
        except InvalidRequestError:
            raise InvalidRequestError

        for user in all_users:
            if email in user.email:
                raise ValueError(f"User {email} already exists")

        pwd = _hash_password(password)
        return self._db.add_user(email, pwd)
