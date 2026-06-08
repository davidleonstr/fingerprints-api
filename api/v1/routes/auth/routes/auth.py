from api.v1.routes.auth import authBP
from api.v1.routes.auth.controller import AuthController
from api.v1.auth import apiKey

@authBP.route('/', methods=['POST'])
@apiKey()
def auth():
    return AuthController.auth()