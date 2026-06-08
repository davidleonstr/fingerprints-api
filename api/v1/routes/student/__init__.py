from flask import Blueprint

studentBP = Blueprint('student', __name__)

from api.v1.routes.student import routes

__load__ = routes

__all__ = ['studentBP']