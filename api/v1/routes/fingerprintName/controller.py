from flask import request
from pydantic import ValidationError

from api.config import DB
from api.tools import Response, ResponseData, dumpModel
from api.v1.models import FingerprintName

from api.v1.routes.fingerprintName.schemas import (
    FingerprintNamesData,
    FingerprintNameData,
    CreateFingerprintNameSchema,
    UpdateFingerprintNameSchema,
)

class FingerprintNameController:

    @staticmethod
    def create():
        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = CreateFingerprintNameSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if FingerprintName.query.filter_by(name=payload.name).first() is not None:
            return Response(
                data=ResponseData(message='Fingerprint name already taken')
            ).send(409)

        record = FingerprintName(
            name=payload.name,
            description=payload.description,
        )

        DB.session.add(record)
        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=FingerprintNameData(fingerprint_name=dumpModel(record))
        ).send(201)

    @staticmethod
    def getAll():
        records = (
            FingerprintName.query
            .order_by(FingerprintName.created_at.desc())
            .all()
        )

        return Response(
            data=FingerprintNamesData(fingerprint_names=[dumpModel(r) for r in records])
        ).send(200)

    @staticmethod
    def getOne(fingerprintNameId: int):
        record = FingerprintName.query.get(fingerprintNameId)

        if record is None:
            return Response(
                data=ResponseData(message='Fingerprint name not found')
            ).send(404)

        return Response(
            data=FingerprintNameData(fingerprint_name=dumpModel(record))
        ).send(200)

    @staticmethod
    def update(fingerprintNameId: int):
        record = FingerprintName.query.get(fingerprintNameId)

        if record is None:
            return Response(
                data=ResponseData(message='Fingerprint name not found')
            ).send(404)

        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = UpdateFingerprintNameSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if payload.name is not None:
            conflict = FingerprintName.query.filter_by(name=payload.name).first()

            if conflict is not None and conflict.id != fingerprintNameId:
                return Response(
                    data=ResponseData(message='Fingerprint name already taken')
                ).send(409)

            record.name = payload.name

        if payload.description is not None:
            record.description = payload.description

        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=FingerprintNameData(fingerprint_name=dumpModel(record))
        ).send(200)

    @staticmethod
    def delete(fingerprintNameId: int):
        record = FingerprintName.query.get(fingerprintNameId)

        if record is None:
            return Response(
                data=ResponseData(message='Fingerprint name not found')
            ).send(404)

        DB.session.delete(record)
        DB.session.commit()

        return Response(
            data=FingerprintNameData(fingerprint_name=dumpModel(record))
        ).send(200)