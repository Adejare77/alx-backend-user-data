#!/usr/bin/env python3
""" Manage the Session authentication """

import base64
import re
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Use Session Authentication to authenticate user Based on
    session token. Session generated by the server will be sent
    to a user as a cookie which is stored by the user's browswer
    """
    pass