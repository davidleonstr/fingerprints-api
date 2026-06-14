from flask import request
from pydantic import ValidationError

from api.config import DB
from api.tools import Response, ResponseData, dumpModel
from api.v1.models import Assistable, Entity

from api.v1.routes.assistable.schemas import (
    AssistableData,
    AssistablesData,
    CreateAssistableSchema,
    UpdateAssistableSchema,
)

class AssistableController:

    @staticmethod
    def create():
        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = CreateAssistableSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        entity = Entity.query.get(payload.entity_id)

        if entity is None:
            return Response(
                data=ResponseData(message='Entity not found')
            ).send(404)

        if Assistable.query.filter_by(carnet=payload.carnet).first() is not None:
            return Response(
                data=ResponseData(message='Carnet already taken')
            ).send(409)

        if Assistable.query.filter_by(email=payload.email).first() is not None:
            return Response(
                data=ResponseData(message='Email already taken')
            ).send(409)

        if Assistable.query.filter_by(phone_number=payload.phone_number).first() is not None:
            return Response(
                data=ResponseData(message='Phone number already taken')
            ).send(409)

        record = Assistable(
            entity_id=payload.entity_id,
            first_name=payload.first_name,
            last_name=payload.last_name,
            birthdate=payload.birthdate,
            carnet=payload.carnet,
            email=payload.email,
            phone_number=payload.phone_number,
            is_active=payload.is_active,
        )

        DB.session.add(record)
        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=AssistableData(assistable=dumpModel(record))
        ).send(201)

    @staticmethod
    def getAll():
        records = (
            Assistable.query
            .order_by(Assistable.created_at.desc())
            .all()
        )

        return Response(
            data=AssistablesData(assistables=[dumpModel(r) for r in records])
        ).send(200)

    @staticmethod
    def getOne(assistableId: str):
        record = Assistable.query.get(assistableId)

        if record is None:
            return Response(
                data=ResponseData(message='Assistable not found')
            ).send(404)

        return Response(
            data=AssistableData(assistable=dumpModel(record))
        ).send(200)

    @staticmethod
    def update(assistableId: str):
        record = Assistable.query.get(assistableId)

        if record is None:
            return Response(
                data=ResponseData(message='Assistable not found')
            ).send(404)

        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = UpdateAssistableSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if payload.carnet is not None:
            conflict = Assistable.query.filter_by(carnet=payload.carnet).first()
            if conflict is not None and str(conflict.id) != assistableId:
                return Response(
                    data=ResponseData(message='Carnet already taken')
                ).send(409)
            record.carnet = payload.carnet

        if payload.email is not None:
            conflict = Assistable.query.filter_by(email=payload.email).first()
            if conflict is not None and str(conflict.id) != assistableId:
                return Response(
                    data=ResponseData(message='Email already taken')
                ).send(409)
            record.email = payload.email

        if payload.phone_number is not None:
            conflict = Assistable.query.filter_by(phone_number=payload.phone_number).first()
            if conflict is not None and str(conflict.id) != assistableId:
                return Response(
                    data=ResponseData(message='Phone number already taken')
                ).send(409)
            record.phone_number = payload.phone_number

        if payload.first_name is not None:
            record.first_name = payload.first_name

        if payload.last_name is not None:
            record.last_name = payload.last_name

        if payload.birthdate is not None:
            record.birthdate = payload.birthdate

        if payload.is_active is not None:
            record.is_active = payload.is_active

        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=AssistableData(assistable=dumpModel(record))
        ).send(200)

    @staticmethod
    def delete(assistableId: str):
        record = Assistable.query.get(assistableId)

        if record is None:
            return Response(
                data=ResponseData(message='Assistable not found')
            ).send(404)

        DB.session.delete(record)
        DB.session.commit()

        return Response(
            data=AssistableData(assistable=dumpModel(record))
        ).send(200)