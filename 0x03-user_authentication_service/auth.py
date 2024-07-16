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


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register a user """
        try:
            all_users = self._db._session.query(User).all()
        except InvalidRequestError:
            raise InvalidRequestError

        for user in all_users:
            if email in user.email:
                raise ValueError(f"User {email} already exists")

        pwd = _hash_password(password)
        return self._db.add_user(email, pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """ credentials validation """
        if not (email and password):
            return False
        user = self._db._session.query(User).filter_by(email=email).first()
        if not user:
            return False
        if bcrypt.checkpw(password.encode(), user.hashed_password):
            return True
        return False

    def _generate_uuid(self) -> str:
        """ generate UUIDs """
        unique_id = str(uuid.uuid4())
        return unique_id
