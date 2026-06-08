from api.v1.routes.status import statusBP
from api.tools import Response, ResponseData
from api.v1.auth import permissionLevel, apiKey

@statusBP.route('/', methods=['POST', 'GET'])
def allStatus():
    return Response(ResponseData(message='Everything works!')).send(200)

@statusBP.route('/auth', methods=['POST', 'GET'])
@apiKey()
@permissionLevel(levelRequired=4)
def authStatus():
    return Response(ResponseData(message='Everything works in Auth!')).send(200)