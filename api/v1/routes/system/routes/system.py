from api.v1.routes.system import systemBP
from api.v1.routes.system.controller import SystemController
from api.v1.auth import apiKey

@systemBP.route('/blank', methods=['POST', 'GET'])
@apiKey()
def blankSystem():
    return SystemController.blankSystem()

@systemBP.route('/owner', methods=['POST'])
@apiKey()
def createOwner():
    return SystemController.createOwner()