from pydantic import BaseModel

class AuthData(BaseModel):
    token: str
    interactor: dict