#!/usr/bin/env python3
""" Manage the Session authentication """

from api.v1.auth.auth import Auth
import uuid
from typing import TypeVar


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
