#!/usr/bin/env python3
""" Hash passwords """

import bcrypt
import uuid
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ hash password """
    if not password:
        return None
    pwd = password.encode()
    hashed_password = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """ generate UUIDs """
    unique_id = str(uuid.uuid4())
    return unique_id


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register a user """
        try:
            existing_user = self._db.find_user_by(email=email)
        except NoResultFound:
            pwd = _hash_password(password)
            return self._db.add_user(email, pwd)

        if existing_user:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """ credentials validation """
        if not (email and password):
            return False
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        pwd = password.encode()
        return bcrypt.checkpw(pwd, user.hashed_password)
