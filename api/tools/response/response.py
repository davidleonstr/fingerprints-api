from pydantic import BaseModel
from flask import jsonify
from flask import Response as FlaskResponse
from .inherentResponseFormat import InherentResponseFormat
from http import HTTPStatus

class Response:
    def __init__(self, data: BaseModel) -> None:
        self.data = data
    
    def send(self, code: int = 200) -> FlaskResponse:
        response = InherentResponseFormat(
            status=HTTPStatus(code).name, 
            data=self.data.model_dump()
        ).model_dump()

        return jsonify(response), code