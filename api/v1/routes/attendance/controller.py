from flask import request
from pydantic import ValidationError

from api.config import DB
from api.tools import Response, ResponseData, dumpModel
from api.v1.models import Attendance, Assistable, AttendanceDayTime, AttendanceMethod, Interactor

from api.v1.routes.attendance.schemas import (
    AttendancesData,
    AttendanceData,
    CreateAttendanceSchema,
    UpdateAttendanceSchema,
)

class AttendanceController:

    @staticmethod
    def create():
        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = CreateAttendanceSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        assistable = Assistable.query.get(payload.assistable_id)

        if assistable is None:
            return Response(
                data=ResponseData(message='Assistable not found')
            ).send(404)

        attendanceDayTime = AttendanceDayTime.query.get(payload.attendance_day_time_id)

        if attendanceDayTime is None:
            return Response(
                data=ResponseData(message='Attendance day time not found')
            ).send(404)

        attendanceMethod = AttendanceMethod.query.get(payload.attendance_method_id)

        if attendanceMethod is None:
            return Response(
                data=ResponseData(message='Attendance method not found')
            ).send(404)

        if payload.recorded_by_interactor_id is not None:
            recorder = Interactor.query.get(payload.recorded_by_interactor_id)

            if recorder is None:
                return Response(
                    data=ResponseData(message='Recording interactor not found')
                ).send(404)

        existing = Attendance.query.filter_by(
            assistable_id=payload.assistable_id,
            attendance_date=payload.attendance_date,
            attendance_day_time_id=payload.attendance_day_time_id,
        ).first()

        if existing is not None:
            return Response(
                data=ResponseData(message='Attendance record already exists for this assistable, date and day time')
            ).send(409)

        record = Attendance(
            assistable_id=payload.assistable_id,
            attendance_date=payload.attendance_date,
            attendance_day_time_id=payload.attendance_day_time_id,
            attendance_method_id=payload.attendance_method_id,
            recorded_by_interactor_id=payload.recorded_by_interactor_id,
        )

        DB.session.add(record)
        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=AttendanceData(attendance=dumpModel(record))
        ).send(201)

    @staticmethod
    def getAll():
        records = (
            Attendance.query
            .order_by(Attendance.attendance_date.desc(), Attendance.created_at.desc())
            .all()
        )

        return Response(
            data=AttendancesData(attendances=[dumpModel(r) for r in records])
        ).send(200)

    @staticmethod
    def getOne(attendanceId: str):
        record = Attendance.query.get(attendanceId)

        if record is None:
            return Response(
                data=ResponseData(message='Attendance not found')
            ).send(404)

        return Response(
            data=AttendanceData(attendance=dumpModel(record))
        ).send(200)

    @staticmethod
    def update(attendanceId: str):
        record = Attendance.query.get(attendanceId)

        if record is None:
            return Response(
                data=ResponseData(message='Attendance not found')
            ).send(404)

        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = UpdateAttendanceSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if payload.attendance_date is not None or payload.attendance_day_time_id is not None:
            newDate = payload.attendance_date if payload.attendance_date is not None else record.attendance_date
            newDayTimeId = payload.attendance_day_time_id if payload.attendance_day_time_id is not None else record.attendance_day_time_id

            conflict = Attendance.query.filter_by(
                assistable_id=str(record.assistable_id),
                attendance_date=newDate,
                attendance_day_time_id=newDayTimeId,
            ).first()

            if conflict is not None and str(conflict.id) != attendanceId:
                return Response(
                    data=ResponseData(message='Attendance record already exists for this assistable, date and day time')
                ).send(409)

            record.attendance_date = newDate
            record.attendance_day_time_id = newDayTimeId

        if payload.attendance_day_time_id is not None:
            attendanceDayTime = AttendanceDayTime.query.get(payload.attendance_day_time_id)

            if attendanceDayTime is None:
                return Response(
                    data=ResponseData(message='Attendance day time not found')
                ).send(404)

        if payload.attendance_method_id is not None:
            attendance_method = AttendanceMethod.query.get(payload.attendance_method_id)

            if attendance_method is None:
                return Response(
                    data=ResponseData(message='Attendance method not found')
                ).send(404)

            record.attendance_method_id = payload.attendance_method_id

        if payload.edited_by_interactor_id is not None:
            editor = Interactor.query.get(payload.edited_by_interactor_id)

            if editor is None:
                return Response(
                    data=ResponseData(message='Editing interactor not found')
                ).send(404)

            record.edited_by_interactor_id = payload.edited_by_interactor_id

        DB.session.commit()
        DB.session.refresh(record)

        return Response(
            data=AttendanceData(attendance=dumpModel(record))
        ).send(200)

    @staticmethod
    def delete(attendanceId: str):
        record = Attendance.query.get(attendanceId)

        if record is None:
            return Response(
                data=ResponseData(message='Attendance not found')
            ).send(404)

        DB.session.delete(record)
        DB.session.commit()

        return Response(
            data=AttendanceData(attendance=dumpModel(record))
        ).send(200)