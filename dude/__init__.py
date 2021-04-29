"""
Main module for flask application
"""
from .app import app
from .auth import auth_protected
from .ping import ping
from .redeploy import redeploy


__all__ = ["app", "ping", "redeploy"]
app.register_blueprint(auth_protected)
