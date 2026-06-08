from api.v1.routes.permissionLevel import permissionLevelBP
from api.v1.auth import permissionLevel, apiKey
from api.v1.routes.permissionLevel.controller import PermissionLevelController

@permissionLevelBP.route('/', methods=['POST'])
@apiKey()
@permissionLevel(levelRequired=4)
def createPermissionLevel():
    return PermissionLevelController.create()

@permissionLevelBP.route('/', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAllPermissionLevels():
    return PermissionLevelController.getAll()

@permissionLevelBP.route('/<int:permissionLevelId>', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getPermissionLevel(permissionLevelId: int):
    return PermissionLevelController.getOne(permissionLevelId=permissionLevelId)

@permissionLevelBP.route('/<int:permissionLevelId>', methods=['PUT'])
@apiKey()
@permissionLevel(levelRequired=4)
def updatePermissionLevel(permissionLevelId: int):
    return PermissionLevelController.update(permissionLevelId=permissionLevelId)

@permissionLevelBP.route('/<int:permissionLevelId>', methods=['DELETE'])
@apiKey()
@permissionLevel(levelRequired=4)
def deletePermissionLevel(permissionLevelId: int):
    return PermissionLevelController.delete(permissionLevelId=permissionLevelId)