from api.v1.routes.role import roleBP
from api.v1.auth import permissionLevel, apiKey
from api.v1.routes.role.controller import RoleController

@roleBP.route('/', methods=['POST'])
@apiKey()
@permissionLevel(levelRequired=3)
def createRole():
    return RoleController.create()

@roleBP.route('/', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAllRoles():
    return RoleController.getAll()

@roleBP.route('/<int:roleId>', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getRole(roleId: int):
    return RoleController.getOne(roleId=roleId)

@roleBP.route('/<int:roleId>', methods=['PUT'])
@apiKey()
@permissionLevel(levelRequired=3)
def updateRole(roleId: int):
    return RoleController.update(roleId=roleId)

@roleBP.route('/<int:roleId>', methods=['DELETE'])
@apiKey()
@permissionLevel(levelRequired=3)
def deleteRole(roleId: int):
    return RoleController.delete(roleId=roleId)