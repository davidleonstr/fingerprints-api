from api.v1.routes.fingerprintType import fingerprintTypeBP
from api.v1.auth import permissionLevel, apiKey
from api.v1.routes.fingerprintType.controller import FingerprintTypeController

@fingerprintTypeBP.route('/', methods=['POST'])
@apiKey()
@permissionLevel(levelRequired=3)
def createFingerprintType():
    return FingerprintTypeController.create()

@fingerprintTypeBP.route('/', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAllFingerprintTypes():
    return FingerprintTypeController.getAll()

@fingerprintTypeBP.route('/<int:fingerprintTypeId>', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getFingerprintType(fingerprintTypeId: int):
    return FingerprintTypeController.getOne(fingerprintTypeId=fingerprintTypeId)

@fingerprintTypeBP.route('/<int:fingerprintTypeId>', methods=['PUT'])
@apiKey()
@permissionLevel(levelRequired=3)
def updateFingerprintType(fingerprintTypeId: int):
    return FingerprintTypeController.update(fingerprintTypeId=fingerprintTypeId)

@fingerprintTypeBP.route('/<int:fingerprintTypeId>', methods=['DELETE'])
@apiKey()
@permissionLevel(levelRequired=3)
def deleteFingerprintType(fingerprintTypeId: int):
    return FingerprintTypeController.delete(fingerprintTypeId=fingerprintTypeId)