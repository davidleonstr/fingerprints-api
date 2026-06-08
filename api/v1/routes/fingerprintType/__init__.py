from flask import Blueprint

fingerprintTypeBP = Blueprint('fingerprintType', __name__)

from api.v1.routes.fingerprintType import routes

__load__ = routes

__all__ = ['fingerprintTypeBP']