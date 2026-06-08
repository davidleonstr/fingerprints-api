from flask import request
from pydantic import ValidationError

from api.config import DB
from api.tools import Response, ResponseData, dumpModel
from api.v1.models import AttendanceMethod

from api.v1.routes.attendanceMethod.schemas import (
    AttendanceMethodsData,
    AttendanceMethodData,
    CreateAttendanceMethodSchema,
    UpdateAttendanceMethodSchema,
)

class AttendanceMethodController:

    @staticmethod
    def create():
        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = CreateAttendanceMethodSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if AttendanceMethod.query.filter_by(name=payload.name).first() is not None:
            return Response(
                data=ResponseData(message='Attendance method name already taken')
            ).send(409)

        record = AttendanceMethod(
            name=payload.name,
            description=payload.description,
        )

        DB.session.add(record)
        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=AttendanceMethodData(attendance_method=dumpModel(record))
        ).send(201)

    @staticmethod
    def getAll():
        records = (
            AttendanceMethod.query
            .order_by(AttendanceMethod.created_at.desc())
            .all()
        )

        return Response(
            data=AttendanceMethodsData(attendance_methods=[dumpModel(r) for r in records])
        ).send(200)

    @staticmethod
    def getOne(attendanceMethodId: int):
        record = AttendanceMethod.query.get(attendanceMethodId)

        if record is None:
            return Response(
                data=ResponseData(message='Attendance method not found')
            ).send(404)

        return Response(
            data=AttendanceMethodData(attendance_method=dumpModel(record))
        ).send(200)

    @staticmethod
    def update(attendanceMethodId: int):
        record = AttendanceMethod.query.get(attendanceMethodId)

        if record is None:
            return Response(
                data=ResponseData(message='Attendance method not found')
            ).send(404)

        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = UpdateAttendanceMethodSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if payload.name is not None:
            conflict = AttendanceMethod.query.filter_by(name=payload.name).first()

            if conflict is not None and conflict.id != attendanceMethodId:
                return Response(
                    data=ResponseData(message='Attendance method name already taken')
                ).send(409)

            record.name = payload.name

        if payload.description is not None:
            record.description = payload.description

        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=AttendanceMethodData(attendance_method=dumpModel(record))
        ).send(200)

    @staticmethod
    def delete(attendanceMethodId: int):
        record = AttendanceMethod.query.get(attendanceMethodId)

        if record is None:
            return Response(
                data=ResponseData(message='Attendance method not found')
            ).send(404)

        DB.session.delete(record)
        DB.session.commit()

        return Response(
            data=AttendanceMethodData(attendance_method=dumpModel(record))
        ).send(200)