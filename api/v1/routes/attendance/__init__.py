from flask import Blueprint

attendanceBP = Blueprint('attendance', __name__)

from api.v1.routes.attendance import routes

__load__ = routes

__all__ = ['attendanceBP']