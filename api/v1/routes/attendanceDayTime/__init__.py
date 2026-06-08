from flask import Blueprint

attendanceDayTimeBP = Blueprint('attendanceDayTime', __name__)

from api.v1.routes.attendanceDayTime import routes

__load__ = routes

__all__ = ['attendanceDayTimeBP']