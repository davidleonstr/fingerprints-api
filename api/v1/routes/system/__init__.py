from flask import Blueprint

systemBP = Blueprint('system', __name__)

from api.v1.routes.system import routes

__load__ = routes

__all__ = ['systemBP']