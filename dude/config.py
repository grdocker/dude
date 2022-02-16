"""
Module for app configuration
"""
import os
from docker import TLSConfig


def _get_str_option(name, default):
    val = os.environ.get(name, default=default)
    return str(val)


def _get_bool_option(name, default):
    str_val = _get_str_option(name, "")
    if str_val == "":
        return default

    return bool(str_val)


def _get_list_option(name, default):
    val = _get_str_option(name, "")
    if not val:
        return default
    return val.split(" ")


SERVICES_DIR = _get_str_option("DUDE_SERVICES_DIR", "/etc/dude/")
DOCKER_URL = _get_str_option("DUDE_DOCKER_URL", "unix://var/run/docker.sock")
DOCKER_TLS = _get_bool_option("DUDE_DOCKER_USE_TLS", False)
if DOCKER_TLS:
    DOCKER_CLIENT_CERT = _get_str_option("DUDE_DOCKER_CLIENT_CERT", None)
    DOCKER_CLIENT_KEY = _get_str_option("DUDE_DOCKER_CLIENT_KEY", None)
    DOCKER_CA_CERT = _get_str_option("DUDE_DOCKER_CA_CERT", None)
    if DOCKER_CLIENT_CERT and DOCKER_CLIENT_KEY:
        DOCKER_TLS = TLSConfig(
            client_cert=(DOCKER_CLIENT_CERT, DOCKER_CLIENT_KEY), ca_cert=DOCKER_CA_CERT
        )
    else:
        DOCKER_TLS = TLSConfig(ca_cert=DOCKER_CA_CERT)

ALLOWED_GITHUB_USERS = _get_list_option("DUDE_ALLOWED_GITHUB_USERS", [])
