from api.tools import Response, ResponseData
from api.tools.dumpModel import dumpModel
from api.config import DB
from api.v1.models import Entity
from api.v1.routes.entity.schemas import EntitiesData, EntityData

class EntityController:

    @staticmethod
    def create():
        record = Entity()
        DB.session.add(record)
        DB.session.commit()
        DB.session.refresh(record)

        return Response(data=EntityData(entity=dumpModel(record))).send(201)

    @staticmethod
    def getAll():
        records = Entity.query.order_by(Entity.created_at.desc()).all()
        
        return Response(data=EntitiesData(entities=[dumpModel(r) for r in records])).send(200)

    @staticmethod
    def getOne(entityId: str):
        record = Entity.query.get(entityId)

        if record is None:
            return Response(data=ResponseData(message='Entity not found')).send(404)

        return Response(data=EntityData(entity=dumpModel(record))).send(200)

    @staticmethod
    def delete(entityId: str):
        record = Entity.query.get(entityId)

        if record is None:
            return Response(data=ResponseData(message='Entity not found')).send(404)

        DB.session.delete(record)
        DB.session.commit()

        return Response(data=EntityData(entity=dumpModel(record))).send(200)