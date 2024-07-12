#!/usr/bin/env python3
""" Stores all Session IDs as a file """
from models.base import Base
import uuid


class UserSession(Base):
    """ New authentication system, based on Session ID stored in
    database
    """
    def __init__(self, *args: list, **kwargs: dict):
        super(UserSession, self).__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', str(uuid.uuid4()))
        self.session_id = kwargs.get('session_id', str(uuid.uuid4()))
