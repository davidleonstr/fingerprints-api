from flask import Blueprint

fingerprintBP = Blueprint('fingerprint', __name__)

from api.v1.routes.fingerprint import routes

__load__ = routes

__all__ = ['fingerprintBP']