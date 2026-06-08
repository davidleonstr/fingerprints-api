from flask import Blueprint

permissionLevelBP = Blueprint('permissionLevel', __name__)

from api.v1.routes.permissionLevel import routes

__load__ = routes

__all__ = ['permissionLevelBP']