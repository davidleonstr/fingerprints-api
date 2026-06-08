from flask import request
from pydantic import ValidationError

from api.config import DB
from api.tools import Response, ResponseData, dumpModel
from api.v1.models import FingerprintType

from api.v1.routes.fingerprintType.schemas import (
    FingerprintTypesData,
    FingerprintTypeData,
    CreateFingerprintTypeSchema,
    UpdateFingerprintTypeSchema,
)

class FingerprintTypeController:

    @staticmethod
    def create():
        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = CreateFingerprintTypeSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if FingerprintType.query.filter_by(name=payload.name).first() is not None:
            return Response(
                data=ResponseData(message='Fingerprint type name already taken')
            ).send(409)

        record = FingerprintType(
            name=payload.name,
        )

        DB.session.add(record)
        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=FingerprintTypeData(fingerprint_type=dumpModel(record))
        ).send(201)

    @staticmethod
    def getAll():
        records = (
            FingerprintType.query
            .order_by(FingerprintType.created_at.desc())
            .all()
        )

        return Response(
            data=FingerprintTypesData(fingerprint_types=[dumpModel(r) for r in records])
        ).send(200)

    @staticmethod
    def getOne(fingerprintTypeId: int):
        record = FingerprintType.query.get(fingerprintTypeId)

        if record is None:
            return Response(
                data=ResponseData(message='Fingerprint type not found')
            ).send(404)

        return Response(
            data=FingerprintTypeData(fingerprint_type=dumpModel(record))
        ).send(200)

    @staticmethod
    def update(fingerprintTypeId: int):
        record = FingerprintType.query.get(fingerprintTypeId)

        if record is None:
            return Response(
                data=ResponseData(message='Fingerprint type not found')
            ).send(404)

        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = UpdateFingerprintTypeSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if payload.name is not None:
            conflict = FingerprintType.query.filter_by(name=payload.name).first()

            if conflict is not None and conflict.id != fingerprintTypeId:
                return Response(
                    data=ResponseData(message='Fingerprint type name already taken')
                ).send(409)

            record.name = payload.name

        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=FingerprintTypeData(fingerprint_type=dumpModel(record))
        ).send(200)

    @staticmethod
    def delete(fingerprintTypeId: int):
        record = FingerprintType.query.get(fingerprintTypeId)

        if record is None:
            return Response(
                data=ResponseData(message='Fingerprint type not found')
            ).send(404)

        DB.session.delete(record)
        DB.session.commit()

        return Response(
            data=FingerprintTypeData(fingerprint_type=dumpModel(record))
        ).send(200)