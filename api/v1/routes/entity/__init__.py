from flask import Blueprint

entityBP = Blueprint('entity', __name__)

from api.v1.routes.entity import routes

__load__ = routes

__all__ = ['entityBP']