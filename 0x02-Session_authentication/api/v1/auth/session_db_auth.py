#!/usr/bin/env python3
""" Authenticate and Stores UserSession IDs in Database """

from  api.v1.auth.session_exp_auth import SessionExpAuth

class SessionDBAuth(SessionExpAuth):
    """ Authenticate Session IDs in Database """
    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession

        Args:
            user_id (str, optional): Users ID. Defaults to None.
        """
        return super().create_session(user_id)

    def user_id_for_session_id(self, session_id=None):
        """ get user id using session id

        Args:
            session_id (str, optional): UserSession ID. Defaults to None.
        """
        return super().user_id_for_session_id(session_id)

    def destroy_sesion(self, request=None):
        """ destroys the UserSession based on Session ID"""
        return super().destroy_session(request)
