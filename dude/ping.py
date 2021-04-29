"""
Module with ping handle implementation
"""
from .app import app


@app.route("/ping")
def ping():
    """
    Implements ping handle
    Always returns pong
    """
    return "pong"
