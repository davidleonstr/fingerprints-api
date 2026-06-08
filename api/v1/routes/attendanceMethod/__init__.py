from flask import Blueprint

attendanceMethodBP = Blueprint('attendanceMethod', __name__)

from api.v1.routes.attendanceMethod import routes

__load__ = routes

__all__ = ['attendanceMethodBP']