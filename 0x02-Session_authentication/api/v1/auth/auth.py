#!/usr/bin/python3
""" Manage the API authentication """

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Authentication class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False if path in excluded_paths else True

        Args:
            path (str): path to check for
            excluded_paths (List[str]): from where to check path

        Returns:
            bool: True or False
        """
        if path and path[-1] != '/':
            path = path + '/'
        if not (path and excluded_paths):
            return True

        for pattern in excluded_paths:
            if pattern.endswith('*'):
                if pattern[:-1] in path[:-1]:
                    return False
            elif path == pattern:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Request Validation

        Args:
            request (_type_, optional): Flask request object.
            Defaults to None.

        Returns:
            str: None
        """
        if not (request and request.headers.get('Authorization')):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None

        Args:
            request (_type_, optional): Flask request object.
            Defaults to None.

        Returns:
            str: None
        """
        return None

    def session_cookie(self, request=None) -> str:
        """ returns a cookie value from a request

        Args:
            request (_type_, optional): Flask request object. Defaults to None.

        Returns:
            str: None if not found, else cookie value
        """
        if not request:
            return None
        _my_session_id = os.getenv('SESSION_NAME')
        cookies = request.cookies.get(_my_session_id)
        return cookies
