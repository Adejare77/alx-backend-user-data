#!/usr/bin/env python3
""" Manage the Session authentication """

from api.v1.auth.auth import Auth
import uuid


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
