from pydantic import BaseModel

class InherentResponseFormat(BaseModel):
    status: str
    data: dict