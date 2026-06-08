from flask import Blueprint

fingerprintNameBP = Blueprint('fingerprintName', __name__)

from api.v1.routes.fingerprintName import routes

__load__ = routes

__all__ = ['fingerprintNameBP']