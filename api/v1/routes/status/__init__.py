from flask import Blueprint

statusBP = Blueprint('status', __name__)

from api.v1.routes.status import routes

__load__ = routes

__all__ = ['statusBP']