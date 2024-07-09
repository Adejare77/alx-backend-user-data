#!/usr/bin/env python3
"""Basic Authentication"""

import base64
import re
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ Use Basic Authentication """
    def extract_base64_authorization_header(
        self, authorization_header: str
            ) -> str:
        """extracts Authorization header for Basic authentication

        Args:
            authorization_header (str): value for field AUTH_TYPE

        Returns:
            str: extracted value for Authorization field else None
        """
        if not (authorization_header and type(authorization_header) is str and
                re.match(r'Basic\s', authorization_header)):
            return None
        auth_value = re.search(r'(?<=Basic\s).*',
                               authorization_header).group()
        return auth_value

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
            ) -> str:
        """ Decode value of Base64 string

        Args:
            base64_authorization_header (str): value extracted by
            extract_base_64_authorization_header

        Returns:
            str: returns decoded value of Base64 string as UTF8 string
            else None
        """
        if not (base64_authorization_header and
                type(base64_authorization_header) is str):
            return None
        try:
            decoded_byte = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_byte.decode('utf-8')
            return decoded_str
        except Exception as e:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """extracts username and password from the Base64 decoded

        Args:
            decoded_base64_authorization_header (str): decoded request header
        """
        if not (decoded_base64_authorization_header and
                type(decoded_base64_authorization_header) is str and
                ":" in decoded_base64_authorization_header):
            return (None, None)
        # email = decoded_base64_authorization_header.split(":")[0]
        # password = decoded_base64_authorization_header.split(":")[1]
        first_colon_index = decoded_base64_authorization_header.find(":")
        email = decoded_base64_authorization_header[:first_colon_index]
        password = decoded_base64_authorization_header[first_colon_index + 1:]
        return (email, password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """_summary_

        Args:
            user_email (str): email of the user
            user_pwd (str): password of the user
        """
        if not (user_email and user_pwd and type(user_email) is str
                and type(user_pwd) is str):
            return None
        # since search is a class method. search requires a dictionary
        cls_obj = User.search({'email': user_email})
        # if cls_obj with the user_email exists, a list will be returned
        # Thus, select the instance returned in the list
        if (cls_obj and cls_obj[0].is_valid_password(user_pwd)):
            return cls_obj[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves the User instance """
        # check if request is none or Authorization head is not present
        if not (request and request.headers.get('Authorization')):
            return None
        # extract Authorization filed and confirm it starts with Basic
        authorization_header = request.headers.get('Authorization')
        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header)
        if not (base64_authorization_header):
            return None
        # Decode authorization value and ensures it's not none
        decode_base64_authorization_header = \
            self.decode_base64_authorization_header(
                base64_authorization_header)
        if not decode_base64_authorization_header:
            return None
        # extracts users credentials for email and password authentication
        users_credentials = self.extract_user_credentials(
            decode_base64_authorization_header)
        if not users_credentials:
            return None
        user_email, user_pwd = users_credentials
        # confirm credentials are present in our DB
        user_object = self.user_object_from_credentials(user_email, user_pwd)
        if not user_object:
            return None
        return user_object
