from flask import Blueprint

roleBP = Blueprint('role', __name__)

from api.v1.routes.role import routes

__load__ = routes

__all__ = ['roleBP']