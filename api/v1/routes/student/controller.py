from flask import request
from pydantic import ValidationError

from api.config import DB
from api.tools import Response, ResponseData, dumpModel
from api.v1.models import Student, Entity

from api.v1.routes.student.schemas import (
    StudentsData,
    StudentData,
    CreateStudentSchema,
    UpdateStudentSchema,
)

class StudentController:

    @staticmethod
    def create():
        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = CreateStudentSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        entity = Entity.query.get(payload.entity_id)

        if entity is None:
            return Response(
                data=ResponseData(message='Entity not found')
            ).send(404)

        if Student.query.filter_by(carnet=payload.carnet).first() is not None:
            return Response(
                data=ResponseData(message='Carnet already taken')
            ).send(409)

        if Student.query.filter_by(email=payload.email).first() is not None:
            return Response(
                data=ResponseData(message='Email already taken')
            ).send(409)

        if Student.query.filter_by(phone_number=payload.phone_number).first() is not None:
            return Response(
                data=ResponseData(message='Phone number already taken')
            ).send(409)

        record = Student(
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
            data=StudentData(student=dumpModel(record))
        ).send(201)

    @staticmethod
    def getAll():
        records = (
            Student.query
            .order_by(Student.created_at.desc())
            .all()
        )

        return Response(
            data=StudentsData(students=[dumpModel(r) for r in records])
        ).send(200)

    @staticmethod
    def getOne(studentId: str):
        record = Student.query.get(studentId)

        if record is None:
            return Response(
                data=ResponseData(message='Student not found')
            ).send(404)

        return Response(
            data=StudentData(student=dumpModel(record))
        ).send(200)

    @staticmethod
    def update(studentId: str):
        record = Student.query.get(studentId)

        if record is None:
            return Response(
                data=ResponseData(message='Student not found')
            ).send(404)

        body = request.get_json(silent=True)

        if body is None:
            return Response(
                data=ResponseData(message='Request body is required')
            ).send(400)

        try:
            payload = UpdateStudentSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        if payload.carnet is not None:
            conflict = Student.query.filter_by(carnet=payload.carnet).first()
            if conflict is not None and str(conflict.id) != studentId:
                return Response(
                    data=ResponseData(message='Carnet already taken')
                ).send(409)
            record.carnet = payload.carnet

        if payload.email is not None:
            conflict = Student.query.filter_by(email=payload.email).first()
            if conflict is not None and str(conflict.id) != studentId:
                return Response(
                    data=ResponseData(message='Email already taken')
                ).send(409)
            record.email = payload.email

        if payload.phone_number is not None:
            conflict = Student.query.filter_by(phone_number=payload.phone_number).first()
            if conflict is not None and str(conflict.id) != studentId:
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
            data=StudentData(student=dumpModel(record))
        ).send(200)

    @staticmethod
    def delete(studentId: str):
        record = Student.query.get(studentId)

        if record is None:
            return Response(
                data=ResponseData(message='Student not found')
            ).send(404)

        DB.session.delete(record)
        DB.session.commit()

        return Response(
            data=StudentData(student=dumpModel(record))
        ).send(200)