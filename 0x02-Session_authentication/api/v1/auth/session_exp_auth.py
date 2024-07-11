#!/usr/bin/env python3
""" sets an expiry date for the session authentication system"""

import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ creates an expiry date for Sessions ID """
    def __init__(self):
        super().__init__()
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ create a Session ID by calling super() and adding expiry logic """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ get user id using session id """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        if not session_dict.get('created_at'):
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        if (created_at + timedelta(seconds=self.session_duration) <
           datetime.now()):
            return None

        return session_dict.get("user_id")
