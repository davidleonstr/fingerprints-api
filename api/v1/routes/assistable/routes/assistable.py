from api.v1.routes.assistable import assistableBP
from api.v1.auth import permissionLevel, apiKey
from api.v1.routes.assistable.controller import AssistableController

@assistableBP.route('/', methods=['POST'])
@apiKey()
@permissionLevel(levelRequired=3)
def createassistable():
    return AssistableController.create()

@assistableBP.route('/', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAllassistable():
    return AssistableController.getAll()

@assistableBP.route('/<string:assistableId>', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getassistable(assistableId: str):
    return AssistableController.getOne(assistableId=assistableId)

@assistableBP.route('/<string:assistableId>', methods=['PUT'])
@apiKey()
@permissionLevel(levelRequired=2)
def updateassistable(assistableId: str):
    return AssistableController.update(assistableId=assistableId)

@assistableBP.route('/<string:assistableId>', methods=['DELETE'])
@apiKey()
@permissionLevel(levelRequired=3)
def deleteassistable(assistableId: str):
    return AssistableController.delete(assistableId=assistableId)