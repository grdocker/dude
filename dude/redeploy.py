"""
Module with redeploy handle implementation
"""
import compose.config
from compose.project import Project, ConvergenceStrategy
from docker import APIClient
from flask import request, current_app as app
from .auth import auth_protected
from .config import DOCKER_URL, DOCKER_TLS, SERVICES_DIR


def _make_docker_client():
    return APIClient(base_url=DOCKER_URL, tls=DOCKER_TLS)


def _load_compose_config(service):
    try:
        return compose.config.load(
            compose.config.find(SERVICES_DIR, [f"{service}.yml"], None)
        )
    except compose.config.ConfigurationError as ex:
        app.logger.error("load config error: %s", str(ex))
        return None


@auth_protected.route("/redeploy")
def redeploy():
    """
    Implements redeploy handle
    Runs docker-compose pull and up commands for specified service
    Service must be preconfigured with yml file in SERVICES_DIR
    Docker URL can be configured with DOCKER_URL option
    """
    service = request.args.get("service", type=str)
    if not service:
        return "service not specified", 400

    config = _load_compose_config(service)
    if not config:
        return "can't load service config", 400

    project = Project.from_config(service, config, _make_docker_client())
    project.pull()
    project.up(strategy=ConvergenceStrategy.always, detached=True)
    return "ok"
