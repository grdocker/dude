"""
Module for app authorization
"""
from flask import Blueprint, request
from github import Github, BadCredentialsException
from .config import ALLOWED_GITHUB_USERS

auth_protected = Blueprint("auth_protected", __name__)


def _unauthorized(reason):
    return reason, 401


def _forbidden(reason):
    return reason, 403


def _authorize_user(token):
    try:
        github = Github(token)
        user = github.get_user().login
        if user not in ALLOWED_GITHUB_USERS:
            return _forbidden(f"current user not allowed: {user}")
        return None
    except BadCredentialsException as ex:
        return _unauthorized(ex.data)


@auth_protected.before_request
def check_auth():
    """
    Authenticates users using github tokens
    Authorizes users from ALLOWED_GITHUB_USERS option
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return _unauthorized("Authorization header required")

    auth_data = auth_header.split(" ")
    if len(auth_data) != 2:
        return _unauthorized("Invalid header format")

    token_type, token = auth_data
    if token_type != "Bearer":
        return _unauthorized(f"Unsupported token type: {auth_data[0]}")

    return _authorize_user(token)
