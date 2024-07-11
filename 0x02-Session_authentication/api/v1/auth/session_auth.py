#!/usr/bin/env python3
""" Manage the Session authentication """

import base64
import re
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Use Session Authentication"""
    pass
