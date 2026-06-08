from flask import Blueprint

authBP = Blueprint('auth', __name__)

from api.v1.routes.auth import routes

__load__ = routes

__all__ = ['authBP']