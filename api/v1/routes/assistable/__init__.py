from flask import Blueprint

assistableBP = Blueprint('assistable', __name__)

from api.v1.routes.assistable import routes

__load__ = routes

__all__ = ['assistableBP']