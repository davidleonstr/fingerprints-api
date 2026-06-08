from api.v1.routes.fingerprintName import fingerprintNameBP
from api.v1.auth import permissionLevel, apiKey
from api.v1.routes.fingerprintName.controller import FingerprintNameController

@fingerprintNameBP.route('/', methods=['POST'])
@apiKey()
@permissionLevel(levelRequired=3)
def createFingerprintName():
    return FingerprintNameController.create()

@fingerprintNameBP.route('/', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAllFingerprintNames():
    return FingerprintNameController.getAll()

@fingerprintNameBP.route('/<int:fingerprintNameId>', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getFingerprintName(fingerprintNameId: int):
    return FingerprintNameController.getOne(fingerprintNameId=fingerprintNameId)

@fingerprintNameBP.route('/<int:fingerprintNameId>', methods=['PUT'])
@apiKey()
@permissionLevel(levelRequired=3)
def updateFingerprintName(fingerprintNameId: int):
    return FingerprintNameController.update(fingerprintNameId=fingerprintNameId)

@fingerprintNameBP.route('/<int:fingerprintNameId>', methods=['DELETE'])
@apiKey()
@permissionLevel(levelRequired=3)
def deleteFingerprintName(fingerprintNameId: int):
    return FingerprintNameController.delete(fingerprintNameId=fingerprintNameId)