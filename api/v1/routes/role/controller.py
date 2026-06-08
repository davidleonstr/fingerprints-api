from flask import request
from pydantic import ValidationError

from api.config import DB
from api.tools import Response, ResponseData, dumpModel
from api.v1.models import Role, PermissionLevel

from api.v1.routes.role.schemas import (
    RolesData,
    RoleData,
    CreateRoleSchema,
    UpdateRoleSchema,
)

class RoleController:

    @staticmethod
    def create():
        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = CreateRoleSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        permissionLevel = PermissionLevel.query.get(payload.permission_level_id)

        if permissionLevel is None:
            return Response(
                data=ResponseData(message='Permission level not found')
            ).send(404)

        if Role.query.filter_by(name=payload.name).first() is not None:
            return Response(
                data=ResponseData(message='Role name already taken')
            ).send(409)

        record = Role(
            name=payload.name,
            description=payload.description,
            permission_level_id=payload.permission_level_id,
        )

        DB.session.add(record)
        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=RoleData(role=dumpModel(record))
        ).send(201)

    @staticmethod
    def getAll():
        records = (
            Role.query
            .order_by(Role.created_at.desc())
            .all()
        )

        return Response(
            data=RolesData(roles=[dumpModel(r) for r in records])
        ).send(200)

    @staticmethod
    def getOne(roleId: int):
        record = Role.query.get(roleId)

        if record is None:
            return Response(
                data=ResponseData(message='Role not found')
            ).send(404)

        return Response(
            data=RoleData(role=dumpModel(record))
        ).send(200)

    @staticmethod
    def update(roleId: int):
        record = Role.query.get(roleId)

        if record is None:
            return Response(
                data=ResponseData(message='Role not found')
            ).send(404)

        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = UpdateRoleSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if payload.name is not None:
            conflict = Role.query.filter_by(name=payload.name).first()

            if conflict is not None and conflict.id != roleId:
                return Response(
                    data=ResponseData(message='Role name already taken')
                ).send(409)

            record.name = payload.name

        if payload.description is not None:
            record.description = payload.description

        if payload.permission_level_id is not None:
            permissionLevel = PermissionLevel.query.get(payload.permission_level_id)

            if permissionLevel is None:
                return Response(
                    data=ResponseData(message='Permission level not found')
                ).send(404)

            record.permission_level_id = payload.permission_level_id

        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=RoleData(role=dumpModel(record))
        ).send(200)

    @staticmethod
    def delete(roleId: int):
        record = Role.query.get(roleId)

        if record is None:
            return Response(
                data=ResponseData(message='Role not found')
            ).send(404)

        DB.session.delete(record)
        DB.session.commit()

        return Response(
            data=RoleData(role=dumpModel(record))
        ).send(200)