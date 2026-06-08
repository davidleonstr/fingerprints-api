from api.v1.models import Interactor, Entity, Role
from api.tools import Response, ResponseData

from api.v1.routes.interactor.controller import InteractorController
from api.v1.routes.interactor.schemas import (
    InteractorData,
    CreateInteractorSchema
)
from api.tools import dumpModel
from pydantic import ValidationError

from flask import request
from api.config import DB

class SystemController:

    @staticmethod
    def blankSystem():
        return Response(
            ResponseData(
                message=str(SystemController.isBlank()).lower()
            )
        ).send(200)

    @staticmethod
    def createOwner():
        body = request.get_json(silent=True)

        if not SystemController.isBlank():
            return Response(
                ResponseData(
                    message='Owner system already exists'
                )
            ).send(403)

        ownerEntity = Entity()

        DB.session.add(ownerEntity)
        DB.session.commit()

        body['entity_id'] = str(ownerEntity.id) 
        body['role_id'] = Role.query.order_by(Role.id.desc()).first().id
        
        try:
            payload = CreateInteractorSchema(**body)
        except ValidationError as e:
            return Response(
                data=ResponseData(message=e.errors()[0]['msg'])
            ).send(422)

        owner = Interactor(
            username=payload.username, 
            entity_id=payload.entity_id, 
            role_id=payload.role_id,
            password_hash=InteractorController.createPasswordHash(payload.password)
        )

        DB.session.add(owner)
        DB.session.commit()
        DB.session.refresh(owner)

        return Response(InteractorData(interactor=dumpModel(owner))).send(201)
    
    @staticmethod
    def isBlank():
        SUCCESS = True
        ERROR = False

        records = (
            Interactor.query
            .order_by(Interactor.created_at.desc())
            .all()
        )

        return ERROR if records else SUCCESS