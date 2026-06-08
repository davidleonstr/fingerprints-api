from functools import wraps

import jwt

from flask import request
from werkzeug.datastructures import Authorization

from api.tools.response import Response, ResponseData

from flask import current_app

def permissionLevel(levelRequired: int = 1, algorithms: list = ['HS256']):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth: Authorization | None = request.authorization

            if auth is None:
                return Response(
                    ResponseData(message='Authorization header missing')
                ).send(401)

            if auth.type != 'bearer':
                return Response(
                    ResponseData(message='Invalid authorization type')
                ).send(401)

            token = auth.token

            try:
                payload = jwt.decode(
                    token,
                    current_app.config.get('JWT_SECRET'),
                    algorithms
                )

            except jwt.InvalidTokenError:
                return Response(
                    ResponseData(message='Invalid token')
                ).send(401)

            accessLevel = payload.get('accessLevel', 0)

            if accessLevel < levelRequired:
                return Response(
                    ResponseData(message='Insufficient permissions')
                ).send(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator