from functools import wraps
from flask import request, current_app
from api.tools.response import Response, ResponseData

def apiKey():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            apiKeyHeader = request.headers.get('x-api-key')

            if not apiKeyHeader:
                return Response(
                    ResponseData(message='API Key missing')
                ).send(401)

            validApiKey = current_app.config.get('API_KEY')

            if apiKeyHeader != validApiKey:
                return Response(
                    ResponseData(message='Invalid API Key')
                ).send(401)

            return func(*args, **kwargs)

        return wrapper
    return decorator