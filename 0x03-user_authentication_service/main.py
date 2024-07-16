#!/usr/bin/env python3
""" End-to-end integeration test """

import requests
from app import app


app.run()


def register_user(email: str, password: str) -> None:
    """ validate new user is created """
    data = {'email': email, 'password': password}
    resp = requests.post("http://localhost:5000/users", data=data)
    if resp.status_code == 200:
        assert resp.json() == {"email": email, "message": "user created"}
    elif resp.status_code == 400:
        assert resp.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Invalid wrong password """
    data = {"email": email, 'password': password}
    resp = requests.post("http://localhost:5000/sessions", data=data)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Valid wrong password """
    data = {"email": email, 'password': password}
    resp = requests.post("http://localhost:5000/sessions", data=data)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "logged in"}
    assert resp.cookies.get('session_id') is not None


def profile_unlogged() -> None:
    """ Unauthorized user log in """
    resp = requests.get("http://localhost:5000/profile")
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Authorized user """
    resp = requests.get("http://localhost:5000/profile", cookies=session_id)
    payload = {'email': resp.json().get('email')}
    assert resp.json() == payload
    assert resp.status_code == 200


def log_out(session_id: str) -> None:
    """ log out user """
    resp = requests.delete("http://localhost:5000/sessions",
                           cookies=session_id)
    if resp.status_code == 200:
        payload = {'email': resp.json().get('email')}
        assert resp.json() == payload
    else:
        assert resp.status_code == 403


def reset_password_token(email: str) -> str:
    """ reset user's password """
    data = {"email": email}
    resp = requests.post("http://localhost:5000/reset_password", data=data)
    if resp.status_code == 200:
        payload = {"email": email,
                   "reset_token": resp.json().get('reset_token')}
        assert resp.json() == payload
    else:
        assert resp.status_code == 403


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ update a user's password """
    data = {
        'email': email, 'reset_token': reset_token, 'password': new_password
        }
    resp = requests.put('http://localhost:5000/reset_password', data=data)
    if resp.status_code == 200:
        assert resp.json() == {"email": email, "message": "Password updated"}
    else:
        assert resp.status_code == 403


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
