from api.v1.routes.fingerprint import fingerprintBP
from api.v1.auth import permissionLevel, apiKey
from api.v1.routes.fingerprint.controller import FingerprintController

@fingerprintBP.route('/', methods=['POST'])
@apiKey()
@permissionLevel(levelRequired=3)
def createFingerprint():
    return FingerprintController.create()

@fingerprintBP.route('/', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAllFingerprints():
    return FingerprintController.getAll()

@fingerprintBP.route('/<string:fingerprintId>', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getFingerprint(fingerprintId: str):
    return FingerprintController.getOne(fingerprintId=fingerprintId)

@fingerprintBP.route('/<string:fingerprintId>', methods=['PUT'])
@apiKey()
@permissionLevel(levelRequired=3)
def updateFingerprint(fingerprintId: str):
    return FingerprintController.update(fingerprintId=fingerprintId)

@fingerprintBP.route('/<string:fingerprintId>', methods=['DELETE'])
@apiKey()
@permissionLevel(levelRequired=3)
def deleteFingerprint(fingerprintId: str):
    return FingerprintController.delete(fingerprintId=fingerprintId)