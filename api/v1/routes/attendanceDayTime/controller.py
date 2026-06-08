from flask import request
from pydantic import ValidationError

from api.config import DB
from api.tools import Response, ResponseData, dumpModel
from api.v1.models import AttendanceDayTime

from api.v1.routes.attendanceDayTime.schemas import (
    AttendanceDayTimesData,
    AttendanceDayTimeData,
    CreateAttendanceDayTimeSchema,
    UpdateAttendanceDayTimeSchema,
)

class AttendanceDayTimeController:

    @staticmethod
    def create():
        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = CreateAttendanceDayTimeSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if AttendanceDayTime.query.filter_by(name=payload.name).first() is not None:
            return Response(
                data=ResponseData(message='Attendance day time name already taken')
            ).send(409)

        record = AttendanceDayTime(
            name=payload.name,
            description=payload.description,
        )

        DB.session.add(record)
        DB.session.commit()

        return Response(
            data=AttendanceDayTimeData(attendance_day_time=dumpModel(record))
        ).send(201)

    @staticmethod
    def getAll():
        records = (
            AttendanceDayTime.query
            .order_by(AttendanceDayTime.created_at.desc())
            .all()
        )

        return Response(
            data=AttendanceDayTimesData(attendance_day_times=[dumpModel(r) for r in records])
        ).send(200)

    @staticmethod
    def getOne(attendanceDayTimeId: int):
        record = AttendanceDayTime.query.get(attendanceDayTimeId)

        if record is None:
            return Response(
                data=ResponseData(message='Attendance day time not found')
            ).send(404)

        return Response(
            data=AttendanceDayTimeData(attendance_day_time=dumpModel(record))
        ).send(200)

    @staticmethod
    def update(attendanceDayTimeId: int):
        record = AttendanceDayTime.query.get(attendanceDayTimeId)

        if record is None:
            return Response(
                data=ResponseData(message='Attendance day time not found')
            ).send(404)

        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = UpdateAttendanceDayTimeSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if payload.name is not None:
            conflict = AttendanceDayTime.query.filter_by(name=payload.name).first()

            if conflict is not None and conflict.id != attendanceDayTimeId:
                return Response(
                    data=ResponseData(message='Attendance day time name already taken')
                ).send(409)

            record.name = payload.name

        if payload.description is not None:
            record.description = payload.description

        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=AttendanceDayTimeData(attendance_day_time=dumpModel(record))
        ).send(200)

    @staticmethod
    def delete(attendanceDayTimeId: int):
        record = AttendanceDayTime.query.get(attendanceDayTimeId)

        if record is None:
            return Response(
                data=ResponseData(message='Attendance day time not found')
            ).send(404)

        DB.session.delete(record)
        DB.session.commit()

        return Response(
            data=AttendanceDayTimeData(attendance_day_time=dumpModel(record))
        ).send(200)