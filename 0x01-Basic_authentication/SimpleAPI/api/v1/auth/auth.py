#!/usr/bin/env python3
""" Manage the API authentication """

from flask import request
from typing import List, TypeVar


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
        if not (path and excluded_paths and path in excluded_paths):
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """returns None

        Args:
            request (_type_, optional): Flask request object.
            Defaults to None.

        Returns:
            str: None
        """
        if not request or not request.headers.get('Authorization'):
            return 'None'
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None

        Args:
            request (_type_, optional): Flask request object.
            Defaults to None.

        Returns:
            str: None
        """
        return 'None'
