import bcrypt

from flask import request, current_app
from pydantic import ValidationError

from api.config import DB
from api.tools import Response, ResponseData, dumpModel
from api.v1.models import Interactor, Entity, Role

from api.v1.routes.interactor.schemas import (
    InteractorsData,
    InteractorData,
    CreateInteractorSchema,
    UpdateInteractorSchema
)

from api.v1.models import Interactor

class InteractorController:

    @staticmethod
    def create():
        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = CreateInteractorSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        entity = Entity.query.get(payload.entity_id)

        if entity is None:
            return Response(
                data=ResponseData(message='Entity not found')
            ).send(404)

        role = Role.query.get(payload.role_id)

        if role is None:
            return Response(
                data=ResponseData(message='Role not found')
            ).send(404)

        existing = Interactor.query.filter_by(username=payload.username).first()

        if existing is not None:
            return Response(
                data=ResponseData(message='Username already taken')
            ).send(409)

        passwordHash = InteractorController.createPasswordHash(payload.password)

        record = Interactor(
            username=payload.username,
            password_hash=passwordHash,
            entity_id=payload.entity_id,
            role_id=payload.role_id,
        )

        DB.session.add(record)
        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=InteractorData(interactor=dumpModel(record))
        ).send(201)

    @staticmethod
    def getAll():
        records = (
            Interactor.query
            .order_by(Interactor.created_at.desc())
            .all()
        )

        return Response(
            data=InteractorsData(interactors=[dumpModel(r) for r in records])
        ).send(200)

    @staticmethod
    def getOne(interactorId: str):
        record = Interactor.query.get(interactorId)

        if record is None:
            return Response(
                data=ResponseData(message='Interactor not found')
            ).send(404)

        return Response(
            data=InteractorData(interactor=dumpModel(record))
        ).send(200)

    @staticmethod
    def update(interactorId: str):
        record = Interactor.query.get(interactorId)

        if record is None:
            return Response(
                data=ResponseData(message='Interactor not found')
            ).send(404)

        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = UpdateInteractorSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if payload.username is not None:
            conflict = Interactor.query.filter_by(username=payload.username).first()

            if conflict is not None and str(conflict.id) != interactorId:
                return Response(
                    data=ResponseData(message='Username already taken')
                ).send(409)

            record.username = payload.username

        if payload.password is not None:
            record.password_hash = InteractorController.createPasswordHash(payload.password)

        if payload.role_id is not None:
            role = Role.query.get(payload.role_id)

            if role is None:
                return Response(
                    data=ResponseData(message='Role not found')
                ).send(404)

            record.role_id = payload.role_id

        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=InteractorData(interactor=dumpModel(record))
        ).send(200)

    @staticmethod
    def delete(interactorId: str):
        record = Interactor.query.get(interactorId)

        if record is None:
            return Response(
                data=ResponseData(message='Interactor not found')
            ).send(404)

        DB.session.delete(record)
        DB.session.commit()

        return Response(
            data=InteractorData(interactor=dumpModel(record))
        ).send(200)
    
    @staticmethod
    def createPasswordHash(password: str) -> str:
        salt = current_app.config.get('PASSWORD_SALT')

        passwordHash = bcrypt.hashpw(
            password.encode('utf-8'),
            salt.encode('utf-8') if isinstance(salt, str) else salt
        ).decode('utf-8')

        return passwordHash