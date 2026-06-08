from api.v1.routes.entity import entityBP
from api.v1.auth import permissionLevel, apiKey
from api.v1.routes.entity.controller import EntityController

@entityBP.route('/', methods=['POST'])
@apiKey()
@permissionLevel(levelRequired=3)
def createEntity():
    return EntityController.create()

@entityBP.route('/', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAllEntities():
    return EntityController.getAll()

@entityBP.route('/<string:entityId>', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getEntity(entityId: str):
    return EntityController.getOne(entityId=entityId)

@entityBP.route('/<string:entityId>', methods=['DELETE'])
@apiKey()
@permissionLevel(levelRequired=3)
def deleteEntity(entityId: str):
    return EntityController.delete(entityId=entityId)