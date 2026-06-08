from flask import request
from pydantic import ValidationError

from api.config import DB
from api.tools import Response, ResponseData, dumpModel
from api.v1.models import PermissionLevel

from api.v1.routes.permissionLevel.schemas import (
    PermissionLevelsData,
    PermissionLevelData,
    CreatePermissionLevelSchema,
    UpdatePermissionLevelSchema,
)

class PermissionLevelController:

    @staticmethod
    def create():
        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = CreatePermissionLevelSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if PermissionLevel.query.filter_by(number=payload.number).first() is not None:
            return Response(
                data=ResponseData(message='Permission level number already taken')
            ).send(409)

        record = PermissionLevel(
            number=payload.number,
            description=payload.description,
        )

        DB.session.add(record)
        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=PermissionLevelData(permission_level=dumpModel(record))
        ).send(201)

    @staticmethod
    def getAll():
        records = (
            PermissionLevel.query
            .order_by(PermissionLevel.number.asc())
            .all()
        )

        return Response(
            data=PermissionLevelsData(permission_levels=[dumpModel(r) for r in records])
        ).send(200)

    @staticmethod
    def getOne(permissionLevelId: int):
        record = PermissionLevel.query.get(permissionLevelId)

        if record is None:
            return Response(
                data=ResponseData(message='Permission level not found')
            ).send(404)

        return Response(
            data=PermissionLevelData(permission_level=dumpModel(record))
        ).send(200)

    @staticmethod
    def update(permissionLevelId: int):
        record = PermissionLevel.query.get(permissionLevelId)

        if record is None:
            return Response(
                data=ResponseData(message='Permission level not found')
            ).send(404)

        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = UpdatePermissionLevelSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if payload.number is not None:
            conflict = PermissionLevel.query.filter_by(number=payload.number).first()

            if conflict is not None and conflict.id != permissionLevelId:
                return Response(
                    data=ResponseData(message='Permission level number already taken')
                ).send(409)

            record.number = payload.number

        if payload.description is not None:
            record.description = payload.description

        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=PermissionLevelData(permission_level=dumpModel(record))
        ).send(200)

    @staticmethod
    def delete(permissionLevelId: int):
        record = PermissionLevel.query.get(permissionLevelId)

        if record is None:
            return Response(
                data=ResponseData(message='Permission level not found')
            ).send(404)

        DB.session.delete(record)
        DB.session.commit()

        return Response(
            data=PermissionLevelData(permission_level=dumpModel(record))
        ).send(200)