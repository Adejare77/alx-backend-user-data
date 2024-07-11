#!/usr/bin/env python3
""" Manage the Session authentication """

from api.v1.auth.auth import Auth
import uuid
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """ Use Session Authentication """
    user_id_by_session_id = {}  # "in-memory session ID storage"

    def create_session(self, user_id: str = None) -> str:
        """ create a Session ID for a user """
        if not (user_id and type(user_id) is str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None):
        """ returns a User ID based on a Session ID given

        Args:
            session_id (str, optional): Session ID. Defaults to None.
        """
        if not (session_id and type(session_id) is str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value

        Args:
            request: Flask object. Defaults to None.
        """
        user_session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(user_session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """ deletes the user session/logout """
        if not (request and self.session_cookie(request)):
            return False
        session_id = self.session_cookie(request)
        if not self.user_id_for_session_id(session_id):
            return False

        del self.user_id_by_session_id[session_id]

        return True
