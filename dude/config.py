"""
Module for app configuration
"""
import os


def _get_str_option(name, default):
    val = os.environ.get(name, default=default)
    return str(val)


def _get_list_option(name, default):
    val = _get_str_option(name, "")
    if not val:
        return default
    return val.split(" ")


SERVICES_DIR = _get_str_option("DUDE_SERVICES_DIR", "/etc/dude/")
DOCKER_URL = _get_str_option("DUDE_DOCKER_URL", "unix://var/run/docker.sock")
ALLOWED_GITHUB_USERS = _get_list_option("DUDE_ALLOWED_GITHUB_USERS", [])
