"""
Main module for flask application
"""
from .app import app
from .ping import ping

__all__ = ["app", "ping"]
