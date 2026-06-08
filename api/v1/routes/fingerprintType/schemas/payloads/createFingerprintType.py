from pydantic import BaseModel

class CreateFingerprintTypeSchema(BaseModel):
    name: str