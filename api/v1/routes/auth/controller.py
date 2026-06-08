import jwt
import bcrypt
from datetime import datetime, timezone, timedelta

from flask import request, current_app
from pydantic import ValidationError

from api.tools import Response, ResponseData, dumpModel
from api.v1.models import Interactor

from api.v1.routes.auth.schemas import AuthData, AuthSchema

class AuthController:

    @staticmethod
    def auth():
        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = AuthSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        interactor = Interactor.query.filter_by(username=payload.username).first()

        if interactor is None:
            return Response(
                data=ResponseData(message='Invalid credentials')
            ).send(401)

        passwordMatch = bcrypt.checkpw(
            payload.password.encode('utf-8'),
            interactor.password_hash.encode('utf-8')
            if isinstance(interactor.password_hash, str)
            else interactor.password_hash,
        )

        if not passwordMatch:
            return Response(
                data=ResponseData(message='Invalid credentials')
            ).send(401)

        accessLevel = interactor.role.permission_level.number

        token = jwt.encode(
            {
                'sub': str(interactor.id),
                'username': interactor.username,
                'accessLevel': accessLevel,
                'iat': datetime.now(timezone.utc),
                'exp': datetime.now(timezone.utc) + timedelta(hours=8),
            },
            current_app.config.get('JWT_SECRET'),
            algorithm='HS256',
        )

        interactorData = dumpModel(interactor)
        interactorData.pop('password_hash', None)

        return Response(
            data=AuthData(token=token, interactor=interactorData)
        ).send(200)