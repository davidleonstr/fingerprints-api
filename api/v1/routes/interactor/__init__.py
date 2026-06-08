from flask import Blueprint

interactorBP = Blueprint('interactor', __name__)

from api.v1.routes.interactor import routes

__load__ = routes

__all__ = ['interactorBP']