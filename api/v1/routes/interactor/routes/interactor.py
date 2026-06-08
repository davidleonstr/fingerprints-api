from api.v1.routes.interactor import interactorBP
from api.v1.auth import permissionLevel, apiKey
from api.v1.routes.interactor.controller import InteractorController

@interactorBP.route('/', methods=['POST'])
@apiKey()
@permissionLevel(levelRequired=3)
def createInteractor():
    return InteractorController.create()

@interactorBP.route('/', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAllInteractors():
    return InteractorController.getAll()

@interactorBP.route('/<string:interactorId>', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getInteractor(interactorId: str):
    return InteractorController.getOne(interactorId=interactorId)

@interactorBP.route('/<string:interactorId>', methods=['PUT'])
@apiKey()
@permissionLevel(levelRequired=3)
def updateInteractor(interactorId: str):
    return InteractorController.update(interactorId=interactorId)

@interactorBP.route('/<string:interactorId>', methods=['DELETE'])
@apiKey()
@permissionLevel(levelRequired=3)
def deleteInteractor(interactorId: str):
    return InteractorController.delete(interactorId=interactorId)