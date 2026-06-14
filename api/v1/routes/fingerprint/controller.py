from flask import request
from pydantic import ValidationError

from api.config import DB
from api.tools import Response, ResponseData, dumpModel
from api.v1.models import Fingerprint, Assistable, FingerprintType, FingerprintName

from api.v1.routes.fingerprint.schemas import (
    FingerprintsData,
    FingerprintData,
    CreateFingerprintSchema,
    UpdateFingerprintSchema,
)

class FingerprintController:

    @staticmethod
    def create():
        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = CreateFingerprintSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        assistable = Assistable.query.get(payload.assistable_id)

        if assistable is None:
            return Response(
                data=ResponseData(message='Assistable not found')
            ).send(404)

        fingerprintType = FingerprintType.query.get(payload.fingerprint_type_id)

        if fingerprintType is None:
            return Response(
                data=ResponseData(message='Fingerprint type not found')
            ).send(404)

        fingerprintName = FingerprintName.query.get(payload.fingerprint_name_id)

        if fingerprintName is None:
            return Response(
                data=ResponseData(message='Fingerprint name not found')
            ).send(404)

        existing = Fingerprint.query.filter_by(
            assistable_id=payload.assistable_id,
            fingerprint_name_id=payload.fingerprint_name_id,
        ).first()

        if existing is not None:
            return Response(
                data=ResponseData(message='Fingerprint record already exists for this assistable and finger')
            ).send(409)

        record = Fingerprint(
            template=bytes.fromhex(payload.template),
            assistable_id=payload.assistable_id,
            fingerprint_type_id=payload.fingerprint_type_id,
            fingerprint_name_id=payload.fingerprint_name_id,
            is_active=payload.is_active,
        )

        DB.session.add(record)
        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=FingerprintData(fingerprint=FingerprintController.dump(record))
        ).send(201)

    @staticmethod
    def getAll():
        records = (
            Fingerprint.query
            .order_by(Fingerprint.created_at.desc())
            .all()
        )

        return Response(
            data=FingerprintsData(fingerprints=[FingerprintController.dump(r) for r in records])
        ).send(200)

    @staticmethod
    def getOne(fingerprintId: str):
        record = Fingerprint.query.get(fingerprintId)

        if record is None:
            return Response(
                data=ResponseData(message='Fingerprint not found')
            ).send(404)

        return Response(
            data=FingerprintData(fingerprint=FingerprintController.dump(record))
        ).send(200)

    @staticmethod
    def update(fingerprintId: str):
        record = Fingerprint.query.get(fingerprintId)

        if record is None:
            return Response(
                data=ResponseData(message='Fingerprint not found')
            ).send(404)

        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = UpdateFingerprintSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if payload.fingerprint_name_id is not None:
            fingerprintName = FingerprintName.query.get(payload.fingerprint_name_id)

            if fingerprintName is None:
                return Response(
                    data=ResponseData(message='Fingerprint name not found')
                ).send(404)

            conflict = Fingerprint.query.filter_by(
                assistable_id=str(record.assistable_id),
                fingerprint_name_id=payload.fingerprint_name_id,
            ).first()

            if conflict is not None and str(conflict.id) != fingerprintId:
                return Response(
                    data=ResponseData(message='Fingerprint record already exists for this assistable and finger')
                ).send(409)

            record.fingerprint_name_id = payload.fingerprint_name_id

        if payload.fingerprint_type_id is not None:
            fingerprintType = FingerprintType.query.get(payload.fingerprint_type_id)

            if fingerprintType is None:
                return Response(
                    data=ResponseData(message='Fingerprint type not found')
                ).send(404)

            record.fingerprint_type_id = payload.fingerprint_type_id

        if payload.template is not None:
            record.template = bytes.fromhex(payload.template)

        if payload.is_active is not None:
            record.is_active = payload.is_active

        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=FingerprintData(fingerprint=FingerprintController.dump(record))
        ).send(200)

    @staticmethod
    def delete(fingerprintId: str):
        record = Fingerprint.query.get(fingerprintId)

        if record is None:
            return Response(
                data=ResponseData(message='Fingerprint not found')
            ).send(404)

        DB.session.delete(record)
        DB.session.commit()

        return Response(
            data=FingerprintData(fingerprint=FingerprintController.dump(record))
        ).send(200)

    @staticmethod
    def dump(record) -> dict:
        d = dumpModel(record)
        if isinstance(d.get('template'), (bytes, memoryview)):
            d['template'] = bytes(d['template']).hex()
        return d