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

    def create_session(self, email: str) -> str:
        """ Get session ID """
        if not email:
            return None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = str(uuid.uuid4())
        setattr(user, 'session_id', session_id)
        self._db._session.commit()
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ find user by session ID """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
