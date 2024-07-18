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

    def destroy_session(self, user_id: str) -> None:
        """ Destroy session """
        if not user_id:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            setattr(user, 'session_id', None)

        except NoResultFound:
            return NoResultFound

    def get_reset_password_token(self, email: str) -> str:
        """ generate reset password token """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = str(uuid.uuid4())
            setattr(user, 'reset_token', reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ update a user's password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        new_passwd = _hash_password(password)
        self._db.update_user(user.id, hashed_password=new_passwd)
        return None
